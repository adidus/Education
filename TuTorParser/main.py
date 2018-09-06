import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from pymongo import MongoClient
from mongoengine import Document
from mongoengine import StringField
from mongoengine import connect


def get_html(url):
    r = requests.get(url)
    return r.text

class tor(Document):
    title = StringField()
    reference = StringField()
    tag = StringField()

def get_references(html, tag):
    http = 'http://www.rutor.org.new-rutor.org'
    soup = BeautifulSoup(html, 'lxml')
    tr = soup.find('div', id = 'index')
    tum = tr.find_all('tr', class_ = 'tum')
    gai = tr.find_all('tr', class_ = 'gai')
    table = tum + gai
    # rfrs = []
    # names = []
    for row in table:
        name = get_names(row)
        refer = row.find('a', class_ = 'downgif').get('href')
        refer = http + refer
        torent = tor(title=name, reference=refer)
        torent.save()
        # data = {'name': name,
        #         'reference': refer,
        #         'tag': tag}
        # record_Mongo(data)

    # references = [http + x for x in rfrs]
    # return(names, references)

def get_names(row):
    res = []
    res = re.findall('href="\/t.*<\/a><\/td>', str(row))
    res = re.findall('">.*<\/a', str(res))
    res[0] = str(res[0])[:-4]
    res[0] = str(res[0])[2:]
    return(res[0])

# def get_size(row):
#     res = []
#     res = re.findall('ght\">\d*.\d*\.\w\w', str(row))
#     res[0] = str(res[0])[6:]
#     print(res[0])
#     return(res[0])


# def record_Mongo(data):
#     db = client['TorentBase']
#     col = db['references']
#     col.insert_one(data)




client = MongoClient('mongodb://localhost:27017')
connect('To')


def main():
    ht = 'http://www.rutor.org.new-rutor.org/browse/'
    tags = {'Films': 1,
            'OurFilms': 5,
            'ScienceFilms': 12,
            'Serials': 4,
            'TV': 6,
            'Anime': 10,
            'Music': 2,
            'Games': 8,
            'Soft': 9,
            'Books': 11}

    for tag in tags:
        for i in range(1):
            url_gen = ht + str(i) + '/' + str(tags[tag]) + '/0/0/'
            htm = get_html(url_gen)
            get_references(htm, tag)


if __name__ == '__main__':
    main()

#engine record
#docker ?
#size, data
#return