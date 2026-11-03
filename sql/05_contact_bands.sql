SELECT contact_band, COUNT(*) AS records, SUM(subscribed) AS subscriptions,
       ROUND(100.0 * AVG(subscribed), 2) AS subscription_pct,
       ROUND(AVG(contact_count), 2) AS avg_contacts
FROM campaign
GROUP BY contact_band_order, contact_band
ORDER BY contact_band_order;
