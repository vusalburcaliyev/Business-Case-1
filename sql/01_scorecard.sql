-- The denominator is campaign records, not unique people or individual calls.
SELECT COUNT(*) AS records, SUM(subscribed) AS subscriptions,
       COUNT(*) - SUM(subscribed) AS no_subscription,
       ROUND(100.0 * SUM(subscribed) / NULLIF(COUNT(*), 0), 2) AS subscription_pct,
       ROUND(AVG(contact_count), 2) AS avg_contacts
FROM campaign;
