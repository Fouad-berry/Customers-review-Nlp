# 📖 Data Dictionary

## Dataset principal : `customer_reviews.csv` (5 000 lignes)

| Variable | Type | Description |
|----------|------|-------------|
| `review_id` | string | Identifiant unique (ex: `R00001`) |
| `company` | string | Entreprise concernée (5 modalités) |
| `category` | string | Secteur d'activité |
| `rating` | int | Note attribuée par le client (1-5) |
| `review_text` | string | Texte de l'avis |
| `review_date` | date | Date de publication |
| `verified_purchase` | bool | Achat vérifié ou non |
| `helpful_votes` | int | Nombre de votes "utile" |
| `review_length` | int | Longueur en caractères |

## Dataset enrichi : `reviews_enriched.csv` (après NLP)

Mêmes colonnes que ci-dessus, **plus** :

| Variable | Description |
|----------|-------------|
| `sentiment_label` | `positive` / `neutral` / `negative` (sortie HF) |
| `sentiment_score` | Score de confiance du modèle (0-1) |
| `topics` | Liste des topics détectés (séparés par `\|`) |
| `top_topic` | Topic principal (livraison, qualité, service_client, prix, application, autre) |
| `top_topic_score` | Score du topic principal |
| `summary` | Résumé automatique de l'avis |
| `review_month` | Mois de publication (format YYYY-MM) |
| `sentiment_match_rating` | 1 si le sentiment prédit correspond à la note (4-5★ → positive, 3★ → neutral, 1-2★ → negative) |

## Entreprises présentes

| Company | Catégorie |
|---------|-----------|
| TechBox | E-commerce électronique |
| FashionLine | Mode et vêtements |
| FoodDelivery | Livraison de repas |
| BankZen | Banque en ligne |
| TravelEase | Voyages et hôtellerie |

## Notes méthodologiques

- **Dataset synthétique** généré par `generate_dataset.py` — pour un vrai projet, remplacer par scraping ou API
- **Période** : 480 jours (~16 mois) à partir du 1er janvier 2024
- **Distribution des notes** : volontairement déséquilibrée (45 % de 5★, 17 % de 1-2★) pour mimer la distribution typique observée sur Trustpilot
- **Modèles HF** : optimisés pour le français
