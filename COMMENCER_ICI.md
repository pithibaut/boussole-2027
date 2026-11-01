# Boussole 2027 — v1.5, hébergement et veille à 0 € (sous conditions)

**Point de départ :** application v1.3 préservée (56 questions, 224 aides, 16 personnalités, 105 fiches de rapprochement et l'ensemble de ses onglets). La v1.4 a ajouté un système de surveillance des sources et un chargement automatique des données **approuvées**. Aucune position personnelle n'est fabriquée à partir d'un changement de page.

## Ce qui fonctionne tout de suite

- `site/index.html` : application v1.3 enrichie du bloc « Suivi des programmes ». Les réponses au questionnaire restent en mémoire dans le navigateur durant la session, et ne sont pas envoyées à notre serveur.
- `config/sources.json` : 36 URL documentaires héritées de la v1.3, réparties entre les 16 personnalités ; certaines sont historiques, collectives ou non exhaustives. Elles nécessitent elles-mêmes des contrôles d'attribution.
- `scripts/scan_sources.py` : détection automatique quotidienne des changements de pages et suggestion de liens nouveaux du même site ; les changements sont stockés dans une file de relecture.
- `data/research_backlog.json` : liste de 896 recherches candidat-question à instruire, sans présenter un « silence » comme une opposition.
- `scripts/validate_publish.py` : refuse une donnée nouvelle mal structurée, non référencée ou sans signature de validation.
- `scripts/build_coverage.py` : calcule la couverture des **positions nouvellement validées**, distincte des liens historiques provisoires.
- `.github/workflows/veille-et-publication.yml` : surveillance quotidienne et publication GitHub Pages gratuite (dépôt public, runners standards).

Vous avez déjà créé le dépôt `pithibaut/boussole-2027`. **Ne créez pas un nouveau dépôt.** Pour transférer les fichiers avec GitHub Desktop, configurer GitHub Pages et vérifier le site, consultez **`LANCER_SUR_GITHUB.md`** dans le même dossier. Cette notice est également reprise dans `README.md`.

## Pour consulter les nouvelles annonces détectées

Dans GitHub, ouvrir le fichier `data/review_queue.json` : il contient les changements et pages suggérées, classés « à vérifier ». `data/watch_state.json` garde les derniers contrôles et les éventuelles erreurs. L'application publique montre une synthèse de la surveillance.

Le contrôle d'une page ne prouve pas une nouvelle mesure : les changements peuvent venir d'un menu, d'une date, d'une correction de texte ou d'une modification technique. La vérification des contenus et des conditions d'une mesure reste donc indispensable.

## Pour enrichir une position (et seulement après vérification)

1. Ouvrir la source officielle, relever la date, l'auteur exact, le passage localisable et ses exceptions. Vérifier que la position s'applique bien à la campagne 2027 et non seulement à un parti ou à une ancienne campagne.
2. Si la source ne figure pas déjà dans `config/sources.json`, l'ajouter après avoir contrôlé son authenticité.
3. Éditer `site/data/approved_positions.json` en ajoutant un objet conforme au modèle dans `MODELE_VALIDATION.md`. Cette étape **doit être validée par une personne**, pas directement par le scanner.
4. Enregistrer les modifications sur `main`. Les contrôles automatiques s'exécutent ; si tout passe, la nouvelle position apparaîtra sur l'application en ligne, sans téléchargement par les utilisateurs.
5. En cas d'erreur, consulter **Actions** dans GitHub : la publication des nouvelles données sera bloquée si la validation structurelle échoue.

## Gratuité : conditions et limites

- GitHub Pages est gratuit pour un dépôt **public** sur GitHub Free, et les runners standard d'Actions sont gratuits pour les dépôts publics dans les conditions publiées par GitHub. Aucun modèle d'IA payant ni API externe n'est requis par ce dossier.
- Pas de domaine personnalisé nécessaire : le lien `github.io` suffit.
- Les tâches planifiées ne sont pas garanties à la minute et peuvent être retardées ou désactivées (surveiller l'onglet Actions de temps à autre). Certains sites protègent leurs pages contre l'automatisation : la surveillance affichera alors des erreurs, sans modifier les preuves.
- Le logiciel propose des documents à vérifier, mais **n'est pas un agent qui complète seul 896 positions**. Une couverture réellement équitable et une contre-expertise de faisabilité demandent encore du travail éditorial.
- Tout le code et les données placés dans le dépôt public sont visibles par des tiers. Ne jamais publier de réponses nominatives, de courriels de proches ou d'identifiants.

## État de fiabilité à la livraison

- 56 questions et corpus historique 1.3 : conservés intégralement.
- 896 recherches candidat-question : planifiées, non considérées comme instruites.
- Nouvelles positions certifiées par la v1.4 : **0** au départ.
- Résultat final : toujours exploratoire ; pas de « meilleur candidat » établi par l'application.

Ce projet est un outil pédagogique d'information et de comparaison documentaire. Les utilisateurs restent libres de leurs choix politiques.
