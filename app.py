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

from KOW import Game
import keyboard, time, os
import colorama
from colorama import Fore, Back, Style

#using gloabal variables to pause and clean exit app
g_pauseRequest = False
g_exitRequest  = False

def on_shortcutPause():
	global g_pauseRequest
	if g_pauseRequest == True:
		g_pauseRequest = False
		print(Fore.GREEN + 'Bot execution restating')
	else:
		g_pauseRequest = True
		print(Fore.YELLOW + 'Bot execution pausing, please wait a few secondes to finish current task')

def on_shortcutExit():
	global g_exitRequest
	g_exitRequest = True
	print(Fore.YELLOW + 'Bot exit requested, please wait tasks to finish')

def on_shortcutKill():
	print(Fore.RED + 'Kill Sequence Initiated')
	colorama.deinit()
	os._exit(0)

def initShortcuts(pauseSeq, exitSeq, killSeq):
	print(Fore.YELLOW + 'To pause the app use "' + Fore.WHITE + pauseSeq + Fore.YELLOW + '" key sequence')
	print(Fore.YELLOW + 'To exit  the app use "' + Fore.WHITE + exitSeq + Fore.YELLOW + '" key sequence')
	print(Fore.YELLOW + 'To kill  the app use "' + Fore.WHITE + killSeq + Fore.YELLOW + '" key sequence')
	keyboard.add_hotkey(pauseSeq, on_shortcutPause)
	keyboard.add_hotkey(exitSeq, on_shortcutExit)
	keyboard.add_hotkey(killSeq, on_shortcutKill)

def main():
	#colorama will reset default setting after each print call
	colorama.init(autoreset = True)
	initShortcuts('ctrl+alt+p', 'ctrl+alt+x', 'ctrl+alt+esc')
	games  = []
	
	#setup instances
	while True:
		games.append(Game())
		if games[-1].initialized == False:
			print(Fore.RED + 'could not start instance, removing it')
			games[-1].exit()
			games.remove(games[-1])
		cont = input('Would you like to add more instances (y/n)?')
		if cont != 'y' or g_exitRequest == True:
			break
	
	#if exit was requested will setup, just exit
	if g_exitRequest == False:
		for game in reversed(games):
			if g_exitRequest == False:
				#call init function on all instances
				enabled = game.init()
			#if init error or exit requested, clean exit
			if enabled == False or g_exitRequest == True:
				game.exit()
				games.remove(game)
				enabled = len(games) > 0
		
		#will be True as long as there is instances actives
		while enabled:
			#run in referse order because we might remove items from it
			for game in reversed(games):
				if g_pauseRequest == True:
					print(Fore.GREEN + 'Bot paused')
					#wait until pause is removed or exit requested
					while g_pauseRequest == True and g_exitRequest == False:
						time.sleep(5)
				#execute instances loop once only if not exiting
				if g_exitRequest == False:
					enabled = game.loop()
				#if instance loop return false, we need to exit this instance
				if enabled == False or g_exitRequest == True:
					game.exit()
					games.remove(game)
					enabled = len(games) > 0
			#don't overload CPU, wait a little
			time.sleep(5)
	
	#need to deinit colorama to restore console normal mode
	colorama.deinit()

if __name__ == '__main__':
	main()
