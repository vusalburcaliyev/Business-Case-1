# Open the Power BI report

This is a native, editable Power BI Desktop project. It contains built-in Power BI visuals, a semantic model, and DAX measures.

1. On the repository's main page, choose **Code → Download ZIP** and extract it. Keep the `.Report` and `.SemanticModel` folders alongside `BankCampaign.pbip`.
2. Open [`BankCampaign.pbip`](BankCampaign.pbip) in an up-to-date **Power BI Desktop** on Windows. If your version labels Power BI Project as a preview option, enable that option and restart Desktop.
3. Choose **Home → Refresh** on the first open. The report imports its embedded summaries; no database credentials or extra CSV downloads are needed.
4. Use the slicers to explore the report. Select a visual to change its fields or formatting, or choose a measure in the model to read its DAX. To keep a single-file copy, use **File → Save as → Power BI file (.pbix)**.

**Pages:** Campaign overview and follow-up history.

The report uses summarized campaign groups by month label, channel, contact frequency, and history. Subscription rate is total subscriptions divided by campaign records in the current selection. The full row-level rebuild remains available in `BUILD_GUIDE.md`.

The report definition was checked with Microsoft's Power BI authoring validator, and the embedded results were reconciled to the project outputs. The report was not opened in Power BI Desktop in this environment.
