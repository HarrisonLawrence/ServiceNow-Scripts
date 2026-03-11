var instance=new SCRIPT_NAME_HERE
var list=[];
for(var prop in instance){
     var temp=instance[prop] instanceof Function ? instance[prop] :JSON.stringify( instance[prop]);
     list.push(prop+": "+temp );
}
gs.print("\n"+list.join("\n"));
