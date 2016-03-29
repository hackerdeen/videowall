<?php


# this is a general array for storing process info
$videowall_globals = array(
    "error_message" => "",
    "error" => FALSE,    
    "alert_message" => "",
    "alert_type" => "info",
    "debug" => "",
);




/*
function to process uploads
*/
function handle_upload() {

    global $videowall_globals;

    //if they DID upload a file...
    if($_FILES['image_upload']['name']){
        //if no errors...
        if(!$_FILES['image_upload']['error']){
            //now is the time to modify the future file name and validate the file
            $new_file_name = strtolower($_FILES['image_upload']['tmp_name']); //rename file
            if($_FILES['image_upload']['size'] > (102400000))	{
                #$valid_file = false;
                #$message = 'Oops!  Your file\'s size is to large.';
                $videowall_globals["error"] = TRUE;
                $videowall_globals["alert_message"] .= "Oops! Your file is size is to large.";
                $videowall_globals["alert_type"] = "danger";
                
            } else {
                $image_fn = 'image_data/raw/'.$_FILES['image_upload']['name'];
                
                //move it to where we want it to be
                move_uploaded_file($_FILES['image_upload']['tmp_name'], $image_fn);
                #$message = 'Congratulations!  Your file was accepted.';
                
                convert_to_size($image_fn);
                if (!$videowall_globals["error"]) {
                    $videowall_globals["alert_message"] .= "Resized ok";
                    $videowall_globals["alert_type"] = "success";                      
                    #$return_array["filename"] = $convert_to_size_return_array["filename"]; 
                } else {
                    $videowall_globals["error"] = TRUE;
                    $videowall_globals["alert_message"] .= "Oops! Your file is size is to large.";
                    $videowall_globals["alert_type"] = "danger";  
                }			
            }
        } else {
            //set that to be the returned message
            #$message = 'Ooops!  Your upload triggered the following error:  '.$_FILES['image_upload']['error'];
            $videowall_globals["error"] = TRUE;
            $videowall_globals["alert_message"] .= "Ooops!  Your upload triggered the following error: " . $_FILES['image_upload']['error'];
            $videowall_globals["alert_type"] = "danger";              
        }
    }

    return;    
    
}    

/*
function to resize and crop images to the right size
*/
function convert_to_size ($image_fn) {
    
    global $videowall_globals;
    
    $output_width   = 2400;
    $output_height  = 1800;
    $image_fn_file  = basename($image_fn);

    $target_output_width   = $output_width;
    $target_output_height  = $output_height;    
    
    $output_x       = 0;
    $output_y       = 0;
    $input_x        = 0; 
    $input_y        = 0; 
    
    list($input_width, $input_height) = getimagesize($image_fn);
    $input_ratio = $input_width / $input_height;
    
    $output_ratio = $output_width / $output_height;    
    
    $videowall_globals["debug"] .= "output_width: " . $output_width . "<br/>\n";
    $videowall_globals["debug"] .= "output_height: " . $output_height . "<br/>\n";
    $videowall_globals["debug"] .= "output_ratio: " . $output_ratio . "<br/>\n";
    
    $videowall_globals["debug"] .= "input_width: " . $input_width . "<br/>\n";
    $videowall_globals["debug"] .= "input_height: " . $input_height . "<br/>\n";
    $videowall_globals["debug"] .= "input_ratio: " . $input_ratio . "<br/>\n";
    
    
    # create an image resourse from the file
    $input_image_res = imagecreatefromjpeg($image_fn);
    
    if ($input_ratio > 1) {
        # ratio is more than 1, so it's a wide image
        $videowall_globals["debug"] .= "Wide image<br/>\n";
    } else {
        # ratio is less than 1, so it's a tall image
        $videowall_globals["debug"] .= "Tall image.<br/>\n";
    }    
    
    if ($input_ratio > $output_ratio) {
        # ratio is...
        $videowall_globals["debug"] .= "Input is wider than the output<br/>\n";

        $videowall_globals["debug"] .= "Resize it making the height " . $output_height . "<br/>\n";
        $output_width = $output_height * $input_ratio;
        $videowall_globals["debug"] .= "output_width: " . $output_width . "<br/>\n";        

    } else {
        # ratio is...
        $videowall_globals["debug"] .= "Input is taller than the output<br/>\n";

        $videowall_globals["debug"] .= "Resize it making the width " . $output_width . "<br/>\n";
        $output_height = $output_width / $input_ratio;
        $videowall_globals["debug"] .= "output_height: " . $output_height . "<br/>\n";      
                
    }     

    # create an image resourse for the output file
    $output_image_res = imagecreatetruecolor($output_width, $output_height);   
    
    imagecopyresampled($output_image_res, $input_image_res, 0, 0, 0, 0, $output_width, $output_height, $input_width, $input_height);    
    
    $to_crop_array = array('x'=>0, 'y'=> 0, 'width'=>$target_output_width, 'height'=>$target_output_height);
    
    # crop the image down
    if ($output_width > $target_output_width) {
        $videowall_globals["debug"] .= "To wide.<br/>\n";
        $width_overflow = $output_width - $target_output_width;
        $to_crop_array['x'] = $width_overflow / 2;
        $output_image_res = imagecrop($output_image_res, $to_crop_array );
    } elseif ($output_height > $target_output_height) {
        $videowall_globals["debug"] .= "To tall.<br/>\n";    
        $height_overflow = $output_height - $target_output_height;
        $to_crop_array['y'] = $height_overflow / 2;        
        $output_image_res = imagecrop($output_image_res, $to_crop_array );
    } else {
        $videowall_globals["debug"] .= "Width and height are fine, no cropping required.<br/>\n";   
    }    

    
    $videowall_globals["debug"] .= "input_x: " . $input_x . "\n";
    $videowall_globals["debug"] .= "input_y: " . $input_y . "\n";
    $videowall_globals["debug"] .= "output_width: " . $output_width . "\n";
    $videowall_globals["debug"] .= "output_height: " . $output_height . "\n";
    $videowall_globals["debug"] .= "input_width: " . $input_width . "\n";
    $videowall_globals["debug"] .= "input_height: " . $input_height . "\n";
   
    $output_image_filename = "image_data/resized/" . $image_fn_file;
    imagejpeg($output_image_res, $output_image_filename);    

    $videowall_globals["alert_message"] .= "Resized ok";
    $videowall_globals["alert_type"] = "success";       
    
    return;

}




/*
delete a single image
*/
function delete_one() {
    
    global $videowall_globals;
    
    $file_to_delete = $_GET["image"];
    
    unlink("image_data/resized/" . $file_to_delete);
    unlink("image_data/raw/" . $file_to_delete);
    
    $videowall_globals["alert_message"] .= "Deleted " . $file_to_delete;
    $videowall_globals["alert_type"] = "success";     
    
    return;

}


?>
