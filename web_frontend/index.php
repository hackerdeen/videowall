<?php
/*
 * This is a main file for the videowall web interface
 * 
 * @author      AndyG - https://twitter.com/andygasman
 * @package     videowall
 * @copyright   Copyright 2016
 * @license     GNU Public License
 * @link        https://github.com/hackerdeen/videowall
 * @version     1.0.0
*/
?>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>57n Video Wall</title>

    <!-- Bootstrap -->
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <link href="videowall.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    
<?php 
# Control
require_once("helper.php");


$debug = TRUE;


if ( isset($_POST["task"])) {
    if ( $_POST["task"] == "upload" )  {
        handle_upload();
    }    
} 
if ( isset($_GET["task"])) {
    if ( $_GET["task"] == "delete_one" )  {
        delete_one();
    }    
} 

/*

$videowall_globals = array(
    "error_message" => "",
    "error" => FALSE,    
    "alert_message" => "",
    "alert_type" => "",
    "debug" => "",
);

*/

//you get the following information for each file:
#echo $_FILES['image_upload']['name'] . "<br/>";
#echo $_FILES['image_upload']['size'] . "<br/>";
#echo $_FILES['image_upload']['type'] . "<br/>";
#echo $_FILES['image_upload']['tmp_name'] . "<br/>";
?>    
    
  </head>
  <body>
    <h1>57n Video Wall</h1>
   
    
    <?php
    if ( $videowall_globals['alert_message'] OR $videowall_globals['error_message'] ) {
        ?>
        <div class="alert alert-<?php echo $videowall_globals['alert_type'] ?>" role="alert">
          <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
          <?php echo $videowall_globals['alert_message']; ?>
          <?php echo $videowall_globals['error_message']; ?>
        </div>
        <?php
    }    
    ?>
    <hr/>
    <?php
    if ( $debug ) {
        ?>
        <pre>
Debug info
----------
<?php echo $videowall_globals['debug']; ?>
----------          
<?php print_r(error_get_last()); ?>
        </pre>
        <?php
    }    
    ?>    
    
    <form class="form-horizontal" action="index.php" method="post" enctype="multipart/form-data">
	    <input type="file" name="image_upload" size="25" />
        <input type="hidden" name="task" value="upload" />
	    <input class="btn btn-default" type="submit" name="submit" value="Upload" />
    </form>
    
    <hr/>
    
    <div class="thumbs">
    <?php
    $images = glob("image_data/resized/*.jpg");

    foreach($images as $image) {
        echo "<div style=\"background-image: url('" . $image . "');\" >";
        echo "<a href=\"" . $_SERVER['PHP_SELF'] . "?task=delete_one&image=" . basename($image) . "\" class=\"btn btn-default\" type=\"submit\"><span aria-hidden=\"true\" class=\"glyphicon glyphicon-trash\"></span> Trash</a>";
        echo "</div>";
    }
    ?>
    </div>
    
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

    <script src="bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
