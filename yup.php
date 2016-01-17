<?php

require 'vendor/mgp25/instagram-php/src/Instagram.php';

/////// CONFIG ///////
$username = 'amazing_outside';
$password = 'organic';
$debug    = true;
$photo    = 'rekt2.jpg';     // path to the photo
$caption  = null;   // caption
//////////////////////

$i = new Instagram($username, $password, $debug);

try {
  $i->login();
} catch (InstagramException $e) {
  $e->getMessage();
  echo "nargs\n";
  exit();
}

echo $i->getSelfUsernameInfo();

try {
  $i->uploadPhoto($photo, $caption);
} catch (Exception $e) {
  echo $e->getMessage();
  echo "slugs\n";
}
echo "woot\n";

?>
