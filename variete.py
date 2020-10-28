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
