

/*
原理：
页码小于等于5时不进行特殊处理
大于5之后，当前页面前面取4页，后面取5页
*/

function pagination(pageIndex, pageSize, totalRecord){
	var pageCount = Math.ceil(totalRecord / pageSize); //共多少页
	var start,end,isendpagenum = false;
	if(pageIndex>5){
		if(pageIndex+5<pageCount){
			end = pageIndex + 5;
			start = pageIndex - 4;
		}
		else{
			end = pageCount;
			start = pageCount - 9;
			isendpagenum=true;
		}
	}
	//输出首页码
	if(pageIndex>5)
		document.write(1+"....<br/>");
	for (var i=start; i<end+1; i++)
	{

		if(i==pageIndex){
			document.write('<span style="color:red;">'+i+'</span><br/>');
			continue;
		}
		document.write(i+"<br/>");
	}
	if(!isendpagenum)
		document.write(pageCount+"....<br/>");
}

pagination(95, 10, 999);