/* 设置透明度style */
function SetOpacity(ev, v){
	ev.filters ? ev.style.filter = 'alpha(opacity=' + v + ')' : ev.style.opacity = v / 100;
}
	
var defaultoptions = {"speed":20, "opacity":100, "callback":null}        

//淡入效果(含淡入到指定透明度)
function fadeIn(elem, options){	    
	options = extend(defaultoptions, options);
	speed = options.speed || 20;
	opacity = options.opacity || 100;
	//显示元素,并将元素值为0透明度(不可见)
	elem.style.display = 'block';
	//初始化透明度变化值为0
	var val = 0;
	//循环将透明值以5递增,即淡入效果
	(function(){
		SetOpacity(elem, val);
		val += 5;
		if (val <= opacity) {
			setTimeout(arguments.callee, speed)
		}else{
			if (options.callback)
				options.callback();
		}
	})();	
}

//淡出效果(含淡出到指定透明度)
function fadeOut(elem, options){
	options = extend(defaultoptions, options);	    
	speed = options.speed || 20;
	opacity = options.opacity || 0;
	//初始化透明度变化值为0
	var val = 100;
	//循环将透明值以5递减,即淡出效果
	(function(){
		SetOpacity(elem, val);
		val -= 5;
		if (val >= opacity) {
			setTimeout(arguments.callee, speed);
		}else if (val < 0) {
			//元素透明度为0后隐藏元素
			elem.style.display = 'none';	                
			if (options.callback)
				options.callback();	            
		}
	})();
}
