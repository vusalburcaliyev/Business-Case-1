PRAGMA foreign_keys = ON;

CREATE TABLE channel (
  channel_id TEXT PRIMARY KEY,
  label TEXT NOT NULL
);
INSERT INTO channel VALUES
  ('cellular', 'Cellular'), ('telephone', 'Telephone'), ('unknown', 'Not recorded');

CREATE TABLE month (
  month_id TEXT PRIMARY KEY,
  month_number INTEGER NOT NULL UNIQUE,
  label TEXT NOT NULL
);
INSERT INTO month VALUES
  ('jan',1,'Jan'), ('feb',2,'Feb'), ('mar',3,'Mar'), ('apr',4,'Apr'),
  ('may',5,'May'), ('jun',6,'Jun'), ('jul',7,'Jul'), ('aug',8,'Aug'),
  ('sep',9,'Sep'), ('oct',10,'Oct'), ('nov',11,'Nov'), ('dec',12,'Dec');

CREATE TABLE campaign_record (
  record_id INTEGER PRIMARY KEY,
  channel_id TEXT NOT NULL REFERENCES channel(channel_id),
  month_id TEXT NOT NULL REFERENCES month(month_id),
  contact_count INTEGER NOT NULL CHECK (contact_count >= 1),
  previous_contacts INTEGER NOT NULL CHECK (previous_contacts >= 0),
  days_since_prior INTEGER CHECK (days_since_prior >= 0),
  prior_outcome TEXT NOT NULL CHECK (prior_outcome IN ('unknown','other','failure','success')),
  subscribed INTEGER NOT NULL CHECK (subscribed IN (0, 1)),
  CHECK ((days_since_prior IS NULL) = (previous_contacts = 0))
);

-- Each join looks up one label, so it cannot multiply the campaign records.
CREATE VIEW campaign AS
SELECT r.record_id, c.label AS channel, m.label AS month, m.month_number,
       r.contact_count,
       CASE WHEN contact_count = 1 THEN '1 contact'
            WHEN contact_count <= 3 THEN '2–3 contacts'
            WHEN contact_count <= 6 THEN '4–6 contacts'
            ELSE '7+ contacts' END AS contact_band,
       CASE WHEN contact_count = 1 THEN 1 WHEN contact_count <= 3 THEN 2
            WHEN contact_count <= 6 THEN 3 ELSE 4 END AS contact_band_order,
       CASE WHEN previous_contacts = 0 THEN 'No prior contact'
            ELSE 'Prior contact' END AS prior_contact,
       CASE WHEN previous_contacts = 0 THEN 'No prior contact'
            WHEN prior_outcome = 'unknown' THEN 'Outcome not recorded'
            ELSE upper(substr(prior_outcome,1,1)) || substr(prior_outcome,2) END AS previous_outcome,
       previous_contacts, days_since_prior, subscribed
FROM campaign_record r
JOIN channel c USING (channel_id)
JOIN month m USING (month_id);
