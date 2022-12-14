import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
# import unittest

# for neg increase
# dates_data[20200301][3] 
# dates_data["20200301"][3] if i make keys strings

# dates from 03/01/20 to 6/08/20:
dates = [20200301, 20200302, 20200303, 20200304, 20200305, 20200306, 20200307, 20200308, 20200309, 20200310, 20200311, 20200312, 20200313, 20200314, 20200315, 20200316, 20200317, 20200318, 20200319, 20200320, 20200321, 20200322, 20200323, 20200324, 20200325, 20200326, 20200327, 20200328, 20200329, 20200330, 20200331, 20200401, 20200402, 20200403, 20200404, 20200405, 20200406, 20200407, 20200408, 20200409, 20200410, 20200411, 20200412, 20200413, 20200414, 20200415, 20200416, 20200417, 20200418, 20200419, 20200420, 20200421, 20200422, 20200423, 20200424, 20200425, 20200426, 20200427, 20200428, 20200429, 20200430, 20200501, 20200502, 20200503, 20200504, 20200505, 20200506, 20200507, 20200508, 20200509, 20200510, 20200511, 20200512, 20200513, 20200514, 20200515, 20200516, 20200517, 20200518, 20200519, 20200520, 20200521, 20200522, 20200523, 20200524, 20200525, 20200526, 20200527, 20200528, 20200529, 20200530, 20200531, 20200601, 20200602, 20200603, 20200604, 20200605, 20200606, 20200607, 20200608] 
    
def get_request_url(date):
    '''
    Builds a request url for an API call

    kripa:
    https://api.covidtracking.com/v1/us/{date}.json
    https://api.covidtracking.com/v1/us/20200501.json
    20200501
    '''
    url = f'https://api.covidtracking.com/v1/us/{date}.json'
    # print(url)
    return url

def get_data(date):
    '''
    Uses the passed search to generate a request_url using the 'get_request_url' function

    If request is successful, add the data to a list (data_list)

    Returns list: data_list
    '''
    url = get_request_url(date)
    
    # Making a get request
    response = requests.get(url)
    data = response.text

    #turns text into a list
    data_dict = json.loads(data)
    data_list = [date, data_dict["positive"], data_dict["positiveIncrease"], data_dict["negative"], data_dict["negativeIncrease"]]
    # print(data_list)
    return data_list

# def compile(dates):
#     dates_data = {}
#     for date in dates:
#         dates_data[date] = get_data(date)
#     # print(dates_data)
#     return dates_data

def compile(dates):
    dates_data = []
    for date in dates:
        dates_data.append(tuple(get_data(date)))
    # print(dates_data)
    return dates_data

# some testing
# get_data(20200501)
# get_data(dates[40])

# in main -- create db
# path = os.path.dirname(os.path.abspath(__file__))
# conn = sqlite3.connect(path+'/'+'covid.db')

# TABLE 1
def pos_table(cur, conn):
    cur = conn.cursor()

    # run compile(dates) function
    compile(dates)

    # create table
    cur.execute("CREATE TABLE IF NOT EXISTS PositiveCases (id_key INTEGER, dates INTEGER, positive_cases INTEGER, positive_increase INTEGER, UNIQUE(dates, positive_cases, positive_increase))")
    tuples = compile(dates)
    id_key = [] 
    for i in range(len(dates)): 
        id_key.append(i+1)
    final_tuples = list(zip(id_key, tuples))
    # print(final_tuples)
    cur.execute("SELECT MAX(id_key) FROM PositiveCases")
    max_key = cur.fetchone()[0]
    if max_key == None:
        max_key = 0
    for i in range(max_key, max_key+25): 
        id = final_tuples[i][0]
        date = final_tuples[i][1][0]
        positive_cases = final_tuples[i][1][1]
        positive_increase = final_tuples[i][1][2]
        cur.execute("INSERT OR IGNORE INTO PositiveCases (id_key, dates, positive_cases, positive_increase) VALUES (?, ?, ?, ?)", (id, date, positive_cases, positive_increase))
    conn.commit()

# TABLE 2
def pos_neg_table(cur, conn):
    cur = conn.cursor()

    # run compile(dates) function
    compile(dates)

    # create table
    cur.execute("CREATE TABLE IF NOT EXISTS NegativeCases (id_key INTEGER, dates INTEGER, positive_cases INTEGER, negative_cases INTEGER, negative_increase INTEGER, UNIQUE(dates, positive_cases, negative_cases, negative_increase))")

    # getting data to add to table
    tuples = compile(dates)
    id_key = [] 
    for i in range(len(dates)): 
        id_key.append(i+1)
    final_tuples = list(zip(id_key, tuples))

    # selecting data from tables
    cur.execute("SELECT MAX(id_key) FROM NegativeCases")

    # adding data to table
    max_key = cur.fetchone()[0]
    if max_key == None:
        max_key = 0
    for i in range(max_key, max_key+25): 
        id = final_tuples[i][0]
        date = final_tuples[i][1][0]
        positive_cases = final_tuples[i][1][1]
        negative_cases = final_tuples[i][1][3]
        negative_increase = final_tuples[i][1][4]
        cur.execute("INSERT OR IGNORE INTO NegativeCases (id_key, dates, positive_cases, negative_cases, negative_increase) VALUES (?, ?, ?, ?, ?)", (id, date, positive_cases, negative_cases, negative_increase))

        # using JOIN to combine tables
        cur.execute("SELECT PositiveCases.id_key, NegativeCases.negative_cases, PositiveCases.positive_cases FROM PositiveCases INNER JOIN NegativeCases ON PositiveCases.dates=NegativeCases.dates;")
    conn.commit()


