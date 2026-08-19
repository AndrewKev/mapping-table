# project : IPRO Revisi Header Laporan Trading Term
import tempfile
import unittest
from pathlib import Path

from mapping.extract_db_usage import extract_ef_entity_usage, index_data_layer, strip_csharp_comments


class CsharpMaskTests(unittest.TestCase):
    def test_comments_are_removed_but_sql_string_is_preserved(self):
        source = (
            "// SELECT * FROM COMMENTED_TABLE\n"
            "var sql = @\"SELECT * FROM REAL_TABLE -- keep SQL text\";\n"
            "/* UPDATE HIDDEN_TABLE SET X = 1 */\n"
        )

        masked = strip_csharp_comments(source)

        self.assertNotIn("COMMENTED_TABLE", masked)
        self.assertNotIn("HIDDEN_TABLE", masked)
        self.assertIn("REAL_TABLE", masked)
        self.assertIn("-- keep SQL text", masked)

    def test_data_layer_index_ignores_commented_methods_and_entities(self):
        source = """
        public class SampleRepository
        {
            // public static void Commented() { CurrentDataContext.CurrentContext.HIDDEN_TABLE; }
            public static void Real() { CurrentDataContext.CurrentContext.REAL_TABLE; }
        }
        """

        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "SampleRepository.cs").write_text(source, encoding="utf-8")

            class_files, class_methods = index_data_layer(directory)

        self.assertIn("SampleRepository", class_files)
        self.assertIn("Real", class_methods["SampleRepository"])
        self.assertNotIn("Commented", class_methods["SampleRepository"])
        self.assertEqual(extract_ef_entity_usage(source)[0], {"REAL_TABLE"})

    def test_data_layer_index_ignores_class_and_method_text_inside_strings(self):
        source = '''
        public class SampleRepository
        {
            var text = "public class Fake { public static void FakeMethod() { } }";
            public static void Real() { }
        }
        '''

        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "SampleRepository.cs").write_text(source, encoding="utf-8")

            _class_files, class_methods = index_data_layer(directory)

        self.assertEqual(set(class_methods["SampleRepository"]), {"Real"})


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
