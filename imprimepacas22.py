
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
for i in range(6989, 7061, 1):
    sqlquery = "SELECT fecha, kilogramos, tipo_paca FROM pacas WHERE id_paca = {};".format(i)
    data = ConsultaDB(sqlquery)
    #p = subprocess.Popen('"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" "http://192.168.5.243/merma/__extensions/tcpdf/examples/ticket.paca.php?fecha={}&peso={}&tipopaca={}&codigo={}"'.format(data[0],data[1],data[2],i), 
	                                #stdout=subprocess.PIPE, 
	                                #shell=True)
    print 'Llamando a printerPacas....'
    time.sleep(5)
    # Imprime el tiket
    fileP = 'C:\Users\BI\Downloads\Ticket_de_Pacas{}.pdf'.format(i)
    p = subprocess.Popen('"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"  /n /s /h /t "{}" "QL-800_pacas"'.format(fileP), stdout=subprocess.PIPE, shell=True)
    print '**********************----'
    print (fileP)
    print '**********************----'
    #subprocess.call('python c:\PacasPython\printerPacas.py')
