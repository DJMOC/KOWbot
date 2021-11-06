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

#Generic import
from helper import *
from globals import *
import time, keyboard, colorama
from colorama import Fore, Back, Style

#Import all independent functions
from eventFalcon import EventFalcon

def findWindow():
	#find all instances
	lst = AppWindow.getGameWindow('BlueStacks')
	if lst == None:
		#no instances running
		print('No instance found, exit')
		time.sleep(2)
		return None
	#display
	i = 0
	while keyboard.is_pressed('enter') == False:
		s = ' '.join(((Fore.BLACK + Back.WHITE + str(x._hWnd) + Style.RESET_ALL) if lst.index(x) == i else str(x._hWnd)) for x in lst)
		print(s, end = '\r')
		lst[i].minimize()
		lst[i].restore()
		while keyboard.is_pressed('enter') == False and keyboard.is_pressed('left')  == False and keyboard.is_pressed('right') == False:
			time.sleep(.04)
		if keyboard.is_pressed('left') == True:
			i = (i - 1) % len(lst)
		if keyboard.is_pressed('right') == True:
			i = (i + 1) % len(lst)
		while keyboard.is_pressed('left') or keyboard.is_pressed('right'):
			time.sleep(.04)
	return lst[i]

class Game:
	def __init__(self):
		print(Fore.MAGENTA + 'Please select a window')
		win = findWindow()
		if win == None:
			self.initialized = False
			return
		print(Fore.MAGENTA + 'Window dimentions : ' + Style.RESET_ALL + 
				str(win.size[0]) + ', ' + str(win.size[1]))
		scrn_size = Screen.resolution()
		if win.size < (425, 730) and scrn_size >= (425, 730):
			print(Fore.YELLOW + 'Window too small, resizing')
			win.resizeTo(425, 730)
		elif win.size < (425, 703):
			print(Fore.RED + 'Screen resolution too small, exit')
			self.initialized = False
			time.sleep(2)
			return
		print(Fore.MAGENTA + 'Finding optiomal play area')
		im = AppWindow.grabAppArea(win.box)
		ct = AppWindow.getCornerText(im, ('vip', 'camp'))
		if len(ct) != 2:
			print(Fore.RED + 'Vision error, exit')
			self.initialized = False
			time.sleep(2)
			return
		window_box = AppWindow.extrapolateGameArea(ct, (Coords.static_window_anchor_vip, Coords.static_window_anchor_camp))
		hq_level = 0
		while hq_level == 0:
			hq_level = input(Fore.MAGENTA + 'Enter the HQ level (1-25): ')
			try:
				hq_level = int(hq_level)
				if hq_level < 1 or hq_level > 25:
					print(Fore.YELLOW + 'The value is invalide')
					hq_level = 0
			except:
				print(Fore.YELLOW + 'The value is not a number')
				hq_level = 0
		#Game window position inside the screen in pixel
		self.window_box             = window_box
		#According to HQ level
		if hq_level < 5:
			self.player_max_march   = 1
		elif hq_level < 11:
			self.player_max_march   = 2
		else:
			self.player_max_march   = 3
		#Events and tasks
		self.event_falcon = EventFalcon(window_box, self.player_max_march)
		#done
		self.initialized = True
	
	def init(self):
		if self.initialized == False:
			return False
		#for now in here, but when eventScanner module is complete, will move to loop
		if self.event_falcon.initEvent() == False:
			return False
		return True
	
	def exit(self):
		if self.initialized == False:
			return
		#for now in here, but when eventScanner module is complete, will move to loop
		self.event_falcon.exitEvent()
	
	def loop(self):
		if self.initialized == False:
			return False
		#for now only run falcon and exit, when event Scanner module is complete, 
		#will add more logic
		if self.event_falcon.eventLoopOnce() == False:
			return False
		return True
