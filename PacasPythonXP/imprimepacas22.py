
import subprocess
import psycopg2
import time

def ConsultaDB(consulta):
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
                        print e
			pass

		finally:
			try:
			    if (cur):
			        cur.close()
			    if (conn):
			        conn.close()
				#print ('Consulta exitosa **' + consulta + '**')
				return resultado
			except:
				pass

def entrada():
    global r_i
    global r_o
    try:
        r_i = int(input("Desde que folio empezara: "))
        r_o = int(input("Hasta que folio terminara: "))
    except Exception as e:
        print e
        print "Error, por favor ingrese de nuevo los datos"
        entrada()
        
global r_i
global r_o
print "Script de apoyo para la impresion masiva de tickets"
entrada()
for i in range(r_i, r_o, 1):
    sqlquery = "SELECT fecha, kilogramos, tipo_paca FROM pacas WHERE id_paca = {};".format(i)
    data = ConsultaDB(sqlquery)
    # Descarga el ticket
    p = subprocess.Popen('C:\PacasPython\wget.exe -O C:\PacasPython\Ticket_de_Pacas{}.pdf -c "http://192.168.5.243/merma/__extensions/tcpdf/examples/ticket.paca.php?fecha={}&peso={}&tipopaca={}&codigo={}"'.format(i,data[0],data[1],data[2],i), 
	                                stdout=subprocess.PIPE, 
	                                shell=True)
    print 'Llamando a printerPacas....'
    time.sleep(5)
    # Imprime el tiket
    fileP = 'C:\PacasPython\Ticket_de_Pacas{}.pdf'.format(i)
    p = subprocess.Popen('"C:\Program Files\Adobe\Reader 11.0\Reader\AcroRd32.exe"  /n /s /h /t "{}" "Brother QL-800"'.format(fileP), stdout=subprocess.PIPE, shell=True)
    print '**********************----'
    print (fileP)
    print '**********************----'
