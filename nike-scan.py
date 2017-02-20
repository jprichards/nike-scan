#!/usr/local/bin/python

import bs4
import requests
import sqlite3
import subprocess
from time import localtime, strftime

# CREATE TABLE IF NOT EXISTS "nikemediumtall" (
#   "id" integer(16) PRIMARY KEY,
#   "seen" text(64),
#   "name" text(128),
#   "link" text(256)
# );

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def add_product(conn, product):
    sql = ''' INSERT OR REPLACE INTO nikemediumtall(id,seen,name,link)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, product)

def main():
    database = '/Users/john/github/nike-scan/medium-tall.sqlite'
    link = "http://store.nike.com/us/en_us/pw/mens-clothing/7j8Z1mdZ7puZpipZono"

    r = requests.get(link)
    t = bs4.BeautifulSoup(r.content, "html.parser")
    products = t.find("div", {"class": "exp-product-wall"})

    h = []
    for l in products:
        for a in products.findAll("a"):
            h.append(a.get("href"))

    links = []
    for l in set(h):
        links.append(str(l))

    conn = create_connection(database)
    with conn:
        for x in links:
            pid = x.split("/")[7][4:]
            name = x.split("/")[6].replace('-', ' ')
            link = str(x)
            seen = strftime("%Y-%m-%d %H:%M:%S", localtime())

            product = (pid, seen, name, link)
            add_product(conn,product)


    print str(len(links)) + " products found"

    cmd = ['/usr/local/bin/terminal-notifier', '-title',\
           "Nike Scan", '-message', str(len(links)) + " products found"]
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, err = proc.communicate()
        return output
    except Exception:
        return None
        
if __name__ == '__main__':
    main()
