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

$time_start = microtime(true); 

# Control
require_once("helper.php");

# set to true or false to switch on a big bunch of debug stuff
$debug = FALSE;


if ( isset($_POST["task"])) {
    if ( $_POST["task"] == "upload" )  {
        handle_upload();
        
        #if ( !$videowall_globals['error'] ) {
        #
        #}
    }    
} 
if ( isset($_GET["task"])) {
    if ( $_GET["task"] == "delete_one" )  {
        delete_one();
    }    
} 

$time_end = microtime(true);
$videowall_globals['debug'] .= "Time running " . ($time_end - $time_start) . "\n";
?>    
    
    </head>
    <body>
        <div class="container">
            <img src="57_North_logo.png" alt="Logo" class="logo" />
            <h1>57n Video Wall</h1>

            <div id="wait_box" style="display: none">
                <div class="alert alert-info" role="alert">
                    <h4>
                        <span class="glyphicon glyphicon-time"> </span> Please Wait, just processing your image, this might take a minute or two.
                    </h4>
                    <div class="progress">
                        <div class="progress-bar progress-bar-info
                        progress-bar-striped active"
                        style="width: 100%">
                        </div>
                    </div>
                </div>
            </div>



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
            debug
            <?php echo $videowall_globals['debug']; ?>
            ----------    
            error_get_last      
            <?php print_r(error_get_last()); ?>
            ----------
            getrusage
            <?php print_r(getrusage()); ?>
                </pre>
                <?php
            }    
            ?>    

            <form class="form-horizontal" action="index.php" method="post" enctype="multipart/form-data">
                <input type="file" name="image_upload" size="25" />
                <input type="hidden" name="task" value="upload" />
                <input class="btn btn-default" type="submit" name="submit" value="Upload" onclick="$('#wait_box').css('display','block');"/>
            </form>

            <hr/>


            <h4>Previosly Uploaded Images</h4>
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
        </div> 
        <script src="bootstrap/js/jquery.min.js"></script>
        <script src="bootstrap/js/bootstrap.min.js"></script>
    </body>
</html>
