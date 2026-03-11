// This script checks for in flow variables for a certain string. 
// I generally use this script to look for flows that reference a group before deactivating the group.

var queryString = 'REPLACEME';
var instanceName = gs.getProperty('instance_name');
var flowVariables = new GlideRecord('sys_hub_action_instance_v2');
flowVariables.addEncodedQuery('valuesISNOTEMPTY^flow.sys_class_name=sys_hub_flow');
flowVariables.query();

while (flowVariables.next()) {
    var byteArray = GlideStringUtil.base64DecodeAsBytes(flowVariables.values);
    var decompressedStr = GlideCompressionUtil.expandToString(byteArray);
    if (decompressedStr.includes(queryString)) {
        gs.print('Flow Name: ' + flowVariables.flow.name + '\nStep: ' + flowVariables.order + '\nLink: https://' + instanceName + '.service-now.com/now/workflow-studio/builder?table=sys_hub_flow&sysId=' + flowVariables.flow.sys_id);
    }
}
