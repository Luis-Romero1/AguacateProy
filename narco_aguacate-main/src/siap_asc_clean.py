
# Lectura y limpieza de tablas consultadas por WebScrapping para
# la producción mensual de aguacate de aguacate de 2018 a 2020

import pandas as pd
import itertools
import janitor


def clean_tbl(tbl, args):
    # Limpieza de dataframes
    anio, mes = args
    tbl.columns = tbl.columns.droplevel()
    tbl["Anio"] = anio
    tbl["Mes"] = mes
    return tbl


def parse_html(path):
    tbls = pd.read_html(path, index_col=0)
    cp = itertools.product(range(2018, 2021), range(1, 13))

    tbls = [*map(lambda pair: clean_tbl(pair[0], pair[1]), zip(tbls, [*cp]))]
    tbl = pd.concat(tbls, ignore_index=True).clean_names()

    return tbl


parse_html("../data/raw/produccion/tbls_html.txt") \
    .to_csv("../data/processed/asc_entidad.csv", index=False)

parse_html("../data/raw/produccion/tbls_mich_html.txt") \
    .to_csv("../data/processed/asc_michoacan.csv", index=False)
