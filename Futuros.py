!pip install tabula-py
import tabula
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt  
from datetime import datetime

dates = ["2014-01-01", "2020-08-01"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
fechas=pd.date_range(start,end, freq='MS').strftime("%Y-%b").tolist()


mes=["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
años=np.arange(14,21)
periodos=[]

for a in años:
  for m in mes:
    periodos.append(m+a.astype(str))


futuros=list()
for p,f in zip(periodos[:-4],fechas): 
  file = "http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/temp{}.pdf".format(p)
  neta = [f, tabula.read_pdf(file, pages = 4, multiple_tables = True)[0].iloc[2,1]]
  futuros.append(neta)

futuros_bcra=pd.DataFrame(futuros,columns=['Fecha', 'Futuros'])
futuros_bcra["Futuros"]=-futuros_bcra["Futuros"].str.replace(',', "").astype(float).fillna(0)
futuros_bcra=futuros_bcra.set_index("Fecha")
futuros_bcra.index= pd.to_datetime(futuros_bcra.index, format="%Y-%b")


plt.style.use('ggplot')

sns.set_style("white")
fig, ax1 = plt.subplots(figsize=(12, 6))
eta=1e-6
y1positive=(futuros_bcra["Futuros"]+eta)>=0
y1negative=(futuros_bcra["Futuros"]-eta)<=0

#ax1.plot(futuros_bcra, color="black")
ax1.fill_between(futuros_bcra.index,futuros_bcra["Futuros"], 0,where=y1negative, facecolor='#00bfc4',interpolate=False,label="Comprado")
ax1.fill_between(futuros_bcra.index,0, futuros_bcra["Futuros"],where=y1positive, facecolor='#F8766D',interpolate=False,label="Vendido")


ax1.tick_params(axis='y')
plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in plt.gca().get_yticks()]) 

ax1 = plt.gca()  # only to illustrate what `ax` is
ax1.autoscale(enable=True, axis='x', tight=True)

ax1.axhline(y=0, linestyle='--', color='black',linewidth=0.5 )
plt.ylabel("Millones de USD")
plt.title("Posición en Futuros del BCRA")
plt.xticks(rotation=90)
plt.legend()  
plt.show()
