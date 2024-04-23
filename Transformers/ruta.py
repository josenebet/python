import requests
import json

def convertir_dms_a_decimal(coordenada):
    """
    Convierte una coordenada en formato DMS (grados, minutos, segundos) a formato decimal.

    Args:
        coordenada (str): La coordenada en formato DMS (por ejemplo, "10°10'22.7"N").

    Returns:
        float: La coordenada en formato decimal.
    """
    direccion = coordenada[-1]  # N, S, E o W
   # grados, minutos, segundos = map(float, coordenada[:-1].split("°"))
    grados=coordenada[:-1].split("°")
    minutos=grados[1].split("'")
    segundos=minutos[1].split('"')
    
    grados_decimales = float(grados[0])+ float(minutos[0]) / 60 + float(segundos[0]) / 3600
    if direccion in "SW":
        grados_decimales *= -1
    return str(grados_decimales)

# Definir la clave de la API de Google Maps
# (Reemplázala con tu clave)
API_KEY = 'AIzaSyCZ7f6GS_dCHFinrO6-TMittNTTu9G_Qmo'

coordenada_origeny = '10°10\'22.7"N'
coordenada_origenx = '67°54\'50.6"W'

coordenada_destinoy = '37°41\'57.2"N' 
coordenada_destinox= '-122°04\'31.7"W'

# Convertir coordenadas a decimal
origen_decimaly = convertir_dms_a_decimal(coordenada_origeny)
origen_decimalx= convertir_dms_a_decimal(coordenada_origenx)
destino_decimaly = convertir_dms_a_decimal(coordenada_destinoy)
destino_decimalx = convertir_dms_a_decimal(coordenada_destinox)

origen="10.173183, -67.913595"
destino="10.176041874545847, -67.91388384894088"

# URL de la API con coordenadas decimales
#url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origen_decimaly},{origen_decimalx}&destinations={destino_decimaly},{destino_decimalx}&mode=driving&key={API_KEY}"
url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origen}&destinations={destino}&mode=driving&key={API_KEY}"

# Enviar la solicitud a la API y obtener la respuesta
respuesta = requests.get(url)
print (respuesta)

# Comprobar si la solicitud fue exitosa
if respuesta.status_code == 200:

    # Convertir la respuesta JSON en un diccionario
    datos = json.loads(respuesta.text)
    print (datos)

    # Obtener la distancia en metros
    distancia_en_metros = datos["rows"][0]["elements"][0]["distance"]["value"]

    # Convertir la distancia a kilómetros
    distancia_en_km = distancia_en_metros / 1000

    # Mostrar la distancia
    print(f"La distancia entre los dos puntos es de {distancia_en_km:.2f} km.")

else:
    print(f"Error al obtener la distancia: {respuesta.status_code}")


