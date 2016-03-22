<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>57n Video Wall</title>

    <!-- Bootstrap -->
    <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    
<?php 
# Control
require_once("helper.php");




$message = "";   
//if they DID upload a file...
if($_FILES['image_upload']['name']){
	//if no errors...
	if(!$_FILES['image_upload']['error']){
		//now is the time to modify the future file name and validate the file
		$new_file_name = strtolower($_FILES['image_upload']['tmp_name']); //rename file
		if($_FILES['image_upload']['size'] > (1024000))	{
			$valid_file = false;
			$message = 'Oops!  Your file\'s size is to large.';
		} else {
		    $valid_file = true;
		}
		//if the file has passed the test
		if($valid_file)	{
		    $image_fn = 'image_data/raw/'.$_FILES['image_upload']['name'];
		    
			//move it to where we want it to be
			move_uploaded_file($_FILES['image_upload']['tmp_name'], $image_fn);
			#$message = 'Congratulations!  Your file was accepted.';
			
            $file = convert_to_size ($image_fn);
            if ($file) {
                
            } else {
                $message = 'Conversion error';
            }			
			
		}
	}else{
		//set that to be the returned message
		$message = 'Ooops!  Your upload triggered the following error:  '.$_FILES['image_upload']['error'];
	}
}




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
    if ($message) {
        ?>
        <div class="alert alert-info" role="alert">
          <span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span>
          <?php echo $message; ?>
        </div>
        <?php
    }    
    ?>
    <form class="form-horizontal" action="index.php" method="post" enctype="multipart/form-data">
	    <input type="file" name="image_upload" size="25" />
	    <input class="btn btn-default" type="submit" name="submit" value="Upload" />
    </form>


    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>

    <script src="bootstrap/js/bootstrap.min.js"></script>
  </body>
</html>
