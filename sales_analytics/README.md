# Sales Analytics

Simple Python script to process sales data from CSV files. It aggregates sales by region, calculates trends, and finds top salespeople.

## Project Structure
- `src/`: Core logic (`sales_analytics.py`)
- `data/`: Sample CSV file
- `tests/`: Unit tests
- `main.py`: Demo script

## How to Run

1. Run the main demo:
   ```bash
   python main.py
   ```

2. Run tests:
   ```bash
   python -m unittest discover tests
   ```

## Features
- Total sales per region
- Average sales by category
- Top 3 salespeople
- Monthly sales trend
- Filter by date range
- Summary report generation

## Sample Data
Input CSV format:
```
transactionId,date,region,salesperson,productCategory,quantity,unitPrice,totalAmount
T1001,2024-01-05,North,John Doe,Electronics,2,500.00,1000.00
```

## Assumptions
- Dates are YYYY-MM-DD
- The CSV header names matter (case-sensitive)
- If a row is broken/malformed, I just skip it and print an error so the whole thing doesn't crash.
