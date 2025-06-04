import time as timer
from datetime import datetime, timedelta
#from datetime import date, time
import pandas as pd
import requests
import json
import Keys as k
import ast
#import numpy as np

## Función crear request json

def createJson (row):
    link = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    headers =   {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": routesKey,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.routeToken"  # Adjust field mask as needed
                }
    json = {
        "origin": {
            "location":{
                "latLng":{
                    "latitude":row['Lat_Origen'],
                    "longitude":row['Lon_Origen']
                    }
                }
            },
        "destination":{
            "location":{
                "latLng":{
                    "latitude":row['Lat_Destino'],
                    "longitude":row['Lon_Destino']
                    }
                }
            },
        "travelMode": row['Modo'],
        "routingPreference": row['Ruteo'],
        "trafficModel" : row['Model'],
        "languageCode": "en-US",
        "units": "METRIC"
        }
    return(link, headers, json)

def createJsonV2(coord, row):
    link = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    headers =   {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": routesKey,
        "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters,routes.polyline.encodedPolyline,routes.routeToken"  # Adjust field mask as needed
                }
    json = {
    "origin": {
        "location":{
            "latLng":{
                "latitude":coord[0][0],
                "longitude":coord[0][1]
                }
            }
        },
    "destination":{
        "location":{
            "latLng":{
                "latitude":coord[-1][0],
                "longitude":coord[-1][1]
                }
            }
        },
    "intermediates":[
        {
            "location":{
                "latLng":{
                    "latitude": loc[0],
                    "longitude":loc[1]
                }
            }
        }for loc in coord[1:-1]
    ],
    "travelMode": row['Modo'],
    "routingPreference": row['Ruteo'],
    "trafficModel" : row['Model'],
    "languageCode": "en-US",
    "units": "METRIC"
    }
    return(link, headers, json)
   
    

def launchRoutesRequest(link, headers, json):
    success = False
    
    while success == False:
        resultJson = requests.post(url = link, headers=headers, json=json)
        # Si la query es exitosa, laza codigo 200, skip while
        print(resultJson.status_code)
        if resultJson.status_code == 200:
            success = True
        else:
            print("Routes API no devolvió resultado exitoso, esperar ")
            timer.sleep(10)
    
    return resultJson
    

## Funcion de crear request link

def createLinkRequest (row):
    core = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
    origin = 'origins='+str(row['origin'])+'&' 
    destin = 'destinations='+str(row['destination'])+'&'
    dTime = 'departure_time=now&'
    tModel = 'traffic_model='+str(row['model'])+'&'
    units = 'units=metric&'
    tKey =  'key=' + key +'&'
    mode = 'mode='+row['Modo']
    
    query = core + origin + destin + dTime + tModel +units + tKey + mode
    #mprint(query)
    return(query)

def launchRequest (row):
    
    # 
    
    print("Lanzar Query")
    header = {
    'User-agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582'
    }
    PARAMS ={'header':header}
    notExecuted = True
    attempt = 1
    attempts = 10
    coolDownSecs = 60
    while (notExecuted == True):
        try:
            response = requests.get(row['linkRequest'], params = PARAMS)    
            resultDictionary = json.loads(response.content.decode('utf-8'))
            notExecuted = False

        except:
            print("Error getting the query, wait "+str(coolDownSecs)+ " seconds and try again, try no: "+ str(attempt))
            
            if attempt >= attempts:            
                notExecuted = False
            else:
                attempt = attempt + 1
                timer.sleep(coolDownSecs)
    
    # Check query results
    queryStatus = resultDictionary['status']
    print(queryStatus)
    if queryStatus == 'OK':
        array = organizeRequestData(resultDictionary)
    else: 
        print("Error getting the query, wait 10 secs and try again")
        timer.sleep(10)
        response = requests.get(row['linkRequest'], params = PARAMS)
        resultDictionary = json.loads(response.content.decode('utf-8'))
    return array

def organizeRequestData(resultDictionary):
    ## Get Json data and organize in list format
    
    print(resultDictionary)
    results = resultDictionary['rows']
    status = results[0]['elements'][0]['status']
    print('Status de la query ' + status)
    # Si la query es correcta, obtener valores
    container = []
    if status == 'OK':
        distanceMeters = results[0]['elements'][0]['distance']['value']
        durationSecond = results[0]['elements'][0]['duration']['value']
        durationTraffic = results[0]['elements'][0]['duration_in_traffic']['value']
        container.append(distanceMeters)
        container.append(durationSecond)
        container.append(durationTraffic)
    else:
        error = resultDictionary['error_message']
        mensaje = results[0]['error_messsage']
        container.append(mensaje)
        container.append(error)
        container.append(error)
    print("Contenedor recibido de GOOGLE API")
    print(container)
    return container

## Code to be depreciated, commented and if everything is ok, delete

#fileName = "20241030_Guayacanes"
#inputFileName = fileName + ".xlsx"
#outputFileName = fileName + "_results.csv"
#partialOutputFilename = fileName + "_partial_results.csv"

#End code to depreciate

def saveSeparatedByProject(dataframe,fileName, model,resultType):

    'This function will save outputs separated by the different project name'
    
    proyectos = dataframe['Proyecto'].unique()
    for proyecto in proyectos:
        ## Create file name
        
        filename = 'Outputs/'+fileName[7:-5]+'_'+proyecto+'_'+resultType+"_"+model+"_results.csv"
        print("Saving results in the next file")
        print(filename)
        proyectDF = dataframe[dataframe['Proyecto']== proyecto]
        proyectDF.to_csv(filename)
        
        

