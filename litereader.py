#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup
import os
import shutil
import sys
from urllib import parse

def get_file(url, path, filename, headers):
    if not os.path.exists(path):
        os.mkdir(path)
    urlsplit = parse.urlsplit(url)
    urlparts = ('https', 'www.literotica.com', urlsplit.path, '', '')
    url = parse.urlunsplit(urlparts)
    print (url)
    if not filename:
        filename = url.split("/")[-1]

    # Open the url image, set stream to True, this will return the stream content.
    try:
        r = requests.get(url, headers=headers, stream = True)
    except:
        return False

    # Check if the image was retrieved successfully
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True
    
        # Open a local file with wb ( write binary ) permission.
        with open(path + '/' + filename,'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image sucessfully Downloaded: ',filename)
        return True
    else:
        print('Image Couldn\'t be retreived')

if len(sys.argv) != 2:
    print ('Usage: ' + sys.argv[0] + ' url')
    exit()

scriptdir = os.path.dirname(sys.argv[0])
url = sys.argv[1]
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:77.0) Gecko/20100101 Firefox/77.0'}
page = 1
story_content = ''
story_filename = url.split('/')[-1]
print (story_filename)

while url:
    print ('Page', page)
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'html.parser')
    if page == 1:
        #story_header = soup.find('div', class_='b-story-header')
        #print (story_header.text)
        story_title = soup.title
        story_keywords = soup.find('meta', attrs={'name':'keywords'})
        story_description = soup.find('meta', attrs={'name':'description'})
    story_body = soup.find('div', class_='aa_ht')
    for tag in story_body.find_all('img'):
        img_filename = tag['src'].split('/')[-1]
        get_file(tag['src'], story_filename, img_filename, headers)
        tag['src'] = story_filename + '/' + img_filename
    story_content += str(story_body)
    next = soup.find('a', title='Next Page')
    if next:
        url = 'https://www.literotica.com' + next['href']
        page += 1
    else:
        url = None

if story_content:
    template_file = open(scriptdir + '/litereader.template.html', mode='r')
    template = template_file.read()
    template_file.close()

    template = template.replace('@TITLE', story_title.text)
    template = template.replace('@KEYWORDS', story_keywords['content'])
    template = template.replace('@DESCRIPTION', story_description['content'])
    template = template.replace('@URL', sys.argv[1])
    template = template.replace('@BODY', story_content)

    out_file = open(story_filename + '.html', 'w')
    out_file.write(template)
    out_file.close()

