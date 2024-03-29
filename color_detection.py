import cv2
import numpy as np
import pandas as pd
import pyttsx3
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
from kivy.core.window import Window

from helper import (color_list, color_text_helper, label_helper,
                    search_button_helper, heading_helper, grid_helper, camswitch_helper)

color_name = ''
clicked = False
Window.size = (800, 700)
class MyLayout(MDScreen):
    global color_name
    def __init__(self, **kwargs):
        super(MyLayout, self).__init__(**kwargs)
       
        self.image = Image()
        self.ids['imageView'] = self.image
        self.img_frame = None

        index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
        self.df = pd.read_csv('colors.csv', names = index, header = None)

        self.add_widget(self.image)

        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.loadVideo, 1.0 / 30.0)

        self.color_result = Builder.load_string(label_helper)
        self.initialColor = ''
        self.color_result.text+='\n'
        self.add_widget(self.color_result)

        self.cam_btn = Builder.load_string(camswitch_helper)
        self.cam_btn.bind(on_press = self.switch_cam)
        self.add_widget(self.cam_btn)

    def loadVideo(self, *args):

        _, frame = self.capture.read()
        self.img_frame = frame
        
        if color_name!='':
            if color_name in color_list:
                blurred_frame = cv2.GaussianBlur(frame, (5,5), 0)
                hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
                lower = color_list[color_name][0]
                upper = color_list[color_name][1]
                mask = cv2.inRange(hsv, lower, upper)
                
                contours, _ = cv2.findContours(mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)

        elif color_name == 'null':
            cv2.drawContours(frame, None, 0, (0, 255, 0), 2)

        buf = cv2.flip(frame, 0).tostring()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.image.texture = texture

        if self.initialColor == '':
            self.getInitialColor()
            # self.color_result.text =  'Color result : '+self.initialColor+'\n'

    def get_color_name(self, p):
        c, d = 81, 584 # top-left
        t, q = 719, 107 # bottom-right

        if p[0]>=c and p[0] <=t and p[1]>=q and p[1]<=d:
            new_pos_x = int(p[0]) - c
            new_pos_y = d - int(p[1])

            b, g, r = self.img_frame[new_pos_y, new_pos_x]
            B = int(b)
            G = int(g)
            R = int(r)
            minimum = 1000
            for i in range(len(self.df)):
                d = abs(R - int(self.df.loc[i, "R"])) + abs(G - int(self.df.loc[i, "G"])) + abs(B - int(self.df.loc[i, "B"]))
                if d <= minimum:
                    minimum = d
                    cname = self.df.loc[i, "color_name"]
            return cname
        else :
            return 'out of frame'

    def getInitialColor(self):
        c, d = 81, 584 # top-left
        t, q = 719, 107 # bottom-right

        mid_x = (c+t)//2
        mid_y = (d+q)//2

        p = [mid_x, mid_y]
        color = self.get_color_name(p)
        self.initialColor = color
        self.color_result.text = 'Color result : '+color+'\n'

    def on_touch_down(self, touch):

        #top left : (80.0, 584.0)
        #right bottom : (719.0, 106.99999999999996)
        print(touch.pos)
        p = touch.pos
        cname = self.get_color_name(p)

        # print(cname)
        self.color_result.text = 'Color result : '+cname+'\n'
        
        # if cname != 'out of frame':
        #     engine = pyttsx3.init()
        #     engine.say(self.color_result.text)
        #     engine.runAndWait()

        return super(MDScreen, self).on_touch_down(touch)

    @staticmethod
    def search_color(t):
        global color_name
        if t!='':
            t = t.lower()
            color_name = t
            print(t)
        if t == '':
            color_name = 'null'
    
    def switch_cam(self, *args):
        print('clicked')
        global clicked
        clicked = not clicked
        if clicked:
            self.capture = cv2.VideoCapture(1)
        else:
            self.capture = cv2.VideoCapture(0)
        self.getInitialColor()

class ColorDetectionApp(MDApp):

    def build(self):
        ly = MDBoxLayout(orientation = 'vertical')

        self.toolbar = Builder.load_string(heading_helper)
        ly.add_widget(self.toolbar)
        
        img = MyLayout()
        ly.add_widget(img)

        temp = Builder.load_string(grid_helper)

        self.color_name = Builder.load_string(color_text_helper)
        temp.add_widget(self.color_name)

        self.color_btn = Builder.load_string(search_button_helper)
        self.color_btn.bind(on_press = self.search_color)
        temp.add_widget(self.color_btn)

        ly.add_widget(temp)

        # self.cam_btn = Builder.load_string(camswitch_helper)
        # self.cam_btn.bind(on_press = self.switch_cam)
        # ly.add_widget(self.cam_btn)
        return ly

    def search_color(self, *args):
        t = self.color_name.text
        MyLayout.search_color(t)

    def switch_cam(self, *args):
        global clicked
        clicked = not clicked

if __name__ == '__main__':
    ColorDetectionApp().run()
