# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import extract_table_ops_from_text


class DmlClassificationTests(unittest.TestCase):
    def test_insert_select_and_merge_separate_targets_from_sources(self):
        source = r'''
        var insertSql = @"INSERT INTO MCGDATA.T_TARGET (ID)
            SELECT ID FROM MCGDATA.T_SOURCE";
        var mergeSql = @"MERGE INTO REPORTING.T_MERGE_TARGET target
            USING MCGDATA.T_MERGE_SOURCE source
            ON (target.ID = source.ID)";
        '''

        read, write = extract_table_ops_from_text(source)

        self.assertEqual(
            read,
            {
                "T_SOURCE": {"MCGDATA"},
                "T_MERGE_SOURCE": {"MCGDATA"},
            },
        )
        self.assertEqual(
            write,
            {
                "T_TARGET": {"MCGDATA"},
                "T_MERGE_TARGET": {"REPORTING"},
            },
        )

    def test_update_and_delete_subquery_sources_are_reads(self):
        source = r'''
        var updateSql = @"UPDATE MCGDATA.T_TARGET
            SET VALUE = (SELECT VALUE FROM MCGDATA.T_UPDATE_SOURCE)";
        var deleteSql = @"DELETE FROM MCGDATA.T_DELETE_TARGET
            WHERE EXISTS (SELECT 1 FROM REPORTING.T_DELETE_SOURCE)";
        '''

        read, write = extract_table_ops_from_text(source)

        self.assertEqual(
            read,
            {
                "T_UPDATE_SOURCE": {"MCGDATA"},
                "T_DELETE_SOURCE": {"REPORTING"},
            },
        )
        self.assertEqual(
            write,
            {
                "T_TARGET": {"MCGDATA"},
                "T_DELETE_TARGET": {"MCGDATA"},
            },
        )


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
