from googleapiclient.http import MediaFileUpload
from bs4 import BeautifulSoup
import requests
from os import listdir, mkdir
import shutil
import re
from os.path import isfile, join
import urllib.parse as urlparse
from urllib.parse import parse_qs

def get_title(soup):
    arr = []
    for i in soup.find_all('p', {"class": "title is-5 mathjax"}):
        arr.append(i.get_text().strip())
    return arr


def get_author(soup):
    arr = []
    for i in soup.find_all('p', {"class": "authors"}):
        temp = []
        for j in i.find_all('a'):
            temp.append(j.get_text())
        arr.append(temp)
    return arr


def get_abstract(soup):
    arr = []
    for i in soup.find_all('span', {"class": "abstract-short has-text-grey-dark mathjax"}):
        arr.append(i.get_text().strip()[:-15])
    return arr


def get_year(soup):
    arr = []
    for i in soup.find_all('li', {"class": "arxiv-result"}):
        j = i.find('p', {"class": "is-size-7"})
        intro = j.get_text()
        res = intro[:intro.find(';')]
        arr.append(res[10:])
    return arr


def get_pdf(soup, path):
    journal_list = []
    name_list = []
    for link in soup.find_all('a'):
        token = link.get('href')
        if token is not None:
            if token.find("https://arxiv.org/pdf/") != -1:
                r = requests.get(token, stream=True)
                return_name = '{}.pdf'.format(re.sub('[\W_]+', '', token[23:]))
                file_name = path +"/"+ return_name
                with open(file_name, 'wb') as f:
                    f.write(r.content)
                name_list.append(return_name)
    return name_list


def get_all(soup, path):
    return get_abstract(soup), get_author(soup), get_title(soup), get_year(soup), get_pdf(soup, path)


def data_loader(url, path):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    abstract, author, title, year, pdf = get_all(soup, path)
    return abstract, author, title, year, pdf, [parse_qs(urlparse.urlparse(url).query)['query'][0] for i in range(len(pdf))]


def send_to_GDisk_pdf(path, gd_folder_path, service):
    pdf_files = [f for f in listdir(path) if isfile(join(path, f))]
    for i in pdf_files:
        name = i
        file_path = path + "/" + name
        print(file_path)
        file_metadata = {
            'name': name,
            'parents': [gd_folder_path]
        }
        media = MediaFileUpload(file_path, resumable=True, mimetype="application/pdf")
        r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        # remove(file_path)
        # print("FIle {} has been successfully send to GD and deleted from local machine".format(i))


def send_to_GDisk_csv(csv_name,path, gd_folder_path, service):
    file_path = path
    file_metadata = {
        'name': csv_name,
        'parents': [gd_folder_path]
    }
    media = MediaFileUpload(file_path, resumable=True, mimetype="text/csv")
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return r


def PDF_Loader_GD(data_folder, url, service, api_folder_path):
    mkdir(data_folder)
    abstract, author, title, year, pdf, journal = data_loader(url, data_folder)
    send_to_GDisk_pdf(data_folder, api_folder_path, service)
    shutil.rmtree(data_folder)
    return abstract, author, title, year, pdf, journal

