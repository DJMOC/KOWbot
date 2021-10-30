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

from helper import *
import time

class Game:
	def __init__(self, window_box):
		#Game window position inside the screen in pixel
		#Top Left corner to bottom right corner
		#Visible game area inclusive
		#self.window_box             = (1, 34, 387, 724)
		self.window_box             = window_box
		#According to HQ level
		self.player_max_march       = 1
		#const defined based on window_box, this is the pxl coords of all elements
		self.event_button           = Screen.coordsToScreen(self.window_box, Coords.event_button       )
		self.event_return           = Screen.coordsToScreen(self.window_box, Coords.event_return       )
		self.event_menu_left        = Screen.coordsToScreen(self.window_box, Coords.event_menu_left    )
		self.event_menu_right       = Screen.coordsToScreen(self.window_box, Coords.event_menu_right   )
		self.event_list_top         = Screen.coordsToScreen(self.window_box, Coords.event_list_top     )
		self.event_list_bottom      = Screen.coordsToScreen(self.window_box, Coords.event_list_bottom  )
		self.event_list_box         = Screen.makeBox(self.event_list_top, self.event_list_bottom       )
		self.event_slide_top        = Screen.coordsToScreen(self.window_box, Coords.event_slide_top    )
		self.event_slide_bottom     = Screen.coordsToScreen(self.window_box, Coords.event_slide_bottom )
		self.event_popup_go         = Screen.coordsToScreen(self.window_box, Coords.event_popup_go     )
		self.event_popup_t_l        = Screen.coordsToScreen(self.window_box, Coords.event_popup_t_l    )
		self.event_popup_b_r        = Screen.coordsToScreen(self.window_box, Coords.event_popup_b_r    )
		self.event_popup_box        = Screen.makeBox(self.event_popup_t_l, self.event_popup_b_r        )
		self.go_button              = Screen.coordsToScreen(self.window_box, Coords.go_button          )
		self.go_top_left            = Screen.coordsToScreen(self.window_box, Coords.go_top_left        )
		self.go_bottom_right        = Screen.coordsToScreen(self.window_box, Coords.go_bottom_right    )
		self.go_box                 = Screen.makeBox(self.go_top_left, self.go_bottom_right            )
		self.scan_button            = Screen.coordsToScreen(self.window_box, Coords.scan_button        )
		self.targetA_button         = Screen.coordsToScreen(self.window_box, Coords.targetA_button     )
		self.targetB_button         = Screen.coordsToScreen(self.window_box, Coords.targetB_button     )
		self.targetC_button         = Screen.coordsToScreen(self.window_box, Coords.targetC_button     )
		self.targetD_button         = Screen.coordsToScreen(self.window_box, Coords.targetD_button     )
		self.targetE_button         = Screen.coordsToScreen(self.window_box, Coords.targetE_button     )
		self.targetF_button         = Screen.coordsToScreen(self.window_box, Coords.targetF_button     )
		self.rescue_button          = Screen.coordsToScreen(self.window_box, Coords.rescue_button      )
		self.deploy_button          = Screen.coordsToScreen(self.window_box, Coords.deploy_button      )
		self.deploy_top_left        = Screen.coordsToScreen(self.window_box, Coords.deploy_top_left    )
		self.deploy_bottom_right    = Screen.coordsToScreen(self.window_box, Coords.deploy_bottom_right)
		self.deploy_time_box        = Screen.makeBox(self.deploy_top_left, self.deploy_bottom_right    )
		#loop control
		self.falcon_event_available = False
		self.marchTime              = []
		self.availableTargets       = 6 * [False]
		self.scanColor              = Colors.scan_button_off
		self.targetColors           = 6 * [Colors.target_button_off]
		
		print('instance created (' + str(id(self)) + '), game location ' + str(self.window_box))
		print('  event_button        position is ' + str(self.event_button       ))
		print('  event_return        position is ' + str(self.event_return       ))
		print('  event_menu_left     position is ' + str(self.event_menu_left    ))
		print('  event_menu_right    position is ' + str(self.event_menu_right   ))
		print('  event_list_top      position is ' + str(self.event_list_top     ))
		print('  event_list_bottom   position is ' + str(self.event_list_bottom  ))
		print('  event_list_box      position is ' + str(self.event_list_box     ))
		print('  event_slide_top     position is ' + str(self.event_slide_top    ))
		print('  event_slide_bottom  position is ' + str(self.event_slide_bottom ))
		print('  event_popup_go      position is ' + str(self.event_popup_go     ))
		print('  event_popup_t_l     position is ' + str(self.event_popup_t_l    ))
		print('  event_popup_b_r     position is ' + str(self.event_popup_b_r    ))
		print('  event_popup_box     position is ' + str(self.event_popup_box    ))
		print('  go_button           position is ' + str(self.go_button          ))
		print('  go_top_left         position is ' + str(self.go_top_left        ))
		print('  go_bottom_right     position is ' + str(self.go_bottom_right    ))
		print('  go_box              position is ' + str(self.go_box             ))
		print('  scan_button         position is ' + str(self.scan_button        ))
		print('  targetA_button      position is ' + str(self.targetA_button     ))
		print('  targetB_button      position is ' + str(self.targetB_button     ))
		print('  targetC_button      position is ' + str(self.targetC_button     ))
		print('  targetD_button      position is ' + str(self.targetD_button     ))
		print('  targetE_button      position is ' + str(self.targetE_button     ))
		print('  targetF_button      position is ' + str(self.targetF_button     ))
		print('  rescue_button       position is ' + str(self.rescue_button      ))
		print('  deploy_button       position is ' + str(self.deploy_button      ))
		print('  deploy_top_left     position is ' + str(self.deploy_top_left    ))
		print('  deploy_bottom_right position is ' + str(self.deploy_bottom_right))
		print('  deploy_time_box     position is ' + str(self.deploy_time_box    ))
	
	def deployScout(self):
		#delay 1 sec after clicking target
		print('(' + str(id(self)) + ') About to click on Rescue Button')
		time.sleep(5)
		Mouse.clickTo(self.rescue_button)
		#let screen change before extracting march time
		time.sleep(5)
		print('(' + str(id(self)) + ') Extracting deployement time')
		timeList = Vision.extractStrings(self.deploy_time_box)
		print('  items found : ' + str(timeList))
		marchTime = Vision.findMarchTime(timeList)
		print('  time required : ' + str(marchTime))
		#back and forth + small delay added to current time to compare later
		self.marchTime.append(int(time.time()) + 2 * marchTime + 5)
		#deploy
		print('(' + str(id(self)) + ') clicking on Deploy')
		Mouse.clickTo(self.deploy_button)
		time.sleep(5)
		print('(' + str(id(self)) + ') clicking on Event Button')
		#return to event screen
		Mouse.clickTo(self.event_button)
		time.sleep(1)
	
	def initEvent(self):
		#goto event menu
		print('(' + str(id(self)) + ') init Event Requested')
		print('(' + str(id(self)) + ') clicking on Event button')
		Mouse.clickTo(self.event_button)
		time.sleep(1)
		#slide all the way to the left
		print('(' + str(id(self)) + ') swip menu to left')
		for i in range(5):#can be up to 4.2 scroll worth of events
			Mouse.moveTo(self.event_menu_left)
			time.sleep(.05)
			Mouse.dragTo(self.event_menu_right)
			time.sleep(1.5)
		#click event calendar
		print('(' + str(id(self)) + ') click on Event Calendar')
		Mouse.clickTo(self.event_menu_left)
		time.sleep(1)
		#slide all the way up
		print('(' + str(id(self)) + ') scroll up')
		for i in range(2):#can be up to 1.4 scroll worth of events
			Mouse.moveTo(self.event_slide_top)
			time.sleep(.05)
			Mouse.dragTo(self.event_slide_bottom)
			time.sleep(1.5)
		#reuse of function
		def _find():#try to find the word 'falcon'
			print('(' + str(id(self)) + ') Try to find the word "falcon"')
			wordList = Vision.extractStrings(self.event_list_box)
			print('  word found : ' + str(wordList))
			location = Vision.findString(wordList, 'falcon')
			print('  location : ' + str(location))
			if location != (0, 0): #found the event
				return (location[0] + self.event_list_box[0], location[1] + self.event_list_box[1])
			else:#scroll down
				print('  not found, scroll down a screen')
				Mouse.moveTo(self.event_slide_bottom)
				time.sleep(.05)
				Mouse.dragTo(self.event_slide_top)
				time.sleep(1.5)
				return (0, 0)
		falconLocation = _find()
		if falconLocation == (0, 0):#not found, retry
			falconLocation = _find()
		if falconLocation == (0, 0):#falcon not found
			self.falcon_event_available = False
			print('(' + str(id(self)) + ') could not find the event location, exit')
			return False
		print('  falcon found, checking if in time zone')
		im = Screen.grabPartialScreen(self.window_box)
		color = Vision.getColor(im, (self.event_slide_top[0], falconLocation[1]))
		#test all 5 colors
		avail_1 = Colors.isOn(color, Colors.background, Colors.falcon_event_1)
		print('  color 1 color is ' + str(color))
		print('  compare to off ' + str(Colors.background) + 'and on ' + str(Colors.falcon_event_1))
		print('  current button is ' + str(avail_1))
		avail_2 = Colors.isOn(color, Colors.background, Colors.falcon_event_2)
		print('  color 2 color is ' + str(color))
		print('  compare to off ' + str(Colors.background) + 'and on ' + str(Colors.falcon_event_2))
		print('  current button is ' + str(avail_2))
		avail_3 = Colors.isOn(color, Colors.background, Colors.falcon_event_3)
		print('  color 3 color is ' + str(color))
		print('  compare to off ' + str(Colors.background) + 'and on ' + str(Colors.falcon_event_3))
		print('  current button is ' + str(avail_3))
		avail_4= Colors.isOn(color, Colors.background, Colors.falcon_event_4)
		print('  color 4 color is ' + str(color))
		print('  compare to off ' + str(Colors.background) + 'and on ' + str(Colors.falcon_event_4))
		print('  current button is ' + str(avail_4))
		avail_5 = Colors.isOn(color, Colors.background, Colors.falcon_event_5)
		print('  color 5 color is ' + str(color))
		print('  compare to off ' + str(Colors.background) + 'and on ' + str(Colors.falcon_event_5))
		print('  current button is ' + str(avail_5))
		if avail_1 == False and avail_2 == False and avail_3 == False and avail_4 == False and avail_5 == False:
			#event not alligned with current day
			print('(' + str(id(self)) + ') event not in current day zone, exit')
			return False
		self.falcon_event_available = True
		self.marchTime              = []
		self.availableTargets       = 6 * [True]
		self.targetColors           = 6 * [Colors.target_button_off]
		self.marchTime.append(time.time())
		#goto falcon menu
		print('(' + str(id(self)) + ') clicking on falcon event')
		Mouse.clickTo(falconLocation)
		time.sleep(1)
		#popup with falcon go
		print('(' + str(id(self)) + ') trying to find if popup apperd')
		popupList     = Vision.extractStrings(self.event_popup_box)
		print('  words : ' + str(popupList))
		popupLocation = Vision.findString(popupList, 'g[o0]')
		print('  location : ' + str(popupLocation))
		if popupLocation != (0, 0):
			print('  clicking on "GO" popup')
			Mouse.clickTo(self.event_popup_go)
			time.sleep(1)
		#first time you can have a go button to click
		print('(' + str(id(self)) + ') trying to find if on "GO" page')
		goList     = Vision.extractStrings(self.go_box)
		print('  words : ' + str(goList))
		goLocation = Vision.findString(goList, 'g[o0]')
		print('  location : ' + str(goLocation))
		if goLocation != (0, 0):
			print('  clicking on "GO" button')
			Mouse.clickTo(self.go_button)
			time.sleep(1)
		#filling colors
		print('(' + str(id(self)) + ') scanning for falcon page status')
		im = Screen.grabPartialScreen(self.window_box)
		self.scanColor       = Vision.getColor(im, Vision.screenToImage(self.window_box, self.scan_button))
		self.targetColors[0] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetA_button))
		self.targetColors[1] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetB_button))
		self.targetColors[2] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetC_button))
		self.targetColors[3] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetD_button))
		self.targetColors[4] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetE_button))
		self.targetColors[5] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetF_button))
		print('  Scan is '     + str(Colors.isOn(self.scanColor, Colors.scan_button_off, Colors.scan_button_on)))
		print('  Target A is ' + str(Colors.isOn(self.targetColors[0], Colors.target_button_off, Colors.target_button_on)))
		print('  Target B is ' + str(Colors.isOn(self.targetColors[1], Colors.target_button_off, Colors.target_button_on)))
		print('  Target C is ' + str(Colors.isOn(self.targetColors[2], Colors.target_button_off, Colors.target_button_on)))
		print('  Target D is ' + str(Colors.isOn(self.targetColors[3], Colors.target_button_off, Colors.target_button_on)))
		print('  Target E is ' + str(Colors.isOn(self.targetColors[4], Colors.target_button_off, Colors.target_button_on)))
		print('  Target F is ' + str(Colors.isOn(self.targetColors[5], Colors.target_button_off, Colors.target_button_on)))
		return True
	
	def exitEvent(self):#exit to main screen and reset all status
		print('(' + str(id(self)) + ') Exit event called')
		print('  clicking on back button')
		print('  reset all variables')
		Mouse.clickTo(self.event_return)
		self.falcon_event_available = False
		self.falcon_as_fuel         = False
		self.marchTime              = []
		self.availableTargets       = 6 * [False]
		self.targetColors           = 6 * [Colors.target_button_off]
	
	def eventLoopOnce(self):
		print('(' + str(id(self)) + ') Event Loop called')
		if self.falcon_event_available == False:
			print('(' + str(id(self)) + ') Falcon Event not available')
			return False
		#place smallest first
		self.marchTime.sort()
		#wait scout plane ready
		print('(' + str(id(self)) + ') march size : ' + str(len(self.marchTime)) + ' vs ' + str(self.player_max_march))
		if len(self.marchTime) >= self.player_max_march:
			print('(' + str(id(self)) + ') ' + str(self.marchTime[0] - time.time()) + ' s left before march ready')
			if self.marchTime[0] <= time.time():
				print('  march done, remove it')
				self.marchTime.pop()
			else:
				print('  march not ready, return and wait again')
				#time.sleep(max(self.marchTime[0] - time.time(), 1))
				return True
		#check target A
		if self.availableTargets[0] == True:
			print('(' + str(id(self)) + ') Trying target A')
			print('  current color is ' + str(self.targetColors[0]))
			print('  compare to off ' + str(Colors.target_button_off) + 'and on ' + str(Colors.target_button_on))
			print('  current button is ' + str(Colors.isOn(self.targetColors[0], Colors.target_button_off, Colors.target_button_on)))
			self.availableTargets[0] = False
			if Colors.isOn(self.targetColors[0], Colors.target_button_off, Colors.target_button_on):
				print('(' + str(id(self)) + ') clicking on Target A button')
				Mouse.clickTo(self.targetA_button)
				self.deployScout()
		#check target B
		elif self.availableTargets[1] == True:
			print('(' + str(id(self)) + ') Trying target B')
			print('  current color is ' + str(self.targetColors[1]))
			print('  compare to off ' + str(Colors.target_button_off) + 'and on ' + str(Colors.target_button_on))
			print('  current button is ' + str(Colors.isOn(self.targetColors[1], Colors.target_button_off, Colors.target_button_on)))
			self.availableTargets[1] = False
			if Colors.isOn(self.targetColors[1], Colors.target_button_off, Colors.target_button_on):
				print('(' + str(id(self)) + ') clicking on Target B button')
				Mouse.clickTo(self.targetB_button)
				self.deployScout()
		#check target C
		elif self.availableTargets[2] == True:
			print('(' + str(id(self)) + ') Trying target C')
			print('  current color is ' + str(self.targetColors[2]))
			print('  compare to off ' + str(Colors.target_button_off) + 'and on ' + str(Colors.target_button_on))
			print('  current button is ' + str(Colors.isOn(self.targetColors[2], Colors.target_button_off, Colors.target_button_on)))
			self.availableTargets[2] = False
			if Colors.isOn(self.targetColors[2], Colors.target_button_off, Colors.target_button_on):
				print('(' + str(id(self)) + ') clicking on Target C button')
				Mouse.clickTo(self.targetC_button)
				self.deployScout()
		#check target D
		elif self.availableTargets[3] == True:
			print('(' + str(id(self)) + ') Trying target D')
			print('  current color is ' + str(self.targetColors[3]))
			print('  compare to off ' + str(Colors.target_button_off) + 'and on ' + str(Colors.target_button_on))
			print('  current button is ' + str(Colors.isOn(self.targetColors[3], Colors.target_button_off, Colors.target_button_on)))
			self.availableTargets[3] = False
			if Colors.isOn(self.targetColors[3], Colors.target_button_off, Colors.target_button_on):
				print('(' + str(id(self)) + ') clicking on Target D button')
				Mouse.clickTo(self.targetD_button)
				self.deployScout()
		#check target E
		elif self.availableTargets[4] == True:
			print('(' + str(id(self)) + ') Trying target E')
			print('  current color is ' + str(self.targetColors[4]))
			print('  compare to off ' + str(Colors.target_button_off) + 'and on ' + str(Colors.target_button_on))
			print('  current button is ' + str(Colors.isOn(self.targetColors[4], Colors.target_button_off, Colors.target_button_on)))
			self.availableTargets[4] = False
			if Colors.isOn(self.targetColors[4], Colors.target_button_off, Colors.target_button_on):
				print('(' + str(id(self)) + ') clicking on Target E button')
				Mouse.clickTo(self.targetE_button)
				self.deployScout()
		#check target F
		elif self.availableTargets[5] == True:
			print('(' + str(id(self)) + ') Trying target F')
			print('  current color is ' + str(self.targetColors[5]))
			print('  compare to off ' + str(Colors.target_button_off) + 'and on ' + str(Colors.target_button_on))
			print('  current button is ' + str(Colors.isOn(self.targetColors[5], Colors.target_button_off, Colors.target_button_on)))
			self.availableTargets[5] = False
			if Colors.isOn(self.targetColors[5], Colors.target_button_off, Colors.target_button_on):
				print('(' + str(id(self)) + ') clicking on Target F button')
				Mouse.clickTo(self.targetF_button)
				self.deployScout()
		elif Colors.isOn(self.scanColor, Colors.scan_button_off, Colors.scan_button_on):
			print('(' + str(id(self)) + ') No target available, clicking on scan')
			Mouse.clickTo(self.scan_button)
			loopCount = 0
			while True:
				time.sleep(1)
				print('(' + str(id(self)) + ') trying to get scan button status')
				im = Screen.grabPartialScreen(self.window_box)
				self.scanColor = Vision.getColor(im, Vision.screenToImage(self.window_box, self.scan_button))
				print('  current color is ' + str(self.scanColor))
				print('  compare to off ' + str(Colors.scan_button_off) + 'and on ' + str(Colors.scan_button_on))
				print('  current button is ' + str(Colors.isOn(self.scanColor, Colors.scan_button_off, Colors.scan_button_on)))
				if Colors.isOn(self.scanColor, Colors.scan_button_off, Colors.scan_button_on) == True:
					break
				loopCount += 1
				if loopCount > 15:
					print('(' + str(id(self)) + ') Timeout on scan button ready, end loop')
					return False
			self.targetColors[0] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetA_button))
			self.targetColors[1] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetB_button))
			self.targetColors[2] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetC_button))
			self.targetColors[3] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetD_button))
			self.targetColors[4] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetE_button))
			self.targetColors[5] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.targetF_button))
			print('  Target A is ' + str(Colors.isOn(self.targetColors[0], Colors.target_button_off, Colors.target_button_on)))
			print('  Target B is ' + str(Colors.isOn(self.targetColors[1], Colors.target_button_off, Colors.target_button_on)))
			print('  Target C is ' + str(Colors.isOn(self.targetColors[2], Colors.target_button_off, Colors.target_button_on)))
			print('  Target D is ' + str(Colors.isOn(self.targetColors[3], Colors.target_button_off, Colors.target_button_on)))
			print('  Target E is ' + str(Colors.isOn(self.targetColors[4], Colors.target_button_off, Colors.target_button_on)))
			print('  Target F is ' + str(Colors.isOn(self.targetColors[5], Colors.target_button_off, Colors.target_button_on)))
			self.availableTargets = 6 * [True]
		else:
			print('(' + str(id(self)) + ') Scan button was off, no more fuel')
			self.falcon_event_available = False
			return False
		print('(' + str(id(self)) + ') Loop done, return True')
		return True
