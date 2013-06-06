<?php

function extend_1($file_name)
{  
	$retval="";  
	$pt=strrpos($file_name, ".");  
	if ($pt) 
		$retval=substr($file_name, $pt+1, strlen($file_name) - $pt);  
	return ($retval);  
}

function extend_2($file_name)  
{  
	$extend = pathinfo($file_name);  
	$extend = strtolower($extend["extension"]);  
	return $extend;  
}  

function extend_3($file_name)  
{  
	$extend =explode("." , $file_name);  
	$va=count($extend)-1;  
	return $extend[$va];
}
?>