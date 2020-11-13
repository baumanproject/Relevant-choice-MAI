from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import json

from pdf_reader_module.pdf_functionality import *


def main_app(path="../config/input.json"):
    with open(path, 'r') as f:
        config_input = json.load(f)
    # "../config/input.json"
    SCOPES = config_input["SCOPES"]
    SERVICE_ACCOUNT_FILE = config_input["SERVICE_ACCOUNT_FILE"]

    api_folder_path = config_input["api_folder_path"]
    data_folder = config_input["data_folder"]
    url = config_input["url"]
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    csv_name = config_input["csv_name"]
    csv_path = data_folder + "/" + csv_name + ".csv"
    print(csv_path)

    abstract, author, title, year, pdf, journal = [], [], [], [], [], []

    for link in url:
        print("New url < <  {0}  > > in run".format(link))
        abstract_, author_, title_, year_, pdf_, journal_ = PDF_Loader_GD(data_folder, link, service, api_folder_path)
        print("Amount: {} of pdf files was deployed on GD".format(len(title_)))
        abstract = abstract + abstract_
        author = author + author_
        title = title + title_
        year = year + year_
        pdf = pdf + pdf_
        journal = journal + journal_

    df = pd.DataFrame(list(zip(pdf, title, author, journal, year, abstract)),
                      columns=['pdf_key', 'title', 'author', 'journal', 'year', 'abstract'])
    mkdir(data_folder)
    df.to_csv(csv_path, index=False, header=True)
    send_to_GDisk_csv(csv_name,csv_path, api_folder_path, service)
    shutil.rmtree(data_folder)
    print("Total amount: {} files".format(df.shape[0]))
