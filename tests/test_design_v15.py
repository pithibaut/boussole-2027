"""Régression de contenu et intégrité de l'habillage v1.5 (zéro dépendance)."""
import unittest,re,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class VisualRegression(unittest.TestCase):
    @staticmethod
    def dataset(path):
        html=path.read_text(encoding='utf8')
        match=re.search(r'<script id="dataset" type="application/json">(.*?)</script>',html,re.S)
        assert match, 'Corpus embarqué absent'
        return match.group(1)
    def test_corpus_identique_v13_v15(self):
        old=self.dataset(ROOT/'archive_v13'/'OUVRIR_BOUSSOLE_2027_v1.3.html')
        new=self.dataset(ROOT/'site'/'index.html')
        self.assertEqual(old,new)
        corpus=json.loads(new)
        self.assertEqual(len(corpus['questions']),56)
        self.assertEqual(len(corpus['candidates']),16)
    def test_design_integre(self):
        html=(ROOT/'site'/'index.html').read_text(encoding='utf8')
        self.assertIn('design-republique-elegante-v15',html)
        self.assertIn('--navy:#16324F',html)
        self.assertIn('--red:#C94B4B',html)
        self.assertIn('id="liveUpdates"',html)
        for i in ['intro','quiz','results','export','inspectWithoutAnswer']:
            self.assertEqual(html.count('id="'+i+'"'),1)
    def test_fichiers_de_deploiement(self):
        for name in ['site/index.html','site/data/approved_positions.json','config/sources.json','.github/workflows/veille-et-publication.yml','scripts/scan_sources.py','scripts/validate_publish.py','scripts/build_coverage.py','LANCER_SUR_GITHUB.md']:
            self.assertTrue((ROOT/name).is_file(),name)
if __name__=='__main__':unittest.main()
