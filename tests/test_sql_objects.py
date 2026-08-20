# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import extract_tables_from_sql


class SqlObjectTests(unittest.TestCase):
    def test_nested_sources_and_cte_names_are_classified_as_physical_objects(self):
        sql = """
        WITH ACTIVE_ITEMS AS (
            SELECT s.ID
            FROM MCGDATA.T_SOURCE s
            WHERE EXISTS (SELECT 1 FROM REPORTING.T_AUX a WHERE a.ID = s.ID)
        ), OTHER_ITEMS AS (
            SELECT ID FROM ACTIVE_ITEMS
        )
        SELECT a.ID
        FROM ACTIVE_ITEMS a
        JOIN MCGDATA.T_JOIN j ON j.ID = a.ID
        """

        self.assertEqual(
            extract_tables_from_sql(sql),
            {
                "T_SOURCE": {"MCGDATA"},
                "T_AUX": {"REPORTING"},
                "T_JOIN": {"MCGDATA"},
            },
        )

    def test_quoted_schema_and_table_are_normalized(self):
        sql = 'SELECT * FROM "REPORTING"."T_SOURCE"'

        self.assertEqual(
            extract_tables_from_sql(sql),
            {"T_SOURCE": {"REPORTING"}},
        )

    def test_oracle_extract_operand_is_not_a_physical_object(self):
        sql = (
            "SELECT EXTRACT(DAY FROM LAST_DAY(ADD_MONTHS(TRUNC(SYSDATE), -1))) "
            "FROM dual"
        )

        self.assertEqual(extract_tables_from_sql(sql), {})


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
