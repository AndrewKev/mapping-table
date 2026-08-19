# project : IPRO Revisi Header Laporan Trading Term
import tempfile
import unittest
from pathlib import Path

from mapping.extract_db_usage import DbUsage, main, render_markdown


class CliDiagnosticsTests(unittest.TestCase):
    def test_strict_mode_fails_for_missing_required_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out.md"

            result = main([
                "--controller", str(Path(directory) / "missing.cs"),
                "--data-root", str(Path(directory) / "missing-data"),
                "--edmx", str(Path(directory) / "missing.edmx"),
                "--output", str(output),
                "--strict",
            ])

        self.assertNotEqual(result, 0)
        self.assertFalse(output.exists())

    def test_normal_mode_writes_visible_input_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out.md"

            result = main([
                "--controller", str(Path(directory) / "missing.cs"),
                "--data-root", str(Path(directory) / "missing-data"),
                "--edmx", str(Path(directory) / "missing.edmx"),
                "--output", str(output),
                "--name", "Sample",
                "--url", "/sample",
            ])

            markdown = output.read_text(encoding="utf-8")

        self.assertEqual(result, 0)
        self.assertIn("# Analysis Notes", markdown)
        self.assertIn("INPUT_MISSING", markdown)

    def test_frontmatter_values_escape_yaml_sensitive_text(self):
        markdown = render_markdown(
            DbUsage({}),
            'Sample\nname: "unsafe"',
            "/sample?x=1\nnext",
            "id: bad\nnext",
        )

        frontmatter = markdown.split("---", 2)[1]
        self.assertNotIn("\nname: unsafe", frontmatter)
        self.assertIn(r'\n', frontmatter)
        self.assertIn(r'\"unsafe\"', frontmatter)


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
