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

from sre_constants import FAILURE
from instance import Game
import keyboard
import time
import os
import sys
import pywinauto
import pygetwindow
import pyautogui
import easyocr
import re
import cv2
import numpy as np
from helper import Mouse, Screen, Vision
from pprint import pprint
from msvcrt import getch, kbhit

autoFalcon = {}
win_titles = [
	'BlueStacks',
	'VM'
]


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


def getRunningApp():
	height = 0
	width = 0
	final = {}
	screens = pygetwindow.getAllWindows()
	for i in range(len(screens)):
		if screens[i].title:
			final[i] = {
				'title': screens[i].title,
				'obj': screens[i],
				'topleft_x': screens[i].topleft.x,
				'topleft_y': screens[i].topleft.y,
				'bottomright_x': screens[i].bottomright.x,
				'bottomright_y': screens[i].bottomright.y,
				'box': Screen.makeBox(
					[screens[i].topleft.x, screens[i].topleft.y],
					[screens[i].bottomright.x, screens[i].bottomright.y]
				)
			}
	if not final:
		return False
	return final


def show_all_screens(kow_windows):
	title_num = ""
	print("{:<8} {:<25} {:<20}".format('Number', 'Title', 'Location'))
	for key, val in kow_windows.items():
		print("{:<8} {:<25} {:<20}".format(
			key, val['title'][:+20], f"x: {val['topleft_x']} - y: {val['topleft_y']}"))


def clear_buff():
	while kbhit():
		getch()


def menu_help():
	print(""
		"Choose the windows to operate on by focusing on it then hit 'd' to accept the selections.\n"
		"\n"
		"(Optional Input)\n"
		"(s): Show titles of all screens and type cooresponding digit to add it to the list.\n"
		"(m): Manually add a screen to list.\n"
		"(?): Show these options again.\n"
		"(q): Exit program.\n"
		"\n"
		"If no windows have been chosen we will assume you want all windows to be used.\n"
		"\n")


def find_hq(vals):
	reader = easyocr.Reader(['en'], gpu=False,
							model_storage_directory='\\assets\\easyOCR\\')
	object = vals['obj']
	if object.isActive == False:
			pywinauto.application.Application().connect(handle=object._hWnd).top_window().set_focus()
			time.sleep(.5)
	box = vals['box']
	image_size_x = 120
	image_size_y = 140
	reducer_integer = 20
	found_it_at = ""
	tries = 2
	hq_level = ""
	while tries > 0:
		for y in range(vals['topleft_y'], vals['topleft_y'] + object.size.height, image_size_x):
			for x in range(vals['topleft_x'], vals['topleft_x'] + object.size.width, image_size_y):
				newbox = Screen.makeBox(
					[x, y],
					[x + image_size_x, y + image_size_y]
				)
				image = Screen.grabPartialScreen(newbox)
				image_array = np.array(image)
				trans_text = reader.readtext(image_array)
				for cc, text, dd in trans_text:
					if re.match('^[H|h]\w{1}\s{1}\d', text):
						nx = x + cc[0][0]
						ny = y + cc[2][1]
						found_it_at = [nx, ny]
						hq_level = text
						pyautogui.moveTo(found_it_at)
						image.save("hq.jpg")
						break
				if found_it_at:
					break
		if found_it_at:
			break
		image_size_x = image_size_x - reducer_integer
		image_size_y = image_size_y - reducer_integer
	if not found_it_at:
		return False
	hq_parse = re.findall('\d.*', hq_level)
	if not hq_parse:
		return False
	if not str(hq_parse[0]).isnumeric():
		return False
	return {
		'current_hq_coords': found_it_at,
		'hq_level': hq_parse[0]
	}


def initAutoFalcon():
	final_selections = {}
	kow_windows = getRunningApp()
	if not kow_windows:
		print("Could not find any running screens.")
		sys.exit(0)
	print(f'Found {len(kow_windows)} active screens with titles.')
	menu_help()

	keyboard.add_hotkey('s', lambda: show_all_screens(
		kow_windows), trigger_on_release=False)

	keyboard.add_hotkey('shift+?', lambda: menu_help(),
						trigger_on_release=False)

	# Start user input cycle.
	chosen_windows = {}
	while True:
		for key, vals in kow_windows.items():
			object = vals['obj']
			if object.isActive and object.title in win_titles and key not in chosen_windows.keys():
				print(f"Attempting to find the HQ level {key}....")
				hq = find_hq(vals)
				if not hq:
					print("Unable to find HQ automatically.")
					vals['HQ'] = int(
						input("What is the HQ level for this screen? "))
				else:
					vals['HQ'] = int(hq['hq_level'])
				vals['Game'] = Game(vals['HQ'], vals['box'])
				print(
					f"Added screen {vals['title']} at location (x: {vals['topleft_x']} - y: {vals['topleft_y']}) to the list.")
				chosen_windows[key] = vals
			if len(chosen_windows) == len(kow_windows) or keyboard.is_pressed('d'):
				time.sleep(.5)
				if not chosen_windows:
					print("No windows chosen, assuming all windows.")
					final_selections = kow_windows
				else:
					final_selections = chosen_windows
				clear_buff()
				break
			if keyboard.is_pressed('m'):
				time.sleep(.5)
				show_all_screens(kow_windows)
				clear_buff()
				select = int(input('Number: ').strip())
				kow_windows[select]['HQ'] = int(
					input("What is the HQ level for this screen? "))
				kow_windows[select]['Game'] = Game(vals['HQ'], vals['box'])
				print(
					f"Added screen {kow_windows[select]['title']} at location (x: {kow_windows[select]['topleft_x']} - y: {kow_windows[select]['topleft_y']}) to the list.")
				chosen_windows[select] = kow_windows[select]
		if final_selections:
			break
	print("")
	clear_buff()
	return final_selections


def main():
	initKillSequence('ctrl+alt+esc')
	autoFalcon = initAutoFalcon()
	pprint(autoFalcon)
	sys.exit(0)
	if initFalcon(0) == False:
		# print('init done with no event available')
		exitFalcon(0)
	else:
		running = True
		# print('init done with event available')
		while running == True:
			time.sleep(5)
			running = loopFalcon(0)
			# print('loop done result : ' + str(running))

		# print('event done, leaving')
		exitFalcon(0)


if __name__ == '__main__':
	main()
