WITH month_totals AS (
  SELECT month, COUNT(*) AS records, SUM(subscribed) AS subscriptions
  FROM campaign GROUP BY month
)
SELECT month, records, subscriptions,
       DENSE_RANK() OVER (ORDER BY subscriptions DESC) AS subscription_count_rank
FROM month_totals ORDER BY subscription_count_rank, month;
