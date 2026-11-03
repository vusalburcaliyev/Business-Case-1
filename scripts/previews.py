"""Generate portable README charts from the SQL output; no chart package needed."""
import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(name):
    with (ROOT / 'results' / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def text(x, y, label, size=18, color='#183441', weight=400):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}">{escape(str(label))}</text>')


def rect(x, y, width, height, fill, radius=0):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" fill="{fill}"/>'


def panel(x, title, subtitle, data, scale):
    parts = [
        rect(x, 144, 532, 296, '#fff', 16),
        text(x+22, 179, title, 23, weight=700),
        text(x+22, 204, subtitle, 15, '#42606c'),
    ]
    for i, (label, detail, value) in enumerate(data):
        y = 242 + 49*i
        parts.extend([
            text(x+22, y, label, 16, weight=650),
            text(x+260, y, detail, 15, '#42606c'),
            rect(x+22, y+10, 488, 9, '#e2eeed', 4),
            rect(x+22, y+10, 488*value/scale, 9, '#007b77', 4)
        ])
    return ''.join(parts)


def save(name, title, sub, panels, foot):
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1140 488" role="img" aria-label="'
        + escape(title, quote=True) + '" font-family="DejaVu Sans, sans-serif">',
        rect(0, 0, 1140, 488, '#eff4f4', 16),
        rect(0, 0, 1140, 122, '#102b38', 16),
        text(25, 30, 'BANK CAMPAIGN REVIEW', 14, '#b8ebe1', 700),
        text(25, 72, title, 33, '#ffffff', 700),
        text(25, 101, sub, 17, '#d8eaed'),
        *panels,
        text(25, 469, foot, 14, '#42606c'),
        '</svg>',
    ]
    (ROOT / 'assets' / (name+'.svg')).write_text('\n'.join(svg), encoding='utf-8')


def rate_rows(source, category):
    return [
        (r[category], f"{float(r['subscription_pct']):.2f}%  ·  {int(r['records']):,} records",
         float(r['subscription_pct']))
        for r in source
    ]


def main():
    (ROOT / 'assets').mkdir(exist_ok=True)
    score = read('01_scorecard.csv')[0]
    months = {r['month']: r for r in read('04_month_mix.csv')}
    month_rows = [
        (label, f"{int(months[label]['subscriptions']):,} yes  ·  {float(months[label]['subscription_pct']):.2f}% rate",
         int(months[label]['subscriptions'])) for label in ('May','Mar')
    ]
    save('overview','A high rate and a high count tell different stories',
         f"{int(score['records']):,} records  /  {int(score['subscriptions']):,} subscriptions  /  {float(score['subscription_pct']):.2f}% overall rate",
         [panel(24,'Rate by last contact channel','Rate scale: 0–20%',rate_rows(read('03_channel_comparison.csv'),'channel'),20),
          panel(584,'May and March: a closer look','Subscription count scale: 0–1,000',month_rows,1000)],
         'Source: UCI Bank Marketing, bank-full.csv. Month names group records; they do not form a time series.')
    save('followup','Review the follow-up pattern',
         'Historical comparisons show where to ask better questions.',
         [panel(24,'Rate by current contacts','Rate scale: 0–20%',rate_rows(read('05_contact_bands.csv'),'contact_band'),20),
          panel(584,'Rate by prior contact','Rate scale: 0–25%',rate_rows(read('06_previous_contact.csv'),'prior_contact'),25)],
         'Source: UCI Bank Marketing. The groups differ in more than contact count. These are observed rates.')


if __name__ == '__main__':
    main()
