import pandas as pd
import numpy as np
from datetime import date

from datetime import datetime
import requests

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import matplotlib
import matplotlib.font_manager as fm


link ="http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/seriese.xls"

tasas = pd.read_excel(link,'TASAS DE MERCADO',skiprows=5,index_col=0).iloc[:-4,:21]

BCRA = pd.read_excel(link,'INSTRUMENTOS DEL BCRA',skiprows=5,index_col=0).iloc[:-11,:14]

tasas.columns=[ 'PF', 'PF Min', 'PF Min (TEA)', 'PF +1m (TEA)', 'PF USD', 'PF Min USD', 'PF +1m USD', 'Badlar', 'Badlar priv', 'Badlar priv (TEA)', 'TM20', 'TM20 priv', 'TM20 priv (TEA)', 'Personales', 'Adelantos', 'Call Priv', 'Call Priv Monto', 'Call', 'Call Monto', 'Pases Priv', 'Pases Priv Monto' ]

BCRA.columns=[ 'Pases Pasivos Monto', 'Pases Pasivos c/ FCI', 'Pases Activos Monto', 'LELIQ Monto', 'LEBAC Monto', 'LEBAC c/ Ent. Fin.', 'LEBAC en USD', 'NOCOM', 'Tasa Polt. Mon.', 'Tasa Polt. Mon. (TEA)', 'Pases Pasivos 1d', 'Pases Pasivos 7d', 'Pases Activos 1d', 'Pases Activos 7d' ]
tasas.index = pd.to_datetime(tasas.index)
BCRA.index = pd.to_datetime(BCRA.index)
BCRA=BCRA.apply(pd.to_numeric, errors='coerce')
BCRA["Pasivos Rem. Prom."]=BCRA["Tasa Polt. Mon."]*(BCRA["LELIQ Monto"]/(BCRA["Pases Pasivos Monto"]+BCRA["LELIQ Monto"]))+BCRA["Pases Pasivos 1d"]*(BCRA["Pases Pasivos Monto"]/(BCRA["Pases Pasivos Monto"]+BCRA["LELIQ Monto"]))

Corredor=BCRA[['Pases Pasivos 1d','Pases Activos 1d', "Tasa Polt. Mon.","Pasivos Rem. Prom."]].merge(tasas[["PF Min", "PF", "Adelantos", "Call Priv"]], left_index=True, right_index=True)
link_tcn="http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/com3500.xls"
TCN=pd.read_excel(link_tcn,'TCR diario y TCNPM',skiprows=3,index_col=2)[["Tipo de Cambio de Referencia - en Pesos - por Dólar"]]
TCN.columns=["TCN"]
TCN["Devaluación"]=(((TCN.TCN.pct_change(5)).rolling(20).mean()+1)**(252/5)-1)*100
TCN.index = pd.to_datetime(TCN.index)
Corredor=Corredor.merge(TCN,left_index=True, right_index=True, how="inner")



mpl.rcParams['figure.dpi'] = 500
plt.style.use("seaborn-colorblind")
fig, ax = plt.subplots(figsize=(8, 4))

plt.plot(Corredor.loc["2020"]["Devaluación"],ls="--",label="Devaluación")
for i in ["PF Min", "PF", "Adelantos", "Call Priv","Tasa Polt. Mon.","Pasivos Rem. Prom."]:
    _ = ax.plot(Corredor.loc["2020"][i], label=i)
    _ = ax.legend(frameon=False, fontsize=9) 
plt.fill_between(Corredor.loc["2020"].index,Corredor.loc["2020"]['Pases Pasivos 1d'].astype(float), Corredor.loc["2020"]['Pases Activos 1d'].astype(float),alpha=0.5, facecolor='grey', label="Corredor de pases")
plt.autoscale(enable=True, axis='x', tight=True)  
legend=plt.legend(loc='upper right'  ,frameon=False,ncol=2, fontsize=8)#, ncol=3,bbox_to_anchor=(0.8, -0.4)
plt.title("Tasas de interés")
plt.xticks(rotation=40)
ax.set_facecolor('white')

plt.setp(legend.get_texts())

plt.tick_params(axis='x')
plt.tick_params(axis='y')
plt.ylabel('%')


plt.annotate('Fuente: BCRA\nDevaluación: tasa anual de la var. semanal promedio (20d)', (0,0), (-20,-50), fontsize=9, 
             xycoords='axes fraction', textcoords='offset points', va='top')
