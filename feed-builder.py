import sys
import os
from datetime import date
from bs4 import BeautifulSoup

URL_BASE = 'https://enforcie.xyz/'

TEMPLATE_HEADER = f'''<?xml version="1.0" encoding="utf-8" ?>
<feed xmlns="http://www.w3.org/2005/Atom">

<title>Billie Enforcie's Vintage Old-Timey Blog</title>
<author><name>Billie Enforcie</name></author>
<id>{URL_BASE + "blog/"}</id>
<link rel="self" href="{URL_BASE + "blog/atom.xml"}" />
<updated>{date.today().strftime("%Y-%m-%dT%H:%M:%SZ")}</updated>

'''

TEMPLATE_FOOTER = '''</feed>'''

def get_pub_date(filename):
    return os.path.basename(filename)[:10]
    

def atomize(filename):
    article = ''
    path = filename.replace('\\', '/')[filename.find('blog'):]
    if os.path.basename(filename) == 'atom.xml':
        return ''

    pub_date = get_pub_date(filename) + 'T01:01:01Z'
    url = URL_BASE + path

    with open(filename, 'r') as file:
        art_soup = BeautifulSoup(file, 'html.parser').article
        title = art_soup.h2.string
        content = art_soup.div
        del content['id']
        content['xmlns']="http://www.w3.org/1999/xhtml"
        
        article = f'''<entry>
<id>{url}</id>
<title>{title}</title>
<updated>{pub_date}</updated>
<author><name>Billie Enforcie</name></author>
<link rel="alternate" href="{url}" />
<content type="xhtml">
{content.prettify()}
</content>
</entry>

'''

    return article 

def feed_builder(target_dir):
    '''Entry point, builds the feed, baby!'''
    sepr = '/'
    if os.name == 'nt':
        sepr ='\\'

    stream = os.popen('git pull origin')
    output = stream.read();

    if not 'files changed' in output:
        return

    filenames = [(root + sepr + file) for (root, dirs, files) in os.walk(target_dir) for file in files]
    filenames.sort(key=get_pub_date, reverse=True)

    items = [atomize(filename) for filename in filenames]

    feed_string = '' + TEMPLATE_HEADER

    for item in items:
        feed_string += item

    feed_string += TEMPLATE_FOOTER
    return feed_string


if __name__ == '__main__':
    target_dir = os.path.abspath(sys.argv[1])
    if target_dir[-1] != '/':
        if os.name == 'nt':
            target_dir += '\\'
        else:
            target_dir += '/'
    feed_string = feed_builder(target_dir)

    feed_file = open(target_dir + 'atom.xml', 'w')
    feed_file.write(feed_string)
    feed_file.close()

