PLEASE READ THIS DOCUMENT BEFORE USING THE CODE.

Needed modules: 
There are a few modules that are not included with Python but are however necessary to run the application we built. It is assumed that pip is used for installing modules and the commands given also use pip for installing modules. 

The first of these modules is the mysql connector, this module can be installed with:
pip3 install mysql-connector-python 

Another module that is used within the code is Pillow, be sure to follow the following command to install Pillow and not the outdated version PIL: 
pip3 install Pillow 

Another module which needs to be installed is pygame, pygame is used for playing music in the GUI. to install pygame, use the following command:
pip3 install pygame

Note:
Sometimes it might look like the game is hanging while it actually isn't, this is due to the use of the external database which is quite slow.

Starting the game:
To start the game, execute the GUI.pyw file. This file will automatically invoke the necessary functions from other files. 