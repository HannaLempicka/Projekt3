
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker,  MarkerMapLayer
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView
from kivy.uix.floatlayout import FloatLayout
import os

import gpxDef as g

class TrackForm(BoxLayout):
	destination=ObjectProperty()
	my_map=ObjectProperty()
	txt1 = ObjectProperty()
	txt2 = ObjectProperty()
	txt3 = ObjectProperty()
	txt4 = ObjectProperty()
	txt5 = ObjectProperty()
	file=None
	data_lay=None
	
	def __inir__(self, **kwargs):
		super(TrackForm, self).__init__(**kwargs)
		self.my_map.map_source = "thunderforest-landscape"
	
	def open_file(self):
		self.show_load()
	
	def analyse_file(self):
		if self.file == None:
			popup = Popup(title='Error',
			content=Label(text='Lack of file'),
			size_hint=(None, None), size=(300, 100))
			popup.open()
			
		else:
			if self.data_lay != None:
				self.my_map.remove_layer(self.data_lay)
				
			if self.file.endswith('.gpx'):
				lon, lat, el, dates = g.czytanie(self.file)
				self.draw_rout(lat, lon)
				
				distance, Vsr, dH, dHplus, dHminus, Hmax, Hmin, h, m, s, alt_dif, dist, v = g.parametry (lon, lat, el, dates)
				
				self.txt1.text =str(distance)
				self.txt1.text += '  [m]'
				
				
				if dHplus != 'brak':
					self.txt2.text =str(dHplus)
					self.txt2.text += '  [m]'
					
					self.txt3.text =str(dHminus)
					self.txt3.text += '  [m]'
					
					self.txt4.text =str(dH)
					self.txt4.text += '  [m]'
					
					self.txt5.text =str(Hmax)
					self.txt5.text += '  [m]'
					
					self.txt6.text =str(Hmin)
					self.txt6.text += '  [m]'
					
					
				
				else:
					self.txt2.text ='lack of date'
					self.txt3.text ='lack of date'
					self.txt4.text ='lack of date'
					self.txt5.text ='lack of date'
					self.txt6.text ='lack of date'
				
				if Vsr != 'brak':
				
					self.txt7.text =str(Vsr)
					self.txt7.text += '  [m/s]'
					
					self.txt8.text =str(h)
					self.txt8.text += '  [h] '
					self.txt8.text += str(m)
					self.txt8.text += '  [min] '
					self.txt8.text += str(s)
					self.txt8.text += '  [s] '
				
				else:
				
					self.txt7.text ='lack of date'
					self.txt8.text ='lack of date'
					
				self.my_map.set_zoom_at(10, 0, 0, scale=None)
				self.my_map.center_on(max(lat), max(lon))
				
			else:
				popup = Popup(title='Error',
				content=Label(text='Incorrect file'),
				size_hint=(None, None), size=(300, 100))
				popup.open()

				

	
	def draw_rout(self, lat, lon):
		self.data_lay = MarkerMapLayer()
		self.my_map.add_layer(self.data_lay)
		lat=lat[::10]
		lon=lon[::10]
		
		for point in zip(lat, lon):
			self.draw_marker(*point, layer=self.data_lay)
		
	
	def draw_marker(self, lat, lon, layer=None):
		markerSource='dot.png'
		if lat != None and lon != None:
			marker=MapMarker(lat=lat, lon=lon, source=markerSource)
			self.my_map.add_marker(marker, layer=layer)
	
	def load_list(self, path, filename):
		self.file=filename[0]
		os.path.join(path, filename[0]) 
		self.dismiss_popup()
	
	def dismiss_popup(self): # zamykanie okienka
		self._popup.dismiss()
	
	def show_load(self):
		content = LoadDialog(load=self.load_list,
		cancel=self.dismiss_popup) # powiazanie metod w oknie wczytywania plikow
		self._popup = Popup(title="Choose file", content=content, size_hint=(1, 1))
		self._popup.open()


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class MapViewApp(App):
    def build(self):
        return TrackForm()        
        
if __name__ == '__main__':
	MapViewApp().run()