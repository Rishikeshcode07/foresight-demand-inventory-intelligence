# Project FORESIGHT: Demand & Inventory Intelligence

## Executive Summary
Project FORESIGHT is an end-to-end, AI-driven inventory analytics and demand forecasting platform. Designed for large-scale retail and supply chain ecosystems, it transforms raw transactional data into strategic procurement directives. By moving beyond static inventory thresholds, this platform dynamically predicts SKU-level demand and categorizes inventory risk, ultimately safeguarding revenue and optimizing capital allocation.

Streamlit dashboard : https://foresight-demand-inventory-intelligence-4gwryzczzehpqohagt4lac.streamlit.app/
![image alt](https://github.com/user-attachments/assets/f78812f1-9c8d-4618-816b-02e18462c9bb)

Power BI Dashboard Explanation: https://drive.google.com/file/d/1-6hBBVesifSyOOJ3YG7RqSNpcYKTpgSL/view?usp=sharing

---

## Business Context & Impact (The STAR Method)

### Situation
In complex supply chain environments, manual inventory tracking and reliance on static, deterministic baselines fail to capture dynamic market demand. For this project, the portfolio analyzed encompassed Rs. 10.89 Billion in total revenue. Misalignment in this scale of inventory operations leads to two critical failures:
1.  **Stockouts:** Direct loss of revenue, fulfillment delays, and diminished customer trust.
2.  **Overstocking:** Inefficient capital lock-up, increased warehouse holding costs, and high risk of product obsolescence. 

### Task
The primary objective was to engineer a robust data science pipeline and an intuitive executive dashboard that could:
*   Forecast weekly demand at an extremely granular (SKU) level.
*   Bridge the gap between complex machine learning outputs and daily procurement operations.
*   Isolate and prioritize the exact items requiring immediate purchasing interventions to prevent supply chain bottlenecks.

### Action
To solve this, Project FORESIGHT was developed through a multi-phase approach:
*   **Data Engineering & Processing:** Aggregated historical sales data, normalizing time-series information for individual SKUs across multiple product categories (e.g., Home & Kitchen).
*   **Predictive Modeling:** Engineered a time-series forecasting model to predict expected weekly demand. The model's performance was rigorously evaluated using three rolling backtest windows against a seasonal-naive baseline to ensure predictive validity.
*   **Risk Simulation Engine:** Developed an algorithm to cross-reference predicted demand against current stock-on-hand and safety stock thresholds, generating automated risk flags.
*   **Application Development:** Built a centralized, interactive web application to serve these insights to stakeholders in real-time, featuring drill-down capabilities for granular SKU investigations.

![image alt](https://github.com/user-attachments/assets/024f9ff3-7095-4408-b0a2-6f6070054dcf)

### Result
The deployment of Project FORESIGHT delivered unprecedented visibility into the inventory ecosystem, yielding the following validated outcomes:
*   **Risk Identification:** Successfully isolated 396 SKUs at immediate risk of stockout and 707 SKUs that were overstocked, enabling immediate corrective action.
*   **Revenue Concentration Insights:** Proved a distinct Pareto distribution within the data, revealing that the top 20% of SKUs generate approximately 73% of the total Rs. 10.89B revenue.
*   **Model Superiority:** The advanced SKU-level demand forecast consistently outperformed the seasonal-naive baseline in all backtested scenarios.
*   **Operational Alignment:** Generated an automated "Top 10 Priority Reorders" roster (e.g., identifying critical shortages like SKU04596 with 0 stock and 1909 expected weekly demand), directly aligning data science with procurement execution.
![image alt](https://github.com/user-attachments/assets/6b3bccf9-722a-4064-9906-43f513000cfe)
![image alt](https://github.com/user-attachments/assets/66973089-ccc7-4e6a-956e-02dba0115bac)
---

## Core Platform Modules

### 1. Executive Summary & High-Level Business Insights
A macro-level view of the entire inventory ecosystem. It tracks total revenue analyzed and provides an immediate count of critical risk categories (Stockouts vs. Overstocked). It also houses the strategic findings derived from the underlying data models.

### 2. Deep Dive: Product Details
A micro-level diagnostic tool for individual SKUs. 
*   **Search & Filtering:** Users can isolate specific SKUs (e.g., SKU00001) to view category, brand alignment, and list price.
*   **Historical Trends:** Visualizes weekly units sold over a multi-year timeline to contextualize current demand predictions.
*   **Current Risk Snapshot:** A real-time calculation comparing Stock on Hand, defined Safety Stock, and Expected Weekly Demand to output a definitive status (e.g., "Action Required: Healthy").
![image alt](https://github.com/user-attachments/assets/eca888fa-ef51-443e-9c00-0f6d8d4c9b62)

### 3. Actionable Target Roster
A dynamically updated table designed specifically for procurement teams. It ranks items based on supply chain urgency, detailing the exact SKU ID, total current stock on hand, and the forecasted expected weekly demand, allowing buyers to execute purchase orders efficiently.
![image alt](https://github.com/user-attachments/assets/6c3de87c-9dbf-46af-bf77-e2dc8c024fe4)

---

## Methodology & Data Science Approach

*   **Time-Series Forecasting:** The core engine relies on analyzing historical weekly sales data to predict future fluctuations, capturing both trend and seasonality.
*   **Rolling Backtest Validation:** To prevent overfitting and ensure real-world reliability, the forecasting model was validated using a rolling backtest methodology. This simulates how the model would have performed in the past, proving its superiority over standard seasonal-naive approaches.
*   **Risk Validation:** Risk categorizations are not purely theoretical; they are cross-validated against ground-truth inventory data to ensure high precision in the resulting procurement recommendations.

![image alt](https://github.com/user-attachments/assets/e2ec1258-6a69-4209-ae6f-d252e8c9d065)



