#!/usr/bin/env python3
"""Validation structurée des nouvelles positions avant publication GitHub Pages.
Un contrôle technique ne remplace pas une vérification humaine contradictoire.
"""
import json,re,sys
from pathlib import Path
from urllib.parse import urlsplit
ROOT=Path(__file__).resolve().parents[1]

def validate(root=ROOT):
    import html.parser
    text=(root/'archive_v13'/'OUVRIR_BOUSSOLE_2027_v1.3.html').read_text(encoding='utf-8')
    base=json.loads(re.search(r'<script id="dataset" type="application/json">(.*?)</script>',text,re.S).group(1))
    data=json.loads((root/'site'/'data'/'approved_positions.json').read_text(encoding='utf-8'))
    sources=json.loads((root/'config'/'sources.json').read_text(encoding='utf-8'))['sources']
    ids={c['id'] for c in base['candidates']};qs={q['id']:{o['id'] for o in q['options']} for q in base['questions']}
    urls={s['url'] for s in sources}
    existing={e['id'] for e in base['evidence']}; unique=set(); errors=[]
    if data.get('schema')!=1 or not isinstance(data.get('positions'),list):return ['Structure de données incompatible']
    for n,e in enumerate(data['positions'],1):
        prefix=f'Ligne {n}'
        if not re.fullmatch(r'V14-[a-zA-Z0-9-]{3,48}',str(e.get('id',''))):errors.append(prefix+': identifiant invalide')
        if e.get('id') in unique or e.get('id') in existing:errors.append(prefix+': identifiant dupliqué')
        unique.add(e.get('id'))
        if e.get('candidate_id') not in ids:errors.append(prefix+': candidat inconnu')
        if e.get('question_id') not in qs or e.get('option_id') not in qs.get(e.get('question_id'),set()):errors.append(prefix+': question/option invalide')
        if e.get('scope')!='personnel' or e.get('level')!='direct' or e.get('review')!='validation_humaine':errors.append(prefix+': statut insuffisant pour publication')
        if e.get('url') not in urls:errors.append(prefix+': URL non inscrite au registre (ajouter la source et contrôler son authenticité)')
        if not isinstance(e.get('measure'),str) or len(e['measure'].strip())<16:errors.append(prefix+': description insuffisante')
        if not isinstance(e.get('approved_by'),str) or len(e['approved_by'])<2:errors.append(prefix+': identité du validateur manquante')
        if not re.fullmatch(r'20\d{2}-\d{2}-\d{2}',str(e.get('approved_at',''))):errors.append(prefix+': date de validation requise')
        if not isinstance(e.get('limit'),str) or len(e['limit'])<15:errors.append(prefix+': limites/interprétation manquantes')
        if not isinstance(e.get('source_location'),str) or len(e['source_location'])<3:errors.append(prefix+': passage source localisable manquant')
    return errors

if __name__=='__main__':
    errs=validate()
    if errs:
        print('\n'.join(errs),file=sys.stderr);sys.exit(1)
    print('Structure des positions publiables : valide. Une vérification indépendante des affirmations demeure indispensable.')
