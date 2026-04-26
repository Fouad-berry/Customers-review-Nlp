# 📊 Guide Looker Studio

## 🔗 Lien du dashboard

> **[👉 Ouvrir le dashboard](https://lookerstudio.google.com/)** *(à remplacer)*

---

## 🚀 Connexion des données

Upload depuis `data/exports/` :
- `main_dataset.csv` (5 000 avis enrichis)
- `by_company.csv`
- `topic_sentiment.csv`
- `timeline.csv`
- `global_kpis.csv`

---

## 🎨 Structure en 5 pages

### 📄 Page 1 — Overview
- **5 scorecards** : total avis, % positif, % négatif, note moyenne, % achats vérifiés
- **Donut** : répartition sentiment global
- **Bar chart** : répartition des notes (1-5★)

### 📄 Page 2 — Companies
Source : `by_company.csv`
- **Bar chart horizontal** : entreprises triées par % négatif
- **Stacked bar** : composition sentiment par entreprise
- **Table** : tous les KPIs comparés

### 📄 Page 3 — Topics & Pain Points
Source : `topic_sentiment.csv` + `main_dataset.csv`
- **Heatmap** : entreprise × topic = % négatif
- **Bar chart** : nombre d'avis par topic
- **Filtrable** par sentiment

### 📄 Page 4 — Timeline
Source : `timeline.csv`
- **Line chart** : évolution sentiment par mois
- **Area chart** : volume d'avis dans le temps
- **Filtrable** par entreprise

### 📄 Page 5 — Word Analysis
Source : `dm_top_negative_keywords.csv` (à uploader)
- **Bar chart horizontal** : top 30 mots dans les avis négatifs
- **Table** : avis exemples filtrables par mot-clé

---

## 🎛️ Filtres globaux

- `company` (dropdown multiple)
- `category` (boutons)
- `sentiment_label` (boutons)
- `top_topic` (dropdown)
- `verified_purchase` (toggle)
- `review_date` (range)

---

## 💡 Champs calculés utiles

- `is_negative = IF(sentiment_label = "negative", 1, 0)` → pour des taux
- `month = MONTH(review_date)` → pour des analyses saisonnières
- `length_bucket = CASE WHEN review_length < 100 THEN "short" WHEN review_length < 300 THEN "medium" ELSE "long" END`

---

## 📸 Captures

```markdown
![Page 1](../images/dashboard_01.png)
![Page 3](../images/dashboard_03.png)
```