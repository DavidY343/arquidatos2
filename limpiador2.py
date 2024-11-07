import pandas as pd
import numpy as np
import re

def quitar_tildes(texto):
        if isinstance(texto, str):
            texto = re.sub(r'[áÁ]', 'a', texto)
            texto = re.sub(r'[éÉ]', 'e', texto)
            texto = re.sub(r'[íÍ]', 'i', texto)
            texto = re.sub(r'[óÓ]', 'o', texto)
            texto = re.sub(r'[úÚ]', 'u', texto)
        return texto

def limpiar_datos_meteo24(nombre_archivo, estaciones_archivo):
    # Leer el archivo CSV
    df = pd.read_csv(nombre_archivo, sep=';')
    
    # Leer el archivo de estaciones
    estaciones_df = pd.read_csv(estaciones_archivo, sep=';')
    estaciones_df['CÓDIGO'] = estaciones_df['CÓDIGO'].astype(str)
    
    # Crear un diccionario para almacenar los registros limpios
    registros_limpios = {}

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Extraer la fecha base
        ano = row['ANO']
        mes = row['MES']
        
        # Iterar sobre los días del mes
        for dia in range(1, 32):
            dia_col = f'D{dia:02d}'
            val_col = f'V{dia:02d}'
            
            # Verificar si el dato es válido
            if row[val_col] == 'V':
                # Crear la fecha
                fecha = f'{ano}-{mes:02d}-{dia:02d}'
                distrito = row['ESTACION']
                
                # Inicializar las variables si no existen
                if (fecha, distrito) not in registros_limpios:
                    registros_limpios[(fecha, distrito)] = {
                        'TEMPERATURA': np.nan,
                        'PRECIPITACION': np.nan,
                        'VIENTO': np.nan,
                        'CÓDIGO': row['PUNTO_MUESTREO'][:8],
                        'DIRECCION': '',
                        'Codigo Postal': ''
                    }
                
                # Extraer los valores según la magnitud
                if row['MAGNITUD'] == 83:
                    registros_limpios[(fecha, distrito)]['TEMPERATURA'] = row[dia_col]
                elif row['MAGNITUD'] == 89:
                    registros_limpios[(fecha, distrito)]['PRECIPITACION'] = row[dia_col]
                elif row['MAGNITUD'] == 81:
                    registros_limpios[(fecha, distrito)]['VIENTO'] = row[dia_col] > 10  # Ejemplo: considerar viento fuerte si > 10
    
    # Agregar la información de dirección y código postal
    for key, datos in registros_limpios.items():
        codigo = datos['CÓDIGO']
        estacion_info = estaciones_df[estaciones_df['CÓDIGO'] == codigo]
        if not estacion_info.empty:
            datos['DIRECCION'] = estacion_info.iloc[0]['DIRECCION']
            datos['Codigo Postal'] = estacion_info.iloc[0]['Codigo Postal']
    
    # Convertir el diccionario a una lista de registros
    registros_limpios_list = [
        [fecha, distrito, 
         datos['TEMPERATURA'] if not pd.isna(datos['TEMPERATURA']) else 0.0, 
         datos['PRECIPITACION'] if not pd.isna(datos['PRECIPITACION']) else 0.0, 
         datos['VIENTO'] if not pd.isna(datos['VIENTO']) else False,
         datos['CÓDIGO'], quitar_tildes(datos['DIRECCION']), datos['Codigo Postal']]
        for (fecha, distrito), datos in registros_limpios.items()
    ]
    
    # Crear un DataFrame con los registros limpios
    df_limpio = pd.DataFrame(registros_limpios_list, columns=['FECHA', 'DISTRITO', 'TEMPERATURA', 'PRECIPITACION', 'VIENTO', 'CÓDIGO', 'DIRECCION', 'Codigo Postal'])
    
    # Guardar el DataFrame limpio en un nuevo archivo CSV
    df_limpio.to_csv('meteo24_limpio.csv', index=False)

if __name__ == "__main__":
    limpiar_datos_meteo24('meteo24.csv', 'estaciones_meteo_CodigoPostal.csv')