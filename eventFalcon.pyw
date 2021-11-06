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
from globals import *

class EventFalcon:
	def __init__(self, window_box, max_march):
		self.window_box       = window_box
		self.player_max_march = max_march
		#const defined based on window_box, this is the pxl coords of all elements
		self.event_button                = Screen.coordsToScreen(self.window_box, Coords.event_button                 )
		self.event_return                = Screen.coordsToScreen(self.window_box, Coords.event_return                 )
		self.event_menu_left             = Screen.coordsToScreen(self.window_box, Coords.event_menu_left              )
		self.event_menu_right            = Screen.coordsToScreen(self.window_box, Coords.event_menu_right             )
		self.event_calendar_topleft      = Screen.coordsToScreen(self.window_box, Coords.event_calendar_topleft       )
		self.event_calendar_bottomright  = Screen.coordsToScreen(self.window_box, Coords.event_calendar_bottomright   )
		self.event_list_box              = Screen.makeBox(self.event_calendar_topleft, self.event_calendar_bottomright)
		self.event_calandar_slide_top    = Screen.coordsToScreen(self.window_box, Coords.event_calandar_slide_top     )
		self.event_calandar_slide_bottom = Screen.coordsToScreen(self.window_box, Coords.event_calandar_slide_bottom  )
		self.event_popup_go              = Screen.coordsToScreen(self.window_box, Coords.event_popup_go               )
		self.event_popup_topleft         = Screen.coordsToScreen(self.window_box, Coords.event_popup_topleft          )
		self.event_popup_bottomright     = Screen.coordsToScreen(self.window_box, Coords.event_popup_bottomright      )
		self.event_popup_box             = Screen.makeBox(self.event_popup_topleft, self.event_popup_bottomright      )
		self.falcon_go_button            = Screen.coordsToScreen(self.window_box, Coords.falcon_go_button             )
		self.falcon_go_topleft           = Screen.coordsToScreen(self.window_box, Coords.falcon_go_topleft            )
		self.falcon_go_bottomright       = Screen.coordsToScreen(self.window_box, Coords.falcon_go_bottomright        )
		self.falcon_go_box               = Screen.makeBox(self.falcon_go_topleft, self.falcon_go_bottomright          )
		self.falcon_scan_button          = Screen.coordsToScreen(self.window_box, Coords.falcon_scan_button           )
		self.falcon_targetA_button       = Screen.coordsToScreen(self.window_box, Coords.falcon_targetA_button        )
		self.falcon_targetB_button       = Screen.coordsToScreen(self.window_box, Coords.falcon_targetB_button        )
		self.falcon_targetC_button       = Screen.coordsToScreen(self.window_box, Coords.falcon_targetC_button        )
		self.falcon_targetD_button       = Screen.coordsToScreen(self.window_box, Coords.falcon_targetD_button        )
		self.falcon_targetE_button       = Screen.coordsToScreen(self.window_box, Coords.falcon_targetE_button        )
		self.falcon_targetF_button       = Screen.coordsToScreen(self.window_box, Coords.falcon_targetF_button        )
		self.falcon_rescue_button        = Screen.coordsToScreen(self.window_box, Coords.falcon_rescue_button         )
		self.falcon_deploy_button        = Screen.coordsToScreen(self.window_box, Coords.falcon_deploy_button         )
		self.falcon_deploy_topleft       = Screen.coordsToScreen(self.window_box, Coords.falcon_deploy_topleft        )
		self.falcon_deploy_bottomright   = Screen.coordsToScreen(self.window_box, Coords.falcon_deploy_bottomright    )
		self.falcon_deploy_time_box      = Screen.makeBox(self.falcon_deploy_topleft, self.falcon_deploy_bottomright  )
		#loop control
		self.falcon_event_available = False
		self.march_time             = []
		self.scan_color             = Colors.falcon_scan_button_off
		self.target_colors          = 6 * [Colors.falcon_target_button_off]
		
	def deployScout(self, func):
		#delay 1 sec after clicking target
		time.sleep(5)
		Mouse.clickTo(self.falcon_rescue_button)
		#let screen change before extracting march time
		time.sleep(5)
		timeList = Vision.extractStrings(self.falcon_deploy_time_box)
		march_time = Vision.findMarchTime(timeList)
		#back and forth + small delay added to current time to compare later
		self.march_time.append(int(time.time()) + 2 * march_time + 5)
		#deploy
		Mouse.clickTo(self.falcon_deploy_button)
		time.sleep(5)
		#if external function, execute will in wolrd view
		# usefull for things like help request
		if callable(func):
			func()
		#return to event screen
		Mouse.clickTo(self.event_button)
		time.sleep(1)
	
	def getTargets(self):
		self.target_colors[0] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_targetA_button))
		self.target_colors[1] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_targetB_button))
		self.target_colors[2] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_targetC_button))
		self.target_colors[3] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_targetD_button))
		self.target_colors[4] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_targetE_button))
		self.target_colors[5] = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_targetF_button))
	
	def initEvent(self):
		#goto event menu
		Mouse.clickTo(self.event_button)
		time.sleep(1)
		#slide all the way to the left
		for i in range(5):#can be up to 4.2 scroll worth of events
			Mouse.moveTo(self.event_menu_left)
			time.sleep(.05)
			Mouse.dragTo(self.event_menu_right)
			time.sleep(1.5)
		#click event calendar
		Mouse.clickTo(self.event_menu_left)
		time.sleep(1)
		#slide all the way up
		for i in range(2):#can be up to 1.4 scroll worth of events
			Mouse.moveTo(self.event_calandar_slide_top)
			time.sleep(.05)
			Mouse.dragTo(self.event_calandar_slide_bottom)
			time.sleep(1.5)
		#reuse of function
		def _find():#try to find the word 'falcon'
			wordList = Vision.extractStrings(self.event_list_box)
			location = Vision.findString(wordList, 'falcon')
			if location != (0, 0): #found the event
				return (location[0] + self.event_list_box[0], location[1] + self.event_list_box[1])
			else:#scroll down
				Mouse.moveTo(self.event_calandar_slide_bottom)
				time.sleep(.05)
				Mouse.dragTo(self.event_calandar_slide_top)
				time.sleep(1.5)
				return (0, 0)
		falconLocation = _find()
		if falconLocation == (0, 0):#not found, retry
			falconLocation = _find()
		if falconLocation == (0, 0):#falcon not found
			self.falcon_event_available = False
			return False
		im = Screen.grabPartialScreen(self.window_box)
		color = Vision.getColor(im, (self.event_calandar_slide_top[0], falconLocation[1]))
		#test all 5 colors
		avail_1 = Colors.isOn(color, Colors.background, Colors.falcon_event_1)
		avail_2 = Colors.isOn(color, Colors.background, Colors.falcon_event_2)
		avail_3 = Colors.isOn(color, Colors.background, Colors.falcon_event_3)
		avail_4 = Colors.isOn(color, Colors.background, Colors.falcon_event_4)
		avail_5 = Colors.isOn(color, Colors.background, Colors.falcon_event_5)
		if avail_1 == False and avail_2 == False and avail_3 == False and avail_4 == False and avail_5 == False:
			#event not alligned with current day
			return False
		#goto falcon menu
		Mouse.clickTo(falconLocation)
		time.sleep(1)
		#popup with falcon go
		popupLocation = Vision.findString(Vision.extractStrings(self.event_popup_box), 'g[o0]')
		if popupLocation != (0, 0):
			Mouse.clickTo(self.event_popup_go)
			time.sleep(1)
		#first time you can have a go button to click
		goLocation = Vision.findString(Vision.extractStrings(self.falcon_go_box), 'g[o0]')
		if goLocation != (0, 0):
			Mouse.clickTo(self.falcon_go_button)
			time.sleep(1)
		#filling colors
		self.falcon_event_available = True
		self.march_time              = []
		im = Screen.grabPartialScreen(self.window_box)
		self.scan_color = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_scan_button))
		self.getTargets()
		return True

	def exitEvent(self):#exit to main screen and reset all status
		Mouse.clickTo(self.event_return)
		self.falcon_event_available = False
		self.falcon_as_fuel         = False
		self.march_time              = []
		self.target_colors           = 6 * [Colors.falcon_target_button_off]
	
	def eventLoopOnce(self, func = None):
		if self.falcon_event_available == False:
			return False
		#place smallest first
		self.march_time.sort()
		#wait scout plane ready
		if len(self.march_time) >= self.player_max_march:
			if self.march_time[0] <= time.time():
				self.march_time.pop()
			else:
				#time.sleep(max(self.march_time[0] - time.time(), 1))
				return True
		#check target A
		if Colors.isOn(self.target_colors[0], Colors.falcon_target_button_off, Colors.falcon_target_button_on):
			Mouse.clickTo(self.falcon_targetA_button)
			self.deployScout(func)
		#check target B
		elif Colors.isOn(self.target_colors[1], Colors.falcon_target_button_off, Colors.falcon_target_button_on):
			Mouse.clickTo(self.falcon_targetB_button)
			self.deployScout(func)
		#check target C
		elif Colors.isOn(self.target_colors[2], Colors.falcon_target_button_off, Colors.falcon_target_button_on):
			Mouse.clickTo(self.falcon_targetC_button)
			self.deployScout(func)
		#check target D
		elif Colors.isOn(self.target_colors[3], Colors.falcon_target_button_off, Colors.falcon_target_button_on):
			Mouse.clickTo(self.falcon_targetD_button)
			self.deployScout(func)
		#check target E
		elif Colors.isOn(self.target_colors[4], Colors.falcon_target_button_off, Colors.falcon_target_button_on):
			Mouse.clickTo(self.falcon_targetE_button)
			self.deployScout(func)
		#check target F
		elif Colors.isOn(self.target_colors[5], Colors.falcon_target_button_off, Colors.falcon_target_button_on):
			Mouse.clickTo(self.falcon_targetF_button)
			self.deployScout(func)
		#check scan available
		elif Colors.isOn(self.scan_color, Colors.falcon_scan_button_off, Colors.falcon_scan_button_on):
			Mouse.clickTo(self.falcon_scan_button)
			loopCount = 0
			#wait scanning is done
			while True:
				time.sleep(1)
				im = Screen.grabPartialScreen(self.window_box)
				self.scan_color = Vision.getColor(im, Vision.screenToImage(self.window_box, self.falcon_scan_button))
				if Colors.isOn(self.scan_color, Colors.falcon_scan_button_off, Colors.falcon_scan_button_on) == True:
					break
				loopCount += 1
				if loopCount > 15:
					#scanning as timed out, exit event
					return False
			self.getTargets()
		#nothing else to do, exit event
		else:
			self.falcon_event_available = False
			return False
		return True
