# Rebuild the dashboard in Power BI Desktop

The [browser dashboard](../dashboard/Bank_Campaign_Dashboard.html) is ready to open offline. To build your own Power BI report, follow the steps below. This project includes the data, measures, and layout; it does not include a tested `.pbix` file.

## 1. Import one clean table

1. In Power BI Desktop, select **Get data → Text/CSV** and open `data/Campaign.csv`. Use UTF-8 and comma delimiter.
2. Select **Transform Data**, rename the table **Campaign**, and check the types in the [data dictionary](../docs/DATA_DICTIONARY.md).
3. Select **Close & Apply**. Sort `month` by `month_number` and `contact_band` by `contact_band_order`.
4. Under **Modeling → New measure**, add each measure from [measures.dax](measures.dax) separately, in file order. Format rates and shares as percentages with two decimals. Format Average Contacts with two decimals.

No relationship setup is required: the SQL model already joins the lookup labels into the CSV. Month is a name, so do not turn it into a fake date.

## 2. Define the measures

| Measure | What it tells the team | Why this formula? |
|---|---|---|
| Campaign Records | Rows in the current selection | COUNTROWS uses the same denominator as SQL. COALESCE shows zero when the selection is empty. |
| Subscriptions | Rows that ended in a yes | The data stores yes as 1 and no as 0, so SUM counts the yes outcomes. |
| Subscription Rate | Subscriptions divided by records | DIVIDE recomputes the rate from the totals in the current view. It returns blank when there are no records to compare. |
| Average Contacts | Mean current-campaign contacts per record | AVERAGE uses the number of contacts recorded on each row. This is not average call duration. |
| Known Channel Records | Rows with a cellular or telephone label | CALCULATE adds a condition. KEEPFILTERS respects the viewer's channel choice: if they pick Not recorded, the result is zero. |
| Known Channel Share | How much of the selection has a known channel | Dividing the known count by all selected rows keeps missing labels visible. |
| Prior Contact Records | Rows with at least one earlier campaign contact | Keep the current filters and narrow the count to the prior-contact group. |
| Prior Contact Subscription Rate | Subscription rate for that prior-contact group | Apply the same group filter to both numerator and denominator by wrapping the rate measure. |
| High Effort Records | Rows with at least seven current contacts | Count rows that cross the review threshold. It is a review flag, not a rule to stop calling. |

References: [DIVIDE](https://learn.microsoft.com/en-us/dax/divide-function-dax) and [CALCULATE / KEEPFILTERS](https://learn.microsoft.com/en-us/dax/calculate-function-dax).

## 3. Build two pages

| Page | Visual | Put these fields on it |
|---|---|---|
| Campaign overview | Four cards | Campaign Records, Subscriptions, Subscription Rate, Known Channel Share |
| Campaign overview | Bar chart: rate by channel | channel on category axis; Subscription Rate as value; add Campaign Records and Subscriptions as tooltips |
| Campaign overview | Column chart: subscriptions by month | month on X; Subscriptions on Y; add Campaign Records and Subscription Rate as tooltips |
| Follow-up and history | Four cards | Average Contacts, High Effort Records, Prior Contact Records, Prior Contact Subscription Rate |
| Follow-up and history | Bar chart: rate by contact band | contact_band on category axis; Subscription Rate as value; add Campaign Records and Subscriptions as tooltips |
| Follow-up and history | Matrix: prior outcomes | previous_outcome on Rows; Campaign Records, Subscriptions, Subscription Rate on Values; filter this visual to Prior contact |

Add `channel`, `month`, and `prior_contact` slicers. Use **View → Sync slicers** if you want the same choices across both pages. Keep a note near the visuals that rates are descriptive and that records are not unique people.

## 4. Check the numbers before styling

| Selection | Records | Subscriptions | Rate |
|---|---:|---:|---:|
| All | 45,211 | 5,289 | 11.70% |
| Cellular | 29,285 | 4,369 | 14.92% |
| Not recorded | 13,020 | 530 | 4.07% |
| Prior contact | 8,257 | 1,905 | 23.07% |

With no filters, also check average contacts **2.76**, known channel share **71.20%**, and high effort records **3,064**. Under Not recorded, known channel share should be **0.00%**. Under No prior contact, prior contact count should be **0** and its subscription rate blank. These expected values come from the tested data and SQL. Use them to verify your Power BI build.
