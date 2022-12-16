import api
import website
import json
import os
import requests
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def set_up_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def make_tables(cur, conn):
    api.pos_table(cur, conn)
    api.pos_neg_table(cur, conn)
    website.get_data_from_website(cur, conn)

def analyze(cur, conn):
    api.analyze_from_api(cur, conn)
    website.analyze_from_website(cur, conn)

def main():
    cur, conn = set_up_db("covid.db")
    make_tables(cur, conn)
    analyze(cur, conn)

if __name__ == "__main__":
    main()