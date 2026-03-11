//Set these fields
var sourceTable = "XXXXXX";
var fieldName = "YYYYYY";
var oldValue = "ZZZZZZ";
var newValue = "AAAAAA";


var recordList = new GlideRecord(sourceTable);
recordList.addQuery(fieldName, "=", oldValue);
recordList.query();
while(recordList.next()){
  recordList.setValue(fieldName, newValue);
  recordList.update();
}
