# Ajouter une nouvelle position politique vérifiée

Une annonce détectée n'est **pas** intégrée dans le calcul. Ouvrir `site/data/approved_positions.json` uniquement après contrôle de la source et, idéalement, une seconde lecture indépendante.

**Modèle de structure : ne pas copier tel quel : c'est un exemple de champs sans affirmation politique.**

```json
{
  "id": "V14-EXEMPLE-001",
  "candidate_id": "ID_DU_CANDIDAT_EXISTANT",
  "question_id": "Q01",
  "option_id": "A",
  "measure": "Décrire précisément la mesure réellement confirmée, y compris ses conditions.",
  "url": "https://source-officielle-ayant-ete-verifiee.example/programme",
  "scope": "personnel",
  "level": "direct",
  "review": "validation_humaine",
  "approved_by": "Initiales ou pseudonyme stable du relecteur",
  "approved_at": "2026-11-01",
  "source_location": "Titre, paragraphe ou page du document où figure la mesure",
  "source_date": "Date de publication du document si connue",
  "limit": "Expliquer les conditions, les exceptions, les désaccords possibles et la différence entre appui et priorité exclusive."
}
```

Ne jamais renseigner `scope: personnel` si une source représente seulement un texte de parti non adopté explicitement par la personnalité. De même, une source historique de 2022 ne vaut pas automatiquement engagement pour 2027. Une mesure compatible avec une option n'établit pas, à elle seule, qu'il s'agit de la priorité du candidat.

**Contrôle technique** : `python scripts/validate_publish.py`. Ce contrôle vérifie les champs et leur rattachement à une source surveillée ; il ne détermine pas si l'affirmation est politiquement exacte. Une attribution controversée doit être laissée dans la file de revue, non dans ce fichier.

**Important** : si un changement est invalidé après publication, supprimer l'objet correspondant et redéployer ; les anciennes versions restent dans l'historique GitHub pour assurer la traçabilité.
