# What one row means

One row is one record from UCI's `bank-full.csv`, with the outcome of the current campaign. Multiple contacts can be recorded on a single row. There is no customer ID, so the project cannot count unique customers across rows. A generated record ID identifies the source row only.

| Campaign.csv field | Type in Power BI | Meaning |
|---|---|---|
| record_id | Whole number | Source row number, starting at 1; not a customer identifier. |
| channel | Text | Last contact type: Cellular, Telephone, or Not recorded. |
| month | Text | Month name of the last recorded contact. There is no year column in this file. |
| month_number | Whole number | January = 1 through December = 12. Used to sort month names. |
| contact_count | Whole number | Contacts in the current campaign for the record, including the last one. |
| contact_band | Text | 1, 2–3, 4–6, or 7+ contacts. |
| contact_band_order | Whole number | Sort order 1 through 4. |
| prior_contact | Text | Prior contact when previous_contacts is greater than zero; otherwise No prior contact. |
| previous_outcome | Text | Prior campaign outcome, No prior contact, or Outcome not recorded when earlier contact exists but its outcome is unknown. |
| previous_contacts | Whole number | Count of contacts before the current campaign. |
| days_since_prior | Whole number (nullable) | Days since last prior campaign contact. Source `-1` becomes blank, not zero days. |
| subscribed | Whole number | 1 if the current record ended in a subscription; otherwise 0. |

The SQLite model has one record table and two lookup tables: channel and month. Each lookup key is unique. The campaign view joins one label per key and adds the contact and history groups. The Power BI CSV is the exported view.

Age, job, marital status, balances, loan fields, and last-call duration are outside this analysis. Last-call duration is only known after the call, so it would not be available for planning before the call.

## Data checks

- Source: 45,211 records; 5,289 yes outcomes. All rows are retained. There were no identical full-source rows. A record ID was assigned in source order; identical analytical values would not prove a duplicate person.
- Channel was unknown on 13,020 records. Those rows remain in the overall rate.
- No prior contact: 36,954 records. Prior contact: 8,257 records. In the prior-contact group, 5 outcomes were not recorded. An unknown prior outcome does not mean there was no prior contact.
- Contact count ranges from 1 to 63. The 25th and 75th percentiles are 1 and 3, so the upper 1.5 × IQR rule gives 6. Values above 6 are flagged for comparison and kept in headline results.
- SQL constraints check valid labels, positive current-contact counts, and the relationship between prior contacts and prior-gap blanks. A source checksum and count reconciliation protect the build.
