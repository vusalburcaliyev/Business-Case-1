const MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
const BANDS = ['1 contact','2–3 contacts','4–6 contacts','7+ contacts'];

// Group rows contain dimensions, followed by records, subscriptions, and contact sum.
// Add the counts first, then divide: an average of subgroup rates would be wrong.
function summarize(rows) {
  const total = rows.reduce((a, r) => ({
    records: a.records + r[5],
    subscriptions: a.subscriptions + r[6],
    contacts: a.contacts + r[7],
    known: a.known + (r[0] === 'Not recorded' ? 0 : r[5])
  }), {records: 0, subscriptions: 0, contacts: 0, known: 0});
  total.rate = total.records ? total.subscriptions / total.records : null;
  total.avgContacts = total.records ? total.contacts / total.records : null;
  total.knownShare = total.records ? total.known / total.records : null;
  return total;
}

function selectGroups(rows, filters) {
  return rows.filter(r =>
    (!filters.channel || r[0] === filters.channel) &&
    (!filters.month || r[1] === Number(filters.month)) &&
    (!filters.history || r[3] === filters.history));
}

function byCategory(rows, index, labels) {
  const groups = new Map();
  for (const row of rows) {
    const key = row[index];
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(row);
  }
  return [...groups].sort(([a],[b]) => typeof a === 'number' ? a - b : a.localeCompare(b))
    .map(([key, group]) => ({label: labels ? labels[key-1] : key, ...summarize(group)}));
}

if (typeof module !== 'undefined') module.exports = { summarize, selectGroups, byCategory };
