def czytanie(plik):
	import gpxpy
	import datetime as dt
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
	from math import pi, sin, cos, sqrt, atan, tan, radians
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
			dist.append(dist_part)												#lista z odległościami
			#print('dist= ', dist)
			
			if el != []:
				alt_part = el[stop]-el[start]								#przeywyższenie z różnicy elewacji
				alt_dif.append(alt_part)
			
			if dates != []:
				time_delta = (dates[stop] - dates[start])						#czas między punktami
				time_dif.append(time_delta.seconds)
				
				if time_delta.seconds == 0:
					v.append(0)
				else:
					v.append(dist_part/time_delta.seconds) 							#średnia prękość między dwoma pkt
			
			distance=round(sum(dist),3)
			dH=round(sum(alt_dif),3)
			sum_time=sum(time_dif)
			h,m,s=d_m_s(sum_time)
			
			dHplus=0
			dHminus=0
			for h in alt_dif:
				if h >= 0:
					dHplus = dHplus + h
					
				else:
					dHminus = dHminus + h
					
			dHplus=round(dHplus,3)
			dHminus=abs(round(dHminus,3))
				
	return(alt_dif, time_dif, dist, v, distance, dH, dHplus, dHminus, h, m, s)
	
if __name__ == '__main__':

	lon, lat, el, dates, =czytanie('gpx/krk1.gpx')
	print('ilość fi= ', len(lon))
	print('ilość lambd= ', len(lat))
	print('ilość elewacji= ', len(el))
	print('ilość dat= ', len(dates))
	
	
	alt_dif, time_dif, dist, v, distance, dH, dHplus, dHminus, h, m, s = parametry (lon, lat, el, dates)
	print('ilość odległości= ', len(dist))
	print('ilość różnic wysokości= ', len(alt_dif))
	print('ilość różnic czasu= ', len(time_dif))
	print(h,m,s)