#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:08:40 2020
Archivo: ImprimeTP.py
Comentarios: Archivo para la descarga e impresión de los tkicets
generados por el alta de pacas de compactadora
@author: LFLQ
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 10:08:40 2020
Archivo: ImprimeTP.py
Comentarios: Archivo para la descarga e impresión de los tkicets
generados por el alta de pacas de compactadora
@author: LFLQ
"""

import subprocess
import psycopg2
import time

# # Linea para mandar a imprimir
# fileP = 'C:\Users\lfdlu\Desktop\Ticket_de_Pacas.pdf'
# p = subprocess.Popen('"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"  /n /s /h /t "{}" "Brother QL-800"'.format(fileP), 
# 	stdout=subprocess.PIPE, 
# 	shell=True)


# Postgres
PSQL_HOST = "192.168.5.243"
PSQL_PORT = "5432"
PSQL_USER = "postgres"
PSQL_PASS = "bi"
PSQL_DB   = "merma"
# connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
# conn = psycopg2.connect(connstr)

# cur = conn.cursor()

# sqlquery = "SELECT max(id_paca) AS ultima_paca FROM pacas;"
# cur.execute(sqlquery)

# prox_folio = cur.fetchone()
# prox_folioN = prox_folio[0] + 1
# print '**********************----'
# print ('Proximo folio: ' + str(prox_folioN))
# print '**********************----'

# cur.close()
# conn.close()

if True:
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
        time.sleep(5)

        if ultima_pacaN == ultima_pacaN:
        #if True:
        	fileP = 'C:\Users\lfdlu\Downloads\Ticket_de_Pacas{}.pdf'.format(ultima_pacaN)
        	p = subprocess.Popen('"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"  /n /s /h /t "{}" "Brother QL-800"'.format(fileP), 
								stdout=subprocess.PIPE, 
								shell=True)
        	# Imprime el tiket
        	prox_folioN = ultima_pacaN + 1
        	print '**********************----'
        	print (fileP)
        	print '**********************----'

    except:
        print("Error de base de datos")
        
    finally:
        if (cur):
            cur.close()
            print "Cursor cerrado"
        if (conn):
            conn.close()
            print("The SQLite connection is closed at " + time.ctime())
            print '\n******************************************************----'
            time.sleep(5)