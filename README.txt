This document explains how to get started with this program

Step 1:
Open the command terminal using cmd

Step 2:
cd into the server folder
for example
"cd \Users\COEN366\project\server"

Step 3:
run the python script titled ser.py
"python ser.py"

Step 4:
Open a second terminal and cd into the client folder

Step 5:
run the script titled cli.py
"python cli.py"

Step 6:
Try the different commands
help			-Returns the available commands
put filename		-Copies filename from the client folder to the server folder
get filename		-Copies filename from the server folder to the client folder
change oldname newname	-Changes the file "oldname" to "newname" in the server folder
bye			-Exits


An example of commands could be:

help
put testimage.jpg
change testimage.jpg changedimage.jpg
get changedimage.jpg
bye