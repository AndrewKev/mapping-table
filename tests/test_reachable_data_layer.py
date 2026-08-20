# project : IPRO Revisi Header Laporan Trading Term
import tempfile
import unittest
from pathlib import Path

from mapping.extract_db_usage import PhysicalObject, analyze_controller


class ReachableDataLayerTestCase(unittest.TestCase):
    def _analyze(
        self,
        controller_source,
        data_source,
        additional_data_sources=None,
        schema_map=None,
    ):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name)
        data_root = root / "IMMD.Data"
        data_root.mkdir()
        controller = root / "MarginIGRController.cs"
        controller.write_text(controller_source, encoding="utf-8")
        (data_root / "IGR_MARGIN_DC.cs").write_text(
            data_source,
            encoding="utf-8",
        )
        for file_name, source in (additional_data_sources or {}).items():
            (data_root / file_name).write_text(source, encoding="utf-8")
        usage, _files, _methods = analyze_controller(
            str(controller),
            str(data_root),
            schema_map or {"IGR_MARGIN_DC": "MCGDATA"},
        )
        return directory, usage


class ReachableClassificationTests(ReachableDataLayerTestCase):
    def test_reachable_read_method_maps_entity_to_direct_read(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Read()
                {
                    IGR_MARGIN_DC.GetAll();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public static IQueryable<IGR_MARGIN_DC> GetAll()
                {
                    return CurrentDataContext.CurrentContext.IGR_MARGIN_DC;
                }
            }
            """,
        )
        try:
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.read,
            )
            self.assertNotIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.write,
            )
            self.assertEqual(usage.calls, set())
        finally:
            directory.cleanup()

    # project : IPRO Revisi Header Laporan Trading Term
    def test_reachable_instance_raw_sql_write_maps_physical_object(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Update()
                {
                    IGR_MARGIN_DC entity = new IGR_MARGIN_DC();
                    entity.UpdateRaw();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public void UpdateRaw()
                {
                    var sql = @"UPDATE MCGDATA.IGR_MARGIN_DC SET VALUE = 1";
                }
            }
            """,
        )
        try:
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.write,
            )
        finally:
            directory.cleanup()
    # end project : IPRO Revisi Header Laporan Trading Term

    # project : IPRO Revisi Header Laporan Trading Term
    def test_updated_name_without_write_body_is_not_classified_as_write(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Update()
                {
                    var entity = IGR_MARGIN_DC.GetByID("IGR", "IDM");
                    entity.Updated();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public static IGR_MARGIN_DC GetByID(string dcIgr, string dcIdm)
                {
                    return CurrentDataContext.CurrentContext.IGR_MARGIN_DC;
                }

                public void Updated()
                {
                    var message = "no database operation";
                }
            }
            """,
        )
        try:
            physical = PhysicalObject("MCGDATA", "IGR_MARGIN_DC")
            self.assertIn(physical, usage.read)
            self.assertNotIn(physical, usage.write)
        finally:
            directory.cleanup()
    # end project : IPRO Revisi Header Laporan Trading Term

    def test_reachable_instance_write_maps_entity_to_direct_write(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Update()
                {
                    var getData = IGR_MARGIN_DC.GetByID("IGR", "IDM");
                    getData.Updated();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public static IGR_MARGIN_DC GetByID(string dcIgr, string dcIdm)
                {
                    return CurrentDataContext.CurrentContext.IGR_MARGIN_DC;
                }

                public void Updated()
                {
                    this.UpdateSave<IGR_MARGIN_DC>();
                }

                public void UncalledWrite()
                {
                    this.UpdateSave<IGR_MARGIN_DC>();
                }
            }
            """,
        )
        try:
            physical = PhysicalObject("MCGDATA", "IGR_MARGIN_DC")
            self.assertIn(physical, usage.read)
            self.assertIn(physical, usage.write)
        finally:
            directory.cleanup()


