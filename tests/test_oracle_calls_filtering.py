# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import (
    DatabaseCall,
    DbUsage,
    extract_functions_from_sql,
    extract_procedures_from_text,
)


class OuterJoinTests(unittest.TestCase):
    def test_old_style_outer_join_operands_are_not_functions(self):
        sql = """
        SELECT C.KD_TIPE(+), D.FTKODE (+)
        FROM HGJUAL_IDM_NASIONAL A, M_TIPE_HARGA_NEW C, T_CABANG D
        WHERE A.KD_TIPE = C.KD_TIPE(+)
          AND A.KD_DC = D.FTKODE(+)
        """

        functions = extract_functions_from_sql(sql)

        self.assertNotIn("C.KD_TIPE", functions)
        self.assertNotIn("D.FTKODE", functions)


class BuiltinTests(unittest.TestCase):
    def test_unqualified_oracle_builtins_are_not_functions(self):
        sql = """
        SELECT LISTAGG(A.NAMA, ', ') WITHIN GROUP (ORDER BY A.NAMA),
               LENGTHB(A.NAMA), NVL(A.NAMA, 'N/A'),
               EXTRACT(DAY FROM A.CREATED_AT)
        FROM M_DATA A
        """

        functions = extract_functions_from_sql(sql)

        self.assertNotIn("LISTAGG", functions)
        self.assertNotIn("LENGTHB", functions)
        self.assertNotIn("NVL", functions)
        self.assertNotIn("EXTRACT", functions)

    def test_qualified_oracle_builtin_packages_are_not_functions(self):
        sql = """
        SELECT DBMS_RANDOM.VALUE(1, 10),
               SYS.UTL_RAW.CAST_TO_VARCHAR2(A.RAW_VALUE)
        FROM M_DATA A
        """

        functions = extract_functions_from_sql(sql)

        self.assertEqual(functions, set())


class CallIntegrationTests(unittest.TestCase):
    def test_custom_function_survives_builtin_and_outer_join_filtering(self):
        sql = """
        SELECT MCGDATA.CUSTOM_FUNC(A.ID), LISTAGG(A.NAME, ', '),
               LENGTHB(A.NAME), C.KD_TIPE(+)
        FROM M_DATA A, M_TIPE C
        WHERE A.KD_TIPE = C.KD_TIPE(+)
        """

        usage = DbUsage({})
        usage.add_raw_text('var sql = @"' + sql + '";')

        self.assertEqual(
            usage.calls,
            {DatabaseCall("MCGDATA", "CUSTOM_FUNC")},
        )

    def test_custom_procedure_literal_remains_a_call(self):
        source = 'var command = new OracleCommand("MCGDATA.PKG.PROC_LOAD", connection);'

        self.assertEqual(
            extract_procedures_from_text(source),
            {"MCGDATA.PKG.PROC_LOAD"},
        )

    def test_builtin_package_literal_is_not_a_custom_call(self):
        source = 'var command = new OracleCommand("DBMS_OUTPUT.PUT_LINE", connection);'

        self.assertEqual(
            extract_procedures_from_text(source),
            set(),
        )


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
