//Deletes Multiple records from the table specified in line 3 and the query in line 4.

var rec = new GlideRecord('samp_bulk_import');
rec.addQuery('status','processing');
rec.query();
while (rec.next()) { 
 gs.print('To delete: ' + rec.sys_id.toString());
 rec.deleteRecord();
}
