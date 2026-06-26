# Online-Retail-Shop-Analysis
# 🛒 Online Retail Sales Dashboard

An end-to-end business intelligence project built on a real-world e-commerce dataset — covering data cleaning, exploratory analysis, and an interactive Streamlit dashboard.

![Dashboard Preview](<img width="1920" height="931" alt="image" src="https://github.com/user-attachments/assets/ec2ab334-396a-4c3a-bf33-54ef45f0fed2" />
)

---

## 📌 Project Overview

This project analyzes **989,571 transactions** from a UK-based online retailer spanning **December 2009 to December 2011**. The goal was to transform raw transactional data into actionable business insights through a fully interactive dashboard.

---

## 📊 Key Insights

- 💰 **£19.96M** total revenue generated across 2 years
- 📦 **39,534** unique orders from **5,860** customers
- 🌍 Sales recorded across **43 countries**, with the UK dominating revenue share
- 🏆 Top-selling products were driven by seasonal gifting and home décor items
- 📅 Mid-week (Tuesday–Thursday) consistently showed the highest order volumes

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)

| Layer | Tools |
|---|---|
| Data Cleaning | Python, Pandas |
| Exploratory Analysis | Pandas, Matplotlib |
| Interactive Dashboard | Streamlit, Plotly |
| Static Dashboard | Matplotlib, GridSpec |

---

## 📁 Project Structure

```
online-retail-dashboard/
├── app.py                  # Streamlit interactive dashboard
├── dashboard.py            # Static Matplotlib dashboard
├── eda.py                  # Exploratory data analysis
├── data_audit.py           # Data cleaning pipeline
├── requirements.txt        # Python dependencies
├── data/
│   └── raw/
│       └── online_retail_II.xlsx   # Source dataset
└── screenshots/
    └── dashboard.png
```

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/rcrahul0001-web/online-retail-dashboard.git
cd online-retail-dashboard
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Clean the data**
```bash
python data_audit.py
```

**4. Launch the dashboard**
```bash
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`

---

## 🔍 Dashboard Features

- **KPI Cards** — Revenue, Orders, Customers, Products, Avg Order Value
- **Monthly Revenue Trend** — area chart across the full 2-year period
- **Top N Products** — best-selling items by quantity (adjustable 5–20)
- **Top N Customers** — highest-value customers by revenue
- **Country Revenue Bar** — top contributing markets
- **Revenue by Day of Week** — weekly purchase pattern analysis
- **Country Share Pie** — donut chart showing geographic distribution
- **Sidebar Filters** — filter by country, year, and top-N count
- **Data Export** — download filtered dataset as CSV

---

## 📂 Dataset

**Source:** [UCI Machine Learning Repository — Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

**Raw shape:** ~1,067,371 rows × 8 columns  
**Cleaned shape:** 989,571 rows (removed nulls, duplicates, returns, and zero-price records)

| Column | Description |
|---|---|
| Invoice | Unique transaction ID |
| StockCode | Product code |
| Description | Product name |
| Quantity | Units sold |
| InvoiceDate | Transaction timestamp |
| Price | Unit price (£) |
| Customer ID | Unique customer identifier |
| Country | Customer's country |

---

## 👤 Author

**Rahul Chauhan**  
B.Sc. Data Science | Mumbai, India  
[![GitHub](https://img.shields.io/badge/GitHub-rcrahul0001--web-181717?style=flat&logo=github)](https://github.com/rcrahul0001-web)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://linkedin.com/in/rahul-chauhan-8b82012b1)

---

## 📄 License

This project is open source under the [MIT License](LICENSE).
