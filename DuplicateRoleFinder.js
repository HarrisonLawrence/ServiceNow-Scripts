//////////////////////////////////////////////////
// Script to cycle through each group and check //
// to see if there are any roles directly       //
// assigned that are inherited by other roles   //
// that are also assigned and can therefore be  //
// removed because they are redundant.          //
//////////////////////////////////////////////////

//Set some initial variables
var results = [];
var groupName = '';

// Look for groups that have roles assigned
var groupGR = new GlideRecord("sys_user_group");
var grJoin = groupGR.addJoinQuery('sys_group_has_role', 'sys_id', 'group');
groupGR.query();


// Cycle through each group
while (groupGR.next()) {
    groupName = groupGR.getValue("name");

    var rolesMap = {};

    // Look for roles in each group
    var grRole = new GlideRecord("sys_group_has_role");
    grRole.addQuery("group", groupGR.getUniqueValue());
    grRole.query();

	// Map each role found
    while (grRole.next()) {
        var roleName = grRole.role.name.toString();

        if (!rolesMap[roleName]) {
            rolesMap[roleName] = {
                roleName: roleName,
                sources: [],
                redundant: false
            };
        }
    }

    // Look for redundant child roles
    for (var roleInstance in rolesMap) {
        var containGR = new GlideRecord("sys_user_role_contains");
        containGR.addQuery("role.name", roleInstance);
        containGR.query();

        while (containGR.next()) {
            var childRoleName = containGR.contains.name.toString();
            if (rolesMap[childRoleName]) {
                rolesMap[childRoleName].redundant = true;
                rolesMap[childRoleName].sources.push(roleInstance);
            }
        }
    }

    // Collect results
    for (var roleKey in rolesMap) {
        var roleData = rolesMap[roleKey];

        results.push({
            group_name: groupName,
            role_name: roleData.roleName,
            removal_candidate: roleData.redundant ? "Yes" : "No",
            sources: roleData.sources
        });
    }
}
var reportOut = '';

// Log only removal candidates
reportOut += "=== Redundant Role Audit Results ===\n";
results.forEach(function(roleInstance) {
    if (roleInstance.removal_candidate === "Yes") {
        reportOut += (
            "Group: " + roleInstance.group_name +
            " | Role: " + roleInstance.role_name +
            " | Contained by: " + roleInstance.sources + 
			"\n"
        );
    }
});

// Print the results
gs.info(reportOut);
