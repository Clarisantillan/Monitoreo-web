

import time
import numpy as np
from selenium import webdriver
from PIL import Image
import smtplib
from email.mime.text import MIMEText
from google.colab import drive
# Montar Google Drive
drive.mount('/content/drive')
# Configuración de correo electrónico
from_email = "remitente@gmail.com"
to_email = "destinatario@gmail.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "usuario@gmail.com"
smtp_password = "contraseña"
url = "https://www.segundopalo.com.ar/primeraa"
# Directorio en Google Drive donde se guardarán las capturas de pantalla
drive_screenshot_dir = '/content/drive/My Drive/ScreenshotsA/Actual/'
def compare_images(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    # Convertir las imágenes en matrices NumPy
    image1_array = np.array(image1)
    image2_array = np.array(image2)
    # Calcular los histogramas de las imágenes
    hist1 = np.histogram(image1_array, bins=256, range=(0, 256))[0]
    hist2 = np.histogram(image2_array, bins=256, range=(0, 256))[0]
    # Calcular la distancia entre los histogramas utilizando la distancia del Qui-Square
    diff = np.sum((hist1 - hist2) ** 2 / (hist1 + hist2 + 1e-10))
    # Establecer un umbral para determinar si hay cambios significativos
    threshold = 10000
    if diff > threshold:
        # Hay cambios significativos en las imágenes
        return False
    else:
        # Las imágenes son similares o iguales
        return True

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=options)
browser.set_window_size(1920, 1080)
previous_screenshot = None
while True:
    screenshot_filename = f"{drive_screenshot_dir}screenshot_{int(time.time())}.png"  # Ruta completa en Google Drive
    browser.get(url)
    time.sleep(5)
    browser.save_screenshot(screenshot_filename)
    print(f"Captura de pantalla tomada: {screenshot_filename}")

    if previous_screenshot is not None:
        if compare_images(previous_screenshot, screenshot_filename):
            print("Las capturas de pantalla son iguales.")
        else:
            print("¡Se detectó un cambio en la página!")
            # Enviar correo electrónico
            subject = "Cambio en el contenido detectado"
            message = f"Se ha detectado un cambio en el contenido de la página: {url}"
            #for to_email in to_emails:
            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = from_email
            msg["To"] = to_email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(from_email, to_email, msg.as_string())
    previous_screenshot = screenshot_filename
    time.sleep(600)
browser.quit()

import numpy as np
from PIL import Image
def compare_images2(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    # Convertir las imágenes en matrices NumPy
    image1_array = np.array(image1)
    image2_array = np.array(image2)
    # Calcular los histogramas de las imágenes
    hist1 = np.histogram(image1_array, bins=256, range=(0, 256))[0]
    hist2 = np.histogram(image2_array, bins=256, range=(0, 256))[0]
    # Calcular la distancia entre los histogramas utilizando la distancia del Qui-Square
    diff = np.sum((hist1 - hist2) ** 2 / (hist1 + hist2 + 1e-10))
    # Establecer un umbral para determinar si hay cambios significativos
    threshold = 10000
    if diff > threshold:
        # Hay cambios significativos en las imágenes
        return False
    else:
        # Las imágenes son similares o iguales
        return True