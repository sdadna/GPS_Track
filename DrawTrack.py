#!/usr/bin/python
#coding:utf-8

import urllib
import os
import re
import json
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import SocketServer
import thread,time
import math

i = 0;
#data = [{'jingdu':117.27,'weidu':31.86},{'jingdu':117.16,'weidu':32.47},{'jingdu':116.98,'weidu':32.62},{'jingdu':118.38,'weidu':31.33}]
#gps_data = {'Lon_EW': 'E', 'Lon': '11715.13750', 'loc_state': 'A', 'Lat': '3150.45775', 'Lat_NS': 'N', 'id': '127.0.0.1'},{'Lon_EW': 'E', 'Lon': '11715.13750', 'loc_state': 'A', 'Lat': '3150.65775', 'Lat_NS': 'N', 'id': '127.0.0.2'}
gps_data = {}
actualGpsData = {}
BaiDuMapData = []
idList = []

#BaiDuMapData = [[{'Lat': 31.8409625, 'Lon': 117.35279166666665, 'id': '127.0.0.1'}],[{'Lat': 31.8409625, 'Lon': 118.35279166666665, 'id': '127.0.0.1'}]]
#BaiDuMapData = [[{'Lat': 31.8409625, 'Lon': 117.35279166666665, 'id': '127.0.0.1'}, {'Lat': 32.8409625, 'Lon': 118.25279166666665, 'id': '127.0.0.2'},{'Lat': 33.8409625, 'Lon': 119.35279166666665, 'id': '127.0.0.3'}],[{'Lat': 40, 'Lon': 120, 'id': '127.0.0.1'}, {'Lat': 41, 'Lon': 121, 'id': '127.0.0.2'},{'Lat': 42, 'Lon': 122, 'id': '127.0.0.3'}]\
#,[{'Lat': 24, 'Lon': 118, 'id': '127.0.0.1'}, {'Lat': 25, 'Lon': 120, 'id': '127.0.0.2'},{'Lat': 33, 'Lon': 120, 'id': '127.0.0.3'}],[{'Lat': 25, 'Lon': 118, 'id': '127.0.0.1'}, {'Lat': 24, 'Lon': 119, 'id': '127.0.0.2'},{'Lat': 23, 'Lon': 120, 'id': '127.0.0.3'}]]
class HTTPHandler(BaseHTTPRequestHandler):

	# 	self.wfile.write("hello world!")
	def do_GET(self):
		print self.client_address
		#web first request ,send track.html to web
		#web will execute track.html
		if self.path == '/':
			#self.path = 'index.html'
			f = open('index.html')
			
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		#This request , server will send track.ico to web
		#The web will marker gps point with this image
		#Now not use
		elif self.path == '/track.html':
			#self.path = 'index.html'
			f = open('track.html')
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()		
		elif self.path == '/jquery-3.2.1.js':
			#self.path = 'index.html'
			f = open('jquery-3.2.1.js')
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()	

		elif self.path == '/track.ico':
			f = open('track.ico')
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
		#
		elif self.path == '/GPSdata':
			global i
			global BaiDuMapData
			#Error_data = {'Lat':999,'Lon':999}

			if len(BaiDuMapData):
				json_str = json.dumps(BaiDuMapData)
				BaiDuMapData = []
			else:
				json_str = json.dumps('Error_data')
			# json_str = json.dumps(data[i])
			#i = (i + 1) % 2
			#print "json:",json_str
			#i = (i + 1) % 4;
			print json_str
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(json_str)

		return

