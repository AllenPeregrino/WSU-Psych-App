import requests
import os

API_URL = "https://redcap.iths.org/api/"  
API_TOKEN = "13AF818FE951B32E1CDB7F67F2A45062"     

def get_redcap_survey(save_path, record_id=None):
    """
    Downloads REDCap survey CSV.
    If record_id is provided, downloads only that record.
    """
    payload = {
        'token': API_TOKEN,
        'content': 'record',
        'format': 'csv',
        'type': 'flat',
        'rawOrLabel': 'raw'
    }

    # Filter by record if provided
    if record_id:
        payload['records'] = [record_id]

    print(f"Sending request to REDCap API for record: {record_id}")
    response = requests.post(API_URL, data=payload)
    print(f"Response status code: {response.status_code}")

    if response.status_code == 200:
        os.makedirs(save_path, exist_ok=True)
        csv_file_name = f"redcap_data_{record_id}.csv" if record_id else "redcap_data.csv"
        csv_file_path = os.path.join(save_path, csv_file_name)

        with open(csv_file_path, "wb") as f:
            f.write(response.content)

        print(f"CSV saved to: {csv_file_path}")
        return csv_file_path
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None


if __name__ == "__main__":
    # Example usage: download a single record
    csv_file = get_redcap_survey(save_path=".", record_id="123")
    print(f"Saved REDCap CSV at: {csv_file}")
