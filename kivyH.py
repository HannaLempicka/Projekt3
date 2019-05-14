# -*- coding: utf-8 -*-
"""
Created on Tue May  7 13:24:58 2019

@author: hania
"""

from kivy.uix.boxlayout import BoxLayout
2 from kivy.uix.label import Label
3 from kivy.app import App
4
5 import time
6
7 # root class
8 # class MyBox which inherits from BoxLayout class
9 class MyBox(BoxLayout):
10 def hello(self):
11 print("--> Hello at time %s" % time.ctime())
12 return
13 def world(self):
14 print("--> World at time %s" % time.ctime())
15 return
16
17 # class HelloWorldApp which inherits from App class
18 class HelloWorldApp(App):
19 def build(self):
20 return MyBox()
21
22 if __name__ == ’__main__’:
23 myApp = HelloWorldApp()
24 print "The name of your app is %s" % myApp.name
25 myApp.run()
