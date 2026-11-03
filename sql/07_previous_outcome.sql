-- Compare recorded outcomes only among records with a prior contact.
SELECT previous_outcome, COUNT(*) AS records, SUM(subscribed) AS subscriptions,
       ROUND(100.0 * AVG(subscribed), 2) AS subscription_pct
FROM campaign WHERE prior_contact = 'Prior contact'
GROUP BY previous_outcome ORDER BY records DESC;
