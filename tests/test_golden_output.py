# project : IPRO Revisi Header Laporan Trading Term
import unittest
from pathlib import Path

from mapping.extract_db_usage import analyze_controller, parse_edmx_schema_map, render_markdown


class GoldenOutputTests(unittest.TestCase):
    def test_sample_fixture_matches_expected_markdown(self):
        mapping_root = Path(__file__).resolve().parents[1]
        fixture_root = mapping_root / "fixtures"
        schema_map = parse_edmx_schema_map(str(fixture_root / "DbModel.edmx"))
        usage, _files, _methods = analyze_controller(
            str(fixture_root / "SampleController.cs"),
            str(fixture_root / "IMMD.Data"),
            schema_map,
        )

        actual = render_markdown(usage, "Sample", "/Sample", "sample")
        expected = (fixture_root / "expected.md").read_text(encoding="utf-8")

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
