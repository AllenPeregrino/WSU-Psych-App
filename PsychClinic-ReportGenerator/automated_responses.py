# Helpful credit to https://community.alteryx.com/t5/Alteryx-Designer-Discussions/Python-Tool-Downloading-Qualtrics-Survey-Data-using-Python-API/td-p/304898 and https://www.youtube.com/@FedericoTartarini

import requests
import zipfile
import io
import os

# uses the survey id to save our survey results automatically
def get_survey(save_survey, survey_id):
    api_token = "4DGKlfv4CPqlSfXQGODa1Yv4lr5V3wZdW19vie7A"
    file_format = "csv"
    data_center = "wsu.iad1"

    request_check_progress = 0
    progress_status = "in progress"
    base_url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
    headers = {
        "content-type": "application/json",
        "x-api-token": api_token,
    }

    download_request_url = base_url
    download_request_payload = '{"format":"' + file_format + '","surveyId":"' + survey_id + '"}'
    download_request_response = requests.request("POST", download_request_url, data=download_request_payload, headers=headers)
    progress_id = download_request_response.json()["result"]["id"]
    # print(download_request_response.text)

    while request_check_progress < 100 and progress_status != "complete":
        request_check_url = base_url + progress_id
        request_check_response = requests.request("GET", request_check_url, headers=headers)
        request_check_progress = request_check_response.json()["result"]["percentComplete"]

    # Step 3: Downloading file
    request_download_url = base_url + progress_id + '/file'
    request_download = requests.request("GET", request_download_url, headers=headers, stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(save_survey)
    print('Downloaded qualtrics survey')

    #
    #new get survey
    api_token = "f5g7StxqprMyQoaQI12XFkqLcIuyEqg4IFRdzlNY"
    file_format = "csv"
    data_center = "wsu.iad1"

    request_check_progress = 0
    progress_status = "in progress"
    base_url = "https://{0}.qualtrics.com/API/v3/responseexports/".format(data_center)
    headers = {
        "content-type": "application/json",
        "x-api-token": api_token,
    }

    download_request_url = base_url
    download_request_payload = '{"format":"' + file_format + '","surveyId":"' + survey_id + '"}'
    download_request_response = requests.request("POST", download_request_url, data=download_request_payload, headers=headers)
    progress_id = download_request_response.json()["result"]["id"]
    # print(download_request_response.text)

    while request_check_progress < 100 and progress_status != "complete":
        request_check_url = base_url + progress_id
        request_check_response = requests.request("GET", request_check_url, headers=headers)
        request_check_progress = request_check_response.json()["result"]["percentComplete"]

    # Step 3: Downloading file
    request_download_url = base_url + progress_id + '/file'
    request_download = requests.request("GET", request_download_url, headers=headers, stream=True)

    # Step 4: Unzipping the file
    zipfile.ZipFile(io.BytesIO(request_download.content)).extractall(save_survey)
    print('Downloaded qualtrics survey')

#path = ""
#get_survey(save_survey = path, survey_id = 'SV_3wvBtxhaQcsl06G')