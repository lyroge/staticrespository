$text = '<p style="padding:0px;"><strong style="padding:0;margin:0;">hello</strong></p>';

echo preg_replace("/<([a-z][a-z0-9]*)[^>]*?(\/?)>/i",'<$1$2>', $text);