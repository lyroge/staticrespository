/* 设置元素属性值 */
function set_attr(obj, name, value){
	obj.setAttribute(name, value);
}

/*  获取元素属性值 */
function get_attr(obj, name){
	return obj.getAttribute(name);
}

/* 移除元素属性 */
function rem_attr(obj, name){
	obj.removeAttribute(name);
}

/* 设置元素样式 */
function set_class(obj, value){
	set_attr(obj, "class", value);
	set_attr(obj, "className", value);
}

/* 移除元素样式 */
function rem_class(obj){
	remove_attr(obj, "class");
	remove_attr(obj, "className");
}