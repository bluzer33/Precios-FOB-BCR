import time
start=time.time()
import requests
import re
from bs4 import BeautifulSoup
import winsound
import pandas as pd


generic_link='https://www.bcr.com.ar/es/mercados/mercado-de-granos/cotizaciones/cotizaciones-locales/fobfas-argentina/precios-fobfas-'
n=2690  #link del q empieza (contando desde abajo)
m=2680  #hasta el link q llega
N_list=[]
Date_list=[]
Precio_Fob_list=[]
Numeric_Date_list=[]
Numeric_Date_List=[]  #listas y variables q se usan dsp
count=0
p=n-m     
est=round(p/22.9, 2)        #estimación de tiempo
print('Tiempo estimado: '+ str(est)+ ' minutos.')   
try:        #para poner el finally
    while n>=m:     #cuando n<m ya no hay mas links
        start_while=time.time() #arranca el tiempo
        n_str=str(n)
        link=generic_link+n_str #arma el link
        page=requests.get(link) #descarga el codigo de la pag
        soup=BeautifulSoup(page.content, 'html.parser') #parsea el html
        date=soup.find_all(class_='datetime') #busca las fechas
        date_1=str(date[0])
        date_val=date_1[81:115] #las extrae
        
        try:
            td_text=re.search('....Precios FOB comprador. BID', str(soup)) #busca el formato 1 
            cl_text=td_text.group()
            
        except AttributeError:
            try:
                td_text=re.search('....FOB en u.s comprador', str(soup))    #busca el formato 2
                cl_text=td_text.group()
            except:
                cl_text='Error' #si no encuentra pone        
        cl_text=cl_text.replace('f', '9')
        
        try:
            text_class=int(cl_text[:2])+1
            search_str='c'+str(text_class)
            fob=soup.find_all(class_=search_str)
            fob_1=str(fob[0])
            fob_2=fob_1.replace(',', '.')
            val=fob_2[16:22]
            
        except:
            try:
                text_class=cl_text[0]+chr(ord(cl_text[1]) + 1)
                search_str='c'+str(text_class)
                fob=soup.find_all(class_=search_str)
                fob_1=str(fob[0])
                fob_2=fob_1.replace(',', '.')
                val=fob_2[16:22]
            except:
                val='Error'            
        n-=1
        N_list.append(int(n_str))
        Date_list.append(date_val)
        count+=1
        end_while=time.time()
        print('Dato N°'+str(count)+' descargado de '+str(p+1)+ ' totales')
        print('Tardó: '+str(round(end_while-start_while, 2))+' segundos.\n')
        
        try:
            Precio_Fob_list.append(float(val))
        except:
            Precio_Fob_list.append(val)

    for x in Date_list:
        if 'Enero' in x:
            x=x.replace(' de Enero de ', '/1/')
            Numeric_Date_list.append(x)
        elif 'Febrero' in x:
            x=x.replace(' de Febrero de ', '/2/')
            Numeric_Date_list.append(x)
        elif 'Marzo' in x:
            x=x.replace(' de Marzo de ', '/3/')
            Numeric_Date_list.append(x)
        elif 'Abril' in x:
            x=x.replace(' de Abril de ', '/4/')
            Numeric_Date_list.append(x)
        elif 'Mayo' in x:
            x=x.replace(' de Mayo de ', '/5/')
            Numeric_Date_list.append(x)
        elif 'Junio' in x:
            x=x.replace(' de Junio de ', '/6/')
            Numeric_Date_list.append(x)
        elif 'Julio' in x:
            x=x.replace(' de Julio de ', '/7/')
            Numeric_Date_list.append(x)
        elif 'Agosto' in x:
            x=x.replace(' de Agosto de ', '/8/')
            Numeric_Date_list.append(x)
        elif 'Septiembre' in x:
            x=x.replace(' de Septiembre de ', '/9/')
            Numeric_Date_list.append(x)
        elif 'Octubre' in x:
            x=x.replace(' de Octubre de ', '/10/')
            Numeric_Date_list.append(x)
        elif 'Noviembre' in x:
            x=x.replace(' de Noviembre de ', '/11/')
            Numeric_Date_list.append(x)
        else:
            x=x.replace(' de Diciembre de ', '/12/')
            Numeric_Date_list.append(x)
            
            
    for x in Numeric_Date_list:
        z=x.replace('\n','')
        Numeric_Date_List.append(z.strip())
        
    print('Datos descargados')

    tabla=pd.DataFrame({'N° de link': N_list,
                        'Fecha': Numeric_Date_List,
                        'Precio FOB (en u$s)': Precio_Fob_list,})

    tabla.to_excel('try.xlsx', index=False)
    print('Excel creado!')
    end=time.time()
    time_taken=end-start
    print('Tiempo total: '+str(round(time_taken, 2))+' segundos')
    q=2690-n
    time_taken_in_min=time_taken/60
    scraps_per_min=q/time_taken_in_min
    print('Velocidad de procesamiento: '+str(round(scraps_per_min, 2))+' datos por minuto')
finally:
        winsound.PlaySound('C:\\Windows\\media\\Windows Hardware Error.wav', winsound.SND_FILENAME)

