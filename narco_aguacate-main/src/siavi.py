
# Obtención y limpieza de datos sobre Exportaciones Mensuales de Aguacate de 2003 a 2020
# http://www.economia-snci.gob.mx/

import requests
import pandas as pd
import janitor
import time


def clean_data_exp(tbl, anio, tipo):
    # Limpieza de dataframes obtenidos
    tbl_wide = (tbl
                .iloc[:-1, 0:13]
                .clean_names()
                .rename(columns={"exportaciones": "pais"})
                .assign(anio=anio, tipo=tipo))
    tbl_long = pd.melt(tbl_wide,
                       var_name="mes",
                       value_name="unidades",
                       id_vars=["tipo", "pais", "anio"],
                       value_vars=["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                   "septiembre", "octubre", "noviembre", "diciembre"])
    return tbl_long


def load_exp(response, anio):
    # Extracción y concatenación de dataframes
    data = pd.read_html(response.text)
    tbl = pd.concat([clean_data_exp(data[3], anio, "USD"),
                     clean_data_exp(data[5], anio, "Kg")])
    return tbl


endpoint = "http://www.economia-snci.gob.mx/siavi4/frac_mensual.php"
tbls = []

for anio in range(2003, 2021):
    time.sleep(15)
    payload = {'fraccion': f"mensual,{anio},08044001"}
    resp = requests.get(endpoint, payload)
    tbls.append(load_exp(resp, anio))


pd.concat(tbls).to_csv("../data/processed/exportaciones_mensuales.csv", index=False)

