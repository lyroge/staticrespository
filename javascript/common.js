(function(window){
	var document   = window.document
	, _hd    = window.hd={
		
	};		
})(window);


/* 去掉首尾空格 */
function trim(str){
	 str.replace(/^\s+|\s+$/g, "")   
}

/* 通过元素id查找元素 */
function $(id){
		return document.getElementById(id);
}

/* 用source中非空属性重写默认对象中的属性 */
function extend (destination, source) {     
	var o = {};       
	for (var property in source) {
		if (source[property] || source[property] == 0)
		o[property] = source[property];   
	}
	return o;   
}

/* 字符串字符个数 */
function getStrActualLen(sChars){
	sChars = $.trim(sChars);
	var len = 0;
	for(i=0;i<sChars.length;i++){
		iCode = sChars.charCodeAt(i);
		if((iCode>=0 && iCode<=255)||(iCode>=0xff61 && iCode<=0xff9f)){
			len += 1;
		}else{
			len += 2;
		}
	}
	return len;
}


