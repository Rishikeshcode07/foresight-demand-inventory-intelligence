# Project FORESIGHT - EDA Insight Memo
### Week 2: Exploratory Data Analysis

Builds on the Week 1 Data Quality Report. All figures below come from `daily_sku_final` (the chain-wide daily aggregate built in Week 1, using `retail_contaminated_dataset` as the working data) unless otherwise noted. All monetary figures in Rs. (PKR).

---

## 1. Revenue trend & the growth-rate discrepancy

Monthly revenue, 2022-2025, shows real growth but not a smooth line - noisy month to month, with a clear repeating shape (see Section 2).

Compound annual growth rate, 2022 → 2025: **4.9%** - measurably below the dataset documentation's claimed ~6%/year.

**This is explained, not just noted:** year-over-year growth came out as 1.9% (2023), 2.0% (2024), then a jump to 11.0% (2025). That final-year spike is suspicious on its own - and it lines up with something already proven in Week 1: the injected stockout windows fall inside the **last ~75 days of the dataset**, i.e. inside 2025. Real demand in that period existed but was never recorded as a sale. That means 2025's growth number - and by extension the 4.9% CAGR - is understating the true underlying trend, not contradicting the documentation. The exact rupee size of that gap will be quantified directly in Week 4, using the paired clean/contaminated comparison.

## 2. Seasonality

**Nov/Dec peak: confirmed cleanly, no exceptions.** December is the single highest-revenue month in all 4 years. November is the second-highest month in all 4 years. This holds without qualification.

**Feb trough: real, but not universal - a genuine exception exists.** February is the lowest month in 2023 and 2025. It is *not* the lowest in 2022 (June is, narrowly ahead of February) or 2024 (March is, with February actually sitting above both January and March that year). Reported as 3-of-4 years, with the two exceptions named rather than smoothed over.

**Seasonality is a company-wide effect, not category-specific.** Measuring how much each category's revenue swings across the year (highest month % of annual revenue minus lowest month %) gives a strikingly narrow range: every one of the 12 categories falls between 5.1 and 5.5 percentage points. In many retail businesses, gift-type categories swing far harder around Nov/Dec than staples do - that pattern is largely absent here. The Nov/Dec effect looks close to uniform across the whole business rather than concentrated in any particular category.

## 3. Revenue concentration & top movers

Sales follow a genuine Pareto-style skew, consistent with the dataset's own documentation: **the top 20% of SKUs (1,000 of 5,000) generate 73.1% of total revenue.**

One SKU stands out enough to name directly: **SKU04321 alone accounts for Rs. 1.069 billion of Rs. 10.89 billion total revenue — roughly 9.8% of the entire company's sales from a single product out of 5,000.** This is the same SKU whose stockout window was directly verified against the raw 10-million-row transaction file in Week 1 (zero sales rows found inside the flagged window) - the single most commercially important product in the business is also a confirmed, real stockout case.

## 4. Risk-flag validation against actual sales rank

The dataset documentation claims `STOCKOUT_RISK` and `SLOW_MOVER` flags were assigned based on real sales rank, not at random. Checked directly, by revenue percentile and units percentile (0% = best-selling, 100% = worst-selling):

| Flag | Avg. revenue percentile | Avg. units percentile |
|---|---|---|
| STOCKOUT_RISK | 11.6 | 2.0 |
| SLOW_MOVER | 65.1 | 96.0 |
| Unflagged | 50.4 | 48.0 |

STOCKOUT_RISK SKUs are extreme on both measures - genuine best-sellers by any definition, consistent with real products running out of stock.

SLOW_MOVER SKUs tell a more specific story: extreme by units (96th percentile - barely moving off shelves) but only moderately below average by revenue (65th percentile). These are lower-volume items priced high enough that weak unit sales don't look alarming in pure revenue terms.

**Direct implication for Week 3:** overstock risk scoring must be built on units sold vs. stock on hand, not revenue - a revenue-based rule would systematically miss the exact SKUs this project needs to catch.

## 5. Promotion effectiveness

Two rounds of testing were needed to get an honest answer here.

