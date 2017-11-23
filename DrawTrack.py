#!/usr/bin/python
#coding:utf-8

import urllib
import os
import json
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import SocketServer
import thread,time

i = 0;
data = [{'jingdu':117.27,'weidu':31.86},{'jingdu':117.16,'weidu':32.47},{'jingdu':116.98,'weidu':32.62},{'jingdu':118.38,'weidu':31.33}]
#data = {}
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
		#	data = {'jingdu':12,'weidu':35} #dict 
			global i		
			
			json_str = json.dumps(data[i])
			i = (i + 1) % 4
			print "json:",json_str


			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write(json_str)

		return

class localHostServer(SocketServer.BaseRequestHandler):

		def handle(self):
			
			conn = self.request
			ret_bytes = conn.recv(1024)
			print ret_bytes
			# data["jingdu"] = 110
			# data["weidu"] = 34
			

def start_server(port):
	http_server = HTTPServer(('', int(port)), HTTPHandler)
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
