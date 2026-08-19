# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import extract_method_bodies, index_data_layer


class SourceIndexTests(unittest.TestCase):
    def test_methods_are_owned_by_their_declaring_class(self):
        source = """
        public class FirstRepository
        {
            public static void FirstMethod() { CurrentDataContext.CurrentContext.FIRST_TABLE; }
        }
        public class SecondRepository
        {
            public static void SecondMethod() { CurrentDataContext.CurrentContext.SECOND_TABLE; }
        }
        """

        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as directory:
            Path(directory, "Repositories.cs").write_text(source, encoding="utf-8")
            _, class_methods = index_data_layer(directory)

        self.assertIn("FirstMethod", class_methods["FirstRepository"])
        self.assertNotIn("SecondMethod", class_methods["FirstRepository"])
        self.assertIn("SecondMethod", class_methods["SecondRepository"])
        self.assertNotIn("FirstMethod", class_methods["SecondRepository"])

    def test_overloads_are_preserved_and_braces_in_comments_are_ignored(self):
        source = """
        public class Repository
        {
            public static void Load(int id)
            {
                // } this brace is not code
                CurrentDataContext.CurrentContext.FIRST_TABLE;
            }

            public static void Load(string id)
            {
                /* { this brace is not code */
                CurrentDataContext.CurrentContext.SECOND_TABLE;
            }
        }
        """

        methods = extract_method_bodies(source)

        self.assertEqual(len(methods["Load"]), 2)
        self.assertIn("FIRST_TABLE", methods["Load"][0])
        self.assertIn("SECOND_TABLE", methods["Load"][1])


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
