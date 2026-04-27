# WRI Recolector de velocidades en tiempo real
## Descripción
Este procedimiento está diseñado para recolectar las velocidades en tiempo real de google API, sea distanceMatrix o RoutesAPI. 
El código toma un archivo de excel con las rutinas a levantar, con su respectiva API y realiza las consultas requeridas a la hora requerida, mientras no recolecta datos, permanece en reposo.
Al finalizar la toma, genera un archivo de resultados en formato (CSV) por proyecto identificado y metodología (distanceMatrix o Routes)

## Requisitos
- Python 3.6.
- Librerías (Pronto se definirá un requirements.txt):
  * pandas
  * Openpyxl
  * requests
## Instrucciones
- Descargar archivos en la misma carpeta
- Preparar archivo de consultas en la carpeta Inputs
- Configurar la máquina para que no hiberne durante el periodo de toma de información
- Ejecutar el archivo run_script.py
El código acaba de correr cuando se tenga la última consulta. Mientras tanto queda en stand by.
####Importante que si se corre en computadores, y el computador entra en stand by, se congela la consulta
### Correr en un dispositivo Android
- Requiere las aplicaciones Termux y Total Commander
#### ¿Cómo ejecutr en dispositivo Android?
1. Descargar Termux de github e instalar (https://github.com/termux/termux-app/releases)
2. Descargar la app "Total Commander" para acceder a la memoria de la máquina virtual
3. Abrir la aplicación y ejecutar:
   
   - "pkg update"
   - "pkg upgrade -y"
   Para actualizar los diferentes repositorios, luego ejecutar
   - "pkg install python -y"
   Verificar la versión de python con python --version
   Para instalar las librerías, aplicar los siguientes comandos
   
   - "pip install openpyxl"
   - "pip install requests"
4. Instalar pandas y otras librerías con este comando:

   - "pkg i tur-repo -y"
   - "pkg i python-pandas -y" 

   Mover el código y el archivo de entrada a la máquina virtual de Termux usando totalcommander
   Ejecutar el código usando el comando:
   "python Run_speeds.py"  
6. Recomendado: 
   Una vez esté ejecutandose, habilitar la opción: "wakelock" para evitar que Android mate el proceso
## Referencias y documentos de apoyo e interés
