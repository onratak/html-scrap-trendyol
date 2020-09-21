# -*- coding: utf-8 -*-
"""
Spyder Editor
Onur ATAK
"""
import openpyxl as op
from openpyxl.styles import Font
import requests as rq
from bs4 import BeautifulSoup
import time
from random import randint

# from os.path  import basename



wb2=op.load_workbook("temp.xlsx")
sayfano=1

# tempsheet=wb2["Sayfa"+str(sayfano)]
tempsheet=wb2["Sayfa1"]
kontrol_liste=[] #link kontrol listesi
liste_temp=[]  
def listeyazdir(satir,gelenliste,tip):
    limit=len(gelenliste)
    for i in range(0,limit):
        hucre=tempsheet.cell(row=satir,column=i+1)
        hucre.value=gelenliste[i]
        if(tip==1):
            hucre.font = hucre.font.copy(bold=True)
      
def tempyazdir(text,url): #çekilen verileri geçiçi listeye yazdır
    liste_temp=[]
    liste_temp.append(text)
    liste_temp.append(url)
    kontrol_liste.append(liste_temp)
    
# def sayfatara(gelenlink):
#     sayfa_istek=rq.get(gelenlink)
#     sorgusayfa=(sayfa_istek.content,"lxml")
#     print("ok")



# burada kategorileri ayrıntılı al 
r=rq.get("http://www.trendyol.com/") #trendyola sorgu attık
sorgu=BeautifulSoup(r.content,"lxml") #lxml kütüphanesini kullanacığımı belirttik

##sitedeki ürünlerin kategori linkleri

tablinkler=sorgu.find_all("div",attrs={"class":"category-box"}) # burası bütün kategoriyi alıyor +
print("byraya kadar")

#%% alt linklerin hepsini alıyor

# bb=0
# for tablink in tablinkler:
#     alt_tablink=tablink.find("ul",attrs={"class":"sub-item-list"})
#     tablink_li=tablink.find_all("li")
#     for tabb in tablink_li:
#         altlinktext=tabb.text
#         altlink=tabb.find("a").get("href")
#         print(altlinktext,altlink)
#     bb+=1
#     print(bb,"-"*10)

#%% GET CATEGORİES FROM TRENDYOL.COM
# GET CATEGORİES
# GET CATEGORİES
# GET CATEGORİES
# GET CATEGORİES


excel_satir=0
bb=0
for alt_kategori_baslik in tablinkler:
    print(alt_kategori_baslik.find("a").text) # ana / üst kategoriler ( koyu yazanlar)
    print(alt_kategori_baslik.find("a").get("href")) # ana / üst kategoriler ( koyu yazanlar)
    print(excel_satir,"-"*50)
    koyulink_text=alt_kategori_baslik.find("a").text
    koyulink_url=alt_kategori_baslik.find("a").get("href")
    # tempyazdir(koyulink_text,koyulink_url)
    
    liste_temp=[]
    liste_temp.append(koyulink_text)
    liste_temp.append(koyulink_url)
    kontrol_liste.append(liste_temp) # CATEGORİES
     
    
    
    excel_satir+=1
    listeyazdir(excel_satir,liste_temp,1) # ana / üst kategoriler ( koyu yazanlar) yazdir

    alt_tablink=alt_kategori_baslik.find("ul",attrs={"class":"sub-item-list"}) #koyu kategori altı
    tablink_li=alt_kategori_baslik.find_all("li")#koyu kategori altı
    liste_temp=[]
    for tabb in tablink_li:
        altlink_text=tabb.text #koyu kategori altı
        altlink_url=tabb.find("a").get("href") #koyu kategori altı
        # tempyazdir(altlink_text,altlink_url) #koyu kategori altı
        
        liste_temp=[]
        liste_temp.append(altlink_text)
        liste_temp.append(altlink_url)
        kontrol_liste.append(liste_temp)
            
        excel_satir+=1
        listeyazdir(excel_satir,liste_temp,0) #koyu kategori altı
        
numara="_categories"
wb2.save("result{}.xlsx".format(numara))
#%% GET PRODUCTS AND PRİCE FROM CATEGORİES TABLE ( kontrol_liste)
starttime=time.time()
##burası çalışıyor
urun_listesi=[]   
excelsatir=0
pages=500 #500# ürün pi sayfa sayısı
for sayfa_link in kontrol_liste:
    print(sayfa_link[1])

sayac=0

for sayfa_link in kontrol_liste:
    # print(sayfa_link[1])
    listelinki="https://www.trendyol.com{}?pi=".format(sayfa_link[1])
    print(listelinki)
    replacefname=sayfa_link[1]
   
    random_time=randint(60, 100)
    time.sleep(random_time)
    sayac+=1
    if sayac%4==0:
        time.sleep(100+random_time)
        
    sorgu=BeautifulSoup(r.content,"lxml") 
       
    ##sadece kadın kategorisi tüm sayfaların listesi
    
    urunler=sorgu.find_all("div",attrs={"class":"p-card-wrppr"})
    liste_temp.append(sayfa_link[0])
    liste_temp.append(sayfa_link[1])
    urun_listesi.append(liste_temp)
    excelsatir+=1
    listeyazdir(excelsatir,liste_temp,1)
    for sayfakaydir in range(1,pages+1): #sayfa tarayıcı
    # for sayfakaydir in range(200,250):
        time.sleep(10)
        pageRequest=rq.get(listelinki+str(sayfakaydir)) #trendyola sorgu attık
        sorgu=BeautifulSoup(pageRequest.content,"lxml") 
        print(pageRequest.url,pageRequest.status_code)
        if(pageRequest.status_code==200): # sayfa yok hatası gelmiyorsa devam
            urunler=sorgu.find_all("div",attrs={"class":"p-card-wrppr"})
            for bilgi in urunler: #sayfa ürün ayıklayıcı
                liste_temp=[]
                try:
                    liste_temp.append(bilgi.find("span",attrs={"class":"prdct-desc-cntnr-name hasRatings"}).text)
                    liste_temp.append(bilgi.find("div",attrs={"class":"prc-box-sllng"}).text)
                    # print(bilgi.find("img",attrs={"class":"p-card-img"}))
                    # resimler=bilgi.find("img",attrs={"class":"p-card-img"})
                    # print(resimler.get("src"))
                    # print(resimler.get('data-src'))
                    urun_listesi.append(liste_temp)
                    excelsatir+=1
                    listeyazdir(excelsatir,liste_temp,0)
                except:
                    pass
        else:
            break  
        numara=replacefname.replace('/','')
        print(numara)
        wb2.save("result{}.xlsx".format(numara))
        if(pageRequest.status_code==404): # sayfa bittiğinde durdur
            break 





numara="Urun-Fiyat-isim10"
wb2.save("result{}.xlsx".format(numara))

print('That took {} minutes'.format((time.time()-starttime)/60))


#%%

streaming = ['netflix', 'hulu', 'appletv+', 'disney+']

for kontrol in kontrol_liste:
    # print(kontrol[1])
    index = kontrol_liste.kontrol[1].index('/veri-depolama')
    print('The index of disney+ is:', index)


