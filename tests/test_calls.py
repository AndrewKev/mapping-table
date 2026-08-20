# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import (
    DatabaseCall,  # project : IPRO Revisi Header Laporan Trading Term
    DbUsage,
    extract_functions_from_sql,
    extract_procedures_from_text,
)


class CallExtractionTests(unittest.TestCase):
    def test_qualified_custom_function_is_preserved_and_builtins_are_filtered(self):
        sql = """
        SELECT MCGDATA.PKG.CUSTOM_FUNC(ID), NVL(VALUE, 0), 'FAKE_FUNC()'
        FROM dual -- OTHER_FUNC()
        """

        self.assertEqual(
            extract_functions_from_sql(sql),
            {"MCGDATA.PKG.CUSTOM_FUNC"},
        )

    def test_qualified_procedure_literal_is_preserved(self):
        source = 'var command = new OracleCommand("PKG.PROC_LOAD", connection);'

        self.assertEqual(
            extract_procedures_from_text(source),
            {"PKG.PROC_LOAD"},
        )

    def test_simple_command_text_assignment_is_preserved(self):
        source = 'command.CommandText = @"PKG.PROC_ASSIGN";'

        self.assertEqual(
            extract_procedures_from_text(source),
            {"PKG.PROC_ASSIGN"},
        )

    def test_dynamic_oracle_command_is_a_diagnostic(self):
        usage = DbUsage({})
        usage.add_raw_text(
            "var commandText = GetCommandText();"
            "var command = new OracleCommand(commandText, connection);"
        )

        self.assertEqual(usage.calls, set())
        self.assertEqual(
            {diagnostic.code for diagnostic in usage.diagnostics},
            {"DYNAMIC_PROCEDURE"},
        )

    def test_concatenated_sql_is_a_dynamic_diagnostic(self):
        usage = DbUsage({})
        usage.add_raw_text('var sql = "SELECT * FROM " + tableName;')

        self.assertEqual(
            {diagnostic.code for diagnostic in usage.diagnostics},
            {"DYNAMIC_SQL"},
        )

    # project : IPRO Revisi Header Laporan Trading Term
    def test_concatenated_command_text_extracts_custom_function_from_later_fragment(self):
        usage = DbUsage({})
        source = r'''
            cmd.CommandText = "SELECT A.ID FROM T_DATA A " +
                              "WHERE A.ID = '" + id +
                              "' AND Get_Flag_Bkl('3', A.REGION, A.ID) = 'Y'";
        '''

        usage.add_raw_text(source)

        self.assertIn(
            DatabaseCall("MCGDATA", "GET_FLAG_BKL"),
            usage.calls,
        )
    # end project : IPRO Revisi Header Laporan Trading Term


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
