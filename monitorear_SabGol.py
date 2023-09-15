import requests
import hashlib
import time
import smtplib
from email.mime.text import MIMEText

smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "clara.santillan.01@gmail.com"
smtp_password = "kjxpppupshsvndgs"

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

def scan_and_compare_multiple_links(base_url, num_links, category_ids):
    previous_hashes = {(i, j): "" for i in range(1, num_links + 1) for j in category_ids[i]}
    first_iteration = True
    changed_links = []

    while True:
        changed_links.clear()
        change_detected = False

        for i in range(1, num_links + 1):
            current_url = f"{base_url}categoria.php?id={i}&a="
            page_ids_to_monitor = category_ids[i]

            for page_id in page_ids_to_monitor:
                additional_url = f"{base_url}fecha.php?id={page_id}"
                current_content = get_page_content(additional_url)

                if current_content:
                    current_hash = calculate_hash(current_content)

                    if not compare_hashes(previous_hashes[(i, page_id)], current_hash):
                        print(f"¡Se detectó un cambio en {additional_url}!")
                        previous_hashes[(i, page_id)] = current_hash
                        changed_links.append(additional_url)
                        change_detected = True
                    else:
                        print(f"No se encontraron cambios en {additional_url}.")

            if change_detected:
                print(f"¡Se detectó un cambio en la categoría {i}! Enlace: {current_url}")
            else:
                print(f"No se ha detectado ningún cambio en la categoría {i}.")

        if change_detected and not first_iteration:
            subject = "Cambio detectado en SabadoGol"
            message = "Se ha detectado un cambio en los siguientes enlaces:\n\n"
            message += "\n".join(changed_links)

            msg = MIMEText(message)
            msg["Subject"] = subject
            msg["From"] = smtp_username
            msg["To"] = to_email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, to_email, msg.as_string())
            change_detected = False
        elif first_iteration:
            first_iteration = False

        time.sleep(360)  # Escanear cada 6 minutos

base_url = "https://sabadogol.com.ar/"
num_links_to_scan = 15
category_ids = {}
for i in range(1, 16):
  category_ids[i] = list(range(420, 470))

to_email = "bautistagil665@gmail.com"

scan_and_compare_multiple_links(base_url, num_links_to_scan, category_
