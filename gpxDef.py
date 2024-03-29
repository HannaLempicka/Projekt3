import gpxpy
import datetime as dt
import numpy as np	
from math import pi, sin, cos, sqrt, atan, tan, radians

def czytanie(plik):
	lat = []
	lon = []
	el = []
	dates = []

	
	with open (plik, 'r') as plikgpx:
		gpx = gpxpy.parse(plikgpx)
	
		for track in gpx.tracks:
			for seg in track.segments:
				for point in seg.points:
					lon.append(point.longitude)
					lat.append(point.latitude)
					
					if point.elevation!=None:
						el.append(point.elevation)
					
					if point.time != None:
						# jezeli informacja o czasie dostepna
						# usuniecie informacji o strefie czasowej
						point.time = point.time.replace(tzinfo=None)
						dates.append(point.time)
	
	return (lon, lat, el, dates)

def Vincenty(fa,la,fb,lb):
	fa=radians(fa)
	la=radians(la)
	fb=radians(fb)
	lb=radians(lb)
	a=6378137
	e2=0.00669438002290
	b=a*sqrt(1-e2) #krótsza półoś
	f=1-(b/a) #spłaszczenie
	l=lb-la #delta lambda
	Ua=atan((1-f)*tan(fa))
	Ub=atan((1-f)*tan(fb))

	L=1
	while True:
		sd=sqrt((cos(Ub)*sin(L))**2+(cos(Ua)*sin(Ub)-sin(Ua)*cos(Ub)*cos(L))**2) 	#sin sigma
		cd=sin(Ua)*sin(Ub)+cos(Ua)*cos(Ub)*cos(L) 									#cos simga
		d=atan(sd/cd) 																#sigma
		sa=(cos(Ua)*cos(Ub)*sin(L))/sd 												#sin alfa
		c2a=1-(sa)**2 																#cos alfa kwadrat
		c2dm=cd-((2*sin(Ua)*sin(Ub))/(c2a)) 										#cos podwojonej sigmy m
		C=(f/16)*(c2a)*(4+f*(4-3*(c2a)))
		Ls=L
		L=l+(1-C)*f*(sa)*(d+C*(sd)*((c2dm)+C*(cd)*(-1+2*(c2dm)**2)))
		if abs(L-Ls)<(0.000001/206265):
			break

	u2=((a**2-b**2)/(b**2))*c2a
	A=1+((u2)/16384)*(4096+(u2)*(-768+(u2)*(320-175*(u2))))
	B=((u2)/1024)*(256+(u2)*(-128+(u2)*(74-47*(u2))))
	dd=B*sd*(c2dm+(1/4)*B*((cd*(-1+2*(c2dm)**2)-(1/6)*B*c2dm*(-3+4*(sd**2))*(-3+4*(c2dm**2))))) #delta sigma

	Sab=b*A*(d-dd)

	return Sab

def d_m_s(czas): 
    d=int(czas) #godziny
    m=int((czas-d)*60.0) #minuty
    s=int((czas-d-m/60.0)*3600.0) #sekundy
    return (d, m, s) #wynik końcowy	
	
def parametry (lon, lat, el, dates):
	alt_dif 	= [0] 															# przewyższenie na kolejnych punktach
	time_dif 	= [0]															# czas pomiędzy punktami
	dist 		= [0]															# odległość między punktami
	v 			= [0]
	d 			= []
	vd 			= []
	degree 		= [0]
	i = 1
	v2=[]
	deg=[]
	S=[0]
	for index in range(len(lat)):												# index - od zera do długości listy z koordynatami
		if index == 0:															# zaczynamy od drugiego elementu
			pass
		else:	
			start = index-1							
			stop = index
			#print('start= ', start)
			#print('stop= ', stop)
			dist_part = Vincenty(lat[start],lon[start],lat[stop],lon[stop])		#liczenie odległośći za pomocą Vincentego
			#print('odleglosc= ', dist_part)
			if dist_part != 0:
				dist.append(dist_part)												#lista z odległościami
				#print('dist= ', dist)
				
				if el != []:
					alt_part = el[stop]-el[start]								#przeywyższenie z różnicy elewacji
					alt_dif.append(alt_part)
				
				if dates != []:
					time_delta = (dates[stop] - dates[start])						#czas między punktami
					time_dif.append(time_delta.seconds)
					
					
					if time_delta.seconds == 0:
						pass
					else:
						i = i + 1
						vv=dist_part/time_delta.seconds							#średnia prękość między dwoma pkt [m/s]
					
					v.append(vv)
					v2.append(vv)
					if vv == min(v2):
						k=i
					if vv == max(v):
						j=i
				else: 
					k=None
					j=None
				
				S.append(sqrt(dist_part**2+alt_part**2))
				degree=atan(alt_part/dist_part)
				deg.append(degree)
				
				if degree == min(deg):
					l=i
				if degree == max(deg):
					n=i
					
			#to będzie zawsze 
	distance=round(sum(dist),3)			#zwracamy długość trasy (pozioma)
			#jeśli będą elewacje
	
	if alt_dif != [0]:
		dHplus=0
		dHminus=0
		for h in alt_dif:
			if h >= 0:
				dHplus = dHplus + h
								
			else:
				dHminus = dHminus + h
					
		dHplus=round(dHplus,3) 				#zwracamy suma wejść 
		dHminus=abs(round(dHminus,3))		#zwracamy suma zejść
		dH=round(sum(alt_dif),3) 			#zwracamy całkowite przewyższenie
		Hmax=max(el) 						#zrawcamy min wysokość
		Hmin=min(el) 						#zwracamy max wysokość
				
		d1=0
		for x in dist:
			d1 += x
			d.append(d1)
					
		S=round(sum(S),3)		
	else:
		dHplus='brak' 			
		dHminus='brak' 			
		dH='brak' 				
		Hmax='brak'				
		Hmin='brak'
			
			
	if time_dif != [0]: 	
		timeH=sum(time_dif)/3600 #h
		h,m,s=d_m_s(timeH)
		Vsr=round(np.mean(v),1)
				
	else:
		h='brak'
		m='brak'
		s='brak'					
		Vsr='brak'		
				
	return distance, Vsr, dH, dHplus, dHminus, Hmax, Hmin, h, m, s, alt_dif, d, v, k ,j, l, n, S

	
	
if __name__ == '__main__':

	lon, lat, el, dates, =czytanie('gpx/krk1.gpx')
	print('ilość fi= ', len(lon))
	print('ilość lambd= ', len(lat))
	print('ilość elewacji= ', len(el))
	print('ilość dat= ', len(dates))
	
	
	distance, Vsr, dH, dHplus, dHminus, Hmax, Hmin, h, m, s, alt_dif, d, v, k ,j, l, n, S= parametry (lon, lat, el, dates)
	print(l)
	print(m)