import argparse
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_amount(path):
    with open(path, 'r') as f:
        config_input = json.load(f)
        # "../config/input.json"
    SCOPES = config_input["SCOPES"]
    SERVICE_ACCOUNT_FILE = config_input["SERVICE_ACCOUNT_FILE"]

    api_folder_path = config_input["api_folder_path"]
    # data_folder = config_input["data_folder"]
    # url = config_input["url"]
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('drive', 'v3', credentials=credentials)
    api_folder_path = config_input["api_folder_path"]

    amount = 0
    page_token = None
    while True:
        response = service.files().list(q="'{}' in parents and name contains 'pdf'".format(api_folder_path),
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
        amount += len(response.get('files', []))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

    print("Amount of pdf files in folder: {}".format(amount))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF GD get amount of pdf in folder')
    parser.add_argument('--path', help='path to config file')
    args = parser.parse_args()
    get_amount(args.path)
