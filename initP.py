#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:38:52 2020
Archivo: Imprime.py
Comentarios: Archivo para la descarga e impresión de los tkicets
generados por el alta de pacas de compactadora
@author: LFLQ
"""

import subprocess 
import time


p = subprocess.Popen('python c:\PacasPython\RunSerPacas.pyw', 
                                stdout=subprocess.PIPE, 
                                shell=True)
time.sleep(5)