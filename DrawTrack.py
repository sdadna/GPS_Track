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
idPointSet = {}

#BaiDuMapData = [[{'Lat': 31.8409625, 'Lon': 117.35279166666665, 'id': '127.0.0.1'}],[{'Lat': 31.8409625, 'Lon': 118.35279166666665, 'id': '127.0.0.1'}]]
#BaiDuMapData = [[{'Lat': 31.8409625, 'Lon': 117.35279166666665, 'id': '127.0.0.1'}, {'Lat': 32.8409625, 'Lon': 118.25279166666665, 'id': '127.0.0.2'},{'Lat': 33.8409625, 'Lon': 119.35279166666665, 'id': '127.0.0.3'}],[{'Lat': 40, 'Lon': 120, 'id': '127.0.0.1'}, {'Lat': 41, 'Lon': 121, 'id': '127.0.0.2'},{'Lat': 42, 'Lon': 122, 'id': '127.0.0.3'}]\
#,[{'Lat': 24, 'Lon': 118, 'id': '127.0.0.1'}, {'Lat': 25, 'Lon': 120, 'id': '127.0.0.2'},{'Lat': 33, 'Lon': 120, 'id': '127.0.0.3'}],[{'Lat': 25, 'Lon': 118, 'id': '127.0.0.1'}, {'Lat': 24, 'Lon': 119, 'id': '127.0.0.2'},{'Lat': 23, 'Lon': 120, 'id': '127.0.0.3'}]]
class HTTPHandler(BaseHTTPRequestHandler):

	#self.wfile.write("hello world!")
	def do_GET(self):
		print self.client_address
		print self.path
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
		elif self.path == '/drawLine':
			json_str = json.dumps(idPointSet)
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			print json_str
			self.wfile.write(json_str)

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
		#for test
		#13045511096
		#+QGNSSRD: $GNRMC,000100.559,V,,,,,0.00,0.00,010104,,,N*5F

		print ret_bytes
		ret = ret_bytes.split('\r\n')

		gpsMsg = re.search(r'\+QGNSSRD: \$GNRMC,([\d.]+),([AV]),([\d.]+),([NS]),([\d.]+),([EW]),([\d.]+),([\d.]+),([\d]+),(.*),(.*),([ADEN]\*[\dABCDEF]+)', ret[1])
		if gpsMsg is None:
			return
		# ret_bytes = gpsMsg.group().replace(' ','')
		# ret = ret_bytes.split('\n')
		gps_data.clear()
		gps_data['id'] = ret[0]
		gps_data['Lat'] = gpsMsg.group(3)
		gps_data['Lat_NS'] = gpsMsg.group(4)
		gps_data['Lon'] = gpsMsg.group(5)
		gps_data['Lon_EW'] = gpsMsg.group(6)
		gps_data['speed'] = gpsMsg.group(7)
		gps_data['status'] = gpsMsg.group(2)
		gps_data['utc'] = gpsMsg.group(1)
		fullDate = "20" + gpsMsg.group(9)[-2:] + "-" + gpsMsg.group(9)[2:4] + "-" + gpsMsg.group(9)[0:2]
		gps_data['date'] = fullDate
		gps_data['altitude'] = gpsMsg.group(8)
		print gps_data
		#support 10 gps device point now
		if len(gps_data) == 10:
			if len(BaiDuMapData) <= 10:
				Lat, Lon = self.parseGPSData(gps_data)
				print Lat, Lon
				if (Lat <= 90 and Lat >= -90) and (Lon <= 180 and Lon >= -180):
					actualGpsData['id'] = gps_data['id']
					actualGpsData['Lat'] = Lat
					actualGpsData['Lon'] = Lon
					actualGpsData['date'] = gps_data['date']
					actualGpsData['altitude'] = gps_data['date']
					actualGpsData['speed'] = gps_data['speed']
					if idPointSet.has_key(actualGpsData['id']):	

						idPointSet[actualGpsData['id']]['points'].append(actualGpsData['Lat'])
						idPointSet[actualGpsData['id']]['points'].append(actualGpsData['Lon'])
					else:
						idPointSet[actualGpsData['id']] = {}
						idPointSet[actualGpsData['id']]['id'] = actualGpsData['id']
						idPointSet[actualGpsData['id']]['points'] = []
						idPointSet[actualGpsData['id']]['points'].append(actualGpsData['Lat'])
						idPointSet[actualGpsData['id']]['points'].append(actualGpsData['Lon'])						
					

					BaiDuMapData.append(actualGpsData)
				#example data parsed
				#BaiDuMapData = [[{'Lat': 31.8409625, 'Lon': 117.35279166666665, 'id': '127.0.0.1'}],\
				#[{'Lat': 31.8409625, 'Lon': 118.35279166666665, 'id': '127.0.0.1'}]]


def start_server(port):
	#moudify the ip address if need
	http_server = HTTPServer(('192.168.1.10', int(port)), HTTPHandler)
	http_server.serve_forever()


def start_local_server(port):
	#local host test
	#moudify the ip address if need
	server_sk = SocketServer.ThreadingTCPServer(("192.168.1.10", int(port)), localHostServer)

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
