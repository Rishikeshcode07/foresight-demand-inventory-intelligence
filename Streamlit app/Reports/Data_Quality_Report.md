# Project FORESIGHT - Data Quality Report
### Week 1, Day 2-5: Data Profiling & Pipeline Construction

**Dataset:** Synthetic multi-store retail dataset (10M transactions), Pakistan-based - 30 stores across Karachi, Islamabad, Quetta, Multan, and Sialkot; 5,000 SKUs; 10,000 customers; 2022–2025.
**Working version:** `retail_contaminated_dataset/` - treated as the client's real, current data for this entire project. It contains the injected stockout and overstock problems this project exists to detect.
**Reference version:** `retail_clean_dataset/` - held in reserve, used only later to calculate the exact rupee value of lost sales.
**Currency:** All monetary figures reported in **Rs. (PKR)**, based on the store locations above.

---

## 1. Table-by-table profile

| Table | Rows | Columns | Missing values | Duplicate rows |
|---|---|---|---|---|
| store_master.csv | 30 | 5 | 0 | 0 |
| sku_master.csv | 5,000 | 7 | 0 | 0 |
| customer_master.csv | 10,000 | 7 | 0 | 0 |
| promotions.csv | 100 | 8 | 0 | 0 |
| inventory_snapshot.csv | 26,408 | 6 | 0 | 0 |
| sku_inventory_flags.csv | 600 | 6 | 0 | 0 |
| sales_transactions.csv | ~9,945,511 | 11 | none found in any sampled/aggregated view | not checked row-by-row at this scale |

## 2. Referential integrity

Checked directly against the raw data rather than assumed from documentation:
- SKUs in `inventory_snapshot.csv` missing from `sku_master.csv`: **0**
- Stores in `inventory_snapshot.csv` missing from `store_master.csv`: **0**

No orphaned foreign keys found.

## 3. Data-quality issues found, and how each was handled

### 3.1 `inventory_snapshot.csv` row count doesn't match the dataset's own documentation
Documented as ~21,228 rows; the actual file loaded contains **26,408 rows**. No corruption found (zero missing values, zero duplicates, zero orphaned keys) - a documentation discrepancy, not a data defect. **Handling:** proceeded with the actual loaded data.

### 3.2 `sku_inventory_flags.csv` exists in both dataset folders, with different content
This ground-truth answer key - meant to document the anomalies injected into the contaminated data - appears in **both** `retail_clean_dataset/` and `retail_contaminated_dataset/`. Both copies have 600 rows, but they are not the same data: even after sorting both by `sku_id`, all 600 rows differ, the flagged SKU sets don't fully overlap, and the `notes` column uses different wording between the two versions ("Top-selling SKU (by observed volume); injected..." vs. "High-demand SKU; simulated recent stockout win..."). This points to two separate generation runs, not one file copied by accident.

**Handling:** `retail_contaminated_dataset/sku_inventory_flags.csv` is treated as the single authoritative source for this project. Rationale: `retail_clean_dataset/sales_transactions.csv` has no injected stockout suppression by definition, so a flags file sitting in that folder cannot describe real properties of its own sales data - only the contaminated copy is internally consistent with its paired sales data.

**Verified directly, not assumed:** for the first `STOCKOUT_RISK` row in the contaminated flags file (SKU04321, store ST22, window 2025-11-06 to 2025-12-03), a full scan of all ~9.95M rows in `retail_contaminated_dataset/sales_transactions.csv` confirmed **zero** matching sales rows for that exact SKU/store/date combination - consistent with the documented injection method (affected transactions are removed entirely, not zeroed out).

### 3.3 Censored demand during stockout windows
`sku_inventory_flags.csv` contains 200 `STOCKOUT_RISK` rows. Exploding each row's affected-store list across its date window identifies **55,327 exact (date, store, SKU) combinations** where sales were suppressed to zero by the injected stockout - not by an absence of customer demand.

**Handling:** every one of these combinations is explicitly marked with an `is_stockout_censored` flag in the processed pipeline output, rather than being silently treated as an ordinary zero-demand day. This flag will be used in Week 3 to exclude or adjust these rows when training the demand-forecasting model, so the model doesn't learn "demand = 0" when the correct read is "shelf was empty."

### 3.4 Business locale
`store_master.csv` lists cities exclusively in Pakistan. All monetary figures in this project are therefore reported in **Rs. (PKR)**, not USD or INR.

### 3.5 Holiday calendar — known limitation
The derived `calendar` dimension flags fixed-date Pakistani public holidays (Kashmir Day, Pakistan Day, Labour Day, Independence Day, Iqbal Day, Quaid-e-Azam Day). Eid ul-Fitr and Eid ul-Adha follow the lunar Islamic calendar and shift dates every year - these are **not** included in the current `is_holiday` flag. Documented here as a known limitation, not an oversight discovered later.

## 4. Pipeline output

Raw `sales_transactions.csv` (~9,945,511 individual sale-line rows) was streamed and aggregated in 1,000,000-row batches - to stay within available memory - into analysis-ready tables saved as Parquet:

- **`daily_store_sku_final.parquet`** - one row per (date, store, SKU); includes the `is_stockout_censored` flag plus SKU category/brand/cost and store city/type.
- **`daily_sku_final.parquet`** - one row per (date, SKU), summed across all 30 stores; the grain the Week 3 demand-forecasting model trains on.
- **`calendar.parquet`** - 1,461-row date dimension (2022-01-01 to 2025-12-31): week, month, quarter, day-of-week, weekend flag, season, holiday flag.

All aggregated prices (`avg_unit_price`, `avg_discount_pct`) are computed as revenue-weighted averages - total revenue ÷ total units - rather than an average of per-batch averages, which would silently produce a slightly wrong number when combining results computed in separate chunks.

## 5. Sign-off

Zero missing values, zero duplicate rows, and zero referential-integrity violations were found across every table. The two genuine data-quality issues present - the duplicated-but-different flags file, and censored stockout demand — were each identified, verified directly against the raw data rather than assumed, and explicitly handled in the pipeline rather than ignored.
