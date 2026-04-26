
# 🧱 Spécification des datamarts

## 1. `dm_global_kpis.csv`

**Grain** : 1 ligne · **Usage** : scorecards

Colonnes : `total_reviews`, `unique_companies`, `avg_rating`, `pct_positive`, `pct_negative`, `pct_neutral`, `pct_verified`, `avg_review_length`, `sentiment_rating_match_pct`.

## 2. `dm_company_performance.csv`

**Grain** : 1 ligne par entreprise · **Usage** : comparatif sur la page "Companies"

Colonnes : `company`, `category`, `reviews`, `avg_rating`, `pct_positive`, `pct_negative`, `pct_neutral`, `pct_verified`, `avg_helpful_votes`.

Tri : par note moyenne décroissante.

## 3. `dm_topic_sentiment.csv`

**Grain** : topic × sentiment (~15 lignes) · **Usage** : matrice de friction

Colonnes : `top_topic`, `sentiment_label`, `reviews`, `avg_rating`.

## 4. `dm_company_topics.csv`

**Grain** : entreprise × topic · **Usage** : pain points spécifiques par entreprise

Colonnes : `company`, `top_topic`, `reviews`, `avg_rating`, `pct_negative`.

## 5. `dm_sentiment_timeline.csv`

**Grain** : mois × sentiment · **Usage** : évolution temporelle

Colonnes : `review_month`, `sentiment_label`, `reviews`, `avg_rating`.

## 6. `dm_top_negative_keywords.csv`

**Grain** : 30 mots les plus fréquents dans les avis négatifs

Colonnes : `word`, `frequency`.

## Règles communes

- Tous les % en base 100
- Arrondis à 2 décimales
- Source : `data/processed/reviews_enriched.csv`
- Régénérés à chaque exécution de `build_project.py`