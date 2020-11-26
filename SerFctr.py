#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 11:35:05 2020
Archivo: SerFctr.py
Comentarios: GUI para la impresión de la prefactura
@author: pi
"""
from datetime import datetime
try:
	import Tkinter as tk
except Exception as e:
	import tkinter as tk
import subprocess
import psycopg2
import os

class SerFctr(object):
    """
	Clase que implementa una ventana donde mostrará el estatus de la impresión de la prefactura
	"""
    def __init__(self, maestro, user, instADR, nomImpre, data):
        # Creamos el marco donde se dibujará el contenido de la ventana
        self.marcoM = maestro

        # Inicialización variables
        self.dirRAIZ = r'C:\PacasPython'
        self.dirLOGimpr = r'{0}\Resources\ImprFctrs.log'.format(self.dirRAIZ)
        if os.path.isfile(self.dirLOGimpr):
            self.banLOGimpr = True
        else:
            self.banLOGimpr = False
        self.banFct = True
        self.progAR = instADR
        self.nomIMP = nomImpre
        self.datos = data
        horaStart = datetime.now()
        horaStart = horaStart.strftime('%d/%m/%Y, %H:%M:%S')
        self.WrReLOG('Hora de inicio del programa: ' + horaStart + os.linesep, self.dirLOGimpr, self.banLOGimpr)
        self.varEdoPStr = tk.StringVar()
        self.varHorPStr = tk.StringVar()
        self.varHorPStr.set(horaStart)
        self.varEdoPStr.set("Esperando a que termine la baja de pacas")
        tk.Label(self.marcoM, text = '*******************************************').grid(row = 0, column = 0, columnspan = 2)
        tk.Label(self.marcoM, text = 'Hora de inicio del programa: {0}'.format(horaStart)).grid(row = 1, column = 0, columnspan = 2)
        tk.Label(self.marcoM, text = '*******************************************').grid(row = 2, column = 0, columnspan = 2)
        tk.Label(self.marcoM, text = 'Pre-Factura N° {0}'.format(self.datos[1])).grid(row = 3, column = 0, columnspan = 2)
        tk.Label(self.marcoM, text = '*******************************************\n**** ATENCIÓN ****\n Esta ventana se cerrará sola').grid(row = 4, column = 0, columnspan = 2)
        self.h = tk.Label(self.marcoM, textvariable = self.varHorPStr)
        self.h.grid(row = 5, column = 0, columnspan = 2)
        tk.Label(self.marcoM, text = '*******************************************').grid(row = 6, column = 0, columnspan = 2)
        self.edo = tk.Label(self.marcoM, textvariable = self.varEdoPStr)
        self.edo.grid(row = 7, column = 0, columnspan = 2)
        self.loop()
    
    def loop(self):
        """
        Ciclo infitito hasta la impresión de la Pre-Factura
        """
        try:
            self.ahora = datetime.now()
            ahoraC = self.ahora.strftime('%H:%M:%S')
            self.varHorPStr.set(ahoraC)
            query = 'SELECT estado, placas FROM camion WHERE id_camion = {0};'.format(self.datos[0])
            self.edo = self.ConsultaDB(query)
            if self.edo[0] == True and self.banFct == True:
                self.banFct = False
                # DESCARGA PRE-FACTURA
                os.system(r'{0}\wget.exe -O {0}\Resources\Pre-factura{1}.pdf -c "http://192.168.5.243/merma/__extensions/tcpdf/examples/factura.prueba.php?camion={2}&factura={1}"'.format(self.dirRAIZ, self.datos[1], self.edo[1]))
                # IMPRIME PREFACTURA
                subprocess.Popen(r'"{2}"  /n /s /h /t "{0}\Resources\Pre-factura{1}.pdf" "{3}"'.format(self.dirRAIZ, self.datos[1], self.progAR, self.nomIMP))
                self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + "Impresión de la pre-factua {0}".format(self.datos[1]) + '\n', self.dirLOGimpr, self.banLOGimpr)
        except Exception as e:
            e
        finally:
            if self.banFct == False:
                print('cerrar')
            else:
                self.marcoM.after(1000, self.loop)

    def ConsultaDB(self, consulta):
        '''
        Función que devuelve una tupla y realiza una consulta en la base de datos 'merma'
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
            self.WrReLOG(self.ahora.strftime('%d/%m/%Y, %H:%M:%S ') + "Error en la consulta de la base de datos" + str(e) + '\n', self.dirLOGimpr, self.banLOGimpr)
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

# app = tk.Tk()
# app.title('Impresión pruebas')
# app.geometry('270x200')
# SerFctr(app, 'lfdo', r'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe', 'ImpresoraFacturacion', [7, 366])
# app.mainloop()