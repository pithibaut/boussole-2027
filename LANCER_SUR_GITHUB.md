# BOUSSOLE 2027 — publication de la v1.5 sur votre dépôt GitHub EXISTANT

Le dépôt cible a déjà été créé : **https://github.com/pithibaut/boussole-2027**. Il n'est pas nécessaire de créer un deuxième dépôt.

## Méthode recommandée sur Windows : GitHub Desktop (sans ligne de commande)

1. Téléchargez **GitHub Desktop** gratuitement sur https://desktop.github.com/ et connectez-vous avec votre compte GitHub.
2. Dans GitHub Desktop, choisissez **File > Clone repository**, puis sélectionnez `pithibaut/boussole-2027` et un dossier de travail sur votre ordinateur. Cliquez **Clone**. Vous devez retrouver le README initial du dépôt.
3. Décompressez le ZIP Boussole 2027 v1.5 ailleurs que dans ce dossier cloné.
4. **Copiez le contenu** du dossier décompressé dans le dossier local cloné (et non le ZIP ou un dossier parent supplémentaire). Copiez également le dossier `.github`, qui contient le workflow d'automatisation. La racine doit ressembler à :

```
boussole-2027/
  README.md
  LANCER_SUR_GITHUB.md
  COMMENCER_ICI.md
  .github/workflows/veille-et-publication.yml
  site/index.html
  site/data/approved_positions.json
  site/data/coverage_status.json
  scripts/scan_sources.py
  scripts/validate_publish.py
  scripts/build_coverage.py
  config/sources.json
  data/research_backlog.json
  tests/test_pipeline.py
  archive_v13/...
```

5. Retournez dans GitHub Desktop : des fichiers ajoutés ou modifiés apparaissent dans **Changes**. Vérifiez que `site/index.html` et `.github/workflows/veille-et-publication.yml` figurent bien parmi les changements.
6. En bas à gauche, inscrivez par exemple `Boussole 2027 v1.5 — design République élégante et surveillance` dans Summary, puis cliquez **Commit to main**.
7. Cliquez **Push origin**. Les fichiers sont maintenant transférés sur votre dépôt.
8. Ouvrez https://github.com/pithibaut/boussole-2027/settings/pages ; dans **Build and deployment** > **Source**, sélectionnez **GitHub Actions**.
9. Allez dans https://github.com/pithibaut/boussole-2027/actions ; si GitHub vous invite à activer les workflows, autorisez-les. Ouvrez **Boussole 2027 - veille et publication** puis **Run workflow**, branche **main**.
10. Attendez le statut vert (« success »), puis récupérez votre adresse depuis **Settings > Pages**. Adresse attendue, **non garantie avant publication réussie** : https://pithibaut.github.io/boussole-2027/

**Si le workflow indique `Resource not accessible by integration` ou refuse de sauvegarder l'état de veille :** consultez **Settings > Actions > General > Workflow permissions**, sélectionnez **Read and write permissions** si l'option est disponible, puis relancez le workflow. Ne communiquez jamais de token, de clé ou de mot de passe.

## Méthode alternative : téléversement depuis le navigateur

Dans le dépôt, ouvrez **Add file > Upload files**, puis déposez le **contenu** du dossier décompressé en respectant exactement les chemins. Certains navigateurs n'envoient pas correctement les dossiers imbriqués ou `.github` : dans ce cas, privilégiez GitHub Desktop. Vérifiez ensuite la présence de `site/index.html` et du workflow avant toute tentative de déploiement.

## Ce qui sera automatisé et ce qui ne le sera pas

- **Chaque jour environ :** GitHub Actions tente de vérifier les URLs présentes dans `config/sources.json` et enregistre les changements.
- **Automatiquement :** le tableau d'état des contrôles et des recherches à approfondir est actualisé ; les nouvelles sources potentielles sont placées en file de vérification.
- **Après validation humaine documentée seulement :** de nouvelles correspondances politiques peuvent être publiées via `site/data/approved_positions.json`.
- **Non automatique :** transformation d'une annonce en engagement personnel 2027, contrôle contradictoire de la faisabilité, achèvement des 896 cases, amélioration autonome du logiciel. Aucun de ces objectifs ne serait fiable sans vérification.

La veille utilise les offres gratuites de GitHub pour un dépôt public dans la limite des conditions et quotas applicables. Les événements planifiés peuvent être retardés, certaines sources peuvent bloquer les robots. Pas d'abonnement ni d'API d'IA payante intégrés au projet.

## Prudence avant partage public

- Les 16 personnalités sont présentes, mais leur couverture n'est pas équivalente.
- Les rapprochements de la base initiale sont encore provisoires. Le résultat n'est pas une recommandation électorale ni un verdict de programme.
- Toutes les données du dépôt public sont publiquement accessibles : n'ajoutez **jamais** les réponses personnelles, coordonnées, informations privées ou clés secrètes.
- La surveillance ne transmet pas les réponses du questionnaire au serveur.
