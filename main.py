
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.garden.mapview import MapMarker,  MarkerMapLayer
import gpxDef as g

class TrackForm(BoxLayout):
	destination=ObjectProperty()
	my_map=ObjectProperty()
	
	def open_file(self):
		#wybrać plik
		plik='gpx/krk1.gpx'
		lon, lat, el, dates = g.czytanie(plik)
		self.draw_rout(lat, lon)
	
	def draw_rout(self, lat, lon):
		data_lay = MarkerMapLayer()
		self.my_map.add_layer(data_lay)
		lat=lat[::10]
		lon=lon[::10]
		
		for point in zip(lat, lon):
			self.draw_marker(*point, layer=data_lay)
	
	def draw_marker(self, lat, lon, layer=None):
		markerSource='dot.png'
		if lat != None and lon != None:
			marker=MapMarker(lat=lat, lon=lon, source=markerSource)
			self.my_map.add_marker(marker, layer=layer)
	
		
class MapViewApp(App):
    def build(self):
        return TrackForm()
#pass
   

#wczytać dane
#obliczyć rzeczy + wyświetlić rzeczy
#narysować wykres
#zaznaczyć na mapie
        
        
if __name__ == '__main__':
	MapViewApp().run()