###################################################################
# Copyright (c) 2021 Ludicrous Speed                              #
#                                                                 #
# Permission is hereby granted, free of charge, to any person     #
# obtaining a copy of this software and associated documentation  #
# files (the "Software"), to deal in the Software without         #
# restriction, including without limitation the rights to use,    #
# copy, modify, merge, publish, distribute, sublicense, and/or    #
# sell copies of the Software, and to permit persons to whom the  #
# Software is furnished to do so, subject to the following        #
# conditions:                                                     #
#                                                                 #
# The above copyright notice and this permission notice shall be  #
# included in all copies or substantial portions of the Software. #
#                                                                 #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, #
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES #
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND        #
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT     #
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,    #
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING    #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR   #
# OTHER DEALINGS IN THE SOFTWARE.                                 #
###################################################################

from instance import Game
import keyboard, time, os
from helper import Mouse, Screen

autoFalcon  = []

def on_shortcutKill():
	print('Kill Sequence Initiated')
	os._exit(0)

def initKillSequence(ks):
	print('To kill the app use"' + ks + '" key sequence')
	keyboard.add_hotkey(ks, on_shortcutKill)

def initFalcon(index):
	if index < 0 or index >= len(autoFalcon):
		return False
	return autoFalcon[index].initEvent()

def exitFalcon(index):
	if index < 0 or index >= len(autoFalcon):
		return
	autoFalcon[index].exitEvent()

def loopFalcon(index):
	if index < 0 or index >= len(autoFalcon):
		return False
	return autoFalcon[index].eventLoopOnce()

def initAutoFalcon():
	#autoFalcon.append(Game((1, 34, 387, 724)))
	print('Make sure you can read the text in the game!!!')
	lvl = int(input('Enter your HQ level : '))
	print('Place the mouse on the top left corner of the window, ')
	print('then press "Enter" or press "space to enter manualy')
	while keyboard.is_pressed('enter') == False and keyboard.is_pressed('space') == False:
		time.sleep(.05)
		print(str(Mouse.getMousePosition()), end='\r')
	if keyboard.is_pressed('space') == True:
		top    = int(input('Top of window : '))
		left   = int(input('Left of window : '))
		bottom = int(input('Bottom of window : '))
		right  = int(input('Right of window : '))
		box = (top, left, bottom, right)
	else:
		top_left = Mouse.getMousePosition()
		while keyboard.is_pressed('enter') == True:
			time.sleep(.1)
		print('Place the mouse on the bottom right corner of the window, ')
		print('then press "Enter"')
		while keyboard.is_pressed('enter') == False:
			time.sleep(.05)
			print(str(Mouse.getMousePosition()), end='\r')
		bottom_right = Mouse.getMousePosition()
		box = Screen.makeBox(top_left, bottom_right)
	print('The game HQ is ' + str(lvl) + ' at location : ' + str(box))
	print('Accept (y), Exit (n), Retry (r)?')
	while keyboard.is_pressed('y') == False and keyboard.is_pressed('n') == False and keyboard.is_pressed('r') == False:
		time.sleep(.05)
	if keyboard.is_pressed('y'):
		autoFalcon.append(Game(lvl, box))
	elif keyboard.is_pressed('n'):
		on_shortcutKill()
	elif keyboard.is_pressed('r'):
		print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
		initAutoFalcon()

def main():
	initKillSequence('ctrl+alt+esc')
	initAutoFalcon()
	
	if initFalcon(0) == False:
		#print('init done with no event available')
		exitFalcon(0)
	else:
		running = True
		#print('init done with event available')
		while running == True:
			time.sleep(5)
			running = loopFalcon(0)
			#print('loop done result : ' + str(running))

		#print('event done, leaving')
		exitFalcon(0)

if __name__ == '__main__':
	main()
