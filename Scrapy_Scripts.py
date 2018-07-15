from bs4 import BeautifulSoup as bs44
from bs4 import BeautifulSoup as bs
import urllib2
import os


# for the coding of scrapy and beautifulsoup, some codes from Github are taken as references

savePath = '.\Texts_Test'


# Download all scripts from www.imsdb.com, with beautifulsoup
def get_scripts():

    script_list = urllib2.urlopen('http://www.imsdb.com/all%20scripts/')
    bsoup = bs(script_list, 'html.parser')
    count = 0

    failedfiles = []

    for link in bsoup.findAll('a'):
        url = link.get('href')
        if url.startswith('/Movie Scripts/'):

            name = (url.split('/')[2])[:-11].strip()  # get the movie name
            name = name.replace(':', '')              # remove invalid characters which will further be just '-'
            name = name.replace('?', '')

            file_name = name  # storage name

            name = '-'.join([n.strip() for n in name.split(' ')]) # script html name
            #print name
            try:
                html = urllib2.urlopen('http://www.imsdb.com/scripts/' + name + '.html').read()
                bsp = bs44(html, "html.parser")
                text = bsp.get_text()

                # get lines and change the symbol not in ASCII to space
                lines = [''.join([i if ord(i) < 128 else ' ' for i in line]) for line in text.splitlines()]

                filtered = []
                started = False

                for line in lines:
                    if line.upper().strip() == 'ALL SCRIPTS':
                        started = True
                    elif line.startswith('Writers : '):
                        started = False
                    if started == True:
                        filtered.append(line)

                script = '\n'.join(filtered) # write all lines into a file
                #print file_name
                with open(os.path.join(savePath, file_name + '.txt'), 'a') as f:
                    f.write(script)
            except urllib2.HTTPError:    # this error happens when the script is of pdf format
                count = count + 1
                failedfiles.append(file_name)
    print failedfiles

get_scripts()