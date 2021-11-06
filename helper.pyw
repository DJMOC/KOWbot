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

import os, time, easyocr, re
import win32api, win32con
from PIL import Image, ImageGrab
from numpy import *
import pygetwindow as pgw
import ctypes
from ctypes import wintypes # We can't use ctypes.wintypes, we must import wintypes this way.

#creater easyocr reader database, called only once
reader = easyocr.Reader(['en'], gpu = False,
                        model_storage_directory =
                        '\\assets\\easyOCR\\')

class Screen:
	def resolution():
		return (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
	
	def saveImage(im, name):
		#print('    requesting image save with name : ' + name)
		im.save(os.getcwd() + '\\' + name + '_' + str(int(time.time())) + '.png', 'PNG')
	
	def grabFullScreen():
		#print('    grab full screen')
		return ImageGrab.grab()
	
	def grabPartialScreen(box):
		#print('    grab screen between ' + str(box))
		return ImageGrab.grab(box)
		
	def screenToCoords(box, xy):
		#print('    mapping screen ' + str(xy) + ' to box ' + str(box))
		_x = (xy[0] - box[0]) / (box[2] - box[0])
		_y = (xy[1] - box[1]) / (box[3] - box[1])
		#print(f'    position will be ({_x:1.6f}, {_y:1.6f})')
		return (_x, _y)
	
	def coordsToScreen(box, xy):
		#print(f'    mapping ({xy[0]:1.6f}, {xy[1]:1.6f}) to screen box ' + str(box))
		_x = (1.0 - xy[0]) * box[0] + xy[0] * box[2]
		_y = (1.0 - xy[1]) * box[1] + xy[1] * box[3]
		#print(f'    position will be ({_x}, {_y})')
		return (int(_x + .5), int(_y + .5))
	
	def makeBox(top_left, bottom_right):
		#print('    makeBox from ' + str(top_left) + ' and ' + str(bottom_right))
		return (top_left[0],     top_left[1], 
				bottom_right[0], bottom_right[1])

class Mouse:
	def getMousePosition():
		#print('    requesting mouse position : ' + str(win32api.GetCursorPos()))
		return win32api.GetCursorPos()

	def getRelativeMousePosition(box):
		(x, y) = win32api.GetCursorPos()
		#print('    requesting mouse position within box ' + str(box) + ' : ' + 
		#			str(Screen.screenToCoords(box, (x, y))))
		return Screen.screenToCoords(box, (x, y))
	
	def presseButtonLeft():
		#print('    pressing left button at ' + str(win32api.GetCursorPos()))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
	
	def releaseButtonLeft():
		#print('    relessing left button at ' + str(win32api.GetCursorPos()))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    
	def clickButtonLeft():
		#print('    single left button click at ' + str(win32api.GetCursorPos()))
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
		time.sleep(.05)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
	
	def clickTo(xy):
		xy = (int(xy[0]), int(xy[1]))
		#print('    moving cursor to ' + str(xy) + ' then left clicking')
		win32api.SetCursorPos(xy)
		time.sleep(.05)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
		time.sleep(.05)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
	
	def moveTo(xy):
		xy = (int(xy[0]), int(xy[1]))
		#print('    moving cursor to ' + str(xy))
		win32api.SetCursorPos(xy)
	
	def dragTo(xy):
		xy = (int(xy[0]), int(xy[1]))
		cuPos = win32api.GetCursorPos()
		#print('    dragging cursor from ' +  str(cuPos) + ' to ' + str(xy))
		(dx, dy) = (xy[0] - cuPos[0], xy[1] - cuPos[1])
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
		time.sleep(.1)
		for i in range(20):
			next = (int(cuPos[0] + i * dx / 20), int(cuPos[1] + i * dy / 20))
			win32api.SetCursorPos(next)
			time.sleep(.025)
		win32api.SetCursorPos(xy)
		time.sleep(.1)
		win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

class Vision:
	def imageToCoords(box, xy):
		_x = float(xy[0]) / float(box[2] - box[0])
		_y = float(xy[1]) / float(box[3] - box[1])
		#print('    mapping ' + str(xy) + ' in image ' + str((0, 0, box[2] - box[0], box[3] - box[1])))
		#print(f'    result is ({_x:1.6f}, {_y:1.6f})')
		return (_x, _y)
	
	def coordsToImage(box, xy):
		_x = (1.0 - xy[0]) * box[0] + xy[0] * box[2] - box[0]
		_y = (1.0 - xy[1]) * box[1] + xy[1] * box[3] - box[1]
		#print(f'    mapping ({xy[0]:1.6f}, {xy[1]:1.6f}) to image ' + str((0, 0, box[2] - box[0], box[3] - box[1])))
		#print('    result is ' + str((_x, _y)))
		return (int(_x + .5), int(_y + .5))
	
	def screenToImage(box, xy):
		#print('    mapping screen ' + str(xy) + ' to image ' + str((xy[0] - box[0], xy[1] - box[1])))
		return (xy[0] - box[0], xy[1] - box[1])
	
	def imageToScreen(box, xy):
		#print('    mapping image ' + str(xy) + 'to screen ' + str((xy[0] + box[0], xy[1] + box[1])))
		return (xy[0] + box[0], xy[1] + box[1])
	
	def getColor(im, xy):
		#print('    get pixel color at ' + str(xy) + ' : ' + str(im.getpixel(xy)))
		return im.getpixel(xy)
	
	def extractStrings(box):
		im = ImageGrab.grab(box)
		ret = reader.readtext(array(im))
		#print('    extracting strings from screen location : ' + str(box))
		#print('    ' + ', '.join([elem[1] for elem in ret]))
		return ret
	
	def findString(obj, st):
		#print('    finding "' + st + '" in ' + ', '.join([elem[1].lower() for elem in obj]))
		for x in obj:
			if len(re.findall(st, x[1].lower())) != 0:
				box = (x[0][0][0], x[0][0][1], x[0][2][0], x[0][2][1]);
				#print('    ' + st + ' found at location ' + str(box))
				return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)
		
		#print('    ' + st + ' not found')
		return (0, 0)
	
	def findMarchTime(stringList):
		#print('    trying to find time from ' + str(stringList))
		#in case of any error, return 3 minutes
		if len(stringList) != 1:#should only have 1 string
			#print('    error : list as not 1 and only 1 strings')
			return 180
		
		st = re.sub('[oO0]', '0', stringList[0][1])
		st = re.sub('[.,:;]', ':', st)
		#print('    reformat to : ' + st)
		textList = st.split(':')
		
		if len(textList) != 2:#should only be minutes and secondes
			#print('    error : splitting with ":" did not returned 2 strings')
			return 180
		
		try:
			#print('    trying to convert ' + textList[0] + ' minutes and ' + textList[1] + ' secondes')
			return 60 * int(textList[0]) + int(textList[1])
		except:#time not recognized correctly
			#print('    error : ' + textList[0] + ' or ' + textList[1] + ' is not in the right format')
			return 180

