import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
link1="https://cdn.bancentral.gov.do/documents/entorno-internacional/documents/Serie_Historica_Spread_del_EMBI.xlsx"

embi=pd.read_excel(link,skiprows=1, index_col=0)
link2="https://www.indec.gob.ar/ftp/cuadros/economia/sh_ipc_aperturas.xls"

ipc=(pd.read_excel(link2,skiprows=5, nrows=3, sheet_name="Índices aperturas").T).reset_index()
ipc=ipc.iloc[1:,[0,3]] 
ipc.columns =["Fecha","IPC"]
ipc=ipc.set_index("Fecha")
ipc["Inflation (M)"]=ipc["IPC"].pct_change(1)
ipc["Inflation (A) "]=ipc["IPC"].pct_change(12)


link3="https://www.indec.gob.ar/ftp/cuadros/economia/sh_emae_mensual_base2004.xls"

emae=pd.read_excel(link3,skiprows=4).iloc[:,[1,3,5]].dropna()

emae.columns=["EMAE", "EMAE Des." , "EMAE T-C"]

start= datetime.strptime("2004-01-01", "%Y-%m-%d")
end=datetime.now()
fechas=pd.date_range(start,end, freq='MS').strftime("%m-%Y")
emae["Fecha"]=fechas[:len(emae)]
emae=emae.set_index("Fecha")

link4="https://www.indec.gob.ar/ftp/cuadros/economia/sh_emae_actividad_base2004.xls"
emae2=pd.read_excel(link4,skiprows=2).iloc[:,1:].dropna()
emae2["Fecha"]=fechas[:len(emae2)]
emae2=emae2.set_index("Fecha")

link5="https://www.indec.gob.ar/ftp/cuadros/economia/sh_ipi_manufacturero_2020.xls"
ipi=pd.read_excel(link5,sheet_name="Cuadro 1",skiprows=7).iloc[:,[3,7,10]].dropna()
ipi.columns=["IPI", "IPI Des." , "IPI T-C"]

start1= datetime.strptime("2016-01-01", "%Y-%m-%d")
end1=datetime.now()
fechas1=pd.date_range(start1,end1, freq='MS').strftime("%m-%Y")
ipi["Fecha"]=fechas1[:len(ipi)]
ipi=ipi.set_index("Fecha")

link6="https://www.indec.gob.ar/ftp/cuadros/economia/sh_oferta_demanda_desest_09_20.xls"
pbi=pd.read_excel(link6,sheet_name="desestacionalizado n",skiprows=3).iloc[:,3:].dropna()

start2= datetime.strptime("2004-01-01", "%Y-%m-%d")
end2=datetime.now()
fechas2=pd.date_range(start2,end2, freq='Q').strftime("%m-%Y")
pbi["Fecha"]=fechas2[:len(pbi)]
pbi=pbi.set_index("Fecha")

link7="http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/Base%20de%20Resultados%20del%20REM%20web.xlsx"
rem=pd.read_excel(link7,sheet_name="Base de Datos Completa",skiprows=1)
rem["Período (ant)"]=rem['Período'].copy()
rem.loc[rem['Período'].str.contains('Trim', na=False),"Período"]=pd.to_datetime(rem[(rem['Período'].str.contains('Trim', na=False))]["Período"].replace({"IV": "12", "III": "9", "II": "6", "I": "3"}, regex=True).str.strip().str[6:], format="%m-%y").copy()

rem.loc[(rem['Período'].str.contains('Próx')) & (rem['Período'].str.contains('12')),"Período"]=pd.to_datetime(rem[(rem['Período'].str.contains('Próx')) & (rem['Período'].str.contains('12'))]["Fecha de pronóstico"]).dt.date+relativedelta(months=12)

rem.loc[(rem['Período'].str.contains('Próx')) & (rem['Período'].str.contains('24')),"Período"]=pd.to_datetime(rem[(rem['Período'].str.contains('Próx')) & (rem['Período'].str.contains('24'))]["Fecha de pronóstico"]).dt.date+relativedelta(months=24)