def run_script(inputFileName, mykey,myRoutesKey):

    ##### Codigo principal
    global key
    global routesKey
    
    key = mykey
    routesKey = myRoutesKey

    listado_req = pd.read_excel(inputFileName)

    ## Crear base con todas las queries en all_requests
    
    all_requests = pd.DataFrame()
    
    for index, row in listado_req.iterrows():
        
        rep_rows = pd.DataFrame([row]*row['Numero_tomas'])        
        rep_rows['Hora_request'] = rep_rows['Hora_inicio']
        rep_rows.reset_index(drop = True, inplace = True)
        rep_rows['No_request'] =rep_rows.index
        rep_rows['Hora_request'] = rep_rows['Hora_inicio'] + pd.to_timedelta(rep_rows['No_request'] * rep_rows['Intervalo_tomas_min'], unit = 'm')
        rep_rows['model'] = row["Model"]
        all_requests = pd.concat([rep_rows,all_requests], ignore_index = True)
    print("Listado de queries a ejecutar"+ '\n'+ '\n')
    print(all_requests)
    
    ## Unir coordenadas
    
    all_requests['origin'] = all_requests['Lat_Origen'].astype(str) + ' ' + all_requests['Lon_Origen'].astype(str)
    all_requests['destination'] = all_requests['Lat_Destino'].astype(str) + ' ' + all_requests['Lon_Destino'].astype(str)
    
    
    ## Crear request 
    
    all_requests['linkRequest'] = all_requests.apply(createLinkRequest, axis = 1)
    
    ## Extraer max time para finalizar queries cuando se alcance el tiempo máximo
    total_queries = len(all_requests['Numero_tomas'])
    
    end_time = max(all_requests['Hora_request'])
    print("La rutina de queries terminará en la siguiente fecha/hora")
    print("Asegurese de que el dispositivo no va a hibernar/congelar las consultas")
    print('Durante la función se ejecutarán '+ str(total_queries)+ ' tomas')
    
    print(end_time)  
    
    
    
    ## loop en tiempo para lanzar los triggers
    i = 0
    j = 0
    
    containerResults = pd.DataFrame()
    routesAPIResults = pd.DataFrame()
    ## Loop de sleep time, terminará una vez se llegue al "End time"
    
    while datetime.now()-timedelta(seconds = 1) <= end_time:
        
        now = datetime.now().replace(second=0, microsecond=0)
        print("Stand by "+ str(now))
        
        filtered = all_requests[(all_requests['Hora_request'] == now)]
        if len(filtered)> 0:
            #Condiciones de ejecución alcanzadas, ejecutar query
            
            filteredAPI = filtered.copy()
            
            # distanceMatrix API
            
            for index, row in filtered.iterrows():
                # execute query

                models = row['APIS'].split()               
                ## Check model to run
                ## Check every model and select if you have to run it
                
                for model in models:
                    print("Modelos")
                    print(model)
                    
                    if('Distance' == model):
                        print('Execute distanceMatrix model')
                        ## Here, the event will be executed in distanceMatrix API
                        results = launchRequest(row)
                        filtered.loc[index, 'Distancia'] = results[0]
                        filtered.loc[index, 'Tiempo'] = results[1]
                        filtered.loc[index, 'Tiempo_Traffic'] = results[2]
                        i = i+1
                        print("Contenedor filtrado")
                        print (filtered)
                    elif('Routes' == model):
                        
                        ## RoutesAPI to be moved
            
                        ## Create query parameters (link, headers (results) and input Json)
                        
                        ## No of coordinates
                        
                        coord = ast.literal_eval(row['Coord_Routes'])
                        
                        ## Split between 2
                        noCoordenadas = len(coord)
                        
                        if noCoordenadas >2:
                            link, headers, json = createJsonV2(coord, row)
                            print(json)
                        else: 
                            link, headers, json = createJson(row)
                        
                        ## 
                        resultJson = launchRoutesRequest(link, headers, json)
                        print("RoutesAPI Results")
                        print(resultJson.json())
                        dataJson = resultJson.json()
                        distanceMeters = dataJson['routes'][0]['distanceMeters']
                        durationSecond = int(dataJson['routes'][0]['duration'].replace("s",""))
                        staticDuration = int(dataJson['routes'][0]['staticDuration'].replace("s",""))
                
                        filteredAPI.loc[index, 'Distancia'] = distanceMeters
                        filteredAPI.loc[index, 'Tiempo'] = staticDuration
                        filteredAPI.loc[index, 'Tiempo_Traffic'] = durationSecond
                        filteredResults = filteredAPI.drop(['Coord_Routes'], axis=1).copy()
                        j = j+1
        
            containerResults = pd.concat([containerResults, filtered], ignore_index = True)
            routesAPIResults = pd.concat([routesAPIResults, filteredResults], ignore_index = True)
            
            saveSeparatedByProject(containerResults, inputFileName, 'Distance', 'parcial')
            saveSeparatedByProject(routesAPIResults, inputFileName, 'Routes', 'parcial')

        timer.sleep(60 - datetime.now().second)
    
    ## Post-procesamientos 
    
    ## Filter databases by project
    
    print("Post procesamiento, 1. Separar bases por proyecto")
    print("Guardando base consultas DistanceMatrixAPI")
    saveSeparatedByProject(containerResults, inputFileName, 'Distance', 'final')    

    print("Guardando base consultas DistanceMatrixAPI")
    
    saveSeparatedByProject(routesAPIResults, inputFileName, 'Routes', 'final')
    
    #containerResults.to_csv(finalOutput)
    #routesAPIResults.to_csv("Outputs/RoutesAPIComplete.csv")
        
    print('Proceso finalizado, se han hecho ' + str(i) + ' solicitudes de DistanceMatrix')
    print('Proceso finalizado, se han hecho ' + str(j) + ' solicitudes de RoutesAPI')









        
