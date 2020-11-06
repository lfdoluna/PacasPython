# PacasPython
Scripst para la impresión de tickets generados por la báscula de merma de forma automática

********************** NOTA **********************

Debe asegurarse de instalar Python contenga la función **PIP**, esta es necesaria para instalar las librerias necesarias de Python

**************************************************
**Preparando la instalación**
1. Asegurese de descargar y copiar todo el código en el directorio raiz de su disco duro, debe quedar algo asi:

`C:\PacasPython\`

1.1 En caso de utilizarlo en el sistema de Windows XP debe asegurarse que la carpeta **PacasPythonXP** quede en el directorio raíz 

**Instalación librerias y programas:**

1. Instalar  *Python 2.7*  y abrir una ventana de *CMD* y escribir `python`, si no  se abre la terminal de Python se debe agregar al *PATH*. 
Para agregarlo debemos buscar **"Editar  las variables de entorno del sistema"** y en la  ventana selecionaremos **"Variables del entorno"**
y en variable *PATH* editamos y seleccionaremos la ruta de instalación de *Python* y la carpeta *Python27\Scripts*, esto con la finalidad
de al momento de instalar con la función **PIP**, no encontremos el mismo error de Python.

2. Abrir una ventana *CMD* y ejecutamos las siguientes lineas de comando:
```
pip install -r requirements.txt
```

2.1 En caso de tener desabilitado el internet ejecute el siguiente comando:

`pip install -r requirementsOFFLINE.txt`

3. Asegurarse de tener instalado *Chrome*, *Acrobat Reader*(Versión Estandar) y *los controladores de la impresora*. En este caso se ocupo la Brother QL-800 por lo que anexamos el link de descarga. También dentro de la carpeta **LibreriasPacasPython(offline)** se dejaron los instaladores de los *controladores de la impresora*, como el instalador de *Acrobat Reader*

https://support.brother.com/g/b/downloadend.aspx?c=mx&lang=es&prod=lpql800eus&os=10011&dlid=dlfp100846_000&flang=201&type3=347

**Instalación Scritps:**

1. Descargaremos y guardaremos en el directorio C:\PacasPython\
2. Modificaremos el Script **Imprime.py**, en la *línea 16*, la variable **userM**, la cambiaremos por el usuario del ordenador del mismo modo
lo realizaremos con el Script **printerPacas.py**, con la excepción que se encuentra en la *línea 15*
3. Para iniciar el script durante el arranque debemos abrir una terminal de  windows (CMD), como administrador. Después escribiremos
lo siguiente:

`python "c:\PacasPython\agrega a inicio.py"`
