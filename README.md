### KOWbot ###

KOWbot is currently in beta testing. Please report problems when found!
Working : 
	-scaling to any window size
	-automaticaly find it Operation Falcon event is available
	-automaticaly run Operation Falcon until there is no Fuel
	-send the maximum number of scouts according to your HQ
	-return to Home/World screen when done

# Install #
* Python 3.7              (tested with 3.7.4)
* pip install easyocr     (tested with 1.4.1)
* pip install keyboard    (tested with 0.13.5)
* pip install numpy       (tested with 1.21.3)
* pip install Pillow      (tested with 8.2.0)
* pip install pywin32     (tested with 302)
* pip install torch       (tested with 1.10.0)
* pip install torchvision (tested with 0.11.1)

# How to #

When everything is installed, clone the project to a folder in your
computer and open "app.py". You will be guided thru the setup 
required for the bot. To work correctly your window need to be large
enough to clearly read the text displayed. You will be asked to 
enter the HQ level of this instance, then you need to specify where
in the desktop the game is. You have 2 choices, 1 you move the
mouse over the top left corner, press enter, then move the mouse
over the bottom right corner and press enter. Choice 2 is available
if you press space, you can manualy enter the window location. You
need to enter the position in this order : top edge, left edge, 
bottom edge and right edge. After the window is set you will be 
asked if everything is good. You have 3 options : press Y to start
the bot, press N to close the bot, press R to restart the setup
process. Because the bot take controle over the mouse, at any time
you can press ctrl+alt+esc to kill the bot.