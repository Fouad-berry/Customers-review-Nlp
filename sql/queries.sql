-- ============================================
-- queries.sql
-- Requêtes analytiques (BigQuery / DuckDB)
-- ============================================

-- 1. KPIs globaux
SELECT
    COUNT(*)                                                AS total_reviews,
    ROUND(AVG(rating), 2)                                   AS avg_rating,
    ROUND(100 * SUM(IF(sentiment_label='positive', 1, 0)) / COUNT(*), 2) AS pct_positive,
    ROUND(100 * SUM(IF(sentiment_label='negative', 1, 0)) / COUNT(*), 2) AS pct_negative
FROM `customer_reviews.reviews`;


-- 2. Performance par entreprise
SELECT
    company, category,
    COUNT(*) AS reviews,
    ROUND(AVG(rating), 2) AS avg_rating,
    ROUND(100 * SUM(IF(sentiment_label='negative', 1, 0)) / COUNT(*), 2) AS pct_negative
FROM `customer_reviews.reviews`
GROUP BY company, category
ORDER BY pct_negative DESC;


-- 3. Pain points par topic
SELECT
    top_topic,
    COUNT(*) AS reviews,
    ROUND(100 * SUM(IF(sentiment_label='negative', 1, 0)) / COUNT(*), 2) AS pct_negative,
    ROUND(AVG(rating), 2) AS avg_rating
FROM `customer_reviews.reviews`
GROUP BY top_topic
ORDER BY pct_negative DESC;


-- 4. Évolution mensuelle
SELECT
    review_month,
    sentiment_label,
    COUNT(*) AS reviews
FROM `customer_reviews.reviews`
GROUP BY review_month, sentiment_label
ORDER BY review_month, sentiment_label;


-- 5. Pire combinaison entreprise × topic
SELECT
    company, top_topic,
    COUNT(*) AS reviews,
    ROUND(100 * SUM(IF(sentiment_label='negative', 1, 0)) / COUNT(*), 2) AS pct_negative
FROM `customer_reviews.reviews`
GROUP BY company, top_topic
HAVING reviews >= 50
ORDER BY pct_negative DESC
LIMIT 10;


-- 6. Cohérence du modèle (sentiment vs rating)
SELECT
    rating,
    sentiment_label,
    COUNT(*) AS n
FROM `customer_reviews.reviews`
GROUP BY rating, sentiment_label
ORDER BY rating, sentiment_label;