class AppWindow:
	def getGameWindow(name):
		wt = pgw.getWindowsWithTitle(name)
		if len(wt) < 1:
			print('Error : no window')
			return None
		print('Got window : ' + str(wt))
		return wt

	def grabAppArea(box):
		print('Grabbing area : ' + str(box))
		im = ImageGrab.grab(box)
		print('Image : ' + str(im))
		return im

	def getCornerText(im, txts):
		if len(txts) != 2:
			print('must find exactly 2 words, requested ' + str(len(txts)))
			return []
		lst = reader.readtext(array(im))
		print('found ' + str(len(lst)) + ' texts')
		imp = []
		for x in lst:
			if len(re.findall('(' + txts[0] + ')|(' + txts[1] + ')', x[1].lower())) != 0:
				imp.append(x)
		if len(imp) != 2:
			print('Error : didn\'t found exacly 2 match')
			return []
		print('Found 2 match : ' + str(imp))
		def findCenter(item):
			return ((item[0][0][0] + item[0][2][0]) / 2, 
					(item[0][0][1] + item[0][2][1]) / 2)
		if len(re.findall(txts[0], imp[0][1].lower())) != 0:
			a = findCenter(imp[0])
			b = findCenter(imp[1])
		else:
			b = findCenter(imp[1])
			a = findCenter(imp[0])
		print('found ' + txts[0] + ' at ' + str(a))
		print('found ' + txts[1] + ' at ' + str(b))
		return (a, b)

	def extrapolateGameArea(ct, const):
		p1 = ct[0]
		p2 = ct[1]
		c1 = const[0]
		c2 = const[1]
		#vip  = Coords.static_window_anchor_vip
		#camp = Coords.static_window_anchor_camp
		w = round(abs(p1[0] - p2[0]) / abs(c1[0] - c2[0]), 0)
		h = round(abs(p1[1] - p2[1]) / abs(c1[1] - c2[1]), 0)
		x = round(p1[0] - c1[0] * w, 0)
		y = round(p1[1] - c1[1] * h, 0)
		print('window W : ' + str(w))
		print('window H : ' + str(h))
		return (x, y, x + w, y + h)

	def isInside(w, xy):
		(l, t, r, b) = (w.left, w.top, w.right, w.bottom)
		(x, y) = xy
		if x >= l and x <= r and y >= t and y <= b:
			ret = True
		else:
			ret = False
		print('is ' + str(xy) + ' inside ' + str((l, t, r, b)) + '? ' + str(ret))
		return ret
