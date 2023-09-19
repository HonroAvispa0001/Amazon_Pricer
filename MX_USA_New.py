import os
import json
import requests
import csv
import time
from tkinter import Tk, Button, Text, END

# Configuración de la ventana
root = Tk() 
root.title("Amazon MX/USA Price Checker")

# Leer la API key y el exchange_rate de settings.json
with open('settings.json') as json_file:
    settings = json.load(json_file)

#with open('asin.txt') as f:
 #   asins = f.read().splitlines()

api_key = settings['api_key']
exchange_rate = settings['exchange_rate']


# Crear el archivo CSV para los resultados si no existe
if not os.path.exists('results.csv'):
    with open('results.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ASIN", "Product Name", "Price in USD", "Price in MXN (USA)", "Price in MXN (MX)", "Profit", "Cost-Profit Ratio", "Avg Price", "Amazon OOS %"])
    print("Archivo results.csv creado.")


def start_bot():
  with open('asin.txt') as f:
    asins = f.read().splitlines()

  how_many_asins = len(asins)
  print(f"Extrayendo datos para {how_many_asins} ASIN")    
  status.insert(END, f"Extrayendo datos para {how_many_asins} ASIN\n")
  root.update()

  # Iterar sobre cada ASIN
  for asin in asins:
    print(f"Procesando ASIN: {asin}")
    # Hacer la solicitud a la API de Keepa para USA
    response_usa = requests.get(f"https://api.keepa.com/product?key={api_key}&domain=1&stats=30&offers=20&asin={asin}")
    # Hacer la solicitud a la API de Keepa para MX
    response_mx = requests.get(f"https://api.keepa.com/product?key={api_key}&domain=11&stats=30&offers=20&asin={asin}")

    # Verificar que las solicitudes fueron exitosas
    if response_usa.status_code == 200 and response_mx.status_code == 200:
        data_usa = response_usa.json()
        data_mx = response_mx.json()

        # La respuesta de la API es una lista de productos
        for product_usa, product_mx in zip(data_usa['products'], data_mx['products']):
            # Extraer el nombre del producto y el precio
            try:
                product_name = product_mx['title'].replace(',', ' ')  # Reemplazar las comas en el nombre del producto
                try:
                    if product_usa['buyBoxPrice'] != -1:
                        price_usd = product_usa['buyBoxPrice'] / 100
                    else:
                        price_usd = next((i for i in product_usa['stats']['current'] if i != -1), -1) / 100
                except KeyError:
                    price_usd = next((i for i in product_usa['stats']['current'] if i != -1), -1) / 100

                try:
                    if product_mx['buyBoxPrice'] != -1:
                        price_mxn_mx = product_mx['buyBoxPrice'] / 100
                    else:
                        price_mxn_mx = next((i for i in product_mx['stats']['current'] if i != -1), -1) / 100
                except KeyError:
                    price_mxn_mx = next((i for i in product_mx['stats']['current'] if i != -1), -1) / 100
                
            # Obtener promedio de precio últimos 90 días 
                avg90 = product_mx['stats']['avg90']
                price_avg90 = avg90[1] / 100

            # Obtener % de no disponibilidad últimos 90 dias
                out_of_stock = product_mx['stats']['outOfStockPercentage90']  
                out_of_stock_pct = out_of_stock[0]
                
                # Convertir el precio a MXN
                price_mxn_usa = price_usd * exchange_rate

                # Calcular la ganancia y la relación costo-ganancia
                profit = price_mxn_mx - price_mxn_usa
                cost_profit_ratio = profit / price_mxn_usa  if profit != 0 else 0

                # Escribir los resultados en el archivo CSV
                with open('results.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([asin, product_name, price_usd, price_mxn_usa, price_mxn_mx,profit, cost_profit_ratio, price_avg90, out_of_stock_pct])
                status.insert(END, f"Datos guardados para ASIN: {asin}\n")
                root.update()
                print(f"Datos guardados para ASIN: {asin}")

                  # Guardar la respuesta JSON completa en un archivo de texto
                #with open(f'{asin}.json', 'w') as f:
                 # json.dump(response_usa.json(), f)

                #with open(f'{asin}_mx.json', 'w') as f:
                 #json.dump(response_mx.json(), f)
            
            except KeyError as e:
                print(f"KeyError: {e} for ASIN: {asin}")
    else:
        print(f"Error en la solicitud de la API para ASIN: {asin}, código de estado: {response_usa.status_code}, {response_mx.status_code}")

    # Esperar 3 segundos antes de la próxima solicitud para no exceder el límite de la API
    time.sleep(12)  
  print(f"Datos extraídos con éxito para {how_many_asins} ASIN")    
  status.insert(END, f"Datos guardados para {how_many_asins} ASIN\n")
  root.update()


def open_asin_file():
  os.startfile("asin.txt")
  
def open_results():
  os.startfile("results.csv")

# Botones    
start_button = Button(root, text="Iniciar Bot", command=start_bot)
start_button.grid(row=0, column=0)

asin_button = Button(root, text="Abrir asin.txt", command=open_asin_file)
asin_button.grid(row=0, column=1)

results_button = Button(root, text="Abrir results.csv", command=open_results)  
results_button.grid(row=0, column=2)

# Caja de texto para los mensajes
status = Text(root, height=10)
status.grid(row=1, column=0, columnspan=3)

root.mainloop()
