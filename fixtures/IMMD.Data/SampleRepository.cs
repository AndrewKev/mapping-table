// project : IPRO Revisi Header Laporan Trading Term
public static class SampleRepository
{
    public static void Load()
    {
        var sql = @"
            WITH ACTIVE_ITEMS AS (
                SELECT ID FROM MCGDATA.T_SOURCE
            )
            INSERT INTO REPORTING.T_TARGET (ID)
            SELECT ID FROM ACTIVE_ITEMS";

        SampleRepository.Lookup();
    }

    public static void Lookup()
    {
        var sql = @"SELECT MCGDATA.PKG.CUSTOM_FUNC(ID) FROM dual";
        var command = new OracleCommand("REPORTING.PKG.PROC_LOAD", connection);
    }
}
// end project : IPRO Revisi Header Laporan Trading Term
