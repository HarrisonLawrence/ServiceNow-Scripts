var taskCount = 0;

var ciGR = new GlideRecord('cmdb_ci_computer');
ciGR.query();

while (ciGR.next()) {
    var duplicateCIs = new GlideRecord('cmdb_ci_computer');
    duplicateCIs.addQuery('serial_number', ciGR.serial_number);
    duplicateCIs.query();

    var ciList = [];
    while (duplicateCIs.next()) {
        ciList.push(duplicateCIs.sys_id.toString());
    }

    if (ciList.length > 1) {
        // Create a deduplication task
        var duplicateTask = new CMDBDuplicateTaskUtils();
		    var string_ids = ciList.join();
        taskCount++;
        duplicateTask.createDuplicateTask(string_ids);
        gs.info(ciList);

        for (each in ciList) {
            var duplicateResult = new GlideRecord('duplicate_audit_result');
        }
    }
 
}

gs.info('Deduplication tasks created: ' + taskCount);
