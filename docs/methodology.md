# 🔬 Méthodologie

## 1. Acquisition des données

Le projet utilise un **dataset synthétique** généré par `generate_dataset.py` pour garantir la reproductibilité (5 000 avis sur 5 entreprises fictives).

**Pour un projet réel**, plusieurs alternatives :
- **Scraping Trustpilot** : avec `requests` + `BeautifulSoup` (attention aux TOS)
- **API Amazon Reviews** : payante mais propre
- **Datasets Hugging Face** :
  - [`amazon_reviews_multi`](https://huggingface.co/datasets/amazon_reviews_multi) — multilingue
  - [`allocine`](https://huggingface.co/datasets/allocine) — avis FR de cinéma
  - [`tweet_eval`](https://huggingface.co/datasets/tweet_eval) — sentiment sur tweets

## 2. Pipeline NLP avec Hugging Face

### Sentiment Analysis
Modèle : **`tblard/tf-allocine`** — DistilBERT fine-tuné sur 200 000 avis AlloCiné.
- ✅ Spécialisé français
- ✅ Rapide en inférence
- Output binaire : `POSITIVE` / `NEGATIVE` (on ajoute `neutral` à partir du score de confiance)

Alternative : `cmarkea/distilcamembert-base-sentiment` qui prédit directement les 5 classes.

### Topic Classification (Zero-Shot)
Modèle : **`MoritzLaurer/mDeBERTa-v3-base-mnli-xnli`** — multilingue, supporte le français.
- ✅ **Pas besoin de fine-tuning** : on donne juste les labels candidats
- ✅ Multi-label : un avis peut parler de plusieurs sujets
- ⚠️ Lent : ~0.5s par avis sur CPU → batch ou GPU recommandé

Labels candidats : `livraison`, `qualité`, `service client`, `prix`, `application`.

### Summarization
Modèle : **`plguillou/t5-base-fr-sum-cnndm`** — T5 français entraîné sur CNN/DailyMail.
- Appliqué uniquement aux avis longs (>200 caractères)
- Output : résumé en 1 phrase

## 3. Mode fallback (rule-based)

Pour la reproductibilité (CI/CD, démos sans GPU), un mode rule-based remplace les modèles HF :
- **Sentiment** : comptage de mots-clés positifs/négatifs/neutres + biais sur la note
- **Topics** : matching de mots-clés thématiques
- **Résumé** : extraction de la première phrase

C'est moins précis qu'un modèle entraîné, mais **runnable partout**. Le code documente clairement les deux modes.

## 4. Construction des datamarts

6 datamarts orientés cas d'usage métier (voir [`datamarts_spec.md`](datamarts_spec.md)). Chaque datamart répond à une question précise et est exportable directement vers Looker Studio.

## 5. Visualisations

- Palette sémantique : vert `#2ecc71` (positif), orange `#f39c12` (neutre), rouge `#e74c3c` (négatif)
- 10 figures PNG générées automatiquement, intégrées dans le README

## 6. Limitations

- **Dataset synthétique** : les insights ne représentent pas une réalité métier — c'est une démo de pipeline
- **Sentiment binaire HF** : le modèle AlloCiné ne prédit pas nativement "neutral" → on l'ajoute via le score
- **Zero-shot lent** : pour 100k+ avis, fine-tuner un modèle dédié sera plus rapide
- **Biais des modèles** : les modèles HF sont entraînés sur des données spécifiques (films, news…) et peuvent être moins précis sur certains domaines (banque, télécom…)

## 7. Pistes d'amélioration

- **Fine-tuning** sur le domaine spécifique pour gagner en précision
- **Embeddings + clustering** (sentence-transformers + HDBSCAN) pour découvrir des topics non prévus
- **NER** (Named Entity Recognition) pour extraire les noms de produits, montants, dates
- **Déploiement Gradio sur Hugging Face Spaces** pour une démo interactive
- **RAG** pour interroger les avis en langage naturel (ChatGPT-like sur tes données)