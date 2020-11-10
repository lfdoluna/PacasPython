#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:44:36 2020
Archivo: SerPacas.py
Comentario: Archivo constructor del contenido de la ventana
para el servicio de impresión de los tickets de pacas
@author: LFLQ
Versión: 3.0
"""

from datetime import datetime, date
import Tkinter as tk
import subprocess
import psycopg2
import time
import sys	
import os

class SerPacas(object):
	"""docstring for SerPacas"""
	def __init__(self, maestro, user):
		# Creamos el marco donde se dibujará el contenido de la ventana
		self.marcoM = maestro

		# Inicialización variables
		horaStart = datetime.now()
		self.prox_folio = 0
		self.prox_folioN= 1
		self.flagEdo = True
		self.flagEdoRprtPcs = False
		self.manana = horaStart.day + 1
		horaStart = horaStart.strftime('%m/%d/%Y, %H:%M:%S')
		self.master = maestro
		self.userM = user
		self.varUltPStr = tk.StringVar()
		self.varProPStr = tk.StringVar()
		self.varEdoPStr = tk.StringVar()
		self.varHorPStr = tk.StringVar()
		self.varHorPStr.set(horaStart)
		self.sqlquery = "SELECT max(id_paca) AS ultima_paca FROM pacas;"
		try:
			self.prox_folio = self.ConsultaDB(self.sqlquery)
			self.varUltPStr.set('Ultimo folio: ' + str(self.prox_folio[0]) + ' a las ' + horaStart)
			self.varProPStr.set('Proximo folio: ' + str(self.prox_folio[0] + 1))
			self.varEdoPStr.set('No cierre la ventana')
			self.prox_folioN = self.prox_folio[0] + 1
		except Exception as e:
			print e
			self.varUltPStr.set('Ultimo folio: ' + 'Sin datos' + ' a las ' + horaStart)
			self.varProPStr.set('Proximo folio: ' + 'Sin datos')
			self.varEdoPStr.set('No cierre la ventana')

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
		try:
			ahora = datetime.now()
			ahoraC = ahora.strftime('%H:%M:%S')
			self.actual_folio = self.ConsultaDB(self.sqlquery)
			#print self.actual_folio[0]
			self.varHorPStr.set(ahoraC)
			if self.actual_folio[0] == self.prox_folioN:
				queryTipo_Paca = "SELECT tipo_paca FROM pacas where id_paca = {};".format(self.actual_folio[0])
				self.tipo_paca = self.ConsultaDB(queryTipo_Paca)
				if self.tipo_paca[0] != 'GRANEL':
					ahor = datetime.now()
					ahoraD = ahor.strftime('%m/%d/%Y, %H:%M:%S')
					self.sqlqueryData = "SELECT fecha, kilogramos, tipo_paca FROM pacas WHERE id_paca = {};".format(self.actual_folio[0])
					data = self.ConsultaDB(self.sqlqueryData)
					p = subprocess.Popen('C:\PacasPythonXP\wget.exe -O C:\PacasPythonXP\Ticket_de_Pacas{}.pdf -c "http://192.168.5.243/merma/__extensions/tcpdf/examples/ticket.paca.php?fecha={}&peso={}&tipopaca={}&codigo={}"'.format(self.actual_folio[0],data[0],data[1],data[2],self.actual_folio[0]), 
										stdout=subprocess.PIPE, 
										shell=True)
					self.varEdoPStr.set('Llamando a printerPacas....')
					print 'Llamando a printerPacas....'
					subprocess.call('python c:\PacasPythonXP\printerPacas.py')
				self.prox_folioN = self.actual_folio[0] + 1
				self.varProPStr.set('Proximo folio: ' + str(self.actual_folio[0] + 1))
				self.varUltPStr.set('Ultimo folio: ' + str(self.actual_folio[0]) + ' a las ' + ahoraD)
			self.deletePDF()
			self.CheakDay()
			if self.flagEdo == False:
				self.flagEdo = True
				self.varEdoPStr.set('Conexión exitosa')
				self.actual_folio = self.ConsultaDB(sqlquery)
				self.prox_folioN = self.actual_folio[0] + 1
				self.varProPStr.set('Proximo folio: ' + str(self.actual_folio[0] + 1))
				self.varUltPStr.set('Ultimo folio: ' + str(self.actual_folio[0]) + ' a las ' + ahoraC)
		except:
			print ('Error inesperado: ' , sys.exc_info()[0])
		finally:
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
			self.varEdoPStr.set("Error de base de datos")
			self.flagEdo = False
			pass

		finally:
			try:
			    if (cur):
			        cur.close()
			    if (conn):
			        conn.close()
				#print ('Consulta exitosa **' + consulta + '**')
				return resultado
			except:
				pass

	def CheakDay(self):
		now = datetime.now()
		if (now.strftime('%w, %H:%M') == '5, 09:00') and (int(now.strftime('%U'))%2 != 0) and (self.flagEdoRprtPcs == False):
			self.varEdoPStr.set('Llamando a RprtPcs.py .....')
			pR = subprocess.Popen('python c:\PacasPythonXP\RprtPcs.py', 
	                              stdout=subprocess.PIPE, 
	                              shell=True)
			self.flagEdoRprtPcs = True
		elif (now.strftime('%w, %H:%M') == '5, 09:01') and (self.flagEdoRprtPcs == True):
			self.flagEdoRprtPcs = False

	def deletePDF(self):
		dimeDia = datetime.now()
		if dimeDia.day == self.manana:
			print ('Eliminando archivos PDF del día :' + str(dimeDia.day - 1))
			# Eliminar archivos
			pZ = subprocess.Popen('del /f C:\PacasPythonXP\*Ticket_de_Pacas*.pdf', 
                                stdout=subprocess.PIPE, 
                                shell=True)
			self.manana = dimeDia.day + 1
