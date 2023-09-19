# Amazon_Pricer
Este script en Python utiliza varias bibliotecas, como `os`, `json`, `requests`, `csv`, `time`, y `tkinter` para crear una interfaz gráfica de usuario (GUI) que permite a los usuarios verificar y comparar los precios de productos en Amazon México y Amazon USA.

Descripción del código:

1. **Importación de Módulos:**
   Se importan los módulos necesarios para ejecutar las funciones y crear la GUI.

2. **Configuración de la Ventana:**
   Se crea una ventana Tkinter con el título "Amazon MX/USA Price Checker".

3. **Configuración de la API y Tasas de Cambio:**
   Se lee un archivo `settings.json` para obtener la API key y el tipo de cambio entre USD y MXN.

4. **Creación del Archivo CSV:**
   Si el archivo 'results.csv' no existe, se crea con un encabezado inicial.

5. **Definición de Funciones:**

   - **`start_bot`:**
      - Lee un archivo de texto `asin.txt` que contiene una lista de los ASINs (Amazon Standard Identification Number) a verificar.
      - Realiza solicitudes a la API de Keepa tanto para Amazon USA como México, utilizando el ASIN de cada producto para obtener datos detallados.
      - Extrae la información relevante de la respuesta JSON, incluido el nombre del producto, precios, disponibilidad, etc.
      - Calcula el precio en MXN (usando el tipo de cambio), la ganancia potencial, y la relación costo-ganancia.
      - Escribe los datos recopilados en el archivo 'results.csv'.
      - En caso de que ocurra un error durante la extracción de datos, se registra un mensaje de error.
      - Hay una demora de 12 segundos entre cada iteración para evitar exceder los límites de la tasa de solicitud de la API.
      
   - **`open_asin_file`:**
      - Abre el archivo `asin.txt` para su edición.
      
   - **`open_results`:**
      - Abre el archivo 'results.csv' para visualizar los resultados.
![Captura de pantalla 2023-09-18 230545](https://github.com/HonroAvisp/Amazon_Pricer/assets/73007200/f2b81194-7232-4d1a-a7c9-8a898fe9002f)

6. **Creación de Botones y Campo de Texto:**
   Se crean tres botones para iniciar el bot, abrir el archivo 'asin.txt', y abrir el archivo 'results.csv'. Además, se establece un campo de texto para mostrar los mensajes de estado del bot.

7. **Loop Principal de Tkinter:**
   Inicia el loop principal de la aplicación Tkinter para mantener abierta la GUI y permitir interacciones del usuario.

El script está diseñado para facilitar el proceso de verificar y comparar precios de productos en las plataformas de Amazon en México y EE. UU., ayudando a identificar oportunidades potenciales para obtener ganancias a través de la compra y venta de productos.
![Captura de pantalla 2023-09-18 230636](https://github.com/HonroAvisp/Amazon_Pricer/assets/73007200/c9c84842-ef57-4c50-b86a-8fe22f5327c1)

