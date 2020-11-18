# Relevant-choice-MAI
### Arxiv parsing module

PDF saving module from arXiv and download it to Google drive:


```
python parsing.py --path path-to-json-file
```


Json format example:

```
{
    {
        "SCOPES": ["https://www.googleapis.com/auth/drive"] (different scopes for GD API),
        "SERVICE_ACCOUNT_FILE" : path-to-GD-service-account-credentials,
        "api_folder_path": id-of-folder-in-GD,
        "data_folder" : path-to-temp-folder,
        "csv_name": csv-name-with-meta-data,
        "url" : [url-to-arXiv-search-promt]
    }

}
```
 All info about GDrive API can found in this guide:See [this guide](http://datalytics.ru/all/rabotaem-s-api-google-drive-s-pomoschyu-python/)


## Receive amount of PDF files in folder:

```
python api.py --path path-to-json-file
```

## Api for arxiv module

```
python get_amount_GD.py --path path-to-json-file
```

####  Json format example:
```
{
    {
        "SCOPES": ["https://www.googleapis.com/auth/drive"] (different scopes for GD API),
        "SERVICE_ACCOUNT_FILE" : path-to-GD-service-account-credentials,
        "api_folder_path": id-of-folder-in-GD,
        "data_folder" : path-to-temp-folder,
        "csv_name": csv-name-with-meta-data,
        "query" : [query-to-arxiv-api<journal, all etc.>]
    }

}
```


## Docker

####  Also you can build image and run container:
```
./runapi.sh [for api module]
./runparser.sh [for parser module]
```

####  To clear your docker space run:
```
./clear.sh
```




