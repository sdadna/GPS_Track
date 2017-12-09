#!/usr/bin/python
#coding:utf-8

import urllib
import os
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
#BaiDuMapData = [[{'Lat': 31.8409625, 'Lon': 117.35279166666665, 'id': '127.0.0.1'}, {'Lat': 32.8409625, 'Lon': 118.25279166666665, 'id': '127.0.0.2'},{'Lat': 33.8409625, 'Lon': 119.35279166666665, 'id': '127.0.0.3'}],[{'Lat': 40, 'Lon': 120, 'id': '127.0.0.1'}, {'Lat': 41, 'Lon': 121, 'id': '127.0.0.2'},{'Lat': 42, 'Lon': 122, 'id': '127.0.0.3'}]\
#,[{'Lat': 24, 'Lon': 118, 'id': '127.0.0.1'}, {'Lat': 25, 'Lon': 120, 'id': '127.0.0.2'},{'Lat': 33, 'Lon': 120, 'id': '127.0.0.3'}],[{'Lat': 25, 'Lon': 118, 'id': '127.0.0.1'}, {'Lat': 24, 'Lon': 119, 'id': '127.0.0.2'},{'Lat': 23, 'Lon': 120, 'id': '127.0.0.3'}]]
class HTTPHandler(BaseHTTPRequestHandler):

	# def do_GET(self):
	# 	self.send_response(200)
	# 	self.send_header('Content-type', 'text/html')
	# 	self.end_headers()

	# 	self.wfile.write("hello world!")
	def do_GET(self):
		if self.path == '/':
			self.path = 'track.html'
			f = open(self.path)
			
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
		elif self.path == '/GPSdata':
			global i
			global BaiDuMapData
			#Error_data = {'Lat':999,'Lon':999}
			if len(BaiDuMapData):
				json_str = json.dumps(BaiDuMapData)
				#BaiDuMapData = []
			else:
				json_str = json.dumps('Error_data')
			# json_str = json.dumps(data[i])
			# i = (i + 1) % 4
			#print "json:",json_str
			# i = (i + 1) % 4;
			# print json_str
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
		
		conn = self.request
		print self.client_address
		#while True:
		ret_bytes = conn.recv(1024)
		print ret_bytes
		ret_bytes = ret_bytes.replace('\t','')
		ret = ret_bytes.split('\n')
		gps_data.clear()
		for string in ret:
			data = string.split(':')
			if (len(data) != 2):
				break
			gps_data[data[0]] = data[1]

		#print gps_data, len(gps_data)
		#Lat	

		if len(gps_data) == 5:
			if len(BaiDuMapData) <= 10:
				#gps_data['id'] = self.client_address[0]
				Lat, Lon = self.parseGPSData(gps_data)
				actualGpsData['id'] = self.client_address[0]
				actualGpsData['Lat'] = Lat
				actualGpsData['Lon'] = Lon
			# BaiDuMapData['Lat'] = Lat
			# BaiDuMapData['Lon'] = Lon
			
				BaiDuMapData.append(actualGpsData)
				#print BaiDuMapData


def start_server(port):
	http_server = HTTPServer(('127.0.0.1', int(port)), HTTPHandler)
	http_server.serve_forever()


def start_local_server(port):
	server_sk = SocketServer.ThreadingTCPServer(("127.0.0.1", int(port)), localHostServer)
	server_sk.serve_forever()

try:
	thread.start_new_thread(start_server,(8000,)) #http server
	thread.start_new_thread(start_local_server,(9000,)) #local host server
except:
	print "Error unable create multi theread"

while 1:
	pass
