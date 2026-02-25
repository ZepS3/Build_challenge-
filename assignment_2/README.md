# Sales Analytics

I built this to analyze sales data from a CSV file. It reads the data, groups it in different ways (by region, category, salesperson, month), and spits out useful stats like totals, averages, and top performers.

I tried to stick with functional-style operations — `map()`, `reduce()`, `filter()`, and `itertools.groupby()` — instead of plain loops, since the assignment wanted something closer to how Java Streams work.

## Setup

No external libraries needed, just Python 3.7+.

```
python main.py
```

To run the tests:
```
python -m unittest discover tests -v
```

## Project Structure

```
├── main.py                  # runs the demo
├── data/
│   └── sales_data.csv       # sample dataset
├── src/
│   └── sales_analytics.py   # SaleRecord, SalesDataLoader, SalesAnalyzer
└── tests/
    └── test_sales_analytics.py
```

## What it does

- Totals sales by region
- Averages by product category
- Finds top N salespeople
- Monthly trend breakdown
- Date range filtering
- Per-region stats (count, sum, min, max, avg) — basically a Python version of `summarizingDouble`
- Summary report with overall numbers

## CSV format

The input file should look like this:
```
transactionId,date,region,salesperson,productCategory,quantity,unitPrice,totalAmount
T1001,2024-01-05,North,John Doe,Electronics,2,500.00,1000.00
```

Column names are case-sensitive, so they need to match exactly.

## Sample output

```
Loading data from data/sales_data.csv...
Loaded 10 records.

--- Total Sales by Region ---
East: $210.00
North: $2,380.00
South: $1,550.00
West: $1,050.00

--- Average Sale by Category ---
Clothing: $226.67
Electronics: $1,050.00
Home: $103.33

--- Top 3 Salespersons ---
Jane Smith: $1,450.00
Charlie Davis: $1,200.00
John Doe: $1,180.00

--- Monthly Sales Trend ---
2024-01: $2,170.00
2024-02: $1,470.00
2024-03: $1,550.00

--- Sales Statistics by Region (summarizingDouble) ---
East: count=2, sum=$210.00, avg=$105.00, min=$90.00, max=$120.00
North: count=3, sum=$2,380.00, avg=$793.33, min=$180.00, max=$1,200.00
South: count=3, sum=$1,550.00, avg=$516.67, min=$100.00, max=$1,200.00
West: count=2, sum=$1,050.00, avg=$525.00, min=$250.00, max=$800.00

=== Sales Analysis Summary Report ===
Total Sales Revenue: $5,190.00
Total Transactions: 10
Average Transaction Value: $519.00
Top Salesperson: Jane Smith
=====================================
```

## Assumptions

- Dates are in YYYY-MM-DD format
- If a row in the CSV is malformed or has missing fields, it just gets skipped
- Everything runs on the standard library, no pip installs needed
