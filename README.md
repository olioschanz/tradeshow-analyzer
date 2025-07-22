# 📡 Conference LeadScope

A Streamlit app that help identify high-value conferences across various research focus areas, and visualizes the top venues prospects attend — enabling data-informed conference planning.

---

## What It Does

- Upload **multiple CSVs** (one per focus area)
- Extract and **deduplicate tradeshows**
- Count per-conference appearances for each topic
- Generate a summary table with **total counts**
- Optional sorting by total appearances
- **Bar charts** for the top 10 conferences per focus area
- CSV download for downstream analysis

---

## Input Format

Each CSV file should contain a `Tradeshow` column. File name will be extracted as respective column name.
Example files:

- `Sarcoma.csv`
- `Breast Cancer.csv`
- `Ovarian Cancer.csv`

---

## Example Output

| Conference      | Sarcoma | Breast Cancer | Ovarian Cancer | Total |
|----------------|---------|----------------|----------------|--------|
| AACR           | 12      | 28             | 16             | 56     |
| ASCO           | 7       | 22             | 12             | 41     |
| SABCS          | 0       | 19             | 0              | 19     |

Also generates interactive bar charts per topic.

---

## How to use it

**Live app:**  
[https://tradeshow-analyzer.streamlit.app/](https://tradeshow-analyzer.streamlit.app/)

**Local use:**
```bash
git clone https://github.com/olioschanz/tradeshow-analyzer.git
cd tradeshow-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
