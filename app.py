from flask import Flask, jsonify,request, render_template, redirect
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseDownload
# from googleapiclient.http import MediaFileUpload
# import io
# from googleapiclient.errors import HttpError
import clustering

# scope = ['https://www.googleapis.com/auth/drive']
# service_account_json_key = '../hardy-gearing-454710-u0-98817d39df51.json'
# credentials = service_account.Credentials.from_service_account_file(
#                               filename=service_account_json_key, 
#                               scopes=scope)
# service = build('drive', 'v3', credentials=credentials)

# results = service.files().list(pageSize = 10).execute()
# items = results.get("files", [])
# file = []
# if not items:
#     print('No files found.')
# else:
#     print('Files:')
#     for item in items:
#         print(f"{item['name']} ({item['id']})")
#         file.append(service.files().get(fileId = item["id"], fields = "webViewLink").execute())

# print(file[0]["webViewLink"], items[0]["id"])

app = Flask(__name__)

preprocessed_data = None
genes = None

@app.route('/')
def index():
    return render_template('index.html')
@app.route("/inputClusteringMethod", methods=["POST"])
def receive_data():
    receive_data_genes = request.form["genes"].splitlines()
    received_data_ge = request.form["data"].splitlines()
    # received_data = received_data.decode("utf-8").split("\"")
    global preprocessed_data, genes
    genes = receive_data_genes 
    preprocessed_data = received_data_ge
    print(preprocessed_data, genes)
    # file_ID = items[0]["id"] if received_data[3] =="GSE108474" else ""
    # # print(file_path)
    # req = service.files().get_media(fileId = file_ID)
    # file_stream = io.BytesIO()
    # downloader = MediaIoBaseDownload(file_stream, req)
    # done = False
    # while not done:
    #     status, done = downloader.next_chunk()

    # # Reset the stream position
    # file_stream.seek(0)
    # # file_content = file_stream.read().decode("utf-8")
    return redirect("inputClusteringMethod")

@app.route("/inputClusteringMethod")
def chooseClustering():
    return render_template("inputClusteringMethod.html")

@app.route("/output", methods=["POST"])
def cluster():
    method = request.form["method"]
    clusters_kmeans, s_score_kmeans,clusters_agc,s_score_agc= clustering.main(preprocessed_data, genes) 
    if method == "K-means clustering":
        result ={
            "clusters_kmeans":clusters_kmeans,
            "s_score_kmeans":s_score_kmeans
        }
    # data0 = " ".join([str(data) for data in data0])
    # data1 = " ".join([str(data) for data in data1])
    elif method == "Agglomerative clustering":
        result ={
            "clusters_agc":clusters_agc,
            "s_score_agc":s_score_agc
        }
    return render_template("output.html", result=result)

if __name__ == '__main__':
    app.run(debug=True)
