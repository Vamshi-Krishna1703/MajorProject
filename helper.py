# -*- coding: utf-8 -*-


import numpy as np

heading_helper = """
MDToolbar:
    title: "Color Detection and Color Search"

"""
grid_helper = """
MDGridLayout:
    pos_hint : {'center_x':0.5, 'center_y':0.9}
    cols : 2
    adaptive_size : True

"""
label_helper = """
MDLabel:
    text : 'Color Result'
    halign : 'center'
    size_hint_y : None
    height : 0
"""

color_text_helper = """
MDTextField:
    hint_text : 'Enter the Color!'
    pos_hint : {'center_x':0.5, 'center_y':0.9}
    size_hint_x : None
    size_hint_y : None
    width : 300
"""

search_button_helper = """
MDIconButton:
    icon : 'magnify'
    pos_hint : {'center_x':.5, 'center_y':.9}
    size_hint_x : None
    size_hint_y : None
"""

camswitch_helper = """
MDFloatingActionButton:
    icon : 'camera-flip'
    pos_hint : {'center_x':.5, 'center_y':.9}
    size_hint_x : None
    size_hint_y : None
"""

color_list = {
    
    'black':[np.array([0, 0, 0]),np.array([250,255,30])],
    'white':[np.array([0, 0, 255]), np.array([0, 0, 255])],
    'blue':[np.array([38, 86, 0]), np.array([121, 255, 255])],
    'red': [np.array([160,50,50]), np.array([180,255,255])],
    'green':[np.array([25,52,72]), np.array([102,255,255])],
    'orange':[np.array([5,50,70]), np.array([15,255,255])],
    'yellow' : [np.array([25,150,50]), np.array([35,255,255])],
    'light blue':[np.array([95,150,0]), np.array([110,255,255])],
    'orange':[np.array([15,150,0]), np.array([25,255,255])],
    'dark pink': [np.array([160,150,0]), np.array([170,255,255])],
    'pink':[np.array([145,150,0]), np.array([155,255,255])],
    'cyan' :[np.array([85,150,0]), np.array([95,255,255])],
    'dark blue': [np.array([115,150,0]), np.array([125,255,255])]

}