#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:37:11 2020
Archivo: runSerPacas.pyw
Comentario: GUI para el sericio de impresión de tickets de sistema
de pacas
@author: LFLQ
"""

from SerPacas import *
try:
	import Tkinter as tk
	import tkMessageBox
except Exception as e:
	import tkinter as tk
	from tkinter import messagebox as tkMessageBox
import getpass

class runSerPacas(object):
	"""docstring for runSerPacas"""
	def __init__(self):
		self.AR_prog = r'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe'
		# self.dirRAIZ = r'C:\PacasPython'
		# subprocess.Popen(r'"{1}"  /n /s /h /t "{0}\Resources\Pre-factura462.pdf" "ImpresoraFacturacion"'.format(self.dirRAIZ, self.AR_prog))
		self.Impresora = 'Brother QL-800'
		self.usuarioMaquina = getpass.getuser()
		self.password = 'ArchiPass'
		self.list_obj = []
		self.list_obj.append(1)
		self.num = 0
		self.inicio()

	def cerrar(self):
		self.ventanaPass = tk.Toplevel(self.list_obj[self.num])
		self.ventanaPass.title('Inserte la contraseña')
		self.ventanaPass.geometry("150x100-5-50")
		self.ventanaPass.resizable(0,0)
		tk.Label(self.ventanaPass, text="Contraseña * ").pack()
		self.entrada_login_clave = tk.Entry(self.ventanaPass, textvariable=self.verifica_clave, show= '*')
		self.entrada_login_clave.pack()
		self.entrada_login_clave.focus()
		tk.Label(self.ventanaPass, text="").pack()
		tk.Button(self.ventanaPass, text="Acceder", width=10, height=1, command = self.verifica_login).pack()
		self.ventanaPass.bind('<Return>', self.verifica_loginE)
		self.ventanaPass.focus_set()
		self.ventanaPass.attributes("-topmost", 1)	

	def verifica_login(self):
		claveUser = self.verifica_clave.get()
		print (claveUser + ' ' + self.password)
		self.entrada_login_clave.delete(0, tk.END)
		if self.password in claveUser:
			tkMessageBox.showinfo(message="¡Exito!", title="Ingreso correcto")
			print('hola')
			self.list_obj[self.num].destroy()
			self.list_obj.append(1)
			self.num += 1
			self.inicio()
		else:
			flagC = tkMessageBox.askretrycancel(message="Contraseña incorrecta, ¿Desea reintentar?", title="Error")
			if flagC == False:
				self.ventanaPass.destroy()
			else:
				self.ventanaPass.deiconify()

	def verifica_loginE(self, event):
		claveUser = self.verifica_clave.get()
		print (claveUser + ' ' + self.password)
		self.entrada_login_clave.delete(0, tk.END)
		if self.password in claveUser:
			tkMessageBox.showinfo(message="¡Exito!", title="Ingreso correcto")
			print('hola')
			self.list_obj[self.num].destroy()
			self.list_obj.append(1)
			self.num += 1
			self.inicio()
		else:
			flagC = tkMessageBox.askretrycancel(message="Contraseña incorrecta, ¿Desea reintentar?", title="Error")
			if flagC == False:
				self.ventanaPass.destroy()
			else:
				# self.ventanaPass.deiconify()
				self.entrada_login_clave.focus()


	def inicio(self):
		self.list_obj[self.num] = tk.Tk()      # Creamos una instancia widget ventana de Tk
		self.list_obj[self.num].title('Servicio de impresión Pacas')
		self.verifica_clave = tk.StringVar()
		self.list_obj[self.num].geometry('270x200-5-40')
		self.list_obj[self.num].resizable(0,0)
		SerPacas(self.list_obj[self.num], self.usuarioMaquina, self.AR_prog, self.Impresora)
		self.list_obj[self.num].protocol("WM_DELETE_WINDOW", self.cerrar)
		self.list_obj[self.num].bind('<Motion>', self.dentro)
		self.list_obj[self.num].bind('<Leave>', self.fuera)
		self.list_obj[self.num].mainloop()

	def dentro(self, event):
		self.list_obj[self.num].attributes("-alpha", 1)
			
	def fuera(self, event):
		self.list_obj[self.num].attributes("-alpha", 0.25)
		
g = runSerPacas()
#wdg.destroy()
