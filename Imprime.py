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
import psycopg2
import time
import os

userM = 'lfdlu'

# Postgres
PSQL_HOST = "192.168.5.243"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASS = "bi"
PSQL_DB   = "merma"
connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
conn = psycopg2.connect(connstr)

cur = conn.cursor()

sqlquery = "SELECT max(id_paca) AS ultima_paca FROM pacas;"
cur.execute(sqlquery)

prox_folio = cur.fetchone()
prox_folioN = prox_folio[0] + 1
print '**********************'
print ('Proximo folio: ' + str(prox_folioN))
print '**********************'

cur.close()
conn.close()

while True:
    try:
        # Conectarse a la base de datos
        connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
        conn = psycopg2.connect(connstr)
        
        # Abrir un cursor para realizar operaciones sobre la base de datos
        cur = conn.cursor()

        # Ejecutar una consulta SELECT
        sqlquery = "SELECT max(id_paca) AS ultima_paca FROM pacas;"
        cur.execute(sqlquery)
        # Obtener los resultados como objetos Python
        ultima_paca = cur.fetchone()
        ultima_pacaN = ultima_paca[0]
        print ('Folio actual: ' + str(ultima_paca[0]))

        if ultima_pacaN == prox_folioN:
            sqlquery = "SELECT fecha, kilogramos, tipo_paca FROM pacas WHERE id_paca = {};".format(ultima_pacaN)
            cur.execute(sqlquery)
            data = cur.fetchone()
            p = subprocess.Popen('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "http://192.168.5.243/merma/__extensions/tcpdf/examples/ticket.paca.php?fecha={}&peso={}&tipopaca={}&codigo={}"'.format(data[0],data[1],data[2],ultima_pacaN), 
                                stdout=subprocess.PIPE, 
                                shell=True)
            print '**********************'
            print ('Proximo folio: ' + str(ultima_pacaN))
            print '**********************'
            while os.path.isfile("C:\Users\{}\Downloads\Ticket_de_Pacas{}.pdf".format(userM, ultima_pacaN))==True:
                print 'No'
            fileP = 'C:\Users\{}\Downloads\Ticket_de_Pacas{}.pdf'.format(userM, ultima_pacaN)
            subprocess.call('python c:\PacasPython\printerPacas.py')
            prox_folioN = ultima_pacaN + 1

    except KeyboardInterrupt:
        break
        print ('Salida')
        
    except:
        print("Error de base de datos")
        
    finally:
        if (cur):
            cur.close()
            print "Cursor cerrado"
        if (conn):
            conn.close()
            print("The SQLite connection is closed at " + time.ctime())
            print '\n******************************************************'
            time.sleep(5)