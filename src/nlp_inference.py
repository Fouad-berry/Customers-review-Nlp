"""
nlp_inference.py
----------------
Inférence NLP avec Hugging Face Transformers.

Trois tâches NLP sont appliquées à chaque avis :
  1. Sentiment (positif / neutre / négatif)
  2. Détection de topics (livraison, qualité, support, prix, app, autre)
  3. Résumé automatique (pour avis longs)

⚠️ MODE D'EXÉCUTION
-------------------
Ce module a deux modes :

  • MODE LOCAL (recommandé) — les vrais modèles HF Transformers sont chargés
    et appliqués. Lance `python build_project.py --use-transformers`
    après avoir installé `pip install transformers torch`.

  • MODE FALLBACK (par défaut dans build_project.py) — utilise une approche
    rule-based qui imite les sorties d'un modèle de sentiment.
    Permet de générer datamarts + figures sans GPU ni install lourde.
    Utile pour CI/CD, démos, et reproductibilité du projet.

En production tu utiliseras toujours le mode LOCAL. Le mode FALLBACK
existe uniquement pour que le pipeline soit runnable partout.
"""

import re
from typing import List, Dict


# ============================================================
# MODE LOCAL — vraie inférence Hugging Face
# ============================================================
def load_real_pipelines():
    """
    Charge les 3 pipelines Hugging Face.
    À appeler quand transformers + torch sont installés.

    Modèles utilisés :
      • Sentiment : tblard/tf-allocine (fine-tuné sur des avis FR)
        Alternative : cmarkea/distilcamembert-base-sentiment
      • Topics    : zero-shot avec MoritzLaurer/mDeBERTa-v3-base-mnli-xnli
        (multilingue, supporte le français, pas besoin de fine-tuning)
      • Résumé    : plguillou/t5-base-fr-sum-cnndm (T5 français)
    """
    from transformers import pipeline

    sentiment_pipe = pipeline(
        "sentiment-analysis",
        model="tblard/tf-allocine",
        tokenizer="tblard/tf-allocine",
    )

    topic_pipe = pipeline(
        "zero-shot-classification",
        model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli",
    )

    summary_pipe = pipeline(
        "summarization",
        model="plguillou/t5-base-fr-sum-cnndm",
    )

    return sentiment_pipe, topic_pipe, summary_pipe


def infer_sentiment_real(texts: List[str], pipe) -> List[Dict]:
    """Applique le modèle de sentiment HF à une liste de textes."""
    results = pipe(texts, batch_size=32, truncation=True, max_length=512)
    return [
        {
            "sentiment_label": "positive" if r["label"] == "POSITIVE" else "negative",
            "sentiment_score": round(r["score"], 4),
        }
        for r in results
    ]


def infer_topics_real(texts: List[str], pipe, candidate_labels: List[str]) -> List[Dict]:
    """Zero-shot classification multi-label des topics."""
    out = []
    for text in texts:
        r = pipe(text, candidate_labels, multi_label=True)
        # On garde les labels avec score > 0.5
        topics = [lab for lab, sc in zip(r["labels"], r["scores"]) if sc > 0.5]
        out.append({
            "topics": "|".join(topics) if topics else "autre",
            "top_topic": r["labels"][0],
            "top_topic_score": round(r["scores"][0], 4),
        })
    return out


def summarize_real(text: str, pipe, max_length: int = 60) -> str:
    """Résume un texte (utile uniquement pour les longs avis)."""
    if len(text.split()) < 30:
        return text
    r = pipe(text, max_length=max_length, min_length=15, do_sample=False)
    return r[0]["summary_text"]


# ============================================================
# MODE FALLBACK — approche rule-based pour reproductibilité
# ============================================================
POSITIVE_KW = {
    "excellent", "super", "parfait", "top", "satisfait", "recommande",
    "bravo", "merci", "fidèle", "rapide", "qualité", "professionnel",
    "bonne", "bluffé", "génial", "ravi", "content", "impeccable",
    "réactif", "soigné", "fluide", "imbattable",
}
NEGATIVE_KW = {
    "déçu", "catastrophique", "honteux", "fuir", "arnaque", "incompétent",
    "défectueux", "cassé", "retard", "abusif", "trompeuse", "fraudes",
    "remboursement", "annulation", "plante", "frais cachés", "pire",
    "déception", "signaler", "perd son temps",
}
NEUTRAL_KW = {
    "correct", "moyen", "moyenne", "acceptable", "sans plus", "ça fait",
    "conforme", "pas mal", "ailleurs",
}

TOPIC_KEYWORDS = {
    "livraison":     ["livraison", "livré", "colis", "emballage", "24h", "48h", "retard", "rapide", "expédition"],
    "qualité":       ["qualité", "produit", "défectueux", "cassé", "fonctionne", "soigné", "description"],
    "service_client": ["service client", "support", "réponse", "réactif", "incompétent", "mail", "contacter", "communication"],
    "prix":          ["prix", "rapport qualité-prix", "frais", "remboursement", "prélèvements", "abusif"],
    "application":   ["application", "app", "fluide", "intuitive", "plante"],
}


def infer_sentiment_fallback(text: str, rating: int) -> Dict:
    """Approche rule-based : compte les mots-clés + biais sur le rating."""
    text_low = text.lower()
    pos = sum(1 for kw in POSITIVE_KW if kw in text_low)
    neg = sum(1 for kw in NEGATIVE_KW if kw in text_low)
    neu = sum(1 for kw in NEUTRAL_KW if kw in text_low)

    # Le rating reste un signal très fort qu'on combine
    if rating >= 4:
        score_pos = pos + 2
        score_neg = neg
        score_neu = neu
    elif rating == 3:
        score_pos = pos
        score_neg = neg
        score_neu = neu + 2
    else:
        score_pos = pos
        score_neg = neg + 2
        score_neu = neu

    scores = {"positive": score_pos, "negative": score_neg, "neutral": score_neu}
    label = max(scores, key=scores.get)
    total = sum(scores.values()) or 1
    return {
        "sentiment_label": label,
        "sentiment_score": round(scores[label] / total, 4),
    }


def infer_topics_fallback(text: str) -> Dict:
    """Détecte les topics par recherche de mots-clés."""
    text_low = text.lower()
    detected = []
    scores = {}
    for topic, kws in TOPIC_KEYWORDS.items():
        match_count = sum(1 for kw in kws if kw in text_low)
        if match_count > 0:
            detected.append(topic)
            scores[topic] = match_count

    if not detected:
        return {"topics": "autre", "top_topic": "autre", "top_topic_score": 0.0}

    top = max(scores, key=scores.get)
    return {
        "topics": "|".join(detected),
        "top_topic": top,
        "top_topic_score": round(scores[top] / 5.0, 4),
    }


def summarize_fallback(text: str, max_words: int = 15) -> str:
    """Extrait la première phrase (ou tronque)."""
    first_sentence = re.split(r"[.!?]", text)[0].strip()
    words = first_sentence.split()
    if len(words) > max_words:
        return " ".join(words[:max_words]) + "..."
    return first_sentence + "."
