#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 15:33:05 2020
Archivo: RprtPcs.py
Comentarios: Script para la generación de un reporte en excel
para la entradas de pacas
@author: LFLQ
"""
from datetime import datetime, date
import calendar
import psycopg2
import pandas as pd

def current_date_format(date1, date2):
	d1 = date(date1[0], date1[1], date1[2])
	d2 = date(date2[0], date2[1], date2[2])
	d1 = d1.strftime("%d-%m-%Y")
	d2 = d2.strftime("%d-%m-%Y")
	messsage = "{}al{}".format(d1, d2)
	return messsage

def addZero(number):
	if number <= 9:
		number = '0' + str(number)
	return number

connstr = "host=192.168.5.243 port=5432 user=postgres password=bi dbname=merma"
conn = psycopg2.connect(connstr)
fecha1 = []
fecha2 = []
now = datetime.now()
desde = now.day - 7
hasta = now.day - 1
if (desde) <= 0:
	mes_desde = now.month - 1
	monthRange = calendar.monthrange(now.year, mes_desde)
	day, days = monthRange
	dia_desde = days + desde
else:
	mes_desde = now.month
	dia_desde = desde
if (hasta) <= 0:
	mes_hasta = now.month - 1
	monthRange = calendar.monthrange(now.year, mes_hasta)
	day, days = monthRange
	dia_hasta = days + hasta
else:
	mes_hasta = now.month
	dia_hasta = hasta
query = "SELECT * FROM pacas WHERE fecha BETWEEN '{}-{}-{}' AND '{}-{}-{}' ORDER BY id_paca;".format(now.year, addZero(mes_desde), addZero(dia_desde), 
																					now.year, addZero(mes_hasta), addZero(dia_hasta),)
print query
dataFrame = pd.read_sql(query, conn)
fecha1.append(now.year)
fecha1.append(mes_desde)
fecha1.append(dia_desde)
fecha2.append(now.year)
fecha2.append(mes_hasta)
fecha2.append(dia_hasta)
nomArch = 'c:\PacasPython\Reporte_Entradas_{}.xlsx'.format(current_date_format(fecha1, fecha2))
print nomArch
dataFrame.to_excel(nomArch, index = False)
conn.close()