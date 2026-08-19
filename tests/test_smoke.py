# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping import extract_db_usage


class AnalyzerSmokeTests(unittest.TestCase):
    def test_module_exposes_default_schema(self):
        self.assertEqual(extract_db_usage.DEFAULT_SCHEMA, "MCGDATA")


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
