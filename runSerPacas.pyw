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
from SerPacas import *

usuarioMaquina = 'lfdlu'

wdg = tk.Tk()      # Creamos una instancia widget ventana de Tk
wdg.title('Servicio de impresión Pacas')
wdg.geometry('300x300')
#wdg.resizable(False)
app = SerPacas(wdg, usuarioMaquina)
wdg.protocol("WM_DELETE_WINDOW", app.cerrar)
wdg.mainloop()
#wdg.destroy()