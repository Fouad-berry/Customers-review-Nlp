"""
generate_dataset.py
-------------------
Génère un dataset synthétique de 5000 avis clients en français
imitant ce qu'on récupèrerait d'une plateforme type Trustpilot.

Pourquoi synthétique ?
- Reproductibilité : n'importe qui peut relancer le projet
- Pas de problème légal (TOS Trustpilot, scraping…)
- Volume contrôlé pour démo

Pour un vrai projet : remplacer par un scraper Trustpilot,
l'API Amazon Reviews, ou des datasets HF (amazon_reviews_multi, etc.)
"""

from pathlib import Path
import random
import pandas as pd
from datetime import datetime, timedelta

random.seed(42)

OUT = Path(__file__).resolve().parent / "data" / "raw" / "customer_reviews.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

# ============================================================
# Templates de reviews par catégorie et par rating
# ============================================================
COMPANIES = {
    "TechBox":      "E-commerce électronique",
    "FashionLine":  "Mode et vêtements",
    "FoodDelivery": "Livraison de repas",
    "BankZen":      "Banque en ligne",
    "TravelEase":   "Voyages et hôtellerie",
}

POSITIVE_TEMPLATES = [
    "Excellent service, je recommande vivement ! La livraison a été {speed} et le produit correspond parfaitement à la description.",
    "Très satisfait de mon achat. {detail_pos} Je commanderai à nouveau sans hésiter.",
    "Super expérience, {detail_pos} Le service client est réactif et professionnel.",
    "Parfait du début à la fin. {detail_pos} Rien à redire, je suis client fidèle maintenant.",
    "Vraiment au top ! {detail_pos} Merci pour cette belle expérience.",
    "Rien à reprocher, tout s'est passé comme prévu. {detail_pos} Bravo à toute l'équipe.",
    "Excellente qualité pour le prix. {detail_pos} Je suis bluffé par la rapidité du service.",
    "Une vraie bonne surprise ! {detail_pos} Je le recommanderai à mes proches.",
]

NEUTRAL_TEMPLATES = [
    "Service correct sans plus. {detail_neu} Pas vraiment de quoi se plaindre mais rien d'extraordinaire non plus.",
    "Expérience moyenne. {detail_neu} J'ai eu mieux ailleurs mais c'est acceptable.",
    "Produit conforme à la description. {detail_neu} La livraison aurait pu être plus rapide.",
    "Ça fait le job. {detail_neu} On verra à la prochaine commande si je reviens.",
    "Bon rapport qualité-prix mais {detail_neu} Quelques détails à améliorer.",
    "Pas mal dans l'ensemble. {detail_neu} Je verrai si je récidive.",
]

NEGATIVE_TEMPLATES = [
    "Très déçu de mon expérience. {detail_neg} Je ne recommande absolument pas.",
    "Service catastrophique ! {detail_neg} Je veux être remboursé immédiatement.",
    "Quelle déception... {detail_neg} On m'avait pourtant recommandé cette entreprise.",
    "Aucune communication, support client inexistant. {detail_neg} À fuir.",
    "Produit défectueux et impossible d'avoir un remboursement. {detail_neg} Honteux.",
    "Pire expérience d'achat. {detail_neg} Je vais signaler à la répression des fraudes.",
    "Arnaque totale. {detail_neg} N'achetez surtout pas chez eux.",
    "Service client incompétent. {detail_neg} On perd son temps à les contacter.",
]

DETAILS_POS = [
    "L'emballage était soigné.",
    "Le produit est de très bonne qualité.",
    "La livraison a été ultra rapide, en 24h.",
    "Le service client a répondu en moins d'une heure.",
    "Le rapport qualité-prix est imbattable.",
    "L'application est fluide et intuitive.",
    "Les frais de livraison sont raisonnables.",
]

DETAILS_NEU = [
    "L'emballage était basique mais protecteur.",
    "La livraison a pris une semaine.",
    "Le produit fonctionne mais sans plus.",
    "Le service client met du temps à répondre.",
    "Le prix est dans la moyenne du marché.",
]

DETAILS_NEG = [
    "Livraison en retard de 3 semaines sans aucune explication.",
    "Produit reçu cassé et remboursement refusé.",
    "Le service client ne répond jamais aux mails.",
    "Frais cachés non mentionnés au moment du paiement.",
    "L'application plante en permanence.",
    "Description du produit complètement trompeuse.",
    "Annulation impossible et prélèvements abusifs.",
]

SPEEDS = ["très rapide", "rapide", "en 48h", "en 24h"]

# ============================================================
# Génération
# ============================================================
def generate_review(company: str, rating: int) -> str:
    if rating >= 4:
        tpl = random.choice(POSITIVE_TEMPLATES)
        return tpl.format(speed=random.choice(SPEEDS),
                          detail_pos=random.choice(DETAILS_POS))
    elif rating == 3:
        tpl = random.choice(NEUTRAL_TEMPLATES)
        return tpl.format(detail_neu=random.choice(DETAILS_NEU))
    else:
        tpl = random.choice(NEGATIVE_TEMPLATES)
        return tpl.format(detail_neg=random.choice(DETAILS_NEG))


def generate_dataset(n: int = 5000) -> pd.DataFrame:
    rows = []
    start_date = datetime(2024, 1, 1)

    # Distribution réaliste : pas mal de 5*, quelques 1*, peu de neutres
    rating_weights = [0.10, 0.07, 0.13, 0.25, 0.45]

    for i in range(1, n + 1):
        company = random.choice(list(COMPANIES.keys()))
        rating = random.choices([1, 2, 3, 4, 5], weights=rating_weights)[0]
        review = generate_review(company, rating)
        date = start_date + timedelta(days=random.randint(0, 480))
        verified = random.random() < 0.78
        helpful = random.randint(0, 50) if rating <= 2 else random.randint(0, 15)

        rows.append({
            "review_id":      f"R{i:05d}",
            "company":        company,
            "category":       COMPANIES[company],
            "rating":         rating,
            "review_text":    review,
            "review_date":    date.strftime("%Y-%m-%d"),
            "verified_purchase": verified,
            "helpful_votes":  helpful,
            "review_length":  len(review),
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = generate_dataset(5000)
    df.to_csv(OUT, index=False)
    print(f"✓ {len(df)} avis générés → {OUT}")
    print("\nDistribution des notes :")
    print(df["rating"].value_counts().sort_index())
    print("\nPar entreprise :")
    print(df["company"].value_counts())