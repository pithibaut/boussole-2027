# Architecture et tests de la v1.4

- Source immuable : `archive_v13/OUVRIR_BOUSSOLE_2027_v1.3.html`.
- Application publiée : `site/index.html` (ajout d'un panneau de surveillance et chargement des données validées ; corpus historique inchangé).
- Mise à jour des **notifications** : `scripts/scan_sources.py` -> `site/data/watch_status.json`.
- Mise à jour des **preuves** : contrôle éditorial -> `site/data/approved_positions.json` -> `validate_publish.py` -> déploiement.
- Couverture : `scripts/build_coverage.py` -> `site/data/coverage_status.json`.
- Recherche de nouvelles pages : liens du même site proposés dans `data/review_queue.json`, pas ajoutés automatiquement au programme.
- Aucun paiement ni clé API nécessaire, mais aucun contrôle en cours d'exécution depuis ChatGPT : le cron démarre après configuration du dépôt GitHub.

## Limites assumées

Une source peut changer sans qu'une nouvelle mesure soit publiée et inversement. Des pages peuvent être inaccessibles, notamment les PDF lourds ou les sites soumis à des protections. L'automatisation détecte des signaux de modification et prépare le travail ; elle ne garantit ni l'exhaustivité du web ni une vérification de faisabilité. Le résultat politique ne doit pas être promu comme fiable tant qu'une revue indépendante des positions et de la méthode n'a pas été menée.

Tests embarqués : `python -m unittest discover -s tests -v`, `python scripts/validate_publish.py` et `python scripts/build_coverage.py`. Les simulations de source sont entièrement locales et n'entraînent pas de récupération web à l'installation.