class ReceiverProvenanceTests(ReachableDataLayerTestCase):
    # project : IPRO Revisi Header Laporan Trading Term
    def test_explicit_entity_receiver_reaches_instance_write(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Insert()
                {
                    IGR_MARGIN_DC entity = new IGR_MARGIN_DC();
                    entity.inserted();
                    entity.Delete();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public void inserted()
                {
                    this.InsertSave<IGR_MARGIN_DC>();
                }

                public Response Delete()
                {
                    this.Delete<IGR_MARGIN_DC>();
                    return null;
                }
            }
            """,
        )
        try:
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.write,
            )
        finally:
            directory.cleanup()
    # end project : IPRO Revisi Header Laporan Trading Term


class InstanceCallGraphTests(ReachableDataLayerTestCase):
    # project : IPRO Revisi Header Laporan Trading Term
    def test_nested_wrapper_reaches_instance_write(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Update()
                {
                    MarginRepository.UpdateMargin();
                }
            }
            """,
            """
            public class MarginRepository
            {
                public static void UpdateMargin()
                {
                    var entity = IGR_MARGIN_DC.GetByID("IGR", "IDM");
                    entity.Updated();
                }
            }

            public partial class IGR_MARGIN_DC
            {
                public static IGR_MARGIN_DC GetByID(string dcIgr, string dcIdm)
                {
                    return CurrentDataContext.CurrentContext.IGR_MARGIN_DC;
                }

                public void Updated()
                {
                    this.UpdateSave<IGR_MARGIN_DC>();
                }
            }
            """,
        )
        try:
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.read,
            )
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.write,
            )
        finally:
            directory.cleanup()
    # end project : IPRO Revisi Header Laporan Trading Term


class ThisReceiverCallGraphTests(ReachableDataLayerTestCase):
    # project : IPRO Revisi Header Laporan Trading Term
    def test_this_receiver_reaches_nested_read_method(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Read()
                {
                    IGR_MARGIN_DC entity = new IGR_MARGIN_DC();
                    entity.LoadThroughThis();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public void LoadThroughThis()
                {
                    this.Load();
                }

                public IGR_MARGIN_DC Load()
                {
                    return CurrentDataContext.CurrentContext.IGR_MARGIN_DC;
                }
            }
            """,
        )
        try:
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.read,
            )
        finally:
            directory.cleanup()
    # end project : IPRO Revisi Header Laporan Trading Term


class ControllerScopeTests(ReachableDataLayerTestCase):
    # project : IPRO Revisi Header Laporan Trading Term
    def test_receiver_inference_is_scoped_to_each_controller_method(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void UpdateDC()
                {
                    var getData = IGR_MARGIN_DC.GetByID("IGR", "IDM");
                    getData.Updated();
                }

                public void UpdatePLU()
                {
                    var getData = IGR_MARGIN_PLU.GetByID("IGR", "IDM");
                    getData.Updated();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public static IGR_MARGIN_DC GetByID(string dcIgr, string dcIdm)
                {
                    return CurrentDataContext.CurrentContext.IGR_MARGIN_DC;
                }

                public void Updated()
                {
                    this.UpdateSave<IGR_MARGIN_DC>();
                }
            }
            """,
            additional_data_sources={
                "IGR_MARGIN_PLU.cs": """
                    public partial class IGR_MARGIN_PLU
                    {
                        public static IGR_MARGIN_PLU GetByID(string dcIgr, string dcIdm)
                        {
                            return CurrentDataContext.CurrentContext.IGR_MARGIN_PLU;
                        }

                        public void Updated()
                        {
                            this.UpdateSave<IGR_MARGIN_PLU>();
                        }
                    }
                    """,
            },
            schema_map={
                "IGR_MARGIN_DC": "MCGDATA",
                "IGR_MARGIN_PLU": "MCGDATA",
            },
        )
        try:
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_DC"),
                usage.write,
            )
            self.assertIn(
                PhysicalObject("MCGDATA", "IGR_MARGIN_PLU"),
                usage.write,
            )
        finally:
            directory.cleanup()
    # end project : IPRO Revisi Header Laporan Trading Term


class ResolutionDiagnosticTests(ReachableDataLayerTestCase):
    # project : IPRO Revisi Header Laporan Trading Term
    def test_unproven_write_like_receiver_is_diagnostic_only(self):
        directory, usage = self._analyze(
            """
            public class MarginIGRController
            {
                public void Update()
                {
                    object entity = ResolveEntity();
                    entity.Updated();
                }
            }
            """,
            """
            public partial class IGR_MARGIN_DC
            {
                public void Updated()
                {
                    this.UpdateSave<IGR_MARGIN_DC>();
                }
            }
            """,
        )
        try:
            physical = PhysicalObject("MCGDATA", "IGR_MARGIN_DC")
            self.assertNotIn(physical, usage.write)
            self.assertIn(
                "UNRESOLVED_INSTANCE_RECEIVER",
                {diagnostic.code for diagnostic in usage.diagnostics},
            )
        finally:
            directory.cleanup()
    # end project : IPRO Revisi Header Laporan Trading Term


if __name__ == "__main__":
    unittest.main()
# end project : IPRO Revisi Header Laporan Trading Term
