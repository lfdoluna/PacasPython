#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 16:38:52 2020
Archivo: Imprime.py
Comentarios: Archivo para la descarga e impresión de los tkicets
generados por el alta de pacas de compactadora
@author: LFLQ
"""

import Tkinter as tk


def update_label():
    var.set("No cierre" if var.get() == "la ventana" else "la ventana")
    l.after(1000, update_label)

root = tk.Tk()
root.geometry("300x100")
var = tk.StringVar()
var.set('No cierre')

l = tk.Label(root, textvariable=var, fg="#660066", font=(None, 30))
l.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
update_label()
root.mainloop()