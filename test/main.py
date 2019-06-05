# -*- coding: utf-8 -*-
"""
Created on Tue May 14 12:54:33 2019

@author: hania
"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker

class AddLocationForm(BoxLayout):
    search_long=ObjectProperty()
    search_lat=ObjectProperty()
    my_map=ObjectProperty()
    
    
    def search_location(self):
        longtitude=self.search_long.text
        latitude=self.search_lat.text
        self.draw_marker(latitude, longtitude)
        print(longtitude, latitude)
    
    def draw_marker(self, lati, long):
        marker=MapMarker(lat=lati, lon=long)
        self.my_map.add_marker(marker)

class MapViewApp(App):
    def build(self):
        return AddLocationForm()
#pass
    
        
        
if __name__ == '__main__':
	MapViewApp().run()