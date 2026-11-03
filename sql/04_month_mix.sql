-- Month-of-year categories, not a timeline: the selected file has no year field.
SELECT month_number, month, COUNT(*) AS records, SUM(subscribed) AS subscriptions,
       ROUND(100.0 * AVG(subscribed), 2) AS subscription_pct
FROM campaign GROUP BY month_number, month ORDER BY month_number;
