#!/usr/bin/env python3
"""Calcule la couverture documentaire VALIDÉE, sans extrapoler les positions manquantes."""
import csv,datetime as dt,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    html=(ROOT/'archive_v13'/'OUVRIR_BOUSSOLE_2027_v1.3.html').read_text(encoding='utf-8')
    base=json.loads(re.search(r'<script id="dataset" type="application/json">(.*?)</script>',html,re.S).group(1))
    approved=json.loads((ROOT/'site'/'data'/'approved_positions.json').read_text(encoding='utf-8'))
    candid={c['name']:c['id'] for c in base['candidates']}
    questions={q['id']:q for q in base['questions']}
    plan=ROOT/'archive_v13'/'PLAN_DE_COUVERTURE_896_v1.3.csv'
    backlog=[]
    with plan.open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f, delimiter=';'):
            name=row['personnalite'];qid=row['question']
            if name in candid and qid in questions:
                backlog.append({'candidate_id':candid[name],'candidate_name':name,'question_id':qid,
                    'core':questions[qid]['core'],'theme':questions[qid]['theme'],
                    'provisional_personal_links':int(row['liens_personnels_provisoires'] or '0'),
                    'historic_context_links':int(row['liens_contexte'] or '0')})
    full={(c['id'],q['id']) for c in base['candidates'] for q in base['questions']}
    valid={(p['candidate_id'],p['question_id']) for p in approved['positions']}
    valid &= full
    for task in backlog:
        task['status']='position_validee' if (task['candidate_id'],task['question_id']) in valid else 'a_documenter'
    by_candidate=[]
    for c in base['candidates']:
        n=sum(cid==c['id'] for cid,qid in valid)
        by_candidate.append({'candidate_id':c['id'],'candidate_name':c['name'],'verified_questions':n,'total_questions':len(questions)})
    status={'schema':1,'updated_at':dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
      'candidate_count':len(candid),'question_count':len(questions),'cells_total':len(full),
      'validated_question_candidate_pairs':len(valid),
      'research_cases_unverified':len(full)-len(valid),
      'original_provisional_evidence':len(base['evidence']),
      'by_candidate':by_candidate,
      'method':'Ne compter comme validé que les liens approuvés dans approved_positions.json; les liens anciens sont conservés mais provisoires.'}
    (ROOT/'data'/'research_backlog.json').write_text(json.dumps(backlog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (ROOT/'site'/'data'/'coverage_status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Couverture validée',len(valid),'/',len(full),'| tâches candidates',len(backlog))
if __name__=='__main__':main()
