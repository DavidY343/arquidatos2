import pandas as pd
import numpy as np
import re
from pymongo import MongoClient

def quitar_tildes(texto):
    if isinstance(texto, str):
        texto = re.sub(r'[áÁ]', 'a', texto)
        texto = re.sub(r'[éÉ]', 'e', texto)
        texto = re.sub(r'[íÍ]', 'i', texto)
        texto = re.sub(r'[óÓ]', 'o', texto)
        texto = re.sub(r'[úÚ]', 'u', texto)
    return texto

def limpiar_usuarios(nombre_archivo):
    # Leer el archivo CSV
    df = pd.read_csv(nombre_archivo)
    
    # Eliminar la columna duplicada 'Email'
    if 'Email' in df.columns:
        df.drop(columns=['Email'], inplace=True)
    
    # Revisar y corregir valores nulos
    df.fillna({
        'NIF': 'DESCONOCIDO',
        'NOMBRE': 'DESCONOCIDO',
        'EMAIL': 'desconocido@example.com',
        'TELEFONO': '000000000'
    }, inplace=True)
    
    # Identificar y consolidar registros duplicados
    df.drop_duplicates(inplace=True)
    
    # Convertir todos los valores a minúsculas
    df['NIF'] = df['NIF'].str.lower()
    df['NOMBRE'] = df['NOMBRE'].str.lower()
    df['EMAIL'] = df['EMAIL'].str.lower()
    df['TELEFONO'] = df['TELEFONO'].str.lower()
    
    # Eliminar tildes
    df['NIF'] = df['NIF'].apply(quitar_tildes)
    df['NOMBRE'] = df['NOMBRE'].apply(quitar_tildes)
    df['EMAIL'] = df['EMAIL'].apply(quitar_tildes)
    df['TELEFONO'] = df['TELEFONO'].apply(quitar_tildes)

    # Eliminar espacios adicionales y caracteres especiales
    df['NIF'] = df['NIF'].str.strip()
    df['NOMBRE'] = df['NOMBRE'].str.strip()
    df['EMAIL'] = df['EMAIL'].str.strip()
    df['TELEFONO'] = df['TELEFONO'].str.replace(' ', '').str.replace('^(\+34|34)', '', regex=True)
    
    # Validar el formato del número de teléfono
    telefono_regex = re.compile(r'^\d{9}$')
    telefonos_invalidos = df[~df['TELEFONO'].apply(lambda x: bool(telefono_regex.match(x)))]
    
    # Validar el formato del email
    email_regex = re.compile(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$')
    emails_invalidos = df[~df['EMAIL'].apply(lambda x: bool(email_regex.match(x)))]

    
    # Imprimir mensajes si hay valores inválidos
    if not telefonos_invalidos.empty:
        print("Hay números de teléfono inválidos:")
        print(telefonos_invalidos[['NIF', 'NOMBRE', 'TELEFONO']])
    
    if not emails_invalidos.empty:
        print("Hay emails inválidos:")
        print(emails_invalidos[['NIF', 'NOMBRE', 'EMAIL']])
    
    # Guardar el DataFrame limpio en un nuevo archivo CSV
    df.to_csv('UsuariosLimpio.csv', index=False)

if __name__ == "__main__":
    limpiar_usuarios('UsuariosSucio.csv')