def analyze_from_api(cur, conn):
    total_pos = 0 
    count_pos = 0 
    total_neg = 0 
    count_neg = 0 
    # getting positive cases total and average
    cur.execute("SELECT positive_cases FROM PositiveCases")
    conn.commit()
    for num in cur.fetchall(): 
        total_pos += num[0]
        count_pos += 1 
    average_pos = total_pos / count_pos
    # getting negative cases total and average 
    result = cur.execute("SELECT march_2021 FROM Unemployment")
    conn.commit()
    for i in result.fetchall():
        total_neg += i[0]
        count_neg += 1 
    average_neg = total_neg / count_neg
    # getting max negative increase
    cur.execute("SELECT PositiveCases.id_key, NegativeCases.negative_cases, PositiveCases.positive_cases FROM PositiveCases INNER JOIN NegativeCases ON PositiveCases.dates=NegativeCases.dates;")
    cur.execute("SELECT negative_increase FROM NegativeCases")
    conn.commit()
    # max_value = None
    # for num in cur.fetchall():
    #     if (max_value is None) or (num > max_value):
    #         max_value = num
    # max_neg = int(max_value)
    max_neg = max(cur.fetchall())
    maxneg = str(max_neg)
    max_neg = maxneg.replace('(','').replace(',)','')
    # print(max_neg)


    # getting max positive increase
    cur.execute("SELECT positive_increase FROM PositiveCases")
    conn.commit()
    # max_value = None
    # for num in cur.fetchall():
    #     if (max_value is None) or (num > max_value):
    #         max_value = num
    # max_pos = int(max_value)
    max_pos = max(cur.fetchall())
    maxpos = str(max_pos)
    max_pos = maxpos.replace('(','').replace(',)','')
    # print(max_pos)

    f = open("api_data.txt", "w")
    f.write("The total amount of positive cases over March 1, 2020 to June 8, 2020 was "+str(total_pos)+".\n")
    f.write("The total amount of negative cases over March 1, 2020 to June 8, 2020 was "+str(total_neg)+".\n")
    f.write("To find the average case numbers over the time period selected, we divided the total number of cases (sum) by the count.\n")
    f.write("The average number of positive cases over March 1, 2020 to June 8, 2020 was "+str(average_pos)+".\n")
    f.write("The average number of negative cases over March 1, 2020 to June 8, 2020 was "+ str(average_neg)+".\n")
    f.write("The maximum number of increase in negative cases over the time period we measured was "+str(max_neg)+".\n")
    f.write("The maximum number of increase in positive cases over the time period we measured was "+str(max_pos)+".\n")
    f.close()

    # first visualization
    x = np.arange(2)
    y = [int(average_pos), int(average_neg)]
    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color = "pink", align = "center", width= 0.4)
    plt.title('Average Positive and Negative Cases of COVID19 From 3/1/20 - 6/8/20')
    plt.xlabel('Type of Case')
    plt.ylabel('Number of Cases')
    plt.xticks(x, ('Positive', 'Negative'))
    plt.show()

    # second visualization
    x = np.arange(2)
    y = [int(max_pos), int(max_neg)]
    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color = "#88c999", align = "center", width= 0.4)
    plt.title('Maximum Number of Increase in Cases of COVID19 From 3/1/20 - 6/8/20')
    plt.xlabel('Type of Case')
    plt.ylabel('Number of Cases')
    plt.xticks(x, ('Positive', 'Negative'))
    plt.show()

    # third visualization
    x = np.arange(2)
    y = [int(total_pos), int(total_neg)]
    plt.figure(figsize=(10, 5))
    plt.bar(x, y, color = "hotpink", align = "center", width= 0.4)
    plt.title('Total Number of Cases of COVID19 From 3/1/20 - 6/8/20')
    plt.xlabel('Type of Case')
    plt.ylabel('Number of Cases')
    plt.xticks(x, ('Positive', 'Negative'))
    plt.show()

# def main():
#     pos_table(conn.cursor(), conn)
#     pos_neg_table(conn.cursor(), conn)
 
# if __name__ == "__main__":
#     main()

# visualization
# SELECT
# date and state id, state and state name

# write json data to database 
# calculations
# visualizations