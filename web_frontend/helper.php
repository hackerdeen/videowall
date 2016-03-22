<?php




function convert_to_size ($image_fn) {
    $newwidth   = 2400;
    $newheight  = 1800;
    $tmp        = imagecreatetruecolor($newwidth, $newheight);
    
    $image_file = imagecreatefromjpeg($image_fn);
    
    list($width,$height)=getimagesize($image_fn);

    $widthProportion  = $width / $newwidth;
    $heightProportion = $height / $newheight;

    if ($widthProportion > $heightProportion) {
        // width proportion is greater than height proportion
        // figure out adjustment we need to make to width
        $widthAdjustment = ($width * ($widthProportion - $heightProportion));

        // Shrink width to proper proportion
        $width = $width - $widthAdjustment;

        $x = 0; // No adjusting height position
        $y = $widthAdjustment / 2; // Center the adjustment
    } else {
        // height proportion is greater than width proportion
        // figure out adjustment we need to make to width
        $heightAdjustment = ($height * ($heightProportion - $widthProportion));

        // Shrink height to proper proportion
        $height = $height - $heightAdjustment;

        $x = $heightAdjustment / 2; // Center the ajustment
        $y = 0; // No adjusting width position
    }

    imagecopyresampled($tmp, $image_file, 0, 0, $x, $y, $newwidth, $newheight, $width, $height);

    $new_image_filename = "image_data/resized/" . $image_fn . "-" . $newwidth . "x" . $newheight . ".jpg";
    imagejpeg($tmp, $new_image_filename);
    
    return $new_image_filename;

}



?>
