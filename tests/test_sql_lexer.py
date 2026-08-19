# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import tokenize_sql


class SqlLexerTests(unittest.TestCase):
    def test_comments_and_quoted_values_are_single_non_identifier_tokens(self):
        sql = "SELECT 'FROM MCGDATA.NOT_REAL', col FROM \"MCGDATA\".\"T_REAL\" -- FROM fake\n"

        tokens = tokenize_sql(sql)
        values = [token.value for token in tokens]

        self.assertIn("FROM MCGDATA.NOT_REAL", values)
        self.assertNotIn("NOT_REAL", values)
        self.assertNotIn("fake", values)
        self.assertIn("T_REAL", values)
        self.assertEqual(
            [token.kind for token in tokens if token.value == "FROM MCGDATA.NOT_REAL"],
            ["string"],
        )
        self.assertEqual(
            [token.kind for token in tokens if token.value == "T_REAL"],
            ["quoted_identifier"],
        )

    def test_nested_parentheses_preserve_tokens_and_depth(self):
        sql = "SELECT * FROM T_OUTER WHERE EXISTS (SELECT 1 FROM T_INNER)"

        tokens = tokenize_sql(sql)
        outer = next(token for token in tokens if token.value == "T_OUTER")
        inner = next(token for token in tokens if token.value == "T_INNER")

        self.assertEqual(outer.kind, "identifier")
        self.assertEqual(inner.kind, "identifier")
        self.assertGreater(inner.depth, outer.depth)
        self.assertEqual(
            [token.value for token in tokens if token.value.lower() == "from"],
            ["FROM", "FROM"],
        )


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
