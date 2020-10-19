import pandas as pd
import numpy as np
!pip install investpy
from datetime import date
import investpy
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
#!sudo apt-get install msttcorefonts -qq
from pylab import rcParams

import matplotlib as mpl
import warnings; warnings.simplefilter('ignore')

import matplotlib
import matplotlib.font_manager as fm


link ='http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/Serieanual.xls'

CNY = investpy.get_currency_cross_historical_data(currency_cross='CNY/USD',
                                                 from_date='01/01/2014', to_date=date.today().strftime('%d/%m/%Y'))
RRII_N=list()

años=np.arange(2014,2021)
for a in años:
  balance_bcra1 = pd.read_excel(link,'serie semanal {}'.format(a),skiprows=3,index_col=0)
  balance_bcra=balance_bcra1.T
  
  
  total = balance_bcra.isnull().sum().sort_values(ascending=False)
  porcentaje = (balance_bcra.isnull().sum()/balance_bcra.isnull().count()).sort_values(ascending=False)
  data_faltante = pd.concat([total, porcentaje], axis=1, keys=['Total', 'Porcentaje'])
  balance_bcra =balance_bcra.drop((data_faltante[data_faltante['Porcentaje'] >0.95]).index,1)
  bcra_bal=balance_bcra.div(balance_bcra["Tipo de Cambio"].iloc[:,1], axis=0).round(0)
  col_rrii=bcra_bal.columns[bcra_bal.columns.str.contains('Divisas \.\.\..*|Oro .*|Colocaciones realizables en divisas.*|Instrumentos Derivados sobre Reservas.*|Convenios Multilaterales de Crédito.*', regex=True)]

  RRII=bcra_bal[col_rrii]
  RRII.columns = ["Oro","Divisas","Inversiones","Derivados","Convenios"]
  pasivos=-bcra_bal[["CUENTAS CORRIENTES EN OTRAS MONEDAS", "- Asignaciones de DEG....................................................................", "OBLIGACIONES CON ORGANISMOS INTERNACIONALES "]]
  pasivos=pasivos.merge(CNY["Close"],left_index=True, right_index=True,how="inner")
  pasivos.columns =["Encajes","DEG", "BIS","Swap"]
  
  RRII["Inversiones y otros"]=RRII[["Inversiones","Derivados","Convenios"]].sum(axis=1)
  RRII=RRII.drop(columns=["Inversiones","Derivados","Convenios"])
  RRII_netas=RRII.merge(pasivos,left_index=True, right_index=True,how="inner")
  RRII_netas=RRII_netas/1000
  RRII_N.append(RRII_netas)
RRII_Netas=pd.concat(RRII_N)

RRII_Netas["2014":"2018-07"]["Swap"]=RRII_Netas["2014":"2018-07"]["Swap"]*-60000000
RRII_Netas["2018-08":]["Swap"]=RRII_Netas["2018-08":]["Swap"]*-130000000
RRII_Netas["RRII Netas"]=RRII_Netas.sum(axis=1)



import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300


ax=RRII_Netas[["Divisas","Inversiones y otros","Oro","Encajes","DEG", "BIS","Swap"]].plot.area(alpha=0.6,figsize=(7, 4), label=["Divisas","Inverversiones y otros","Oro","Encajes","DEG", "BIS","Swap"])
RRII_Netas["RRII Netas"].plot(color="black",ls="--", label="Reservas Netas")
plt.gca().set_yticklabels(['{:,.0f}'.format(x).replace(',','.') for x in plt.gca().get_yticks()]) 
legend=plt.legend(loc='upper left', ncol=2,frameon=False) #bbox_to_anchor=(.9, -0.4)
plt.ylabel("Millones de USD")
plt.title("Reservas Internacionales")
ax.autoscale(enable=True, axis='x', tight=True)


plt.setp(legend.get_texts(),  fontsize=7)
plt.tick_params(axis='x')
plt.tick_params(axis='y')

ax.set_facecolor('white')




plt.annotate('Fuente: BCRA' , (0,0), (-20,-50), fontsize=9, 
             xycoords='axes fraction', textcoords='offset points', va='top')
ax = plt.gca()
plt.show()
