from xml.sax import parseString
import requests
from bs4 import BeautifulSoup
import os
import sqlite3
import matplotlib.pyplot as plt
import numpy as np



def get_data_from_website(): 
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path+'/'+'covid.db')
        cur = conn.cursor()
        #cur.execute("DROP TABLE IF EXISTS Unemployment")
        cur.execute("CREATE TABLE IF NOT EXISTS Unemployment (id_key INTEGER, place TEXT, march_2020 INTEGER, march_2021 INTEGER, UNIQUE(place, march_2020, march_2021))")
        states = []
        march2020 = []
        march2021 = []
        url = "https://www.bls.gov/news.release/archives/laus_04162021.htm"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, 'html.parser')
        unemployment_table = soup.find('table',class_="regular")
        states_and_territories = unemployment_table.find_all('p',class_="sub0")
        for place in states_and_territories: 
            states.append(place.text)
        for i in range(1,53):
            row2020 = unemployment_table.find_all('td',headers="lau_srd_tb1.r."+str(i)+" lau_srd_tb1.h.1.6 lau_srd_tb1.h.2.10 lau_srd_tb1.h.3.10")
            row2021 = unemployment_table.find_all('td',headers="lau_srd_tb1.r."+str(i)+" lau_srd_tb1.h.1.6 lau_srd_tb1.h.2.10 lau_srd_tb1.h.3.13")
            for data in row2020: 
                if data.text == "-": 
                    march2020.append(0)
                else:
                    march2020.append(float(data.text))
            for data in row2021: 
                if data.text == "-": 
                    march2021.append(0)
                else:
                    march2021.append(float(data.text))
        unemployment_data = soup.find('table',class_= "regular",id="lau_srd_tb2")
        states_and_territories_2 = unemployment_data.find_all('p',class_="sub0")
        for place in states_and_territories_2: 
            states.append(str(place.text) + " (not seasonally adjusted)")
        for i in range(1,53):
            col2020 = unemployment_data.find_all('td',headers="lau_srd_tb2.r."+str(i)+" lau_srd_tb2.h.1.6 lau_srd_tb2.h.2.10 lau_srd_tb2.h.3.12 lau_srd_tb2.h.4.12")
            col2021 = unemployment_data.find_all('td',headers="lau_srd_tb2.r."+str(i)+" lau_srd_tb2.h.1.6 lau_srd_tb2.h.2.10 lau_srd_tb2.h.3.12 lau_srd_tb2.h.4.13")
            for data in col2020: 
                if data.text == "-": 
                    march2020.append(0)
                else:
                    march2020.append(float(data.text))
            for data in col2021: 
                if data.text == "-": 
                    march2021.append(0)
                else:
                    march2021.append(float(data.text))
        id_key = [] 
        for i in range(1,len(states)+1): 
            id_key.append(i)
        final_tuples = list(zip(id_key,states,march2020,march2021))
        cur.execute("SELECT MAX(id_key) FROM Unemployment")
        max_key = cur.fetchone()[0]
        if max_key == None:
            max_key = 0
        for i in range(max_key,max_key+25): 
            id= final_tuples[i][0]
            place= final_tuples[i][1]
            march2020 = final_tuples[i][2]
            march2021 = final_tuples[i][3]
            cur.execute("INSERT OR IGNORE INTO Unemployment (id_key, place, march_2020 , march_2021) VALUES (?, ?, ?, ?)", (id, place, march2020, march2021))
        conn.commit()
    except IndexError: 
        print("All data added to database")
        return None

def analyze_from_website():
    total_2020 = 0 
    count_2020 = 0 
    total_2021 = 0 
    count_2021 = 0 
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'covid.db')
    cur = conn.cursor()
    cur.execute("SELECT march_2020 FROM Unemployment")
    conn.commit()
    for num in cur.fetchall(): 
        total_2020 += num[0]
        count_2020+=1 
    avg_2020 = total_2020 / count_2020
    result = cur.execute("SELECT march_2021 FROM Unemployment")
    conn.commit()
    for i in result.fetchall():
        total_2021 += i[0]
        count_2021+=1 
    avg_2021 = total_2021 / count_2021
    f = open("website_data.txt", "w")
    f.write("The total unemployment rate for March 2020 was "+str(total_2020)+".\n")
    f.write("The total unemployment rate for March 2021 was "+str(total_2021)+".\n")
    f.write("To find the average unemployment rate for each year, we divided the total unemployment rate (sum) by the count.\n")
    f.write("The average unemployment rate for March 2020 was "+str(avg_2020)+".\n")
    f.write("The average unemployment rate for March 2021 was "+ str(avg_2021)+".\n")
    f.close()
    x = np.arange(2)
    y = [avg_2020, avg_2021]
    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color = "red", align = "center", width= 0.4)
    plt.title('Unemployment Rate Before and After COVID19')
    plt.xlabel('Year')
    plt.ylabel('Unemployment Rate')
    plt.xticks(x, ('March 2020', 'March 2021'))
    plt.show()

get_data_from_website()
analyze_from_website()