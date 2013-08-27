(function(window){
	var document   = window.document
	, _hd    = window.hd={
		
	};		
})(window);


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