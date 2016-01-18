<?php

// $url = 'https://500px.com/search?q=adventure&type=photos&sort=pulse';
// $url = 'https://www.flickr.com/photos/robmacklin/21117877326/';
$url = 'http://www.hammersstore.com/';

include('image_finder.class.php');
$finder = new ImageFinder($url);
$images = $finder->get_images();

// var_dump($images);

foreach($images as $img) {
  echo $img['src'] . "\n";
}

?>
