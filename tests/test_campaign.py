import csv
import sqlite3
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CampaignChecks(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(ROOT / 'data/campaign.sqlite')
        self.addCleanup(self.db.close)

    def test_headline_and_export_grain(self):
        self.assertEqual(self.db.execute(
            'SELECT COUNT(*),COUNT(DISTINCT record_id),SUM(subscribed) FROM campaign'
        ).fetchone(), (45211, 45211, 5289))
        with (ROOT / 'data/Campaign.csv').open(encoding='utf-8', newline='') as f:
            rows = list(csv.DictReader(f))
        self.assertEqual((len(rows), sum(int(r['subscribed']) for r in rows)), (45211, 5289))

    def test_every_query_runs_and_month_groups_reconcile(self):
        for query in sorted((ROOT / 'sql').glob('[0-9][0-9]_*.sql')):
            if query.name.startswith('00_'):
                continue
            with self.subTest(query=query.name):
                self.assertTrue(self.db.execute(query.read_text(encoding='utf-8')).fetchall())
        monthly = self.db.execute((ROOT / 'sql/04_month_mix.sql').read_text(encoding='utf-8')).fetchall()
        self.assertEqual([r[0] for r in monthly], list(range(1, 13)))
        self.assertEqual((sum(r[2] for r in monthly),sum(r[3] for r in monthly)),(45211,5289))

    def test_unknown_channel_is_kept_and_subset_is_rebased(self):
        self.assertEqual(self.db.execute(
            "SELECT COUNT(*),SUM(subscribed) FROM campaign WHERE channel = 'Not recorded'"
        ).fetchone(), (13020, 530))
        self.assertEqual(self.db.execute((ROOT / 'sql/08_known_channel_baseline.sql').read_text(encoding='utf-8')).fetchone(),
                         (32191,4759,14.78))

    def test_no_prior_contact_is_distinct_from_unknown_outcome(self):
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM campaign WHERE days_since_prior IS NULL').fetchone()[0],36954)
        self.assertEqual(self.db.execute(
            "SELECT COUNT(*) FROM campaign WHERE prior_contact='Prior contact' AND previous_outcome='Outcome not recorded'"
        ).fetchone()[0],5)

    def test_effort_sensitivity_has_a_separate_denominator(self):
        rows = self.db.execute((ROOT / 'sql/14_effort_sensitivity.sql').read_text(encoding='utf-8')).fetchall()
        self.assertEqual(rows[0][1:4], (45211,5289,11.70))
        self.assertEqual(rows[1][1:4], (42147,5128,12.17))


if __name__ == '__main__':
    unittest.main()
