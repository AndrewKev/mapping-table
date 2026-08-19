# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import DbUsage, PhysicalObject, render_markdown


class RenderingTests(unittest.TestCase):
    def test_rendering_keeps_schema_identity_and_separate_cte_section(self):
        usage = DbUsage({})
        usage.add_read("T_SOURCE", "REPORTING")
        usage.add_read("T_SOURCE", "MCGDATA")
        usage.add_write("T_TARGET", "MCGDATA")
        usage.add_call("MCGDATA.PKG.CUSTOM_FUNC")
        usage.add_cte(
            "ACTIVE_ITEMS",
            physical_reads={PhysicalObject("MCGDATA", "T_SOURCE")},
            cte_dependencies={"OTHER_ITEMS"},
            consumers={"OUTER_QUERY"},
        )

        output = render_markdown(usage, "Sample", "/sample", "sample-id")

        self.assertLess(output.index("- MCGDATA.T_SOURCE"), output.index("- REPORTING.T_SOURCE"))
        self.assertIn("# Calls\n\n- MCGDATA.PKG.CUSTOM_FUNC", output)
        self.assertIn("# CTE / Logical Relations", output)
        self.assertIn("- ACTIVE_ITEMS", output)
        self.assertIn("  - Reads: MCGDATA.T_SOURCE", output)
        self.assertIn("  - Depends on: OTHER_ITEMS", output)
        self.assertIn("  - Consumers: OUTER_QUERY", output)
        self.assertNotIn("MCGDATA.ACTIVE_ITEMS", output)


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
