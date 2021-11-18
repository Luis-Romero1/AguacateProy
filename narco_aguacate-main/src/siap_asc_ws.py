
# Obtención de datos de la Producción mensual de aguacate de 2018 a 2020
# por entidad federativa.
# https://nube.siap.gob.mx/avance_agricola/
#
# WebScrapping usando selenium para modificar formularios desarrollados en javascript
# y extraer el código HTML de las tablas generadas en la consulta.
#
# Microsoft Edge 89.0.774.48

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

url = "https://nube.siap.gob.mx/avance_agricola/"
tbls_html = []

web = webdriver.Edge("msedgedriver.exe", )
web.get(url)

time.sleep(0.7)
cicloProd = Select(web.find_element_by_id("cicloProd"))
cicloProd.select_by_value("3") # Código para Perennes

time.sleep(0.7)
modalidad = Select(web.find_element_by_id("modalidad"))
modalidad.select_by_value("3") # Código para Riego + Temporal

time.sleep(0.7)
cultivo = Select(web.find_element_by_id("cultivo"))
cultivo.select_by_value("7") # Código para Aguacate

time.sleep(1)
for anio in range(2018, 2021):

    time.sleep(0.8)
    anioagric = Select(web.find_element_by_id("anioagric"))
    anioagric.select_by_value(str(anio))

    for mes in range(1, 13):

        time.sleep(0.8)
        mesagric = Select(web.find_element_by_id("mesagric"))
        mesagric.select_by_value(str(mes))

        time.sleep(0.8)
        consultar = web.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pull-right", " " ))]')
        consultar.click() # Botón de consulta
        
        time.sleep(1)
        tbl_html = web.find_element_by_id("Resultados-reporte").get_attribute("outerHTML")
        tbls_html.append(tbl_html)

time.sleep(0.5)
web.close()

f = open("../data/raw/produccion/tbls_html.txt", "w")
f.write("\n".join(tbls_html))
f.close()