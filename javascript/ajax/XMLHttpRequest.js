/* 原生的ajax类，post、get方法 详细说明见类下面说明 */
function Ajax(callback) {
  var xmlhttp;
  if (window.XMLHttpRequest) { // code for IE7+, Firefox, Chrome, Opera, Safari
    xmlhttp = new XMLHttpRequest();
  } else { // code for IE6, IE5
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }

  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
      if (typeof(callback) != "undefined") {
        callback(xmlhttp.responseText);
      }
    }
  };
  this.get = function(url) {
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
  };
  this.post = function(url, data) {
    xmlhttp.open("POST", url, true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(data);
  };
}


var xmlhttp;
if (window.XMLHttpRequest)
{// code for IE7+, Firefox, Chrome, Opera, Safari
xmlhttp=new XMLHttpRequest();
}
else
{// code for IE6, IE5
xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}

/*
GET Requests
	A simple GET request:
	###Example

	//To avoid this, add a unique ID to the URL:
	//?t=" + Math.random()
	xmlhttp.open("GET","demo_get.asp?id=1",true);
	xmlhttp.send();


POST Requests
	A simple POST request:

	###Example
	xmlhttp.open("POST","demo_post.asp",true);
	xmlhttp.send();

	###Example
	xmlhttp.open("POST","ajax_test.asp",true);
	xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
	xmlhttp.send("fname=Henry&lname=Ford");

	Async=true
	###Example

	xmlhttp.onreadystatechange=function()
	{
	  if (xmlhttp.readyState==4 && xmlhttp.status==200)
	    {
	    document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
	    }
	}
	xmlhttp.open("GET","ajax_info.txt",true);
	xmlhttp.send();

xmlhttp Property
	onreadystatechange	Stores a function (or the name of a function) to be called automatically each time the readyState property changes
	readyState			Holds the status of the XMLHttpRequest. Changes from 0 to 4: 
			0: request not initialized 
			1: server connection established
			2: request received 
			3: processing request 
			4: request finished and response is ready
	status	200: "OK"
			404: Page not found

Server Response
	xmlhttp.responseText
	xmlhttp.responseXML

Cross Domain Solution

*/