base_mon = pd.read_excel(link,'BASE MONETARIA',skiprows=8,index_col=0)
base_mon=base_mon.loc[:"Mes"].iloc[:-1]
total = base_mon.isnull().sum().sort_values(ascending=False)
porcentaje = (base_mon.isnull().sum()/base_mon.isnull().count()).sort_values(ascending=False)
data_faltante = pd.concat([total, porcentaje], axis=1, keys=['Total', 'Porcentaje'])
base_mon=base_mon.drop((data_faltante[data_faltante['Porcentaje'] > 0.9]).index,1)
start_bcra= datetime.strptime("2003-01-02", "%Y-%m-%d")
end_bcra=datetime.now()
fechas_bcra=pd.DataFrame(pd.date_range(start_bcra,end_bcra, freq='d'))
fechas_bcra=fechas_bcra.set_index(0)
base_mon=fechas_bcra.merge(base_mon,  how="inner",left_index=True, right_index=True)
base_mon.columns=['Total Factores', 'Intervención cambiaria', 'Op. de divisas con el Tesoro', 'Adelantos Transitorios', 'Transferencia de Utilidades', 'Resto Tesoro', 'Pases', 'LELIQ', 'Redescuentos y Adelantos', 'Intereses', 'LEBAC y NOBAC', 'Rescate de Cuasimonedas', 'Otros', 'Var. Billetes y Monedas en Poder del Público', 'Var. Billetes y Monedas en Entidades', 'Var. Cheques Cancelatorios', 'Var. Cuenta Corriente en el BCRA', 'Var. Base Monetaria', 'Var. Cuasimonedas', 'Var. Base Monetaria + cuasimonedas', 'Billetes y Monedas en Poder del Público', 'Billetes y Monedas en Entidades', 'Cheques Cancelatorios', 'Cuenta Corriente en el BCRA', 'Base Monetaria', 'Cuasimonedas', 'Base Monetaria + cuasimonedas']
base_mon.index = pd.to_datetime(base_mon.index)


rrii = pd.read_excel(link,'RESERVAS',skiprows=8,index_col=0)
rrii=rrii.loc[:"Mes"].iloc[:-1]
total =  rrii.isnull().sum().sort_values(ascending=False)
porcentaje = (rrii.isnull().sum()/rrii.isnull().count()).sort_values(ascending=False)
data_faltante = pd.concat([total, porcentaje], axis=1, keys=['Total', 'Porcentaje'])
rrii=rrii.drop((data_faltante[data_faltante['Porcentaje'] > 0.9]).index,1)

rrii=fechas_bcra.merge(rrii,  how="inner",left_index=True, right_index=True)
rrii.columns=['RRII', 'Oro, Divisas, Colocaciones a Plazo y Otros', 'Divisas - Pase Pasivo en USD con el Exterior', 'Var. RRII', 'Intervenciones', 'OOII', 'Otros Sec. Pub.', 'Encajes', 'Otros', 'DEG', 'TCN']
rrii.index = pd.to_datetime(rrii.index)


depositos = pd.read_excel(link,'DEPOSITOS',skiprows=6,index_col=0)
depositos=depositos.loc[:"Variaciones Fin de Mes"].iloc[:-1]
total = depositos.isnull().sum().sort_values(ascending=False)
porcentaje = (depositos.isnull().sum()/depositos.isnull().count()).sort_values(ascending=False)
data_faltante = pd.concat([total, porcentaje], axis=1, keys=['Total', 'Porcentaje'])
depositos=depositos.drop((data_faltante[data_faltante['Porcentaje'] > 0.5]).index,1)
depositos.columns=['Cuenta Corriente', 'Caja de Ahorros', 'Plazo Fijo', 'Plazo Fijo UVA', 'Otros Dépositos', 'CEDROS con CER', 'Total Depósitos en Pesos', 'BODEN contabilizado', 'Total Depósitos en Pesos+BODEN', 'Cuenta Corriente Priv.', 'Caja de Ahorros Priv.', 'Plazo Fijo  Priv.', 'Plazo Fijo UVA  Priv.', 'Otros Dépositos  Priv.', 'CEDROS con CER  Priv.', 'Total Depósitos en Pesos  Priv.', 'BODEN contabilizado  Priv.', 'Total Depósitos en Pesos+BODEN  Priv.', 'Depósitos en Dólares (expresados en Pesos)', 'Depósitos en Dólares Priv. (expresados en Pesos)', 'Total Depósitos ', 'Total Depósitos  Priv.', 'Depósitos en Dólares', 'Depósitos en Dólares Priv.', 'M2']
depositos=depositos.loc[depositos.index.isin(fechas_bcra.index)]

