# project : IPRO Revisi Header Laporan Trading Term
import unittest

from mapping.extract_db_usage import DbUsage, PhysicalObject


class EfUsageTests(unittest.TestCase):
    def test_controller_entity_read_and_ef_writes_share_canonical_identity(self):
        usage = DbUsage({"CUSTOMER": "REPORTING"})
        usage.add_raw_text(
            "var rows = CurrentDataContext.CurrentContext.CUSTOMER;"
            "entity.InsertSave<CUSTOMER>();"
            "entity.UpdateSave<CUSTOMER>();"
            "entity.Delete<CUSTOMER>();"
        )

        self.assertEqual(
            usage.read,
            {PhysicalObject("REPORTING", "CUSTOMER")},
        )
        self.assertEqual(
            usage.write,
            {PhysicalObject("REPORTING", "CUSTOMER")},
        )

    def test_context_object_writes_are_classified_as_direct_write(self):
        usage = DbUsage({})
        usage.add_raw_text(
            'CurrentDataContext.CurrentContext.AddObject("T_INSERT", entity);'
            'CurrentDataContext.CurrentContext.DeleteObject(entity);'
        )

        self.assertEqual(
            usage.write,
            {PhysicalObject("MCGDATA", "T_INSERT")},
        )


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
