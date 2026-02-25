import sys
import os
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sales_analytics import SalesDataLoader, SalesAnalyzer

def main():
    data_file = 'data/sales_data.csv'
    
    print(f"Loading data from {data_file}...")
    try:
        records = SalesDataLoader.load_sales_data(data_file)
        print(f"Loaded {len(records)} records.\n")
        
        analyzer = SalesAnalyzer(records)
        
        print("--- Total Sales by Region ---")
        for region, total in analyzer.get_total_sales_by_region().items():
            print(f"{region}: ${total:,.2f}")
        print()

        print("--- Average Sale by Category ---")
        for category, avg in analyzer.get_average_sale_by_category().items():
            print(f"{category}: ${avg:,.2f}")
        print()

        print("--- Top 3 Salespersons ---")
        for person, total in analyzer.get_top_salespersons(3):
            print(f"{person}: ${total:,.2f}")
        print()

        print("--- Monthly Sales Trend ---")
        for month, total in analyzer.get_monthly_sales_trend().items():
            print(f"{month}: ${total:,.2f}")
        print()

        start = datetime(2024, 1, 1)
        end = datetime(2024, 1, 31)
        print(f"--- Sales from {start.date()} to {end.date()} ---")
        
        filtered = analyzer.get_sales_by_date_range(start, end)
        for sale in filtered:
            print(f"{sale.date.date()} | {sale.salesperson} | ${sale.total_amount:,.2f}")
        print(f"Count: {len(filtered)}")
        print()

        print(analyzer.generate_summary_report())

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
