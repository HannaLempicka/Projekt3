
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker,  MarkerMapLayer
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserIconView, FileChooserListView
from kivy.uix.floatlayout import FloatLayout
import os

import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

import gpxDef as g

class TrackForm(BoxLayout):
	destination=ObjectProperty()
	my_map=ObjectProperty()
	txt1 = ObjectProperty()
	txt2 = ObjectProperty()
	txt3 = ObjectProperty()
	txt4 = ObjectProperty()
	txt5 = ObjectProperty()
	txt6 = ObjectProperty()
	txt7 = ObjectProperty()
	txt8 = ObjectProperty()
	txt9 = ObjectProperty()
	plots = ObjectProperty()
	file=None
	data_lay=None
	
	def __init__(self, **kwargs):
		super(TrackForm, self).__init__(**kwargs)
		self.my_map.map_source = "thunderforest-outdoors"
		self.fig = plt.figure()
		self.cnv = FigureCanvasKivyAgg(self.fig)
		self.plots.add_widget(self.cnv)

	def rysuj_wykres(self):
		self.ax1 = self.fig.add_subplot(121) #dodajemy tylko 1 wykres
		self.ax2 = self.fig.add_subplot(122) #dodajemy tylko 1 wykres
		lon, lat, el, dates = g.czytanie(self.file)
		distance, Vsr, dH, dHplus, dHminus, Hmax, Hmin, h, m, s, alt_dif, d, v, k ,j, l, n, S = g.parametry (lon, lat, el, dates)
		
		if alt_dif != [0]:
			self.ax1.scatter(d[l], alt_dif[l], label='the harderst part', color='red')
			self.ax1.scatter(d[n], alt_dif[n], label='the easiest part', color='black')
			self.ax1.plot(d[::20], alt_dif[::20])

			self.ax1.set_ylabel("dH[dist] [m]")
		
		if v != [0]:
			self.ax2.plot(d, v)
			self.ax2.scatter(d[k], v[k], label='the slowest part', color='red')
			self.ax2.scatter(d[j], v[j], label='the fastest part', color='black')
			
			self.ax2.set_ylabel("v[dis]   [m/s]")
		
		self.ax1.legend()
		self.ax2.legend()
		self.cnv.draw()

	
	def open_file(self):
		self.txt1.text = ''
		self.txt2.text = ''	
		self.txt3.text = ''	
		self.txt4.text = ''	
		self.txt5.text = ''	
		self.txt6.text = ''	
		self.txt7.text = ''	
		self.txt8.text = ''
		self.txt9.text = ''
		self.fig.clear()
		self.cnv.draw()
		if self.data_lay is not None:
			self.my_map.remove_layer(self.data_lay)
		
		self.my_map.set_zoom_at(1, 0, 0, scale=None)
		self.my_map.center_on(0, 0)
		
		self.show_load()
	
	def analyse_file(self):
		if self.file == None:
			popup = Popup(title='Error',
			content=Label(text='Lack of file'),
			size_hint=(None, None), size=(300, 100))
			popup.open()
			
		else:
			self.fig.clear()
			self.cnv.draw()
			self.rysuj_wykres()
			
			if self.file.endswith('.gpx'):
				lon, lat, el, dates = g.czytanie(self.file)
				self.draw_rout(lat, lon)
				
				distance, Vsr, dH, dHplus, dHminus, Hmax, Hmin, h, m, s, alt_dif, d, v, k ,j, i, n, S = g.parametry (lon, lat, el, dates)
				
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
				
					self.txt9.text =str(S)
					self.txt9.text += '  [m]'
					
				else:
					self.txt2.text = 'lack of date'
					self.txt3.text = 'lack of date'
					self.txt4.text = 'lack of date'
					self.txt5.text = 'lack of date'
					self.txt6.text = 'lack of date'
					self.txt9.text = 'lack of date'
				
				if Vsr != 'brak':
				
					self.txt7.text = str(Vsr)
					self.txt7.text += '  [m/s]'
					
					self.txt8.text = str(h)
					self.txt8.text += '  [h] '
					self.txt8.text += str(m)
					self.txt8.text += '  [min] '
					self.txt8.text += str(s)
					self.txt8.text += '  [s] '
				
				else:
				
					self.txt7.text ='lack of date'
					self.txt8.text ='lack of date'
					
				self.my_map.set_zoom_at(8, 0, 0, scale=None)
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