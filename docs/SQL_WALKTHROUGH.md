# Why each SQL query is here

Run `python scripts/build.py` to create the SQLite database and every CSV in `results/`. The database uses SQLite. Use the files in order if you want to follow the business questions.

| SQL file | Question it answers | Why the query is written this way |
|---|---|---|
| [00_model](../sql/00_model.sql) | How do the source values become report labels? | Two small lookup tables keep month order and channel labels in one place. A view adds readable bands with CASE without changing the original counts. |
| [01_scorecard](../sql/01_scorecard.sql) | What is the overall result? | COUNT gives the number of records and SUM counts yes outcomes. NULLIF protects division when the table is empty. |
| [02_channel_coverage](../sql/02_channel_coverage.sql) | Can we compare channels on all records? | CASE counts known and missing labels before comparing rates. |
| [03_channel_comparison](../sql/03_channel_comparison.sql) | Which channels account for the subscriptions? | GROUP BY creates one row per channel. AVG on a 1/0 column gives the yes share within that group. |
| [04_month_mix](../sql/04_month_mix.sql) | How do counts and rates differ by month name? | Month number sorts the labels correctly. The table keeps both volume and rate visible. |
| [05_contact_bands](../sql/05_contact_bands.sql) | How do rates vary with the number of contacts? | A few readable ranges make 63 possible contact counts easier to compare. |
| [06_previous_contact](../sql/06_previous_contact.sql) | How different are records with and without earlier contact? | Group by the prior-contact flag, not by the previous campaign outcome. Those are different questions. |
| [07_previous_outcome](../sql/07_previous_outcome.sql) | Within prior contact, does the earlier outcome matter? | WHERE limits the comparison to records with prior contact. Unknown outcomes stay visible. |
| [08_known_channel_baseline](../sql/08_known_channel_baseline.sql) | How does the rate change if missing channels are excluded? | Recalculate the numerator and denominator together for the reduced set. |
| [09_channel_by_effort](../sql/09_channel_by_effort.sql) | Does the contact-count pattern look the same within channels? | Group by both labels so a channel with more high-effort records does not hide the within-channel pattern. This still does not control for every difference. |
| [10_rate_vs_baseline](../sql/10_rate_vs_baseline.sql) | How far is each band from the overall rate? | One CTE builds a single baseline; a CROSS JOIN attaches it to each band. Subtract rates before rounding, and multiply by 100 for percentage points. |
| [11_rank_months_by_volume](../sql/11_rank_months_by_volume.sql) | Which month labels produced the most subscriptions? | First total the rows by month; then DENSE_RANK ranks those totals and gives tied totals the same rank. |
| [12_history_by_effort](../sql/12_history_by_effort.sql) | What happens when we compare earlier outcomes within effort bands? | HAVING applies after grouping, so cells under 100 records stay out of this comparison. This rule is about readability, not statistical significance. |
| [13_prior_contact_recency](../sql/13_prior_contact_recency.sql) | How does the rate vary with the gap since earlier contact? | Remove blank gaps before putting known gaps into ranges. A record with no prior contact should not appear in the shortest-gap group. |
| [14_effort_sensitivity](../sql/14_effort_sensitivity.sql) | How much do high contact counts affect the overall numbers? | UNION ALL displays the full dataset beside the subset with up to six contacts. The sets overlap and should not be added together. |
| [15_history_coverage](../sql/15_history_coverage.sql) | Are earlier outcomes and contact gaps usable? | Check missing outcome labels and the observed range only for records with earlier contact. |

**A quick SQL vs. DAX distinction:** SQL groups and calculates a result table when the query runs. A DAX measure recalculates its result in the report each time the viewer changes the filters.
