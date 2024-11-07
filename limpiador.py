import pandas as pd
import numpy as np

def limpiar_datos(nombre_archivo):
    # Leer el archivo CSV
    df = pd.read_csv(nombre_archivo, sep=';')
    
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
                        'VIENTO': np.nan
                    }
                
                # Extraer los valores según la magnitud
                if row['MAGNITUD'] == 83:
                    registros_limpios[(fecha, distrito)]['TEMPERATURA'] = row[dia_col]
                elif row['MAGNITUD'] == 89:
                    registros_limpios[(fecha, distrito)]['PRECIPITACION'] = row[dia_col]
                elif row['MAGNITUD'] == 81:
                    registros_limpios[(fecha, distrito)]['VIENTO'] = row[dia_col] > 10  # Ejemplo: considerar viento fuerte si > 10
    
    # Convertir el diccionario a una lista de registros
    registros_limpios_list = [
        [fecha, distrito, 
         datos['TEMPERATURA'] if not pd.isna(datos['TEMPERATURA']) else 0.0, 
         datos['PRECIPITACION'] if not pd.isna(datos['PRECIPITACION']) else 0.0, 
         datos['VIENTO'] if not pd.isna(datos['VIENTO']) else False]
        for (fecha, distrito), datos in registros_limpios.items()
    ]
    
    # Crear un DataFrame con los registros limpios
    df_limpio = pd.DataFrame(registros_limpios_list, columns=['FECHA', 'DISTRITO', 'TEMPERATURA', 'PRECIPITACION', 'VIENTO'])
    
    # Guardar el DataFrame limpio en un nuevo archivo CSV
    df_limpio.to_csv('meteo24_limpio.csv', index=False)

if __name__ == "__main__":
    limpiar_datos('meteo24.csv')