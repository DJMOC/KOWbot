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

autoFalcon  = []

def on_shortcutKill():
	print('Kill Sequence Initiated')
	os._exit(0)

def initKillSequence(ks):
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

def main():
	initKillSequence('ctrl+alt+esc')
	autoFalcon.append(Game((1, 34, 387, 724)))
	
	if initFalcon(0) == False:
		print('init done with no event available')
		exitFalcon(0)
	else:
		running = True
		print('init done with event available')
		while running == True:
			time.sleep(5)
			running = loopFalcon(0)
			print('loop done result : ' + str(running))

		print('event done, leaving')
		exitFalcon(0)

if __name__ == '__main__':
	main()
