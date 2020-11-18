from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
from arxiv_api import logging
from arxiv_api.functionality import *
import pandas as pd
import shutil
from os import mkdir


def main_app(path):
    with open(path, 'r') as f:
        config_input = json.load(f)
        # "../config/input.json"
    SCOPES = config_input["SCOPES"]
    SERVICE_ACCOUNT_FILE = config_input["SERVICE_ACCOUNT_FILE"]

    api_folder_path = config_input["api_folder_path"]
    data_folder = config_input["data_folder"]
    query = config_input["query"]
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)

    csv_name = config_input["csv_name"]
    csv_path = data_folder + "/" + csv_name + ".csv"
    logging.info(csv_path)

    abstract, author, title, year, pdf, journal_name = [], [], [], [], [], []

    for journal in query:

        logging.info("Journal: {} is running".format(journal))
        mkdir(data_folder)
        pdf_, title_, abstract_, author_, journal_, year_ = receive_data_by_query(journal, data_folder)
        abstract = abstract + abstract_
        author = author + author_
        title = title + title_
        year = year + year_
        pdf = pdf + pdf_
        journal_name = journal_name + journal_
        logging.info("Send received pdf to google disk")
        send_to_GDisk_pdf(data_folder,api_folder_path, service)
        logging.info("Amount: {} of pdf files was deployed on GD".format(len(title_)))
        shutil.rmtree(data_folder)

    df = pd.DataFrame(list(zip(pdf, title, author, journal_name, year, abstract)),
                   columns=['pdf_key', 'title', 'author', 'journal', 'year', 'abstract'])
    mkdir(data_folder)

    df.to_csv(csv_path, index=False, header=True)
    send_to_GDisk_csv(csv_name, csv_path, api_folder_path, service)
    shutil.rmtree(data_folder)
    logging.info("Total amount: {} files".format(df.shape[0]))



