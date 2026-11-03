-- A readability threshold, not a significance test.
SELECT previous_outcome, contact_band, COUNT(*) AS records,
       SUM(subscribed) AS subscriptions, ROUND(100.0 * AVG(subscribed), 2) AS subscription_pct
FROM campaign
WHERE prior_contact = 'Prior contact'
GROUP BY previous_outcome, contact_band_order, contact_band
HAVING COUNT(*) >= 100
ORDER BY previous_outcome, contact_band_order;
