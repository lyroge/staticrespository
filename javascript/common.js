/* 去掉首尾空格 */
function trim(str){
	 str.replace(/^\s+|\s+$/g, "")   
}

/* 通过元素id查找元素 */
function $(id){
		return document.getElementById(id);
}


