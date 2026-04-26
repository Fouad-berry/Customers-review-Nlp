# 🗣️ Customer Reviews NLP Analysis

> Pipeline complet d'analyse d'avis clients avec **Hugging Face Transformers** : sentiment, détection de topics et résumé automatique sur **5 000 avis**.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![HuggingFace](https://img.shields.io/badge/🤗_Hugging_Face-Transformers-FFD21E.svg)
![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458.svg)
![Looker Studio](https://img.shields.io/badge/Looker_Studio-Dashboard-4285F4.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🎯 Objectif du projet

Construire un pipeline NLP de bout en bout pour analyser des avis clients :
1. **Récupération** des avis (ici dataset synthétique réaliste, à remplacer par scraping Trustpilot ou API en prod)
2. **Inférence Hugging Face** : sentiment + topics + résumé
3. **Datamarts analytiques** orientés cas d'usage métier
4. **Dashboard Looker Studio** pour les parties prenantes

**Questions métier :**
- Quelles entreprises ont le plus d'avis négatifs ?
- Sur quels sujets se concentre l'insatisfaction (livraison ? qualité ? service client ?)
- Le sentiment évolue-t-il dans le temps ?
- Quels mots reviennent dans les plaintes ?

---

## 🤗 Modèles Hugging Face utilisés

| Tâche | Modèle | Lien |
|-------|--------|------|
| **Sentiment FR** | `tblard/tf-allocine` | [HF Hub](https://huggingface.co/tblard/tf-allocine) |
| **Topic classification (zero-shot)** | `MoritzLaurer/mDeBERTa-v3-base-mnli-xnli` | [HF Hub](https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-mnli-xnli) |
| **Résumé FR** | `plguillou/t5-base-fr-sum-cnndm` | [HF Hub](https://huggingface.co/plguillou/t5-base-fr-sum-cnndm) |

---

## 📊 Aperçu des résultats

### Distribution des notes

![Rating distribution](images/figures/01_rating_distribution.png)

### Sentiment global détecté

![Sentiment pie](images/figures/02_sentiment_pie.png)

### Matrice topic × sentiment (où sont les pain points ?)

![Topic sentiment heatmap](images/figures/05_topic_sentiment_heatmap.png)

> La **livraison** génère le plus d'avis (positifs et négatifs confondus) — c'est le sujet le plus visible. La **qualité** et le **service client** concentrent une part significative d'avis négatifs.

### Évolution mensuelle du sentiment

![Sentiment timeline](images/figures/06_sentiment_timeline.png)

📁 **10 figures générées** dans [`images/figures/`](images/figures/).

---

## 📁 Structure du projet

```
customer-reviews-nlp/
│
├── data/
│   ├── raw/customer_reviews.csv              # 5000 avis bruts
│   ├── processed/reviews_enriched.csv        # Avec sentiment + topics + résumés
│   ├── datamarts/                            # 🧱 6 datamarts analytiques
│   │   ├── dm_global_kpis.csv
│   │   ├── dm_company_performance.csv
│   │   ├── dm_topic_sentiment.csv
│   │   ├── dm_company_topics.csv
│   │   ├── dm_sentiment_timeline.csv
│   │   └── dm_top_negative_keywords.csv
│   └── exports/                              # Exports Looker Studio
│
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_nlp_inference.ipynb                # 🤗 Pipeline HF Transformers
│   ├── 03_datamarts.ipynb
│   └── 04_visualizations.ipynb
│
├── src/
│   ├── nlp_inference.py                      # 🤗 Wrappers HF + fallback
│   └── __init__.py
│
├── sql/queries.sql                           # Requêtes BigQuery
├── dashboards/looker_studio_guide.md
├── docs/                                     # data dict, méthodologie, datamarts spec
├── images/figures/                           # 10 PNG pré-générés
│
├── generate_dataset.py                       # ⭐ Génère le dataset synthétique
├── build_project.py                          # ⭐ Pipeline complet (NLP + DM + figs)
├── .gitignore, LICENSE, requirements.txt
└── README.md
```

---

## 🚀 Installation & utilisation

### 1. Cloner le repo

```bash
git clone https://github.com/<ton-username>/customer-reviews-nlp.git
cd customer-reviews-nlp
```

### 2. Environnement virtuel + dépendances

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Générer le dataset synthétique

```bash
python generate_dataset.py
```

> Pour un vrai projet : remplace ce script par un scraper Trustpilot, l'API Amazon Reviews, ou charge un dataset depuis Hugging Face Datasets (`amazon_reviews_multi`, `allocine`, etc.)

### 4. Lancer le pipeline complet

**Mode rapide (rule-based, sans GPU)** :
```bash
python build_project.py
```

**Mode Hugging Face (vraie inférence Transformers)** :
```bash
pip install transformers torch
python build_project.py --use-transformers
```

> ⚠️ Le mode Transformers peut prendre 10-30 minutes sur CPU pour 5 000 avis. Sur GPU : ~2 minutes. Pour les démos rapides, le mode fallback rule-based suffit largement.

---

## 🔎 Workflow NLP

```
Raw reviews (5000)
     │
     ▼
[1] Sentiment analysis
     │  • Modèle FR fine-tuné sur AlloCine
     │  • Output : positive / neutral / negative + score de confiance
     ▼
[2] Topic classification (zero-shot)
     │  • mDeBERTa multilingue
     │  • Labels : livraison, qualité, service_client, prix, application
     │  • Pas besoin de fine-tuning !
     ▼
[3] Summarization (sur avis longs)
     │  • T5 français
     │  • Résumé en 1 phrase pour avis > 200 caractères
     ▼
[4] Datamarts + Figures + Looker
```

---

## 🧱 Les 6 datamarts

| Datamart | Cas d'usage |
|----------|-------------|
| `dm_global_kpis` | Scorecards (% positif, % négatif, note moyenne, total avis) |
| `dm_company_performance` | Comparaison des entreprises sur tous les KPIs |
| `dm_topic_sentiment` | Matrice de friction (où concentrer les efforts ?) |
| `dm_company_topics` | Pain points spécifiques à chaque entreprise |
| `dm_sentiment_timeline` | Évolution mensuelle du sentiment |
| `dm_top_negative_keywords` | Top 30 mots dans les avis négatifs |

---

## 📈 Dashboard Looker Studio

Le dashboard est organisé en **5 pages** :
1. **Overview** — KPIs globaux + distribution
2. **Companies** — Comparatif entreprises
3. **Topics** — Analyse des pain points
4. **Timeline** — Évolution temporelle
5. **Word analysis** — Mots-clés des avis négatifs

📄 Guide complet : [`dashboards/looker_studio_guide.md`](dashboards/looker_studio_guide.md).

---

## 📌 Principaux insights

- **45 %** des avis sont à 5 étoiles, **17 %** à 1-2 étoiles → distribution typique en U
- La **livraison** est le sujet le plus mentionné (positif comme négatif)
- Les avis négatifs sont en moyenne **plus courts** que les positifs (les clients mécontents sont plus directs)
- Le mot "**remboursement**" apparaît dans une grande partie des avis négatifs → KPI à surveiller

---

## 🛠️ Stack technique

- **Python 3.10+** · Pandas · NumPy
- **🤗 Hugging Face Transformers** (sentiment, zero-shot, summarization)
- **PyTorch** (backend)
- **Matplotlib / Seaborn** pour les figures
- **Jupyter** pour l'exploration
- **Looker Studio** pour le dashboard final

---

## 🚀 Pistes d'amélioration

- [ ] Remplacer le dataset synthétique par un vrai scraping Trustpilot ou un dataset HF
- [ ] Fine-tuner un modèle sur le domaine spécifique (e-commerce français)
- [ ] Déployer sur **Hugging Face Spaces** (Gradio) pour une démo interactive
- [ ] Ajouter un système RAG pour interroger les avis en langage naturel
- [ ] Embeddings (sentence-transformers) pour clustering des avis similaires

---

## 📝 Licence

MIT — voir [`LICENSE`](LICENSE).

---

## 👤 Auteur

**Fouad MOUTAIROU**
- GitHub : https://github.com/Fouad-berry
- LinkedIn : https://www.linkedin.com/in/fouad-moutairou-044460273
