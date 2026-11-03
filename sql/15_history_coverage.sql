SELECT COUNT(*) AS prior_contact_records,
       SUM(CASE WHEN previous_outcome = 'Outcome not recorded' THEN 1 ELSE 0 END) AS outcome_not_recorded,
       MIN(days_since_prior) AS min_days_since_prior,
       MAX(days_since_prior) AS max_days_since_prior
FROM campaign WHERE prior_contact = 'Prior contact';
