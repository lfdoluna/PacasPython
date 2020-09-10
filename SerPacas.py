#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:44:36 2020
Archivo: SerPacas.py
Comentario: Archivo constructor del contenido de la ventana
para el servicio de impresión de los tickets de pacas
@author: LFLQ
"""

import subprocess
import time
import os
import Tkinter as tk
import psycopg2
from datetime import datetime

class SerPacas(object):
	"""docstring for SerPacas"""
	def __init__(self, maestro, user):
		# Creamos el marco donde se dibujará el contenido de la ventana
		self.marcoM = maestro

		# Inicialización variables
		horaStart = datetime.now()
		self.manana = horaStart.day + 1
		horaStart = horaStart.strftime('%H:%M:%S')
		self.master = maestro
		self.userM = user
		self.varUltPStr = tk.StringVar()
		self.varProPStr = tk.StringVar()
		self.varEdoPStr = tk.StringVar()
		self.varHorPStr = tk.StringVar()
		sqlquery = "SELECT max(id_paca) AS ultima_paca FROM pacas;"
		self.prox_folio = self.ConsultaDB(sqlquery)
		self.varUltPStr.set('Ultimo folio: ' + str(self.prox_folio[0]) + ' a las ' + horaStart)
		self.varProPStr.set('Proximo folio: ' + str(self.prox_folio[0] + 1))
		self.varEdoPStr.set('No cierre la ventana')
		self.varHorPStr.set(horaStart)
		self.prox_folioN = self.prox_folio[0] + 1

		# Inicialización contenido ventana
		tk.Label(self.marcoM, text = '*******************************************').grid(row = 0, column = 0, columnspan = 2)
		tk.Label(self.marcoM, text = 'Hora de inicio del programa: {}'.format(horaStart)).grid(row = 1, column = 0, columnspan = 2)
		tk.Label(self.marcoM, text = '*******************************************').grid(row = 2, column = 0, columnspan = 2)
		self.proxL = tk.Label(self.marcoM, textvariable = self.varProPStr)
		self.proxL.grid(row = 3, column = 0, columnspan = 2)
		tk.Label(self.marcoM, text = '*******************************************').grid(row = 4, column = 0, columnspan = 2)
		self.ultmL = tk.Label(self.marcoM, textvariable = self.varUltPStr)
		self.ultmL.grid(row = 5, column = 0, columnspan = 2)
		tk.Label(self.marcoM, text = '*******************************************').grid(row = 6, column = 0, columnspan = 2)
		self.edoLa = tk.Label(self.marcoM, textvariable = self.varEdoPStr)
		self.edoLa.grid(row = 7, column = 0)
		self.horaLa = tk.Label(self.marcoM, textvariable = self.varHorPStr)
		self.horaLa.grid(row = 7, column = 1)

		#Llamamos ciclo infinito
		self.loopPacas()

	def loopPacas(self):
		ahora = datetime.now()
		ahoraC = ahora.strftime('%H:%M:%S')
		sqlquery = "SELECT max(id_paca) AS ultima_paca FROM pacas;"
		self.actual_folio = self.ConsultaDB(sqlquery)
		#print self.actual_folio[0]
		self.varHorPStr.set(ahoraC)
		if self.actual_folio[0] == self.prox_folioN:
			ahor = datetime.now()
			ahora = ahor.strftime('%H:%M:%S')
			sqlquery = "SELECT fecha, kilogramos, tipo_paca FROM pacas WHERE id_paca = {};".format(self.actual_folio[0])
			data = self.ConsultaDB(sqlquery)
			p = subprocess.Popen('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "http://192.168.5.243/merma/__extensions/tcpdf/examples/ticket.paca.php?fecha={}&peso={}&tipopaca={}&codigo={}"'.format(data[0],data[1],data[2],self.actual_folio[0]), 
                                stdout=subprocess.PIPE, 
                                shell=True)
			self.varEdoPStr.set('Llamando a printerPacas....')
			print 'Llamando a printerPacas....'
			subprocess.call('python c:\PacasPython\printerPacas.py')
			self.prox_folioN = self.actual_folio[0] + 1
			self.varProPStr.set('Proximo folio: ' + str(self.actual_folio[0] + 1))
			self.varUltPStr.set('Ultimo folio: ' + str(self.actual_folio[0]) + ' a las ' + ahora)
		self.deletePDF()
		self.proxL.after(1000, self.loopPacas)

	def ConsultaDB(self, consulta):
		# Postgres
		PSQL_HOST = "192.168.5.243"
		PSQL_PORT = "5432"
		PSQL_USER = "postgres"
		PSQL_PASS = "bi"
		PSQL_DB   = "merma"
		try:
			connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
			conn = psycopg2.connect(connstr)
			cur = conn.cursor()
			cur.execute(consulta)
			resultado = cur.fetchone()

		except Exception as e:
			print("Error de base de datos")
			raise e

		finally:
		    if (cur):
		        cur.close()
		    if (conn):
		        conn.close()
			#print ('Consulta exitosa **' + consulta + '**')
			return resultado

	def cerrar(self):
		print "No" 

	def deletePDF(self):
		dimeDia = datetime.now()
		if dimeDia.day == self.manana:
			print ('Eliminando archivos PDF del día :' + str(dimeDia.day - 1))
			# Eliminar archivos
			pZ = subprocess.Popen('del /f c:\Users\{}\Downloads\*Ticket_de_Pacas*.pdf'.format(self.userM), 
                                stdout=subprocess.PIPE, 
                                shell=True)
			self.manana = dimeDia.day + 1