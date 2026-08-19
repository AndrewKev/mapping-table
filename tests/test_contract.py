# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import (
    CteRelation,
    DbUsage,
    Diagnostic,
    PhysicalObject,
)


class UsageContractTests(unittest.TestCase):
    def test_same_name_in_two_schemas_remains_two_physical_objects(self):
        usage = DbUsage({})

        usage.add_read("T_SOURCE", "MCGDATA")
        usage.add_read("T_SOURCE", "REPORTING")

        self.assertEqual(
            usage.read,
            {
                PhysicalObject("MCGDATA", "T_SOURCE", "unknown"),
                PhysicalObject("REPORTING", "T_SOURCE", "unknown"),
            },
        )

    def test_cte_is_logical_and_tracks_physical_reads_and_dependencies(self):
        usage = DbUsage({})

        usage.add_cte(
            "ACTIVE_ITEMS",
            physical_reads={PhysicalObject("MCGDATA", "T_SOURCE", "unknown")},
            cte_dependencies={"BASE_ITEMS"},
            consumers={"OUTER_QUERY"},
        )

        relation = usage.ctes["ACTIVE_ITEMS"]
        self.assertIsInstance(relation, CteRelation)
        self.assertEqual(relation.cte_dependencies, {"BASE_ITEMS"})
        self.assertEqual(relation.consumers, {"OUTER_QUERY"})
        self.assertNotIn("ACTIVE_ITEMS", usage.read)
        self.assertNotIn("ACTIVE_ITEMS", usage.write)

    def test_cte_tuple_reads_are_canonicalized_to_physical_objects(self):
        usage = DbUsage({})

        usage.add_cte("ACTIVE_ITEMS", physical_reads={("MCGDATA", "T_SOURCE")})

        self.assertEqual(
            usage.ctes["ACTIVE_ITEMS"].physical_reads,
            {PhysicalObject("MCGDATA", "T_SOURCE")},
        )

    def test_diagnostic_has_stable_code_and_severity(self):
        diagnostic = Diagnostic("UNRESOLVED_SQL", "SQL is dynamic", "warning")

        self.assertEqual(diagnostic.code, "UNRESOLVED_SQL")
        self.assertEqual(diagnostic.severity, "warning")

    def test_unmapped_entity_is_visible_as_a_diagnostic(self):
        usage = DbUsage({"KNOWN": "MCGDATA"})

        usage.add_entity("UNKNOWN")

        self.assertEqual(
            {diagnostic.code for diagnostic in usage.diagnostics},
            {"EDMX_MAPPING_MISSING"},
        )


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
