import html5lib
import PyRSS2Gen
import datetime
import lxml
import urllib
import pickle
import time

from ConfigParser import SafeConfigParser

conf = SafeConfigParser()
conf.read("./vars.ini")

f = urllib.urlopen(conf.get('web', 'page'))
doc = html5lib.parse(f, treebuilder='lxml')

L = []

for element in doc.iter():
    if element.tag == '{http://www.w3.org/1999/xhtml}article':
        for i in list(element):
            if i.attrib.get('class') == 'entity-title':
                D = {}
                tmp = i.getchildren()
                D['name'] = tmp[0].attrib['name']
                D['href'] = "http://www.njuskalo.hr/" + tmp[0].attrib['href']
                D['title'] = tmp[0].text.encode('utf-8')
                D['time'] = time.time()
                D['datetime'] = datetime.datetime.now()
            if i.attrib.get('class') == 'entity-description':
                tmp = i.getchildren()
                D['text'] = tmp[0].text.encode('utf-8').strip()
            if i.attrib.get('class') == 'entity-prices':
                tmp = i.getchildren()  # ul
                tmp = tmp[0].getchildren()  # li
                tmp = tmp[0].getchildren()  # strong
                D['price'] = tmp[0].text.encode('utf-8').strip()
                L.append(D)


Lnames = [x['name'] for x in L]

try:
    fdump = open('dump.pickle', 'r')
except IOError:
    fdump = open('dump.pickle', 'w')
    pickle.dump({'data': L}, fdump)
    L2 = L
else:
    tmp = pickle.load(fdump)
    L2 = tmp['data']
    L2names = [x['name'] for x in L2]
    for x in L:
        if x['name'] not in L2names:
            L2names.append(x['name'])
            L2.append(x)
    # clear old
    L2 = [x for x in L2 if x.get('time') is not None
          and (time.time() - x['time']) < 172800]
    fdump = open('dump.pickle', 'w')
    pickle.dump({'data': L2}, fdump)
    f.close()


def f(x):
    return PyRSS2Gen.RSSItem(
        title=x['title'] + "[" + x['price'] + "]",
        link=x['href'],
        description=x['text'],
        guid=x['name'],
        pubDate=x.get('datetime')
    )

rssitems = [f(x) for x in L2]


rss = PyRSS2Gen.RSS2(
    title=conf.get('rss', 'title'),
    link=conf.get('rss', 'web_path'),
    description=conf.get('rss', 'description'),
    lastBuildDate=datetime.datetime.now(),
    items=rssitems
)

rss.write_xml(open(conf.get('rss', 'file_path') + conf.get('rss', 'file_name'), "w"))
