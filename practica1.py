#!/usr/bin/python3
# -*- coding: utf-8 -*-

import webapp
import csv
import os

class acortador (webapp.webApp):

	url_real={}
	url_acortada={}

	def escribirFichero(self,file, urlreal, urlacortada):
		with open(file, "a") as csvfile:
			write = csv.writer(csvfile)
			write.writerow([int(urlacortada)] + [urlreal])
		return None
	def leerFichero(self,file):
		with open (file,'r') as csvfile:
			if os.stat(file).st_size == 0: #mirar si el fichero esta vacio
				print("No hay urls en el fichero")
				return "Vacio"
			else:
				reader = csv.reader(csvfile)
				for row in reader:
					self.url_acortada[row[1]]= int(row[0])
					self.url_real[row[0]]= row[1]
				return None
	def procesar_cabecera(self, url):
		if("%3A%2F%2F" in url):
			sin_cabecera = url.split("%3A%2F%2F")
			valor_completo = sin_cabecera[0] + "://" + sin_cabecera[1]
		else:
			valor_completo = "http://" + url
		return valor_completo

	def parse(self,request):
		if not request:
			return '','',''
		method = request.split(" ",1)[0]
		resource = request.split(" ",2)[1][1:]
		body = request.split("\r\n\r\n")[1]
		return method,resource,body

	def quitar_barras(self,url):
		fracciones=url.split("%2F")
		respuesta =""
		vuelta = 1
		for fraccion in fracciones:
			if vuelta == len(fracciones):
				respuesta += fraccion
				break;
			vuelta += 1
			respuesta += fraccion + "/"
		return respuesta

	def imprimir_diccionario(self):
		response = ""
		numero = 0
		while numero < len(self.url_real):
			response += "URL real: <a href=" + self.url_real[str(numero)]
			response += ">" + self.url_real[str(numero)] + "</a>"
			response += " -> URL acortada: <a href=" 'http://localhost:1234/'
			response += str(numero) + ">http://localhost:1234/"
			response += str(numero) + "</a><br>"
			numero += 1
		return response

	def process(self, parsedRequest):
		(method,resource,body)= parsedRequest
		#formulario
		persistencia = 0
		self.leerFichero('urls.csv')
		for ult_linea in self.url_real:
			if int(ult_linea) >= persistencia:
				persistencia = int(ult_linea) + 1
		if method == "GET":
			print ("RESOURCE: "+ str(resource))
			if resource != "":
				if resource in self.url_real:
					returnCode = "200 Ok"
					response = "<html><head><meta http-equiv='refresh' content='1;"
					response += "url=" + self.url_real[resource]
					response += "'></head>" + "<body></body></html>\r\n"
				else:
					returnCode = "404 NOT FOUND"
					response = "<html><body>Recurso no disponible<br>"
					response += "<a href='/'>Inicio</a></body></html>"
			else:
				formulario="""
				<form action="/" method="post">
				<p>Introduce la Url <input type="text" name="url"/></p>
				<p><input type="submit" value="Enviar"/></p>
				</form>
				"""
				returnCode = "200 OK"
				urls_acortadas=self.imprimir_diccionario()
				response = "<html><body>" + formulario + urls_acortadas + "</body></html>"
		elif method == "POST":
			form = body.split('=')
			if form[0] == "url":
				valor_url=form[1]
				if valor_url != "":
					url_cabecera=self.procesar_cabecera(valor_url)
					url = self.quitar_barras(url_cabecera)
					if not url in self.url_acortada:
						self.escribirFichero('urls.csv', url, persistencia)
						self.leerFichero('urls.csv')
						returnCode = "200 OK"
						response = "<html><body>URL original: <a href=" + url
						response += ">" + url + "</a>"
						response += " -> URL acortada: <a href=" 'http://localhost:1234/'
						response += str(self.url_acortada[url]) + ">http://localhost:1234/"
						response += str(self.url_acortada[url])
						response += "<br><a href='/'>Inicio</a></body></html>"
					else:
						returnCode = "200 OK"
						response = "<html><body>URL original: <a href=" + url
						response += ">" + url + "</a>"
						response += " -> URL acortada: <a href=" 'http://localhost:1234/'
						response += str(self.url_acortada[url]) + ">http://localhost:1234/"
						response += str(self.url_acortada[url]) + "</a>"
						response += "</body></html>"
				else:
					returnCode = "403 Invalid"
					response = "<html><body>Introduce una URL<br>"
					response += "<a href='/'>Inicio</a></body></html>"
			else:
				returnCode = "404 NOT FOUND"
				response = "invalid qs"
		else:
			returnCode = "404 NOT FOUND"
			response = "invalid method"
		return (returnCode, response)
		
if __name__ == "__main__":
	testWebApp = acortador("localhost", 1234)
