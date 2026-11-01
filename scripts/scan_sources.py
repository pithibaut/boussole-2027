#!/usr/bin/env python3
"""Surveillance gratuite : changements des sources != positions politiques validées.

Seules des métadonnées limitées sont publiées ; aucun questionnaire utilisateur n'est collecté.
Le scanner ne modifie jamais approved_positions.json ni les réponses aux questions.
"""
import argparse
import datetime as dt
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.parse import urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
NOW = lambda: dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')
MAX_FETCH = 5_000_000
KEYWORDS = re.compile(r'(programme|proposition|mesure|actualit[eé]|communiqu[eé]|livret|priorit[eé]|candidat|2027|projet)', re.I)

class VisibleText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.text = []
        self.links = []
        self.inlink = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script','style','svg','noscript'):
            self.skip += 1
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in ('h1','h2','h3','h4','p','li','article') and not self.skip:
            self.text.append(' ')
    def handle_endtag(self, tag):
        if tag in ('script','style','svg','noscript') and self.skip:
            self.skip -= 1
    def handle_data(self, content):
        if not self.skip:
            self.text.append(content)

def clean_html(content):
    parser = VisibleText()
    parser.feed(content)
    stripped = re.sub(r'\s+', ' ', html.unescape(' '.join(parser.text))).strip()
    return stripped, parser.links

def fetch(url, timeout):
    req = Request(url, headers={'User-Agent':'Boussole2027-SourceWatch/1.4 (public document monitoring; no automated attribution)', 'Accept':'text/html,application/pdf;q=0.9,*/*;q=0.5'})
    with urlopen(req, timeout=timeout) as response:
        final = response.geturl()
        if urlsplit(final).scheme not in ('http','https'):
            raise ValueError('Redirection vers protocole non autorisé')
        raw = response.read(MAX_FETCH+1)
        if len(raw)>MAX_FETCH:
            raise ValueError('Document trop volumineux pour la surveillance gratuite')
        mimetype = response.headers.get('Content-Type','').split(';')[0].lower()
        if mimetype=='application/pdf' or raw.startswith(b'%PDF-'):
            return {'fingerprint':hashlib.sha256(raw).hexdigest(),'kind':'pdf','links':[],'bytes':len(raw)}
        codec = response.headers.get_content_charset() or 'utf-8'
        content = raw.decode(codec,errors='replace')
        visible, links = clean_html(content)
        # fingerprint is based on visible content, not volatile HTML attributes
        digest = hashlib.sha256(visible.encode('utf-8')).hexdigest()
        return {'fingerprint':digest,'kind':'html','links':links,'bytes':len(raw)}

def suggested_links(raw_links, parent_url, tracked):
    host = urlsplit(parent_url).hostname or ''
    out = []
    for href in raw_links:
        url = urljoin(parent_url, href).split('#',1)[0]
        parts = urlsplit(url)
        if parts.scheme != 'https' or parts.hostname != host or url in tracked:
            continue
        clean = urlunsplit((parts.scheme,parts.netloc,parts.path,'',''))
        if clean in tracked or not KEYWORDS.search(parts.path):
            continue
        if clean not in out: out.append(clean)
        if len(out)>=3: break
    return out

def load(path, fallback):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else fallback

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def scan(root=ROOT, fetcher=fetch, now=None):
    now = now or NOW()
    cfg = load(root/'config'/'sources.json',{'sources':[]})
    enabled=[s for s in cfg['sources'] if s.get('enabled')]
    state=load(root/'data'/'watch_state.json',{})
    queue=load(root/'data'/'review_queue.json',[])
    known_q = {x['id'] for x in queue if 'id' in x}
    tracked={s['url'] for s in cfg['sources']}
    events=[]; ok=0; errors=0; changes=0
    for item in enabled:
        key=item['id'];old=state.get(key,{})
        nextstate={**old, 'url':item['url'],'candidate_id':item['candidate_id'],'last_checked':now}
        try:
            found=fetcher(item['url'], timeout=12)
            ok+=1
            h=found['fingerprint'];before=old.get('fingerprint')
            nextstate.update({'fingerprint':h,'last_success':now,'last_error':None,'format':found['kind']})
            if before is not None and h!=before:
                changes+=1
                event={'type':'changed','candidate_id':item['candidate_id'],'candidate_name':item['candidate_name'],'source_id':key,'url':item['url'],'observed_at':now}
                events.append(event)
                task_id=key+':'+h[:16]
                if task_id not in known_q:
                    queue.insert(0,{'id':task_id,'type':'source_change','status':'a_verifier','source_id':key,'candidate_id':item['candidate_id'],'url':item['url'],'observed_at':now,'instructions':'Comparer le texte avant/après ; vérifier l’auteur, la date, la nuance et la question concernée. Ne pas coder automatiquement une réponse.'})
                    known_q.add(task_id)
            # Only suggest relevant page URLs under the SAME hostname; never attribute positions.
            for link in suggested_links(found.get('links',[]),item['url'],tracked):
                task_id='suggest:'+hashlib.sha256(link.encode()).hexdigest()[:16]
                if task_id not in known_q:
                    queue.insert(0,{'id':task_id,'type':'new_page_suggestion','status':'a_verifier','source_id':key,'candidate_id':item['candidate_id'],'url':link,'observed_at':now,'instructions':'Page candidate à contrôler avant de l’ajouter au registre. Ne pas traiter comme position politique.'})
                    known_q.add(task_id)
        except Exception as exc:
            errors+=1
            nextstate['last_error']=str(exc)[:180]
        state[key]=nextstate
    events = events[:25]
    oldstatus=load(root/'site'/'data'/'watch_status.json',{})
    history=(events+oldstatus.get('recent_changes',[]))[:25]
    status={'schema':1,'last_run_at':now,'sources_total':len(enabled),'ok':ok,'errors':errors,'changes':changes,'recent_changes':history,
            'note':'Changements de pages détectés automatiquement ; aucune position politique publiée sans validation.'}
    write(root/'data'/'watch_state.json',state)
    write(root/'data'/'review_queue.json',queue[:350])
    write(root/'site'/'data'/'watch_status.json',status)
    return status

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args();r=scan(args.root)
    print(f"Sources : {r['sources_total']} | disponibles : {r['ok']} | erreurs : {r['errors']} | nouvelles modifications : {r['changes']}")
    if r['errors']:print('Certains sites sont inaccessibles, sans incidence sur les données déjà validées.',file=sys.stderr)

if __name__=='__main__':main()
