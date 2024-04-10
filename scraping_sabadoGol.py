
import requests
import hashlib
import time
import smtplib
from email.mime.text import MIMEText

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "email@gmaila.com"
smtp_password = "contraseña"

def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def calculate_hash(content):
    return hashlib.md5(content.encode()).hexdigest()

def compare_hashes(old_hash, new_hash):
    return old_hash == new_hash

def scan_and_compare_links(base_url, start_id, end_id, category_start_id, category_end_id):
    previous_hashes = {}
    first_iteration = True
    changed_links = []

    while True:
        changed_links.clear()
        change_detected = False

        for page_id in range(start_id, end_id + 1):
            current_url = f"{base_url}fecha.php?id={page_id}"
            current_content = get_page_content(current_url)

            if current_content:
                current_hash = calculate_hash(current_content)

                if not compare_hashes(previous_hashes.get(page_id, ""), current_hash):
                    print(f"¡Se detectó un cambio en {current_url}!")
                    previous_hashes[page_id] = current_hash
                    changed_links.append(current_url)
                    change_detected = True
                else:
                    print(f"No se encontraron cambios en {current_url}.")

        for i in range(category_start_id, category_end_id + 1):
            current_url = f"{base_url}categoria.php?id={i}&a="

            if change_detected:
                print(f"¡Se detectó un cambio en la categoría {i}! Enlace: {current_url}")

        if change_detected and not first_iteration:
            subject = "Cambio detectado en SabadoGol"
            message = "Se ha detectado un cambio en los siguientes enlaces:\n\n"
            message += "\n".join(changed_links)

            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = smtp_username
            msg["To"] =  ', '.join(to_emails)
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, to_emails, msg.as_string())
            change_detected = False
        elif first_iteration:
            first_iteration = False

        time.sleep(420)

base_url = "https://sabadogol.com.ar/"
start_id_fecha = 140
end_id_fecha = 820
start_id_categoria = 1
end_id_categoria = 25
to_emails = ['destinatario1_@gmail.com','destinatario2_@gmail.com']

scan_and_compare_links(base_url, start_id_fecha, end_id_fecha, start_id_categoria, end_id_categoria)