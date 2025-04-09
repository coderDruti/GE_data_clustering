from flask import Flask, jsonify,request, render_template, redirect
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaFileUpload
import io
from googleapiclient.errors import HttpError
import clustering

app = Flask(__name__)

preprocessed_data = None
samples = None
file_content = None
file_ID = ""

@app.route('/')
def index():
    return render_template('index.html')
@app.route("/inputClusteringMethod", methods=["POST"])
def receive_data():
    # receive_data_samples = request.form["samples"].splitlines()
    received_data_ge = request.form["data"]
    # received_data = received_data.decode("utf-8").split("\"")

    scope = ['https://www.googleapis.com/auth/drive']
    service_account_json_key = '../hardy-gearing-454710-u0-98817d39df51.json'
    credentials = service_account.Credentials.from_service_account_file(
                              filename=service_account_json_key, 
                              scopes=scope)
    service = build('drive', 'v3', credentials=credentials)

    def download_text_file(file_id, service):
        try:
            request = service.files().get_media(fileId=file_id)
            file_stream = io.BytesIO()
            downloader = MediaIoBaseDownload(file_stream, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

            # Reset the stream and decode as UTF-8 text
            file_stream.seek(0)
            file_content = file_stream.read().decode("utf-8")
            
            # Save locally or process the content
            # with open(file_name, 'w', encoding='utf-8') as f:
            #     f.write(file_content)
            
            # print(f"File '{file_name}' downloaded and saved successfully!")
            return file_content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    global preprocessed_data, samples, file_content, file_ID
    # samples = receive_data_samples 
    preprocessed_data = received_data_ge
    print(preprocessed_data)
    # file_ID = items[0]["id"] if received_data_ge =="GSE108474" else ""
    
    # # print(file_path)

    query = "mimeType='text/plain' or name contains '.CEL'"
    results = service.files().list(q = query, pageSize = 10, fields="files(id, name, mimeType)").execute()
    items = results.get("files", [])
    print(items)
    if received_data_ge == "GSM1214834":
        file_ID = items[0]["id"]
    elif received_data_ge == "GSM317711":
        file_ID = items[1]["id"]
    elif received_data_ge == "GSE108474":
        file_ID = items[2]["id"]

    file = []
    if not items:
        print('No files found.')
    else:
        # print('Files:')
        file_id  = file_ID
        # file_name = items['name']
        # if file_name.endswith('.txt') or '.CEL' in file_name:
        file_content = download_text_file(file_id, service)
        # print(f"{item['name']} ({item['id']})")
        # file.append(service.files().get(fileId = file_ID, fields = "webViewLink").execute())

    # print(file)

    # req = service.files().get_media(fileId = file_ID)
    # file_stream = io.BytesIO()
    # downloader = MediaIoBaseDownload(file_stream, req)
    # done = False
    # while not done:
    #     status, done = downloader.next_chunk()

    # Reset the stream position
    # file_stream.seek(0)
    # file_content = file_stream.read().decode("utf-8")
    return render_template("inputClusteringMethod.html")

# @app.route("/inputClusteringMethod")
# def chooseClustering():
#     return render_template("inputClusteringMethod.html")

@app.route("/output", methods=["POST"])
def cluster():
    method = request.form["method"]
    result = {}
    clusters_kmeans, s_score_kmeans = [], None
    clusters_agc, s_score_agc = [], None
    if method == "K-means clustering":
        clusters_kmeans, s_score_kmeans= clustering.main(file_content, "K-means clustering") 
        return render_template("output.html", result={
            'clusters':clusters_kmeans,
            's_score':s_score_kmeans
        })
    # data0 = " ".join([str(data) for data in data0])
    # data1 = " ".join([str(data) for data in data1])
    elif method == "Agglomerative clustering":
        clusters_agc,s_score_agc= clustering.main(file_content, "Agglomerative clustering")
        return render_template("output.html", result={
            'clusters':clusters_agc,
            's_score':s_score_agc
        })
    

if __name__ == '__main__':
    app.run(debug=True)
