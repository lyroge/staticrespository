<?php

	//empty array
	$ary = array()
	$ary[0] = 1
	$ary[1] = 2
	$ary['a'] = 'A'
	$ary['b'] = 'B'
	$ary=array('a'=>'A', 'b'=>'B');
	

	//empty isset diffenrence
	$i = 0
	isset($i) = true
	empty($I) = false


	//array implode explode
	implode($ary, ',') => a,b,c
	explode(":", 'a:b:c'); => array()


	//mixed str_replace ( mixed $search , mixed $replace , mixed $subject [, int &$count ] )
	//str replace 
	str_replace("&", "_", $str); //return replaced result
	str_ireplace

	// 赋值: <body text='black'>
	$bodytag = str_replace("%body%", "black", "<body text='%body%'>");

	// 赋值: Hll Wrld f PHP
	$vowels = array("a", "e", "i", "o", "u", "A", "E", "I", "O", "U");
	$onlyconsonants = str_replace($vowels, "", "Hello World of PHP");

	// 赋值: You should eat pizza, beer, and ice cream every day
	$phrase  = "You should eat fruits, vegetables, and fiber every day.";
	$healthy = array("fruits", "vegetables", "fiber");
	$yummy   = array("pizza", "beer", "ice cream");

	$newphrase = str_replace($healthy, $yummy, $phrase);

	//正则替换
	$string = 'April 15, 2003';
	$pattern = '/(\w+) (\d+), (\d+)/i';
	$replacement = '${1}1,$3';
	echo preg_replace($pattern, $replacement, $string);
	$url = preg_replace("/250x250/", "100x100", $url);
?>