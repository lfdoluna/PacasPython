#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:37:11 2020
Archivo: runSerPacas.pyw
Comentario: GUI para el sericio de impresión de tickets de sistema
de pacas
@author: LFLQ
"""

import Tkinter as tk
import tkMessageBox
from SerPacas import *

class runSerPacas():
	"""docstring for runSerPacas"""
	def __init__(self):
		self.usuarioMaquina = 'lfdlu'
		self.password = 'ArchiPass'
		self.list_obj = []
		self.list_obj.append(1)
		self.num = 0
		self.inicio()

	def cerrar(self):
		self.ventanaPass = tk.Toplevel(self.list_obj[self.num])
		self.ventanaPass.title('Inserte la contraseña')
		self.ventanaPass.geometry("150x100")
		tk.Label(self.ventanaPass, text="Contraseña * ").pack()
		self.entrada_login_clave = tk.Entry(self.ventanaPass, textvariable=self.verifica_clave, show= '*')
		self.entrada_login_clave.pack()
		tk.Label(self.ventanaPass, text="").pack()
		tk.Button(self.ventanaPass, text="Acceder", width=10, height=1, command = self.verifica_login).pack()

	def verifica_login(self):
		claveUser = self.verifica_clave.get()
		print (claveUser + ' ' + self.password)
		self.entrada_login_clave.delete(0, tk.END)
		if self.password in claveUser:
			tkMessageBox.showinfo(message="¡Exito!", title="Ingreso correcto")
			print 'hola'
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

	def inicio(self):
		self.list_obj[self.num] = tk.Tk()      # Creamos una instancia widget ventana de Tk
		self.list_obj[self.num].title('Servicio de impresión Pacas')
		self.verifica_clave = tk.StringVar()
		self.list_obj[self.num].geometry('270x200')
		self.list_obj[self.num].resizable(0,0)
		app = SerPacas(self.list_obj[self.num], self.usuarioMaquina)
		self.list_obj[self.num].protocol("WM_DELETE_WINDOW", self.cerrar)
		self.list_obj[self.num].mainloop()

g = runSerPacas()
#wdg.destroy()