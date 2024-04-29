//Set these fields

var titleQuery = "XXXXX";
var groupSysID = "XXXXX";


//Leave these fields
var sourceTable = "sys_report";
var shareTable = "sys_report_users_groups";
var fieldName = "title";


var recordList = new GlideRecord(sourceTable);
recordList.addQuery(fieldName, "CONTAINS", titleQuery);
recordList.query();
while(recordList.next()){
  gs.print(recordList.title + " " + groupSysID);
  var shareGr = new GlideRecord(shareTable);
  shareGr.initialize();
  shareGr.group_id = groupSysID;
  shareGr.report_id = recordList.sys_id.toString();
  shareGr.insert();
}
