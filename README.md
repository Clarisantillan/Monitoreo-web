# Monitoreo-web
En este proyecto implemento un sistema automatizado de monitoreo web utilizando Python, Selenium, email, smtplib, PIL, Numpy, time, hashlib, request.

-  Diseñé un sistema en forma de Jupyter Notebook que monitorea múltiples páginas web en busca de cambios en su contenido.
- Implementé una función para calcular y comparar hashes del contenido, lo que asegura una detección precisa de cambios.
- Habilité la notificación por correo electrónico cuando se detectan cambios, permitiendo una respuesta inmediata del equipo de colaboradores.

En la carpeta Monitoreo con capturas encontraran 2 archivos, que a diferencia de los otros sitios monitoreados,en estos hago uso de capturas ya que el cambio de contenido es indetectable mediante hash. Por lo que mediante el driver realizo estas capturas de pantalla, que son convertidas a matrices Numpy y luego comparo la distancia entre los histogramas utilizando la distancia del Qui-Square para detectar cambios significativos. En el scrip que monitoreo de 'siguiente fecha' mediante el webdriver ejecuto un script js para automatizar el click al boton que me enseña la sigueinte tabla. En caso de detectar cambios se notifica al cliente mediante email. 
