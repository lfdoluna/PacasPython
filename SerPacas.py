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
from subprocess import check_output
from SerFctr import *
try:
	import Tkinter as tk
except Exception as e:
	import tkinter as tk
import subprocess
import psycopg2
import time
import sys	
import os

class SerPacas(object):
	"""
	Clase que implementa una ventana donde mostrará el estatus de la impresión de los tickets generados por la báscula de merma
	"""
	def __init__(self, maestro, user, instADR, nomImpre):
		# Creamos el marco donde se dibujará el contenido de la ventana
		self.marcoM = maestro

		# Inicialización variables
		self.dirRAIZ = r'C:\PacasPython'
		self.dirLOGimpr = r'{0}\Resources\ImprPcs.log'.format(self.dirRAIZ)
		self.dirLOGpacs = r'{0}\Resources\Pacas.log'.format(self.dirRAIZ)
		if os.path.isfile(self.dirLOGimpr):
			self.banLOGimpr = True
		if os.path.isfile(self.dirLOGpacs):
			self.banLOGpacs = True
		if not(os.path.isfile(self.dirLOGpacs)):
			self.banLOGpacs = False
		if not(os.path.isfile(self.dirLOGimpr)):
			self.banLOGimpr = False
		self.progAR = instADR
		self.nomIMP = nomImpre
		horaStart = datetime.now()
		self.prox_folio = 0
		self.numFAC = 0
		self.banFAC = False
		self.QUERYmaxPcCmn = 'SELECT max(id_pacas_camion) FROM pacas_camion;'
		pacFAC = self.ConsultaDB(self.QUERYmaxPcCmn)
		self.pacFAC = pacFAC[0]
		self.prox_folioN= 1
		self.flagEdo = True
		self.flagEdoRprtPcs = False
		self.manana = horaStart.day + 1
		horaStart = horaStart.strftime('%d/%m/%Y, %H:%M:%S')
		self.WrReLOG('Hora de inicio del programa: ' + horaStart + os.linesep, self.dirLOGpacs, self.banLOGpacs)
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
			self.folio_anterior = self.prox_folio[0]
		except Exception as e:
			print(e)
			self.WrReLOG(str(e) + '\n', self.dirLOGpacs, self.banLOGpacs)
			self.varUltPStr.set('Ultimo folio: ' + 'Sin datos' + ' a las ' + horaStart)
			self.varProPStr.set('Proximo folio: ' + 'Sin datos')
			self.varEdoPStr.set('No cierre la ventana')

		# Inicialización contenido ventana
		tk.Label(self.marcoM, text = '*******************************************').grid(row = 0, column = 0, columnspan = 2)
		tk.Label(self.marcoM, text = 'Hora de inicio del programa: {0}'.format(horaStart)).grid(row = 1, column = 0, columnspan = 2)
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
			self.ahora = datetime.now()
			self.ahoraC = self.ahora.strftime('%H:%M:%S')
			self.actual_folio = self.ConsultaDB(self.sqlquery)
			#print self.folio_anterior
			self.varHorPStr.set(self.ahoraC)
			if ((self.actual_folio[0] == self.prox_folioN) or (self.actual_folio[0] != self.folio_anterior)) and False:
				queryTipo_Paca = "SELECT tipo_paca FROM pacas where id_paca = {0};".format(self.actual_folio[0])
				self.tipo_paca = self.ConsultaDB(queryTipo_Paca)
				fileName = r"{1}\Resources\Ticket_de_Pacas{0}.pdf".format(self.actual_folio[0], self.dirRAIZ)
				if self.tipo_paca[0] != 'GRANEL' and not(os.path.isfile(fileName)):
					self.sqlqueryData = "SELECT fecha, kilogramos, tipo_paca FROM pacas WHERE id_paca = {0};".format(self.actual_folio[0])
					data = self.ConsultaDB(self.sqlqueryData)
					# Descarga el ticket
					subprocess.Popen(r'{4}\wget.exe -O {4}\Resources\Ticket_de_Pacas{0}.pdf -c "http://192.168.5.243/merma/__extensions/tcpdf/examples/ticket.paca.php?fecha={1}&peso={2}&tipopaca={3}&codigo={0}"'.format(self.actual_folio[0],data[0],data[1],data[2], self.dirRAIZ), 
										stdout=subprocess.PIPE, 
										shell=True)
					self.varEdoPStr.set('Llamando a printerPacas....')
					print('Llamando a printerPacas....')
					self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + 'Llamando a printerPacas....' + '\n', self.dirLOGpacs, self.banLOGpacs)
					# Imprime el tiket
					subprocess.Popen(r'"{1}"  /n /s /h /t "{0}" "{2}"'.format(fileName, self.progAR, self.nomIMP), stdout=subprocess.PIPE, shell=True)
					print('**********************----')
					self.WrReLOG('**********************' + '\n', self.dirLOGimpr, self.dirLOGimpr)
					print (fileName)
					self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + (fileName) + '\n', self.dirLOGimpr, self.dirLOGimpr)
					print('**********************----')
				self.prox_folioN = self.actual_folio[0] + 1
				self.folio_anterior = self.actual_folio[0]
				self.varProPStr.set('Proximo folio: ' + str(self.actual_folio[0] + 1))
				ahoraD = self.ahora.strftime('%d/%m/%Y, %H:%M:%S')
				self.varUltPStr.set('Ultimo folio: ' + str(self.actual_folio[0]) + ' a las ' + ahoraD)
			self.CheakTime(self.ahora)
			# Reconexión en caso de haber fallo de internet
			if self.flagEdo == False:
				self.flagEdo = True
				self.varEdoPStr.set('Conexión exitosa')
				self.actual_folio = self.ConsultaDB(self.sqlquery)
				self.prox_folioN = self.actual_folio[0] + 1
				self.varProPStr.set('Proximo folio: ' + str(self.actual_folio[0] + 1))
				self.varUltPStr.set('Ultimo folio: ' + str(self.actual_folio[0]) + ' a las ' + self.ahoraC)
		except Exception as e:
			self.varEdoPStr.set('Error inesperado dentro loopPacas')
			print ('Error inesperado dentro loopPacas: ', e)
			self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + 'Error inesperado dentro loopPacas: ' + str(e) + '\n', self.dirLOGimpr, self.dirLOGimpr)
		finally:
			self.proxL.after(1000, self.loopPacas)

	def CheakIP(self):
		"""
		Método para el checar si la maquina virtual de corrugadora funciona
		"""
		try:
			check_output('ping -w 50 -n 1 192.168.5.170', shell=True)
			band = True
		except Exception as e:
			self.varEdoPStr.set('Máquina virtual desconectada')
			print ('Máquina virtual desconectada ', e)
			self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + str('Máquina virtual desconectada '+ e) + '\n', self.dirLOGimpr, self.dirLOGimpr)
			band = False
		finally:
			return band

	def ConsultaDB(self, consulta):
		'''
		Función que devuelve una tupla y realiza una consulta en la base de datos 'merma'
		* consulta(str) = Consulta que se requiere, recuerde guardar el valor en una variable
		'''
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
			self.varEdoPStr.set("Error en la consulta de la base de datos")
			print("Error en la consulta de la base de datos", e)
			self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + "Error en la consulta de la base de datos" + str(e) + '\n', self.dirLOGpacs, self.banLOGpacs)
			self.flagEdo = False
			pass

		finally:
			try:
				if (cur):
					cur.close()
				if (conn):
					conn.close()
				return resultado
			except:
				pass

	def CheakTime(self, tiempoDT):
		'''
		Función para llamar los diversas tareas asignadas a determinada hora o fecha
		* tiempoDT(obj): objeto de la clase datetime.now()
		'''
		# Envia reporte de entradas de pacas
		if (tiempoDT.strftime('%w, %H:%M') == '5, 09:00') and (int(tiempoDT.strftime('%U'))%2 != 0) and (self.flagEdoRprtPcs == False):
			self.varEdoPStr.set('Llamando a RprtPcs.py .....')
			subprocess.Popen(r'python {0}\RprtPcs.py'.format(self.dirRAIZ), 
	                              stdout=subprocess.PIPE, 
	                              shell=True)
			self.flagEdoRprtPcs = True
		elif (tiempoDT.strftime('%w, %H:%M') == '5, 09:01') and (self.flagEdoRprtPcs == True):
			self.flagEdoRprtPcs = False
		# Eliminar archivos
		elif tiempoDT.day == self.manana:
			print ('Eliminando archivos PDF del día :' + str(tiempoDT.day - 1))
			self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + str('Eliminando archivos PDF del día :' + str(tiempoDT.day - 1)) + '\n', self.dirLOGpacs, self.banLOGpacs)
			subprocess.Popen(r'del /f {0}\Resources\*Ticket_de_Pacas*.pdf'.format(self.dirRAIZ), 
                                stdout=subprocess.PIPE, 
                                shell=True)
			self.manana = tiempoDT.day + 1
		elif int(tiempoDT.strftime('%S'))%15 == 0:
			pacFAC = self.ConsultaDB(self.QUERYmaxPcCmn)
			# print(str(self.banFAC), self.pacFAC)
			if ((pacFAC[0] != self.pacFAC) and self.banFAC == False):
				query0 = 'SELECT camion_id FROM pacas_camion WHERE id_pacas_camion = {0};'.format(pacFAC[0])
				dat0 = self.ConsultaDB(query0)
				print(dat0[0])
				query1 = 'SELECT factura_id FROM factura_pacas_camion WHERE pacas_camion_id = {0};'.format(pacFAC[0])
				dat1 = self.ConsultaDB(query1)
				print(dat1[0])
				datos = [dat0[0], dat1[0]]
				self.banFAC = True
				self.ventFAC = tk.Toplevel(self.marcoM)
				self.ventFAC.title('Servicio de impresión de la prefactura')
				self.ventFAC.geometry('270x200')
				self.ventFAC.resizable(0,0)
				self.h = SerFctr(self.ventFAC, self.userM, self.progAR, 'ImpresoraFacturacion', datos)
			else:
				if self.h.banFct == False:
					self.ventFAC.destroy()
					self.banFAC = False
					pacFAC = self.ConsultaDB(self.QUERYmaxPcCmn)
					self.pacFAC = pacFAC[0]

	def WrReLOG(self, txt, dirLOG, bandExis):
		"""
		Método para la lectura y escritura de un archivo LOG ocupado para el registro de los eventos en el sistema
		* txt(string) = Texto que se desea agregar al archivo.
		* dirLOG(string) = Directorio del archivo.
		* bandExis(bool) = Bandera para checar si existe o no dicho archivo.
		"""
		if bandExis == False:
			objFichLOG = open(dirLOG, 'w')
			bandExis = True
		else:
			objFichLOG = open(dirLOG, 'a')
		objFichLOG.write(txt)
		objFichLOG.close()