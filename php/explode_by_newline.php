<?php
	echo implode('|||', (preg_split( '/\r\n|\r|\n/', 'abc
def
')));
?>
