from flask import Flask,request,jsonify
import requests
import xmltodict
app = Flask(__name__)


@app.route('/receiveRequests', methods=['POST'])
def receiveRequests():
    try:
       
        xmlData = {}
        jsonData = {}
        queryData = request.args.to_dict()
        # print(request.data)

        if request.content_type in ['application/xml', 'text/xml']:
            try:

                xml_data = request.data
                xmlData = xmltodict.parse(xml_data)
                # print(xmlData)
                
            except Exception as e:
                return jsonify({'error': 'Failed to parse XML', 'details': str(e)}), 400
        if not xmlData:
            jsonData = request.get_json() or {}

       
        receivedData = { **jsonData,**queryData, **xmlData}

        # print(receivedData)

        headers = {"Content-Type": "application/json"}
        targetEndpoint = "http://127.0.0.1:8000/acceptData"
        
        response = requests.post(targetEndpoint, json=receivedData, headers=headers)
        
        if response.status_code == 200:
            return response.json(), 200
        else:
            return jsonify({'error': 'Failed to forward data', 'details': response.text}), response.status_code

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/acceptData',methods =['POST'])
def acceptData():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No JSON data found'}), 400

    return jsonify({'message':"data recieved", "data":data}), 200



if __name__ == "__main__":
    app.run(debug=True,port=8000)