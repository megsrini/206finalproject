import json
# import unittest
import os
import requests

# for neg increase
# dates_data[20200301][3] 
# dates_data["20200301"][3] if i make keys strings

# dates from 3/1/20 to 6/15/20:
dates = [20200301, 20200302, 20200303, 20200304, 20200305, 20200306, 20200307, 20200308, 20200309, 20200310, 20200311, 20200312, 20200313, 20200314, 20200315, 20200316, 20200317, 20200318, 20200319, 20200320, 20200321, 20200322, 20200323, 20200324, 20200325, 20200326, 20200327, 20200328, 20200329, 20200330, 20200331, 20200401, 20200402, 20200403, 20200404, 20200405, 20200406, 20200407, 20200408, 20200409, 20200410, 20200411, 20200412, 20200413, 20200414, 20200415, 20200416, 20200417, 20200418, 20200419, 20200420, 20200421, 20200422, 20200423, 20200424, 20200425, 20200426, 20200427, 20200428, 20200429, 20200430, 20200501, 20200502, 20200503, 20200504, 20200505, 20200506, 20200507, 20200508, 20200509, 20200510, 20200511, 20200512, 20200513, 20200514, 20200515, 20200516, 20200517, 20200518, 20200519, 20200520, 20200521, 20200522, 20200523, 20200524, 20200525, 20200526, 20200527, 20200528, 20200529, 20200530, 20200531, 20200601, 20200602, 20200603, 20200604, 20200605, 20200606, 20200607, 20200608, 20200609, 20200610, 20200611, 20200612, 20200613, 20200614, 20200615] 
    
def get_request_url(date):
    '''
    Builds a request url for an API call

    kripa:
    https://api.covidtracking.com/v1/us/{date}.json
    https://api.covidtracking.com/v1/us/20200501.json
    2020501
    '''
    url = f'https://api.covidtracking.com/v1/us/{date}.json'
    # print(url)
    return url

def get_data(date):
    '''
    Uses the passed search generate a request_url using the 'get_request_url' function

    If request is successful, add the data to a list (data_list)

    Returns list: data_list
    '''
    url = get_request_url(date)
    
    # Making a get request
    response = requests.get(url)
    data = response.text

    #turns text into a list
    data_dict = json.loads(data)
    data_list = [data_dict["positive"], data_dict["positiveIncrease"], data_dict["negative"], data_dict["negativeIncrease"]]
    # print(data_list)
    return data_list

def compile(dates):
    dates_data = {}
    for date in dates:
        dates_data[date] = get_data(date)
    print(dates_data)
    return dates_data

# need to write json data to database instead 

def main():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # cache_filename = dir_path + '/' + "cache_bestseller.json"
    # get_data(20200501)
    # get_data(dates[40])
    compile(dates)
 
if __name__ == "__main__":
    main()
    # You can comment this out to test with just the main function,
    # But be sure to uncomment it and test that you pass the unittests before you submit!
    # unittest.main(verbosity=2)
