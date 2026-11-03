WITH recency AS (
  SELECT CASE WHEN days_since_prior <= 90 THEN '0–90 days'
              WHEN days_since_prior <= 180 THEN '91–180 days'
              ELSE '181+ days' END AS prior_gap,
         CASE WHEN days_since_prior <= 90 THEN 1
              WHEN days_since_prior <= 180 THEN 2 ELSE 3 END AS sort_key,
         subscribed
  FROM campaign WHERE days_since_prior IS NOT NULL
)
SELECT prior_gap, COUNT(*) AS records, SUM(subscribed) AS subscriptions,
       ROUND(100.0 * AVG(subscribed), 2) AS subscription_pct
FROM recency GROUP BY sort_key, prior_gap ORDER BY sort_key;
