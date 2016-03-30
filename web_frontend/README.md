# Video Wall Front-end
This is a web front end and processing engine for the 57n video wall

3bit RGB

3x3 screens @ 800x600



## Directories 
- /image_data/raw - the uploaded image un modified
- /image_data/resized - the resized image
- /image_data/datafile - the data file, a text file or rgb values, comma delineated per x pixel, line delineated per y pixel



## UI
- Upload button
- Thumbnails of previous uploads
- Delete button for each image
- Delete all button

## Send to wall logic
- Send newest image
- Rotate through other images. 30 secs each

## To-do / needed...
- UI for uploading images
- Sample to size
- Render image effects to improve output
- Create data file
- Create image file, preview of data

## Further ideas
- Cam to source
- Google image search source
- Text to image
- Twitter to image
- Video source

## Background (Rob's email)
Some of us had discussed making a video wall thing for the Edinburgh
mini maker faire. This should be an FPGA driving (up to) 9 VGA displays
and being fed images via USB.

The faire is coming up fast (less than a month away!) and I am nothing
like as far along with making this work as I would like. To avoid
failing miserably to get anything working (again) I could do with some
help.

Tom has already volunteered to do the physical construction of the
shield thing to connect VGA ports to pins.

The rest of the work splits up into writing the firmware for the FPGA,
and the software to feed it images. If I could get someone else to take
care of the SW side it would help the chances of this working (and my
sanity) greatly. Also if anyone want's to pick up the FPGA side I am
more than happy to do nothing :)

My plan for the software was to have something read in image files,
scale them to the right resolution (I think 800x600, remind me to check
before you start coding against that), reduce the colour to 3 bits (one
each for red, green and blue) and then send that down to the FPGA (if I
do get a volunteer, I'll document how that happens). I had vague plans
for a web interface to that (and did think about making it publicly
accessible - it would probably be best to have a moderation feature to
approve things before they go on the screens if we do implement that). I
was thinking to write it in python as I know the PIL can handle the
image parts quite easily, but if someone has a different preference I
don't particularly care.

Can I rope anyone in to help with this?

Robert

## Random dev notes
          
/var/www/html/videowall.git/trunk/web_frontend

\\ASUS-12\code\videowall.git\trunk\web_frontend

http://localhost/videowall.git/trunk/web_frontend/

http://asus-12/code/videowall.git/trunk/web_frontend/
