"""
## Python Automated Launcher (ES)
@author: Rafael Muñoz
"""

## Import libraries

import os
import time as timer

#Import another files

import schedule_example as se
import Keys as K

print( '##  GOOGLE API PROGRAMADO POR TRAMOS ##'+'\n'+'\n')

timer.sleep(2)

## Read filelist in folder 'Inputs'

files = os.listdir('Inputs')

print("# Revisando el archivo de queries en el folder 'Inputs'")
timer.sleep(5)

## Checking if more than 1 file in the folder
if len(files)>1:
    print("Hay mas de un archivo en el folder 'Inputs', revise y deje únicamente un archivo de consultas, luego ejecute de nuevo el código")
else:    
    inputFileNameComplete = files[0]
    print('\n')
    print('Se usará el archivo: '+ inputFileNameComplete+ ' para ejecutar las queries de velocidades')
    
    inputFileName = 'Inputs/'+ inputFileNameComplete
    
    print('Inicia la función de consultas')
    
    se.run_script(inputFileName, K.apiKey, K.routesKey)