**First test** (each SKU's promo days vs. all its non-promo days, pooled across all 4 years): weak and inconsistent - only 36.4% of SKUs showed any positive lift at all, with every promo type showing a negative or near-zero median.

**This test design was flawed, not the promotions:** pooling "all other days" mixes in unrelated seasons, growth years, and troughs, diluting any real short-term effect. A fairer test compares each promotion's window against the equivalent-length period immediately before it, for the same targeted SKUs:

| Promo type | Mean lift | Median lift | n |
|---|---|---|---|
| BOGO | +3.6% | +1.4% | 17 |
| Bundle Offer | +4.2% | +0.9% | 23 |
| Percentage Discount | +3.2% | +0.9% | 22 |
| Clearance | -0.3% | +1.9% | 20 |
| Flat Discount | -0.4% | -1.4% | 18 |

Four of five promo types flip meaningfully more positive under the fairer comparison, confirming the first test understated real lift by comparing against a noisy baseline.

**Two exceptions worth naming specifically, not averaging away:**
- **Flat Discount** stays negative on both mean and median under either test - the one promo type with no evidence of driving incremental volume.
- **Clearance** is genuinely mixed: a positive median (+1.9%, so a typical Clearance promotion does lift sales) pulled to a negative mean by a handful of weak-performing promotions. Reported as "mixed," not simplified to a single verdict.

**Limitations, stated plainly:** each promo type is backed by only 17-23 promotions - enough to see direction, not enough to treat individual percentage points as precise. The "compare against the period right before" method also carries a possible bias: if promotions are deliberately timed to follow a natural sales dip, some of the measured "lift" could be ordinary reversion to normal rather than the promotion's own effect. Both caveats are documented here rather than resolved further within Week 2's scope.

## 6. Category economics

Revenue rank and units rank diverge sharply for several categories - this is a real pattern, not noise:

| Category | Rs./unit | Revenue rank | Units rank |
|---|---|---|---|
| Electronics & Accessories | 1,689.13 | 1 | 9 |
| Apparel & Footwear | 1,561.88 | 2 | 12 |
| Personal Care | 598.25 | 3 | 1 |
| Home & Kitchen | 1,125.83 | 4 | 8 |
| Health & Wellness | 708.16 | 5 | 11 |
| Frozen Foods | 525.40 | 6 | 5 |
| Home Care | 271.62 | 7 | 4 |
| Dairy & Bakery | 204.30 | 8 | 3 |
| Grocery | 234.25 | 9 | 6 |
| Stationery & Office | 177.56 | 10 | 2 |
| Beverages | 127.64 | 11 | 7 |
| Snacks & Confectionery | 105.09 | 12 | 10 |

Two clear groupings: high-ticket, lower-volume categories (Electronics, Apparel - Apparel is the most extreme case, #2 by revenue but dead last by units) versus high-volume, low-ticket staples (Personal Care, Stationery - Stationery is #2 by units but only #10 by revenue).

**Implication for Week 3:** a raw "units sitting in stock" overstock rule needs to account for what's normal per category - high unit volume is simply expected for staple categories and shouldn't be flagged the same way it would be for Electronics or Apparel.

## 7. Summary - key insights for a non-technical stakeholder

1. The business grew 4.9%/year on paper, but real growth is understated because recent stockouts on best-sellers suppressed recorded 2025 sales - the true figure is closer to the documented ~6% once that's corrected for (Week 4).
2. Almost three-quarters of revenue comes from one-fifth of products, and a single SKU (SKU04321) drives nearly 1 in every 10 rupees the business makes - exactly the kind of product that cannot be allowed to run out of stock, and the same one already confirmed to have done so.
3. "Slow-moving" stock is a shelf-space problem, not a lost-revenue problem - these items still sell for reasonable prices, they just move too slowly. Reordering rules need to watch units, not sales value.
4. Promotions do work, on average - but Flat Discount offers show no measurable benefit, and Clearance events are inconsistent rather than reliably effective. Worth reviewing which promo types are worth running at all.
5. Nov/Dec is reliably the strongest period company-wide, across every category roughly equally - not just a gift-category effect.

## What's next

Feature engineering (lag features, rolling averages, calendar features) using the patterns confirmed above, followed by the seasonal-naive baseline model - the last steps before Week 3's actual forecasting model.
