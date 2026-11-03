SELECT COUNT(*) AS records,
       SUM(CASE WHEN channel = 'Not recorded' THEN 1 ELSE 0 END) AS unknown_channel,
       ROUND(100.0 * SUM(CASE WHEN channel <> 'Not recorded' THEN 1 ELSE 0 END)
             / NULLIF(COUNT(*), 0), 2) AS known_channel_pct
FROM campaign;
