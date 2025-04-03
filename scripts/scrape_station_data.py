"""
Extracts station coordinates from a pdf table in a ACP report.

ACP Report: https://pancanal.com/wp-content/uploads/2021/09/Anuario-Hidrologico-2022.pdf

INSPECT RESULTS AND MODIFIY AS NEEDED.

Originally scrapee location data from https://www.imhpa.gob.pa/es/estaciones-meteorologicas/,
but one station was in the middle of Alajuela, which was clearly wrong.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from pypdf import PdfReader
import re


def parse_funky_pdf():
    pdf_path = 'Anuario-Hidrologico-2022.pdf'
    reader = PdfReader(pdf_path)

    columns = ['No.', 'Nombre', 'ID', 'Code', 'UTM E', 'UTM N', 'Elevación pie', 'Elevación m',
               'Latitud Norte', 'Longitud Oeste', 'Tipo de Estación', 'Parámetros']    
    data_lists = [[] for _ in columns]

    line_pattern = re.compile(r'^(\d*) ([A-Za-z ].*) ([A-Z]{3}) (\d*) (\d*) (\d*) ([\d\.]*) ([\d\.]*) (\d\d \d\d \d\d\.\d\d) (\d\d \d\d \d\d\.\d\d) ([A-Za-zá \/\.()]*[a-z)]) ([A-Za-z]*)')

    table_text = reader.pages[102].extract_text()
    table_lines = table_text.split('\n')
    for line in table_lines:
        if not line[0].isnumeric():
            continue
        
        match = line_pattern.match(line)
        if match:
            groups = match.groups()
            for i in range(len(columns)):
                data_lists[i].append(groups[i])
        
                
    data_df = pd.DataFrame({columns[i]: data_lists[i] for i in range(len(columns))})
    print(data_df)
    data_df.to_csv('station_data.csv', index=False)



def get_station_data():
    """This site had funky data, so replaced it with pdf. """
    url = 'https://www.imhpa.gob.pa/es/estaciones-meteorologicas/p$?f_institucion=A.C.P.'

    page_dfs = []
    for page_num in range(1, 4):
        page_url = url.replace('$', str(page_num))
        response = requests.get(page_url)

        soup = BeautifulSoup(response.text, 'html.parser')
        table_html = soup.find('table')

        page_df = pd.read_html(str(table_html))[0]
        page_dfs.append(page_df)

    stations_df = pd.concat(page_dfs)
    stations_df['Longitud'] = '-'+stations_df['Longitud']

    stations_df.to_csv('station_data.csv', index=False)



if __name__ == '__main__':
    parse_funky_pdf()