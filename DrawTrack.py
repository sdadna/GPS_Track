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
gps_data = {}
BaiDuMapData = {}
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
			Error_data = {'Lat':999,'Lon':999}
			if len(BaiDuMapData):
				json_str = json.dumps(BaiDuMapData)
				BaiDuMapData.clear()
			else:
				json_str = json.dumps(Error_data)
			# json_str = json.dumps(data[i])
			# i = (i + 1) % 4
			print "json:",json_str

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
		Lon = self.parseLon(gps_data['Lon'])

		if data['Lon_EW'] == 'W':
			Lon = -Lon
		if data['Lat_NS'] == 'S':
			Lat = -Lat

		return Lat, Lon

	def handle(self):
		
		conn = self.request
		while (1):
			ret_bytes = conn.recv(1024)
			ret_bytes = ret_bytes.replace('\t','')
			ret = ret_bytes.split('\n')
			for string in ret:
				data = string.split(':')
				if(len(data) < 2):
					break
				gps_data[data[0]] = data[1]

			print gps_data
			#Lat		
			Lat, Lon = self.parseGPSData(gps_data)
			BaiDuMapData['Lat'] = Lat
			BaiDuMapData['Lon'] = Lon
		# data['jingdu'] = Lat
		# data['weidu'] = Lon
		#print ret[1], ret[2]
		# data["jingdu"] = 110
		# data["weidu"] = 34
			

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
