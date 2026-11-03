WITH baseline AS (SELECT AVG(subscribed) AS rate FROM campaign),
bands AS (
  SELECT contact_band, contact_band_order, COUNT(*) AS records,
         AVG(subscribed) AS rate
  FROM campaign GROUP BY contact_band, contact_band_order
)
SELECT contact_band, records, ROUND(100.0 * bands.rate, 2) AS subscription_pct,
       ROUND(100.0 * (bands.rate - baseline.rate), 2) AS gap_pp
FROM bands CROSS JOIN baseline ORDER BY contact_band_order;
