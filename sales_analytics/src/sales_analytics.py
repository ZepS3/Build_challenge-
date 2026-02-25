from dataclasses import dataclass
from datetime import datetime
import csv
from typing import List, Dict
from collections import defaultdict
import statistics

@dataclass(frozen=True)
class SaleRecord:
    transaction_id: str
    date: datetime
    region: str
    salesperson: str
    product_category: str
    quantity: int
    unit_price: float
    total_amount: float

class SalesDataLoader:
    
    @staticmethod
    def load_sales_data(file_path: str) -> List[SaleRecord]:
        records = []
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        record = SaleRecord(
                            transaction_id=row['transactionId'],
                            date=datetime.strptime(row['date'], '%Y-%m-%d'),
                            region=row['region'],
                            salesperson=row['salesperson'],
                            product_category=row['productCategory'],
                            quantity=int(row['quantity']),
                            unit_price=float(row['unitPrice']),
                            total_amount=float(row['totalAmount'])
                        )
                        records.append(record)
                    except (ValueError, KeyError):
                        continue
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")
            
        return records

class SalesAnalyzer:
    
    def __init__(self, sales_records: List[SaleRecord]):
        self.sales_records = sales_records

    def get_total_sales_by_region(self) -> Dict[str, float]:
        sales_by_region = defaultdict(float)
        for record in self.sales_records:
            sales_by_region[record.region] += record.total_amount
        return dict(sales_by_region)

    def get_average_sale_by_category(self) -> Dict[str, float]:
        category_totals = defaultdict(list)
        for record in self.sales_records:
            category_totals[record.product_category].append(record.total_amount)
            
        return {
            category: statistics.mean(amounts) 
            for category, amounts in category_totals.items()
        }

    def get_top_salespersons(self, n: int) -> List[tuple]:
        salesperson_totals = defaultdict(float)
        for record in self.sales_records:
            salesperson_totals[record.salesperson] += record.total_amount
            
        return sorted(
            salesperson_totals.items(), 
            key=lambda item: item[1], 
            reverse=True
        )[:n]

    def get_monthly_sales_trend(self) -> Dict[str, float]:
        monthly_sales = defaultdict(float)
        for record in self.sales_records:
            month_key = record.date.strftime('%Y-%m')
            monthly_sales[month_key] += record.total_amount
        
        return dict(sorted(monthly_sales.items()))

    def get_sales_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SaleRecord]:
        return list(filter(
            lambda record: start_date <= record.date <= end_date,
            self.sales_records
        ))

    def generate_summary_report(self) -> str:
        total_sales = sum(r.total_amount for r in self.sales_records)
        total_transactions = len(self.sales_records)
        avg_transaction_value = total_sales / total_transactions if total_transactions > 0 else 0
        
        top_salesperson = self.get_top_salespersons(1)
        top_performer = top_salesperson[0][0] if top_salesperson else "N/A"
        
        return "\n".join([
            "=== Sales Analysis Summary Report ===",
            f"Total Sales Revenue: ${total_sales:,.2f}",
            f"Total Transactions: {total_transactions}",
            f"Average Transaction Value: ${avg_transaction_value:,.2f}",
            f"Top Salesperson: {top_performer}",
            "====================================="
        ])
