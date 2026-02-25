import unittest
from datetime import datetime
from src.sales_analytics import SaleRecord, SalesDataLoader, SalesAnalyzer

class TestSalesAnalytics(unittest.TestCase):
    
    def setUp(self):
        self.records = [
            SaleRecord("T1", datetime(2024, 1, 1), "North", "Alice", "Electronics", 1, 100.0, 100.0),
            SaleRecord("T2", datetime(2024, 1, 2), "South", "Bob", "Clothing", 2, 50.0, 100.0),
            SaleRecord("T3", datetime(2024, 1, 3), "North", "Alice", "Electronics", 2, 100.0, 200.0),
            SaleRecord("T4", datetime(2024, 2, 1), "East", "Charlie", "Home", 1, 20.0, 20.0),
            SaleRecord("T5", datetime(2024, 2, 2), "North", "Alice", "Clothing", 1, 50.0, 50.0),
        ]
        self.analyzer = SalesAnalyzer(self.records)

    def test_get_total_sales_by_region(self):
        result = self.analyzer.get_total_sales_by_region()
        self.assertEqual(result["North"], 350.0)
        self.assertEqual(result["South"], 100.0)
        self.assertEqual(result["East"], 20.0)

    def test_get_average_sale_by_category(self):
        result = self.analyzer.get_average_sale_by_category()
        self.assertEqual(result["Electronics"], 150.0)
        self.assertEqual(result["Clothing"], 75.0)
        self.assertEqual(result["Home"], 20.0)

    def test_get_top_salespersons(self):
        result = self.analyzer.get_top_salespersons(2)
        self.assertEqual(result[0][0], "Alice")
        self.assertEqual(result[0][1], 350.0)
        self.assertEqual(result[1][0], "Bob")
        self.assertEqual(result[1][1], 100.0)

    def test_get_monthly_sales_trend(self):
        result = self.analyzer.get_monthly_sales_trend()
        self.assertEqual(result["2024-01"], 400.0)
        self.assertEqual(result["2024-02"], 70.0)

    def test_get_sales_by_date_range(self):
        start = datetime(2024, 1, 2)
        end = datetime(2024, 2, 1)
        result = self.analyzer.get_sales_by_date_range(start, end)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].transaction_id, "T2")
        self.assertEqual(result[2].transaction_id, "T4")

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            SalesDataLoader.load_sales_data("non_existent_file.csv")

if __name__ == '__main__':
    unittest.main()
