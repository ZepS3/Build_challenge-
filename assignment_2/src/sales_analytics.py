from dataclasses import dataclass
from datetime import datetime
import csv
from typing import List, Dict, Optional
from functools import reduce
from itertools import groupby
from operator import attrgetter


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


def summarizing_double(values: List[float]) -> Dict[str, float]:
    """Returns count, sum, min, max, mean for a list of numbers."""
    if not values:
        return {'count': 0, 'sum': 0.0, 'min': 0.0, 'max': 0.0, 'mean': 0.0}

    total = reduce(lambda acc, x: acc + x, values)
    count = len(values)
    return {
        'count': count,
        'sum': total,
        'min': min(values),
        'max': max(values),
        'mean': total / count
    }


def _group_by(records, key_func):
    """Sort + groupby to collect records into a dict of lists."""
    sorted_records = sorted(records, key=key_func)
    return {
        key: list(group) 
        for key, group in groupby(sorted_records, key=key_func)
    }


class SalesDataLoader:

    @staticmethod
    def _parse_row(row: dict) -> Optional[SaleRecord]:
        """Try to build a SaleRecord from a row, return None if it's bad."""
        try:
            return SaleRecord(
                transaction_id=row['transactionId'],
                date=datetime.strptime(row['date'], '%Y-%m-%d'),
                region=row['region'],
                salesperson=row['salesperson'],
                product_category=row['productCategory'],
                quantity=int(row['quantity']),
                unit_price=float(row['unitPrice']),
                total_amount=float(row['totalAmount'])
            )
        except (ValueError, KeyError):
            return None

    @staticmethod
    def load_sales_data(file_path: str) -> List[SaleRecord]:
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                # parse rows, skip any that came back as None
                parsed = map(SalesDataLoader._parse_row, reader)
                records = list(filter(None, parsed))
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error reading CSV: {e}")

        return records


class SalesAnalyzer:

    def __init__(self, sales_records: List[SaleRecord]):
        self.sales_records = sales_records

    def get_total_sales_by_region(self) -> Dict[str, float]:
        grouped = _group_by(self.sales_records, key_func=attrgetter('region'))
        return {
            region: reduce(lambda acc, r: acc + r.total_amount, records, 0.0)
            for region, records in grouped.items()
        }

    def get_average_sale_by_category(self) -> Dict[str, float]:
        grouped = _group_by(self.sales_records, key_func=attrgetter('product_category'))
        return {
            category: summarizing_double(
                list(map(attrgetter('total_amount'), records))
            )['mean']
            for category, records in grouped.items()
        }

    def get_top_salespersons(self, n: int) -> List[tuple]:
        grouped = _group_by(self.sales_records, key_func=attrgetter('salesperson'))
        totals = {
            person: reduce(lambda acc, r: acc + r.total_amount, records, 0.0)
            for person, records in grouped.items()
        }
        return sorted(totals.items(), key=lambda item: item[1], reverse=True)[:n]

    def get_monthly_sales_trend(self) -> Dict[str, float]:
        month_key = lambda r: r.date.strftime('%Y-%m')
        grouped = _group_by(self.sales_records, key_func=month_key)
        return {
            month: reduce(lambda acc, r: acc + r.total_amount, records, 0.0)
            for month, records in sorted(grouped.items())
        }

    def get_sales_by_date_range(self, start_date: datetime, end_date: datetime) -> List[SaleRecord]:
        return list(filter(
            lambda record: start_date <= record.date <= end_date,
            self.sales_records
        ))

    def get_sales_stats_by_region(self) -> Dict[str, Dict[str, float]]:
        grouped = _group_by(self.sales_records, key_func=attrgetter('region'))
        return {
            region: summarizing_double(list(map(attrgetter('total_amount'), records)))
            for region, records in grouped.items()
        }

    def generate_summary_report(self) -> str:
        amounts = list(map(attrgetter('total_amount'), self.sales_records))
        stats = summarizing_double(amounts)

        top_salesperson = self.get_top_salespersons(1)
        top_performer = top_salesperson[0][0] if top_salesperson else "N/A"

        return "\n".join([
            "=== Sales Analysis Summary Report ===",
            f"Total Sales Revenue: ${stats['sum']:,.2f}",
            f"Total Transactions: {stats['count']}",
            f"Average Transaction Value: ${stats['mean']:,.2f}",
            f"Top Salesperson: {top_performer}",
            "====================================="
        ])
