# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import DbUsage, sorted_objects


class SchemaIdentityTests(unittest.TestCase):
    def test_sorted_objects_renders_every_schema(self):
        usage = DbUsage({})
        usage.add_read("T_SOURCE", "MCGDATA")
        usage.add_read("T_SOURCE", "REPORTING")

        self.assertEqual(
            sorted_objects(usage.read),
            ["MCGDATA.T_SOURCE", "REPORTING.T_SOURCE"],
        )


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
