# project : IPRO Revisi Header Laporan Trading Term
import tempfile
import unittest
from pathlib import Path

from mapping.extract_db_usage import parse_edmx_entity_map, parse_edmx_schema_map


class EdmxMappingTests(unittest.TestCase):
    def test_entity_set_attribute_order_and_namespace_prefix_do_not_matter(self):
        edmx = """
        <edmx:Edmx xmlns:edmx="http://schemas.microsoft.com/ado/2009/11/edmx"
                   xmlns:store="http://schemas.microsoft.com/ado/2007/12/edm/ssdl">
          <edmx:Runtime>
            <edmx:StorageModels>
              <Schema Namespace="DbModel.Store"
                      xmlns="http://schemas.microsoft.com/ado/2009/11/edm/ssdl">
                <EntityContainer Name="DbEntitiesStoreContainer">
                  <EntitySet Schema="MCGDATA"
                             EntityType="DbModel.Store.T_SOURCE"
                             Name="T_SOURCE" />
                  <EntitySet store:Schema="REPORTING"
                             store:Name="T_REPORT"
                             Name="REPORT_ALIAS"
                             EntityType="DbModel.Store.REPORT_ALIAS" />
                </EntityContainer>
              </Schema>
            </edmx:StorageModels>
          </edmx:Runtime>
        </edmx:Edmx>
        """

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "DbModel.edmx"
            path.write_text(edmx, encoding="utf-8")

            self.assertEqual(
                parse_edmx_schema_map(str(path)),
                {"T_SOURCE": "MCGDATA", "REPORT_ALIAS": "REPORTING"},
            )
            self.assertEqual(
                parse_edmx_entity_map(str(path))["REPORT_ALIAS"],
                ("REPORTING", "T_REPORT"),
            )


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
