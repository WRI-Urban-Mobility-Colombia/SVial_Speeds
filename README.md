# WRI Recolector de velocidades en tiempo real
## Descripción
Este procedimiento está diseñado para recolectar las velocidades en tiempo real de google API, sea distanceMatrix o RoutesAPI. 
El código toma un archivo de excel con las rutinas a levantar, con su respectiva API y realiza las consultas requeridas a la hora requerida, mientras no recolecta datos, permanece en reposo.
Al finalizar la toma, genera un archivo de resultados por proyecto identificado y metodología (distanceMatrix o Routes)

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
- Ejecutar el archivo Ru
## Referencias y documentos de apoyo de interés
