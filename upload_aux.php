<?php

require 'uploadImage.php';

// $argv[0]; is always the script name
$un = $argv[1];
$pw = $argv[2];
$path = $argv[3];

uploadImage($un, $pw, $path);

?>
