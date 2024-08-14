//Finds a record anywhere in ServiceNow on any table using the sysID.
//(Slightly) adapted from https://snprotips.com/blog/sncprotips/2015/12/locate-any-record-in-any-table-by-sysidhtml

function findAnywhere(sysIDToFind) {

    var grCheck;
    var tableName;
    var url = gs.getProperty('glide.servlet.uri');
    var grTable = new GlideRecord('sys_db_object');
    //Make sure we're not looking at a ts (text search) table.
    grTable.addEncodedQuery('sys_update_nameISNOTEMPTY^nameISNOTEMPTY^nameNOT LIKEts_');
    grTable.query();
    while (grTable.next()) {
        tableName = grTable.getValue('name');
        grCheck = new GlideRecord(tableName);
        if (grCheck.get(sysIDToFind)) {
            url += tableName + '.do?sys_id=' + sysIDToFind;
            return url;
        }
    }
}
gs.print(findAnywhere('SYSIDHERE'));
