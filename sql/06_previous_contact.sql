SELECT prior_contact, COUNT(*) AS records, SUM(subscribed) AS subscriptions,
       ROUND(100.0 * AVG(subscribed), 2) AS subscription_pct
FROM campaign GROUP BY prior_contact ORDER BY records DESC;
