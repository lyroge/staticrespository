/* 判断是否选中了 radio */
function is_radio_checked(name){
	var obj = document.getElementsByName(name);
	for(i=0;i<obj.length;i++){
		if(obj[i].checked){
			b = true;
		}
	}
	return false;
}