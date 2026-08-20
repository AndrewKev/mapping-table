# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import extract_sql_literals, extract_table_ops_from_text


class SqlLiteralTests(unittest.TestCase):
    def test_verbatim_string_is_extracted_once(self):
        source = 'var sql = @"SELECT * FROM MCGDATA.T_SOURCE";'

        self.assertEqual(
            list(extract_sql_literals(source)),
            ["SELECT * FROM MCGDATA.T_SOURCE"],
        )

    def test_merge_using_is_not_rejected_as_csharp_fragment(self):
        source = (
            'var sql = "MERGE INTO MCGDATA.T_TARGET '
            'USING MCGDATA.T_SOURCE ON (T_TARGET.ID = T_SOURCE.ID)";'
        )

        self.assertEqual(
            list(extract_sql_literals(source)),
            [
                "MERGE INTO MCGDATA.T_TARGET "
                "USING MCGDATA.T_SOURCE ON (T_TARGET.ID = T_SOURCE.ID)"
            ],
        )

    def test_interpolated_literal_is_scanned_once(self):
        source = 'var sql = $"SELECT * FROM MCGDATA.T_SOURCE WHERE ID = {id}";'

        self.assertEqual(
            list(extract_sql_literals(source)),
            ["SELECT * FROM MCGDATA.T_SOURCE WHERE ID = {id}"],
        )

    def test_at_dollar_verbatim_interpolation_is_scanned_once(self):
        source = 'var sql = @$"SELECT * FROM MCGDATA.T_SOURCE WHERE ID = {id}";'

        self.assertEqual(
            list(extract_sql_literals(source)),
            ["SELECT * FROM MCGDATA.T_SOURCE WHERE ID = {id}"],
        )

    def test_comment_literal_is_not_scanned(self):
        source = '// var sql = "SELECT * FROM MCGDATA.NOT_REAL";'

        self.assertEqual(list(extract_sql_literals(source)), [])

    # project : IPRO Revisi Header Laporan Trading Term
    def test_error_message_with_update_is_not_database_sql(self):
        source = 'return Content(string.Format("Gagal update karena {0}", ex.Message));'

        self.assertEqual(
            extract_table_ops_from_text(source),
            ({}, {}),
        )

    def test_status_message_starting_with_update_is_not_database_sql(self):
        source = (
            'Console.WriteLine(rowsAffected > 0 ? "Update successful." : '
            '"Update failed.");'
        )

        self.assertEqual(
            extract_table_ops_from_text(source),
            ({}, {}),
        )
    # end project : IPRO Revisi Header Laporan Trading Term


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
