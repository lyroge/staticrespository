<?php

function get_file_extensions($file_name)  
{  
	$extend =explode('.' , $file_name);
	$va=count($extend)-1;
	return $extend[$va];
}

function resize_image($filename,$maxwidth,$maxheight, $markname)
{
	$ext = get_file_extensions($filename);
	$im = "";
	switch(strtolower($ext))
	{
		case "gif":
			$im = imagecreatefromgif($filename);
			break;
		case "jpg":
			$im = imagecreatefromjpeg($filename);
			break;
		case "jpeg":
			$im = imagecreatefromjpeg($filename);
			break;
		case "png":
			$im = imagecreatefrompng($filename);
			break;
	}

	//picture real diomand
    $pic_width = imagesx($im);
    $pic_height = imagesy($im);

	if(($pic_width > $maxwidth) || ($pic_height > $maxheight))
    {
		//cal ratio
		$widthratio = $maxwidth/$pic_width;
		$heightratio = $maxheight/$pic_height;
		if($pic_width >$maxwidth && $pic_height > $maxheight)
			$ratio = max($widthratio, $heightratio);
		else
			$ratio = min($widthratio, $heightratio);

		//newwidth newheight
		$newwidth = $pic_width * $ratio;
		$newheight = $pic_height * $ratio;

		if(function_exists("imagecopyresampled"))
		{
		   $newim = imagecreatetruecolor($newwidth,$newheight);
		   imagecopyresampled($newim,$im,0,0,0,0,$newwidth,$newheight,$pic_width,$pic_height);
		}
		else
		{
			$newim = imagecreate($newwidth,$newheight);
		   imagecopyresized($newim,$im,0,0,0,0,$newwidth,$newheight,$pic_width,$pic_height);
		}

        $name = str_replace(".".$ext, '_'.$markname.".".$ext, $filename);
		imagejpeg($newim,$name);
		imagedestroy($newim);
    }
    else
    {
        $name = str_replace(".".$ext, '_'.$markname.".".$ext, $filename);
        imagejpeg($im,$name);
    }
}

resize_image("3.png", 100, 100, '100x100');
resize_image("3.png", 250, 250, '250x250');
?>