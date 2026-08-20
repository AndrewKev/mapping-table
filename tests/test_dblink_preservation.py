# project : IPRO Revisi Header Laporan Trading Term
import unittest
from pathlib import Path

from mapping.extract_db_usage import (
    DbUsage,
    PhysicalObject,
    extract_cte_relations,
    extract_table_ops_from_text,
    extract_tables_from_sql,
    read_file,
    render_markdown,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class DblinkParserTests(unittest.TestCase):
    def test_qualified_and_unqualified_dblinks_are_preserved(self):
        source = (
            'var readSql = @"SELECT * FROM HO_MEKANISME_NOMINAL_T@mpromo";'
            'var writeSql = @"INSERT INTO MCGDATA.T_TARGET@HODB (ID) VALUES (1)";'
        )

        read, write = extract_table_ops_from_text(source)

        self.assertEqual(
            read["HO_MEKANISME_NOMINAL_T@MPROMO"],
            {"MCGDATA"},
        )
        self.assertEqual(write["T_TARGET@HODB"], {"MCGDATA"})

    def test_objects_without_dblink_keep_existing_identity(self):
        self.assertEqual(
            extract_tables_from_sql("SELECT * FROM MCGDATA.T_SOURCE"),
            {"T_SOURCE": {"MCGDATA"}},
        )

    def test_cte_physical_reads_keep_dblink(self):
        sql = """
        WITH REMOTE_ITEMS AS (
            SELECT ID FROM MCGDATA.T_SOURCE@mpromo
        )
        SELECT ID FROM REMOTE_ITEMS
        """

        relations = extract_cte_relations(sql)

        self.assertIn(
            PhysicalObject("MCGDATA", "T_SOURCE", dblink="MPROMO"),
            relations["REMOTE_ITEMS"].physical_reads,
        )

    def test_same_table_on_different_dblinks_remains_distinct(self):
        usage = DbUsage({})
        usage.add_read("T_SOURCE", "MCGDATA")
        usage.add_read("T_SOURCE@mpromo", "MCGDATA")
        usage.add_read("T_SOURCE@hodb", "MCGDATA")

        self.assertEqual(
            usage.read,
            {
                PhysicalObject("MCGDATA", "T_SOURCE"),
                PhysicalObject("MCGDATA", "T_SOURCE", dblink="MPROMO"),
                PhysicalObject("MCGDATA", "T_SOURCE", dblink="HODB"),
            },
        )


class DblinkRenderingTests(unittest.TestCase):
    def test_rendering_includes_dblink_for_physical_objects_only(self):
        usage = DbUsage({})
        usage.add_read("HO_MEKANISME_NOMINAL_T@mpromo", "MCGDATA")
        usage.add_call("MCGDATA.PKG.CUSTOM_FUNC")
        usage.add_cte(
            "REMOTE_ITEMS",
            physical_reads={
                PhysicalObject("MCGDATA", "T_SOURCE", dblink="MPROMO")
            },
        )

        output = render_markdown(usage, "Sample", "/sample", "sample-id")

        self.assertIn("- MCGDATA.HO_MEKANISME_NOMINAL_T@MPROMO", output)
        self.assertIn("  - Reads: MCGDATA.T_SOURCE@MPROMO", output)
        self.assertIn("- MCGDATA.PKG.CUSTOM_FUNC", output)
        self.assertNotIn("CUSTOM_FUNC@", output)


class RealControllerDblinkTests(unittest.TestCase):
    def test_quotation_controller_contains_mpromo_table_samples(self):
        controller = PROJECT_ROOT / "IMMD.Web/Areas/Transaction/Controllers/QuotationMerchandisingController.cs"

        read, _write = extract_table_ops_from_text(read_file(str(controller)))

        self.assertIn("HO_MEKANISME_NOMINAL_T@MPROMO", read)
        self.assertIn("HO_MEKANISME_SPONSOR_T@MPROMO", read)

    def test_approval_controller_contains_hodb_table_samples(self):
        controller = PROJECT_ROOT / "IMMD.Web/Areas/Transaction/Controllers/ApprovalTradingTermController.cs"

        read, _write = extract_table_ops_from_text(read_file(str(controller)))

        self.assertIn("M_LOGIN_HIRARKI_TRADINGTERM@HODB", read)
        self.assertIn("D_LOGIN_HIRARKI_TRADINGTERM@HODB", read)


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