m2=base_mon[["Base Monetaria",'Billetes y Monedas en Poder del Público',  'Cheques Cancelatorios']]
m2=m2.merge(depositos[['Cuenta Corriente Priv.', 'Caja de Ahorros Priv.']], left_index=True, right_index=True)
m2["M2"]=m2[['Billetes y Monedas en Poder del Público',  'Cheques Cancelatorios','Cuenta Corriente Priv.', 'Caja de Ahorros Priv.']].sum(axis=1)

link_uva="http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/diar_uva.xls"
uva=pd.read_excel(link_uva,skiprows=26).iloc[:,[1]]
uva.columns=["UVA"]
start_uva= datetime.strptime("2016-03-31", "%Y-%m-%d")
end_uva=datetime.strptime("2025-03-31", "%Y-%m-%d")
fechas_uva=pd.date_range(start_uva,end_uva, freq='d')
uva["Fecha"]=fechas_uva[:len(uva)]
uva=uva.set_index("Fecha")
uva=uva.drop_duplicates()
uva.index=pd.to_datetime(uva.index)

m2=m2.merge(uva,left_index=True, right_index=True, how="inner")
m2["M2 real"]=(m2["M2"]/m2["UVA"])*m2[m2.UVA==m2.UVA[-1]]["UVA"][0]
m2["Base Monetaria real"]=(m2["Base Monetaria"]/m2["UVA"])*m2[m2.UVA==m2.UVA[-1]]["UVA"][0]


start= datetime.strptime("1990-01-01", "%Y-%m-%d")
end=datetime.now()
fechas=pd.date_range(start,end, freq='MS').strftime("%Y-%b").tolist()
link1="https://www.indec.gob.ar/ftp/cuadros/economia/balanmensual.xls"
link2="http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/Anexo.xls"


ICA= pd.read_excel(link1,skiprows=6)
ICA=ICA.iloc[:,[1,2,7]].dropna()
ICA.columns=["Mes", "Exportaciones", "Importaciones"]
ICA["Fecha"]=fechas[:len(ICA)]
ICA=ICA.set_index("Fecha")
ICA["Saldo ICA"]=ICA["Exportaciones"]-ICA["Importaciones"]
ICA12=ICA.rolling(12).sum()


link2="http://www.bcra.gov.ar/Pdfs/PublicacionesEstadisticas/Anexo.xls"
MULC= pd.read_excel(link2,"Balance Cambiario Mensual" ,skiprows=25)
MULC=MULC.iloc[:,[5,6]].dropna()
MULC.columns=["Exportaciones (M)","Importaciones (M)"]
MULC["Saldo MULC"]=MULC["Exportaciones (M)"]-MULC["Importaciones (M)"]
MULC["Fecha"]=fechas[156:(156+len(MULC))]
MULC=MULC.set_index("Fecha")


saldo_com=ICA.merge(MULC, left_index=True, right_index=True, how="left")
saldo_com.index=pd.to_datetime(saldo_com.index, format="%Y-%b")

chart=saldo_com[["Saldo ICA","Saldo MULC"]].loc["2020"].cumsum()
mpl.rcParams['figure.dpi'] = 300

fig = plt.figure(figsize=(8, 4)) 
ax = fig.add_subplot(111) 
ax.plot(chart.index ,chart, marker="o", alpha=0.8,linewidth=3)
plt.gca().set_yticklabels(['{:,.0f}'.format(x).replace(',','.') for x in plt.gca().get_yticks()]) 

ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%Y"))


plt.xlabel("")
plt.title("Saldo Comercial Devengado y Caja Acumulado 2020",color='#3D3D3E',**{'fontname':'Calibri'})
legend= plt.legend(["Saldo (INDEC)","Saldo (BCRA)"],loc='upper left',frameon=False)  
plt.xticks(rotation=90)


