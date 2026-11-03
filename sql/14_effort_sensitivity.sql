SELECT 'All records' AS population, COUNT(*) AS records, SUM(subscribed) AS subscriptions,
       ROUND(100.0 * AVG(subscribed), 2) AS subscription_pct,
       ROUND(AVG(contact_count), 2) AS avg_contacts
FROM campaign
UNION ALL
SELECT 'Up to 6 contacts', COUNT(*), SUM(subscribed),
       ROUND(100.0 * AVG(subscribed), 2), ROUND(AVG(contact_count), 2)
FROM campaign WHERE contact_count <= 6;
