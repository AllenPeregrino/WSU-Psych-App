import requests
import pandas as pd
import os


API_URL = "https://redcap.iths.org/api/"  
API_TOKEN = "13AF818FE951B32E1CDB7F67F2A45062"     


def get_redcap_survey(save_path, completed_only=False):
   
    payload = {
        'token': API_TOKEN,
        'content': 'record',
        'format': 'csv',
        'type': 'flat',
        'rawOrLabel': 'raw'
    }
    

    print("Sending request to REDCap API...")
    response = requests.post(API_URL, data=payload)
    print(f"Response status code: {response.status_code}")

    if response.status_code == 200:
        os.makedirs(save_path, exist_ok=True)
        csv_file_path = os.path.join(save_path, "redcap_data.csv")
        with open(csv_file_path, "wb") as f:
            f.write(response.content)
        print(f"CSV saved to: {csv_file_path}")
        return csv_file_path
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
    
if __name__ == "__main__":
    csv_file = get_redcap_survey(save_path=".", completed_only=False)
    print(f"Saved REDCap CSV at: {csv_file}")

    