import unittest
import os
import tempfile
from datetime import datetime
from src.sales_analytics import SaleRecord, SalesDataLoader, SalesAnalyzer, summarizing_double


class TestSummarizingDouble(unittest.TestCase):

    def test_basic_stats(self):
        result = summarizing_double([10.0, 20.0, 30.0])
        self.assertEqual(result['count'], 3)
        self.assertAlmostEqual(result['sum'], 60.0)
        self.assertAlmostEqual(result['mean'], 20.0)
        self.assertAlmostEqual(result['min'], 10.0)
        self.assertAlmostEqual(result['max'], 30.0)

    def test_empty_list(self):
        result = summarizing_double([])
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['sum'], 0.0)

    def test_single_value(self):
        result = summarizing_double([42.0])
        self.assertEqual(result['count'], 1)
        self.assertAlmostEqual(result['sum'], 42.0)
        self.assertAlmostEqual(result['mean'], 42.0)


class TestSalesDataLoader(unittest.TestCase):

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            SalesDataLoader.load_sales_data("non_existent_file.csv")

    def test_load_valid_csv(self):
        records = SalesDataLoader.load_sales_data("data/sales_data.csv")
        self.assertTrue(len(records) > 0)
        self.assertIsInstance(records[0], SaleRecord)

    def test_malformed_rows_skipped(self):
        """Bad rows produce None from _parse_row, which filter(None) removes."""
        csv_content = (
            "transactionId,date,region,salesperson,productCategory,quantity,unitPrice,totalAmount\n"
            "T1,2024-01-01,North,Alice,Electronics,2,100.00,200.00\n"
            "BAD_ROW,invalid-date,South,,Clothing,abc,50.00,nope\n"
            "T3,2024-01-03,East,Bob,Home,1,20.00,20.00\n"
        )
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as f:
            f.write(csv_content)
            tmp_path = f.name

        try:
            records = SalesDataLoader.load_sales_data(tmp_path)
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0].transaction_id, "T1")
            self.assertEqual(records[1].transaction_id, "T3")
        finally:
            os.unlink(tmp_path)


class TestSalesAnalyzer(unittest.TestCase):

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
        self.assertAlmostEqual(result["North"], 350.0)
        self.assertAlmostEqual(result["South"], 100.0)
        self.assertAlmostEqual(result["East"], 20.0)

    def test_get_average_sale_by_category(self):
        result = self.analyzer.get_average_sale_by_category()
        self.assertAlmostEqual(result["Electronics"], 150.0)
        self.assertAlmostEqual(result["Clothing"], 75.0)
        self.assertAlmostEqual(result["Home"], 20.0)

    def test_get_top_salespersons(self):
        result = self.analyzer.get_top_salespersons(2)
        self.assertEqual(result[0][0], "Alice")
        self.assertAlmostEqual(result[0][1], 350.0)
        self.assertEqual(result[1][0], "Bob")
        self.assertAlmostEqual(result[1][1], 100.0)

    def test_get_monthly_sales_trend(self):
        result = self.analyzer.get_monthly_sales_trend()
        self.assertAlmostEqual(result["2024-01"], 400.0)
        self.assertAlmostEqual(result["2024-02"], 70.0)

    def test_get_sales_by_date_range(self):
        start = datetime(2024, 1, 2)
        end = datetime(2024, 2, 1)
        result = self.analyzer.get_sales_by_date_range(start, end)
        self.assertEqual(len(result), 3)
        ids = [r.transaction_id for r in result]
        self.assertIn("T2", ids)
        self.assertIn("T3", ids)
        self.assertIn("T4", ids)

    def test_get_sales_stats_by_region(self):
        result = self.analyzer.get_sales_stats_by_region()
        north = result["North"]
        self.assertEqual(north['count'], 3)
        self.assertAlmostEqual(north['sum'], 350.0)
        self.assertAlmostEqual(north['min'], 50.0)
        self.assertAlmostEqual(north['max'], 200.0)

    def test_generate_summary_report(self):
        report = self.analyzer.generate_summary_report()
        self.assertIn("Total Sales Revenue", report)
        self.assertIn("Alice", report)

    def test_empty_records(self):
        analyzer = SalesAnalyzer([])
        self.assertEqual(analyzer.get_total_sales_by_region(), {})
        self.assertEqual(analyzer.get_top_salespersons(3), [])
        report = analyzer.generate_summary_report()
        self.assertIn("N/A", report)


if __name__ == '__main__':
    unittest.main()
