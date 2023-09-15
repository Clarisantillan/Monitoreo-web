import requests
from bs4 import BeautifulSoup
import hashlib
import time
import smtplib
from email.mime.text import MIMEText
url = "https://www.afa.com.ar/es/boletins/Comite%20Ejecutivo?s=3"
from_email = "origen@.com"
to_email = "destino@.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "tunombredeusuario"
smtp_password = "contraseña"
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        for aside in soup.select('aside.btSidebar'):
            aside.decompose()
        return str(soup)
    else:
        return None
def calculate_hash(content):
    return hashlib.md5(content.encode()).hexdigest()
def compare_hashes(old_hash, new_hash):
    return old_hash == new_hash
previous_hash = ""
first_iteration = True
change_detected = False
while True:
    current_content = get_page_content(url)
    if current_content:
        current_hash = calculate_hash(current_content)
        if not compare_hashes(previous_hash, current_hash):
            print("¡Se detectó un cambio en el contenido!")
            previous_hash = current_hash
            change_detected = True
        else:
            print("No se encontraron cambios.")
            change_detected = False
    if change_detected and not first_iteration:
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
        change_detected = False
    elif first_iteration:
        first_iteration = False
    time.sleep(180)
