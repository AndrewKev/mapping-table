# project : IPRO Revisi Header Laporan Trading Term
import tempfile
import unittest
from pathlib import Path

from mapping.extract_db_usage import PhysicalObject, analyze_controller


class AnalyzerIntegrationTests(unittest.TestCase):
    def test_controller_and_nested_data_layer_usage_share_one_aggregate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data_root = root / "IMMD.Data"
            data_root.mkdir()
            controller = root / "SampleController.cs"
            controller.write_text(
                "public class SampleController { "
                "public void Run() { Repository.Load(); } }",
                encoding="utf-8",
            )
            (data_root / "Repository.cs").write_text(
                "public static class Repository { "
                "public static void Load() { "
                'var sql = @"WITH ACTIVE AS (SELECT ID FROM MCGDATA.T_SOURCE) '
                'SELECT ID FROM ACTIVE"; '
                "Repository.Write(); } "
                "public static void Write() { "
                'var sql = @"MERGE INTO REPORTING.T_TARGET USING '
                'MCGDATA.T_SOURCE ON (1 = 1)"; } }',
                encoding="utf-8",
            )

            usage, _files, _methods = analyze_controller(
                str(controller),
                str(data_root),
                {"CUSTOMER": "REPORTING"},
            )

        self.assertIn(PhysicalObject("MCGDATA", "T_SOURCE"), usage.read)
        self.assertIn(PhysicalObject("REPORTING", "T_TARGET"), usage.write)
        self.assertIn("ACTIVE", usage.ctes)
        self.assertEqual(usage.diagnostics, [])

    def test_missing_method_is_reported_without_creating_database_object(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data_root = root / "IMMD.Data"
            data_root.mkdir()
            controller = root / "SampleController.cs"
            controller.write_text(
                "public class SampleController { "
                "public void Run() { Repository.Missing(); } }",
                encoding="utf-8",
            )
            (data_root / "Repository.cs").write_text(
                "public static class Repository { "
                "public static void Existing() { } }",
                encoding="utf-8",
            )

            usage, _files, _methods = analyze_controller(
                str(controller), str(data_root), {}
            )

        self.assertEqual(usage.read, set())
        self.assertEqual(usage.write, set())
        self.assertEqual(
            {diagnostic.code for diagnostic in usage.diagnostics},
            {"UNRESOLVED_METHOD"},
        )

    def test_recursive_data_layer_calls_terminate_with_visited_keys(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data_root = root / "IMMD.Data"
            data_root.mkdir()
            controller = root / "SampleController.cs"
            controller.write_text(
                "public class SampleController { "
                "public void Run() { Repository.First(); } }",
                encoding="utf-8",
            )
            (data_root / "Repository.cs").write_text(
                "public static class Repository { "
                "public static void First() { Repository.Second(); } "
                "public static void Second() { Repository.First(); } }",
                encoding="utf-8",
            )

            usage, _files, _methods = analyze_controller(
                str(controller), str(data_root), {}
            )

        self.assertEqual(usage.diagnostics, [])


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
