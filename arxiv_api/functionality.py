
from googleapiclient.http import MediaFileUpload
from os import listdir
from os.path import isfile, join
import arxiv
import re

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
        query="journal reference:{}".format(journal),
        max_chunk_results=10,
        max_results=10,
        iterative=True,
        prune=True
    )

    abstract_list, authors_list, title_list, year_list, pdf_list, journal_list = [], [], [], [], [], []
    for paper in result():
        #print(paper)
        url_pdf = paper['pdf_url']
        # print('{}.pdf'.format(re.sub('[\W_]+', '', url_pdf.split("/pdf")[-1])))
        pdf_list.append('{}.pdf'.format(re.sub('[\W_]+', '', url_pdf.split("/pdf")[-1])))
        # print(paper['title'])
        title_list.append(paper['title'])
        abstract_list.append(paper['summary'])
        authors_list.append(paper['authors'])
        journal_list.append(journal)
        year_list.append(paper['published'])
        arxiv.download(obj={"pdf_url": url_pdf}, dirpath=path,
                       slugify=lambda paper: '{}'.format(re.sub('[\W_]+', '', paper["pdf_url"].split("/pdf")[-1])))



    return pdf_list, title_list, abstract_list, authors_list, journal_list, year_list
