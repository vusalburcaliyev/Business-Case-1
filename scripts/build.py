"""Build the SQLite model, SQL results, Power BI data, and browser dashboard."""
import csv
import gzip
import hashlib
import io
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_source():
    raw = gzip.decompress((ROOT / 'source/bank-full.csv.gz').read_bytes())
    expected = (ROOT / 'source/SHA256.txt').read_text(encoding='utf-8').split()[0]
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('The source snapshot does not match its checksum.')
    return list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig')), delimiter=';'))


def build_model(db, rows):
    db.executescript((ROOT / 'sql/00_model.sql').read_text(encoding='utf-8'))
    cleaned = []
    for i, row in enumerate(rows, 1):
        gap = int(row['pdays'])
        if gap < -1:
            raise ValueError(f'Unexpected prior gap at source row {i}')
        cleaned.append((
            i, row['contact'].strip().lower(), row['month'].strip().lower(),
            int(row['campaign']), int(row['previous']), None if gap == -1 else gap,
            row['poutcome'].strip().lower(), {'yes': 1, 'no': 0}[row['y']],
        ))
    with db:
        db.executemany('INSERT INTO campaign_record VALUES (?,?,?,?,?,?,?,?)', cleaned)
    if db.execute('PRAGMA foreign_key_check').fetchall():
        raise ValueError('The model contains unmatched lookup keys.')


def csv_export(path, cursor):
    with path.open('w', newline='', encoding='utf-8') as target:
        writer = csv.writer(target)
        writer.writerow([x[0] for x in cursor.description])
        writer.writerows(cursor)


def main():
    rows = load_source()
    out = ROOT / 'data'
    out.mkdir(exist_ok=True)
    (ROOT / 'results').mkdir(exist_ok=True)
    database = out / 'campaign.sqlite'
    database.unlink(missing_ok=True)
    with sqlite3.connect(database) as db:
        build_model(db, rows)
        csv_export(out / 'Campaign.csv', db.execute('SELECT * FROM campaign ORDER BY record_id'))
        for sql in sorted((ROOT / 'sql').glob('[0-9][0-9]_*.sql')):
            if sql.name.startswith('00_'):
                continue
            csv_export(ROOT / 'results' / (sql.stem + '.csv'), db.execute(sql.read_text(encoding='utf-8')))
        groups = db.execute("""
          SELECT channel, month_number, contact_band_order, prior_contact, previous_outcome,
                 COUNT(*), SUM(subscribed), SUM(contact_count)
          FROM campaign GROUP BY 1,2,3,4,5 ORDER BY 1,2,3,4,5
        """).fetchall()
        score = db.execute('SELECT COUNT(*), SUM(subscribed) FROM campaign').fetchone()
    if score != (len(rows), sum(row['y'] == 'yes' for row in rows)):
        raise ValueError('Counts did not reconcile with the source.')
    template = (ROOT / 'dashboard/template.html').read_text(encoding='utf-8')
    logic = (ROOT / 'dashboard/metrics.js').read_text(encoding='utf-8')
    html = template.replace('/* @METRICS */', logic).replace('/* @GROUPS */', json.dumps(groups).replace('<', '\\u003c'))
    (ROOT / 'dashboard/Bank_Campaign_Dashboard.html').write_text(html, encoding='utf-8')
    from previews import main as build_previews
    build_previews()
    print(f'{score[0]:,} records; {score[1]:,} subscriptions; {score[1]/score[0]:.2%} subscription rate.')
    print(f'Created 15 SQL result tables and {len(groups)} dashboard groups.')


if __name__ == '__main__':
    main()
