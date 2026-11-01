import json
from pathlib import Path
import tempfile
import unittest
from importlib.util import spec_from_file_location,module_from_spec
ROOT=Path(__file__).resolve().parents[1]
spec=spec_from_file_location('scanner',ROOT/'scripts'/'scan_sources.py');module=module_from_spec(spec);spec.loader.exec_module(module)
class Tests(unittest.TestCase):
    def test_initialisation_et_modification_non_publiee(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)
            (root/'config').mkdir();(root/'site'/'data').mkdir(parents=True)
            source={'id':'S001','candidate_id':'X','candidate_name':'Exemple','url':'https://example.org/programme','enabled':True}
            (root/'config'/'sources.json').write_text(json.dumps({'sources':[source]}))
            n=[0]
            def fetcher(url,timeout):
                n[0]+=1
                return {'fingerprint':'same' if n[0]==1 else 'modified','kind':'html','links':[]}
            a=module.scan(root,fetcher,now='2026-11-01T10:00:00Z')
            self.assertEqual(a['changes'],0)
            b=module.scan(root,fetcher,now='2026-11-02T10:00:00Z')
            self.assertEqual(b['changes'],1)
            queue=json.loads((root/'data'/'review_queue.json').read_text())
            self.assertEqual(queue[0]['status'],'a_verifier')
            self.assertFalse((root/'site'/'data'/'approved_positions.json').exists())
    def test_suggestions_restreintes_a_l_hote(self):
        urls=module.suggested_links(['/programme-2027','https://evil.example/mesures','/produits'], 'https://example.org/accueil',set())
        self.assertEqual(urls,['https://example.org/programme-2027'])
    def test_aides_questions_heritees(self):
        import re
        base=(ROOT/'archive_v13'/'OUVRIR_BOUSSOLE_2027_v1.3.html').read_text()
        curr=(ROOT/'site'/'index.html').read_text()
        get=lambda s:json.loads(re.search(r'<script id="dataset" type="application/json">(.*?)</script>',s,re.S).group(1))
        a,b=get(base),get(curr)
        for key in ['questions','candidates','evidence','audits','question_audit','measure_lab']:
            self.assertEqual(a[key],b[key])
        self.assertEqual(len(a['questions']),56)
        self.assertEqual(len(a['candidates']),16)
if __name__=='__main__':unittest.main()
