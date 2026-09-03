# Project FORESIGHT - Executive Readout
### Demand & Inventory Intelligence | Prepared for Operations & Finance

---

## The Problem

Two inventory problems are quietly costing this business money in opposite directions: best-selling products run out of stock and lose sales that can never be recovered, while slow-moving products pile up in the warehouse, tying up cash that could be used elsewhere. Project FORESIGHT was built to catch both - before they happen, not after.

## The Impact, in Rupees

| | Amount | What kind of number this is |
|---|---|---|
| **Sales lost to stockouts** | **Rs. 32,257,801** | Gone. Real revenue that did not happen, over the observed stockout period - this cannot be recovered. |
| **Capital locked in overstock** | **Rs. 799,172,105** | Stuck, not lost. This value still exists as unsold inventory and can be partially recovered through a clearance campaign. |

These are not the same kind of loss, and they call for different action - one argues for preventing future stockouts, the other for clearing existing stock now.

**The single highest-priority finding:** one product - **SKU04321** - accounts for **Rs. 10.83 million, roughly a third of all stockout losses company-wide**, from one SKU out of 5,000. This is the same product independently confirmed earlier in this project to drive close to 10% of total company revenue. It should not be possible for this specific product to run out of stock again.

## What Was Built

**A weekly, SKU-level demand forecast.** Given a product's recent sales history, seasonal pattern, and category, the model predicts how many units it will sell in the coming weeks. Tested on three separate past periods it never saw during training, it beat a simple "same week as last year" baseline every time - by 9.9%, 22.8%, and 24.7%. The single strongest signal driving its predictions is exactly that same-week-last-year comparison, followed by the season of the year - confirming this business's demand is genuinely seasonal, not just generally trending upward.

**A stockout and overstock risk score for every SKU.** Rather than leaving this as an assumption, the risk rules were checked directly against a known-correct answer key built into this project's data: out of every product genuinely at risk of stocking out, the system catches 95.5% of them; out of every genuinely overstocked product, it catches 100%. Roughly half of what gets flagged turns out to be a false alarm - an honest number, not a polished one, and one worth improving before this runs unattended.

**An interactive dashboard** covering company performance, the forecast, current inventory position, and a prioritised action list - built for the operations team to use directly, not just for a one-time report.

## Recommended Actions, in Order

1. **Protect SKU04321 specifically.** A dedicated safety-stock policy for this one product is justified given it alone represents roughly a third of the company's entire stockout loss and close to a tenth of all revenue.
2. **Act on the 396 SKUs currently flagged "Reorder now."** Ranked by expected demand in the dashboard - the top of that list is where a stockout would hurt next.
3. **Launch a clearance review of the 707 SKUs flagged "Markdown/clear."** Recovering even a fraction of the Rs. 799M currently tied up frees real cash.
4. **Re-run this pipeline and re-check the risk thresholds periodically.** The current thresholds were calibrated against a single point-in-time snapshot of known outcomes — they should be expected to drift and are worth re-validating as new data comes in, not treated as permanently fixed.

## Limitations, Stated Plainly

- The forecast model does not know the store's exact restock lead time or how much is already on order - that data wasn't available, so a documented assumption (roughly one week's lead time) stands in its place.
- Roughly half of flagged risk SKUs are false alarms at current settings - worth tightening further before this drives reordering decisions unattended.
- The risk-detection percentages above were measured against this project's own known-answer dataset, not an independent, unseen test - real-world performance should be re-validated once live outcomes are available.
- The capital-locked figure values excess stock at cost price; it does not assume 100% of that value is recoverable through a markdown, since clearance sales typically recover less than full value.

## Where to Look for More Detail

The dashboard's Risk Dashboard page holds the full, filterable reorder and markdown lists referenced above. The Forecast page shows the model's prediction against actual sales for any individual product. Full methodology, data-quality findings, and backtesting detail are documented in the project's Week 1–3 reports.
