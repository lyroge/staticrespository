/* set automaticly input element height attribute */
function autoheight(obj){
	if (obj.scrollHeight > obj.offsetHeight){
		obj.style.height = obj.scrollHeight + "px";
	}
}

/* 

relative event for all browsers 

===== html sample ====

<textarea name="wonderfulpoint" 
	onpaste="autoheight(this)"
	oninput="autoheight(this)" 
	onkeypress="autoheight(this)"
	onchange="autoheight(this)">
</textarea>

*/