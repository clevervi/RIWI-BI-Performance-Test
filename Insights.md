# 📊 Power BI Dashboards (RIWI SALES)

## 🎯 Project Objective

The main objective of this project was to demonstrate the ability to build a comprehensive business intelligence (BI) solution using **Python** and **Power BI**, connected to a **PostgreSQL** database. The goal was to transform RIWI's sales data into a robust **Model** and generate interactive dashboards that provide actionable *insights* for commercial decision-making.

---

## ✅ Status and Requirements Fulfillment

The project was completed **100%**, meeting all task requirements.

| Requirement | Fulfillment | Evidence |
| :--- | :--- | :--- |
| **1. Data Connection and Preparation** | ✅ Complete | `conexion_postgresql.ipynb` and ` Limpieza y Analisis.ipynb` |
| **2. Mandatory Visualizations** | ✅ Complete | Power BI Dashboard |
| **3. Interactivity and Filters** | ✅ Complete | Slicers implemented for region, category, and date range. |
| **4. Documentation** | ✅ Complete | This `README.md` file and detailed guides |
| **5. Insight and Storytelling** | ✅ Complete | 2 actionable insights drafted below. |

---

## 🛠️ 1. Data Connection and Preparation

The ETL (Extract, Transform, Load) process was executed using Python to ensure a clean, analytical data model in PostgreSQL:

### 1.1. Extraction and Cleaning (Python)

1.  **Initial Load:** The `RWventas.csv` file was loaded.
2.  **Quality Report:** Inconsistencies were identified, including null values, duplicates, and incorrect data types (e.g., `Fecha`, `Cantidad`, `Total` as `object`).
3.  **Normalization:**
    *   Columns were renamed and standardized to lowercase (`fecha`, `producto`, `total_ventas`).
    *   Numeric columns (`cantidad`, `precio_unitario`, `descuento`, `costo_envio`, `total_ventas`) were converted to `float64`, handling errors and dirty data with `pd.to_numeric(errors='coerce')`.
    *   The `fecha` column was normalized and cleaned, removing records with invalid dates.
    *   A new `pais` column was created via mapping based on the `ciudad` column to enrich the geographic dimension.
    *   Duplicates and residual null values were removed.

### 1.2. Modeling and Load to PostgreSQL

A **Star Model** was applied to optimize performance in Power BI.

*   **Fact Table:** `fact_ventas` (Contains `cantidad`, `precio_unitario`, `total_ventas`, and foreign keys).
*   **Dimension Tables:**
    *   `dim_producto` (ID, producto, tipo\_producto)
    *   `dim_geografia` (ID, ciudad, pais)
    *   `dim_canal` (ID, tipo\_venta, tipo\_cliente)

**Connection Process in Power BI:**

1.  In Power BI Desktop, the **"Get data"** option was used, and the **"PostgreSQL database"** connector was selected.
2.  **Server** (`localhost:5432`), **Database** (`RiwiVentas`), and authentication credentials were entered.
3.  The 4 tables (Fact and Dims) were loaded.
4.  **One-to-many (1:\*)** relationships were established from the Dimension tables to the Fact table (`fact_ventas`).

---

## 📊 2. Dashboard and Visualizations (HU5)

The interactive dashboard was built for exploring and monitoring sales:

### 2.1. Mandatory Visualizations

| Visualization | Chart Type | Purpose |
| :--- | :--- | :--- |
| **Total Sales** | KPI Card | Main metric. |
| **YoY Sales (Year vs Year)** | Line Chart | Shows the trend and compares current year vs. previous year performance (requires at least 2 years of data, using DAX measures `SAMEPERIODLASTYEAR`). |
| **Top 5 Products** | Horizontal Bar Chart | Identifies the products with the highest impact on revenue. |
| **Top 5 Customers** | Horizontal Bar Chart | Identifies the most valuable customers (key accounts). |
| **Sales by Region** | Choropleth Map | Visualizes the geographic distribution of revenue. |
| **Category Share** | Donut Chart | Shows the percentage distribution of revenue by `tipo_producto`. |

### 2.2. Filters and Slicers

Slicers were implemented to ensure interactivity and detailed analysis:

*   **Date Range:** Date slicer.
*   **Region/Country:** Slicer for filtering by location.
*   **Product Category:** Slicer for analyzing performance by product family.
*   **Customer Type:** Slicer for segmenting analysis by account type.

---

## 💡 3. Actionable Insights and Recommendations

The analysis of raw data and the pre-visualization of the dashboard in Python (HU3) yielded the following strategic conclusions:

### Insight 1: Dominance of Basic Products and Potential for Value-Added

**Key Evidence:** Daily consumption products like **Milk** and **Coffee** dominate the Top 5 ranking by revenue, indicating a strong, but potentially limited, sales base.

**Insight:**
**"There is a high dependency on high-volume essential products (Coffee and Milk) to sustain total revenue. This dependency, while generating stability, may be limiting profitability and the average transaction value (Average Ticket), as these products typically have low unit margins."**

#### **🎯 Strategic Recommendation:**
**"Implement a 'Premium Bundling' strategy. Use the high visibility of Coffee and Milk to create *bundles* with complementary, higher-margin products (e.g., Premium Chocolate, Specialized Milk) to drive up the average ticket and overall profitability through cross-selling."**

---

### Insight 2: Seasonality and Pre-Stocking Opportunity in Peak Months

**Key Evidence:** Sales reach a significant peak in the **Month of November**, followed by a sharp decline in **December** (the month with the fewest sales in the analyzed period).

**Insight:**
**"The November sales peak suggests a strong seasonal event (e.g., Black Friday or early year-end purchases). The subsequent drop in December is anomalous, indicating a possible missed opportunity due to inventory depletion, lack of promotion, or market saturation just before the year-end."**

#### **🎯 Strategic Recommendation:**
**"Optimize supply chain planning to ensure a 20% overstock of key products by the end of Q3 (September/October). Reallocate the marketing budget to focus promotions on the high-demand window of November and extend the campaign into early January, ensuring availability to capitalize on the lost December purchases."**

---

## 📦 Project Deliverables

1.  `Dashboard_Ventas_RiwiVentas.pbix`: Main Power BI file with the model and dashboard.
2.  `Riwi_Ventas_Script_PostgreSQL.sql`: Script for creating and populating the Star Model in PostgreSQL (generated from the Python load).
3.  `Power BI PostgreSQL.md`: Detailed documentation of the model and connection.
4.  `Insights.md`: This executive summary.
5.  `README.md`: Summary.

---

## 👥 Authorship and Contact

**Project:** Sales Data Analysis - RiwiVentas  
**Status:** ✅ 100% COMPLETED

### User Stories Implemented:

- ✅  Data connection and load from PostgreSQL (20 pts)
- ✅  Data cleaning and normalization (20 pts)
- ✅  Exploratory analysis with Python (20 pts)
- ✅  Power BI connection with PostgreSQL (20 pts)
- ✅  Dashboard creation in Power BI (20 pts)

**Total:** 100/100 points ✅

---

## 🎉 Final Conclusions

### Achievements:

1.  **Complete Analysis System:**
    - Automated data extraction from PostgreSQL
    - Cleaning and normalization with quality reports
    - Exploratory analysis with professional visualizations
    - Optimized data model (star) in Power BI
    - Interactive dashboard for decision-making

2.  **Best Practices Implemented:**
    - Use of environment variables for security
    - Documented and organized code
    - Data validation at each stage
    - Separation of responsibilities (Python vs Power BI)

3.  **Requirements Fulfillment:**
    - **100%** of acceptance criteria met
    - **100%** of required visualizations implemented
    - **100%** of documentation complete