# project : IPRO Revisi Header Laporan Trading Term
import tempfile
import unittest
from pathlib import Path

from mapping.extract_db_usage import index_data_layer


class IndexingPerformanceTests(unittest.TestCase):
    def test_generated_and_build_directories_are_excluded_by_default(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "Keep.cs").write_text(
                "public class KeepRepository { public static void Load() { } }",
                encoding="utf-8",
            )
            (root / "Generated.Designer.cs").write_text(
                "public class GeneratedRepository { public static void Load() { } }",
                encoding="utf-8",
            )
            for excluded in ("bin", "obj", "node_modules"):
                nested = root / excluded
                nested.mkdir()
                (nested / "Hidden.cs").write_text(
                    "public class HiddenRepository { public static void Load() { } }",
                    encoding="utf-8",
                )

            class_files, class_methods = index_data_layer(str(root))

        self.assertEqual(set(class_files), {"KeepRepository"})
        self.assertEqual(set(class_methods), {"KeepRepository"})


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