class localHostServer(SocketServer.BaseRequestHandler):

	def parseLon(self, lon):
		
		Lon_min_decimal,Lon_deg_int = math.modf(float(lon))
		
		Lon_int = int(Lon_deg_int / 100)
		
		Lon_decimal = (Lon_deg_int % 100 + Lon_min_decimal)/ 60.0
				
		Lon = Lon_int + Lon_decimal

		return Lon

	def parseLatitude(self, lat):
		Lat_min_decimal,Lat_deg_int = math.modf(float(lat))
		Lat_int = int(Lat_deg_int / 100)
		Lat_decimal = (Lat_deg_int % 100 + Lat_min_decimal)/ 60.0
		Lat = Lat_int + Lat_decimal
		return Lat

	def parseGPSData(self, data):
		Lat = self.parseLatitude(data['Lat'])
		Lon = self.parseLon(data['Lon'])

		if data['Lon_EW'] == 'W':
			Lon = -Lon
		if data['Lat_NS'] == 'S':
			Lat = -Lat

		return Lat, Lon

	def handle(self):
		#receive the gps data from device with into this code
		conn = self.request
		
		#receive data
		ret_bytes = conn.recv(1024)
		#split device  str to extract gps data
		#example str:"loc_state:A\n\
		#		Lat:3150.45775\n\
		#		Lat_NS:N\n\
		#		Lon:11715.13750\n\
		#		Lon_EW:E\n"
		# Time:14d48m54s\n loc_state:A\n Lat:3149.63573\nLat_NS:N\n Lon:11707.18372       Lon_EW:E\n Speed:0.038\n Azimuth:\n Utc231217\n Alti:41.0
		#for test
		#13045511096
		#+QGNSSRD: $GNRMC,000100.559,V,,,,,0.00,0.00,010104,,,N*5F


		print ret_bytes
		#
		#data = "Time:14d48m54s\nloc_state:A\nLat:3149.63573\nLat_NS:N\nLon:11707.18372\nLon_EW:E\nSpeed:0.038\nAzimuth:\nUtc:231217\nAlti:41.0"
		#gpsMsg = re.search(r'Time:[\d]+d[\d]+m[\d]+s\nloc_state:[AV]\nLat:[\d.]+\nLat_NS:[NS]\nLon:[\d.]+\nLon_EW:[EW]\nSpeed:[\d.]+\nAzimuth:(.*)\nDate:[\d]+\nAlti:[\d.]+',ret_bytes)
		#example :+QGNSSRD: $GNRMC,130225.000,A,3149.6525,N,11707.1847,E,1.96,159.44,301217,,,A*73
		idInfo = re.search(r'([\d]+)\n\+QGNSSRD: \$GNRMC,[\d.]+,V,,,,,[\d.]+,[\d.]+,[\d]+,,,N\*[\dABCDEF]{2}',ret_bytes)
#		print idInfo.group(1)
		if idInfo is not None:
			if idInfo.group(1) not in idList:
				idList.append(idInfo.group(1))
		print idList
		gpsMsg = re.search(r'([\d]+)\n\+QGNSSRD: \$GNRMC,([\d.]+),([AV]),([\d.]+),([NS]),([\d.]+),([EW]),([\d.]+),([\d.]+),([\d]+),(.*),(.*),([ADEN]\*[\d]+)', ret_bytes)
		if gpsMsg is None:
			return
		# ret_bytes = gpsMsg.group().replace(' ','')
		# ret = ret_bytes.split('\n')
		gps_data.clear()
		gps_data['Lat'] = gpsMsg.group(4)
		gps_data['Lat_NS'] = gpsMsg.group(5)
		gps_data['Lon'] = gpsMsg.group(6)
		gps_data['Lon_EW'] = gpsMsg.group(7)
		# for string in ret:
		# 	data = string.split(':')
		# 	if (len(data) != 2):
		# 		break
		# 	gps_data[data[0]] = data[1]

		print gps_data
		#support 10 gps device point now
		if len(gps_data) == 4:
			if len(BaiDuMapData) <= 10:
				#gps_data['id'] = self.client_address[0]
				Lat, Lon = self.parseGPSData(gps_data)
				print Lat, Lon
				if (Lat <= 90 and Lat >= -90) and (Lon <= 180 and Lon >= -180):
					actualGpsData['id'] = gpsMsg.group(1)
					actualGpsData['Lat'] = Lat
					actualGpsData['Lon'] = Lon

					BaiDuMapData.append(actualGpsData)
				#example data parsed
				#BaiDuMapData = [[{'Lat': 31.8409625, 'Lon': 117.35279166666665, 'id': '127.0.0.1'}],\
				#[{'Lat': 31.8409625, 'Lon': 118.35279166666665, 'id': '127.0.0.1'}]]


def start_server(port):
	#moudify the ip address if need
	http_server = HTTPServer(('127.0.0.1', int(port)), HTTPHandler)
	http_server.serve_forever()


def start_local_server(port):
	#local host test
	#moudify the ip address if need
	server_sk = SocketServer.ThreadingTCPServer(("127.0.0.1", int(port)), localHostServer)

	server_sk.serve_forever()


#start here
if __name__ == '__main__':
	try:
		#port could be modify ,command 8000, 8080s
		thread.start_new_thread(start_server,(8000,)) #http server
		thread.start_new_thread(start_local_server,(8080,)) #local host server
	except:
		print "Error unable create multi theread"

	while 1:
		pass
