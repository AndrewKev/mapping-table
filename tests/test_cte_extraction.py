# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import PhysicalObject, extract_cte_relations


class CteExtractionTests(unittest.TestCase):
    def test_chained_ctes_keep_physical_reads_dependencies_and_consumers(self):
        sql = """
        WITH ACTIVE_ITEMS AS (
            SELECT ID FROM MCGDATA.T_SOURCE
        ),
        CURRENT_ITEMS AS (
            SELECT ID FROM ACTIVE_ITEMS
        )
        SELECT ID FROM CURRENT_ITEMS
        """

        relations = extract_cte_relations(sql)

        self.assertEqual(set(relations), {"ACTIVE_ITEMS", "CURRENT_ITEMS"})
        self.assertEqual(
            relations["ACTIVE_ITEMS"].physical_reads,
            {PhysicalObject("MCGDATA", "T_SOURCE")},
        )
        self.assertEqual(relations["ACTIVE_ITEMS"].cte_dependencies, set())
        self.assertEqual(relations["ACTIVE_ITEMS"].consumers, {"CURRENT_ITEMS"})
        self.assertEqual(relations["CURRENT_ITEMS"].physical_reads, set())
        self.assertEqual(
            relations["CURRENT_ITEMS"].cte_dependencies,
            {"ACTIVE_ITEMS"},
        )
        self.assertEqual(relations["CURRENT_ITEMS"].consumers, {"OUTER_QUERY"})

    def test_cte_source_is_logical_while_physical_target_stays_separate(self):
        sql = """
        WITH SOURCE_ITEMS AS (
            SELECT ID FROM MCGDATA.T_SOURCE
        )
        INSERT INTO REPORTING.T_TARGET
        SELECT ID FROM SOURCE_ITEMS
        """

        relations = extract_cte_relations(sql)

        self.assertEqual(
            relations["SOURCE_ITEMS"].physical_reads,
            {PhysicalObject("MCGDATA", "T_SOURCE")},
        )
        self.assertEqual(relations["SOURCE_ITEMS"].consumers, {"OUTER_QUERY"})


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
