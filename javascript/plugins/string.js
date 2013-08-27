
/* 去掉首尾空格 */
function trim(str){
	return str.replace(/^\s+|\s+$/g, "");
}

/* 获取字符串字符个数 （按字节算） */
function str_len(str){
	str = trim(str);
	var len = 0;
	for(var i=0;i<str.length;i++){
		code = str.charCodeAt(i);
		if((code>=0 && code<=255)||(code>=0xff61 && code<=0xff9f)){
			len += 1;
		}else{
			len += 2;
		}
	}
	return len;
}