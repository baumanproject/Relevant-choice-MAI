
from googleapiclient.http import MediaFileUpload
from os import listdir, stat, remove
from os.path import isfile, join
import arxiv
import re
import requests
from arxiv_api import logging

import time
from urllib.error import HTTPError

def send_to_GDisk_csv(csv_name,path, gd_folder_path, service):
    file_path = path
    file_metadata = {
        'name': csv_name,
        'parents': [gd_folder_path]
    }
    media = MediaFileUpload(file_path, resumable=True, mimetype="text/csv")
    r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()



def send_to_GDisk_pdf(path, gd_folder_path, service):
    pdf_files = [f for f in listdir(path) if isfile(join(path, f))]
    for i in pdf_files:
        name = i
        file_path = path + "/" + name
        #logging(file_path)
        file_metadata = {
            'name': name,
            'parents': [gd_folder_path]
        }
        media = MediaFileUpload(file_path, resumable=True, mimetype="application/pdf")
        r = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        # remove(file_path)
        # print("FIle {} has been successfully send to GD and deleted from local machine".format(i))

def receive_data_by_query(journal,path):

    result = arxiv.query(
        query="jr:\"{}\"".format(journal),
        max_chunk_results=100,
        max_results=1000,
        iterative=True,
        prune=False,
        sort_order="descending"
    )
    #print(journal)
    url_list , memory_list = [],[]
    abstract_list, authors_list, title_list, year_list, pdf_list, journal_list = [], [], [], [], [], []
    for paper in result():
        #https: // export.arxiv.org / pdf / 2006.02728

        url_pdf = paper['pdf_url']
        new_url = "https://export.arxiv.org" + url_pdf[16:]
        #print(url_pdf)
        #time.sleep(4)
        r = requests.get(new_url, stream=True)
        #time.sleep(5)
        return_name = '{}.pdf'.format(re.sub('[\W_]+', '', paper["pdf_url"].split("/pdf")[-1]))
        file_name = path + "/" + return_name
        with open(file_name, 'wb') as f:
            f.write(r.content)
        if stat(file_name).st_size <= 9001:
            remove(file_name)
            time.sleep(5)
            r = requests.get(new_url, stream=True)
            # time.sleep(5)
            logging.warning("File {} was broken :(".format(return_name))
            return_name = '{}.pdf'.format(re.sub('[\W_]+', '', paper["pdf_url"].split("/pdf")[-1]))
            file_name = path + "/" + return_name
            with open(file_name, 'wb') as f:
                f.write(r.content)
            time.sleep(10)

        memory_list.append(stat(file_name).st_size)
        url_list.append(new_url)
        # print('{}.pdf'.format(re.sub('[\W_]+', '', url_pdf.split("/pdf")[-1])))
        pdf_list.append(return_name)
        #print(paper['title'])
        title_list.append(paper['title'])
        abstract_list.append(paper['summary'])
        authors_list.append(paper['authors'])
        journal_list.append(journal)
        year_list.append(paper['published'])



    logging.info("Journal successfully passed {}".format(journal))
    return pdf_list, title_list, abstract_list, authors_list, journal_list, year_list, url_list, memory_list
