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

# Coords are 0..1, so it scale to window size
class Coords:
	#Static references to Zero-Span gameplay area
	static_window_anchor_vip     = (0.678571, 0.060345)
	static_window_anchor_camp    = (0.234594, 0.979885)
	#inGame Position
	event_button                 = (.917098, .228986)
	event_return                 = (.064767, .092754)
	event_menu_left              = (.199482, .092754)
	event_menu_right             = (.898964, .092754)
	event_calendar_topleft       = (.007772, .217391)
	event_calendar_bottomright   = (.971503, .95942 )
	event_calandar_slide_top     = (.30829,  .243478)
	event_calandar_slide_bottom  = (.30829,  .93913 )
	event_popup_go               = (.5,      .717391)
	event_popup_topleft          = (.463731, .707246)
	event_popup_bottomright      = (.546632, .730435)
	falcon_go_button             = (.5,      .915942)
	falcon_go_topleft            = (.445596, .894203)
	falcon_go_bottomright        = (.554404, .930435)
	falcon_scan_button           = (.341969, .915942)
	falcon_targetA_button        = (.098446, .72029 )
	falcon_targetB_button        = (.411917, .72029 )
	falcon_targetC_button        = (.727979, .72029 )
	falcon_targetD_button        = (.098446, .781159)
	falcon_targetE_button        = (.411917, .781159)
	falcon_targetF_button        = (.727979, .781159)
	falcon_rescue_button         = (.5,      .371014)
	falcon_deploy_button         = (.401554, .905797)
	falcon_deploy_topleft        = (.354922, .849275)
	falcon_deploy_bottomright    = (.453368, .866667)

# Colors are (R, G, B)
class Colors:
	falcon_scan_button_off   = (133, 116,  89)
	falcon_scan_button_on    = (220, 194, 139)
	falcon_target_button_off = (73,  100,  69)
	falcon_target_button_on  = (65,  247,  91)
	falcon_background        = (113, 108,  93)
	event_color_1            = (210, 106,  28)
	event_color_2            = (193, 135,  11)
	event_color_3            = ( 32,  98, 142)
	event_color_4            = ( 65,  99,  65)
	event_color_5            = (109,  63, 134)
	
	def isOn(test, off, on):
		#print('    requested color test' + str(test) + ' vs off' + str(off) + ' and on' + str(on))
		eucOff = pow(test[0] - off[0], 2) + pow(test[1] - off[1], 2) + pow(test[2] - off[2], 2)
		eucOn  = pow(test[0] - on[0],  2) + pow(test[1] - on[1],  2) + pow(test[2] -  on[2], 2)
		
		#print('    euclidian distance from off is : ' + str(eucOff))
		#print('    euclidian distance from on  is : ' + str(eucOn))
		#print('    test color is probably : ' + str(eucOn < eucOff))
		
		if eucOn < eucOff:
			return True
		else:
			return False