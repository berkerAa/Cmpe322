from flask import Flask, request, Response
import jsonpickle
import json
import numpy as np
import sys, os
#sys.path.append('/home/berker/github-remote/TIRPORT/ocr-document')
# Initialize the Flask application
app = Flask(__name__)
# route http posts to this method
@app.route('/', methods=['POST'])
def test():
    r = request.get_json(silent=True)
    # convert string of image data to uint8,
    print(r)
    print(request)
    #nparr = np.fromstring(r.data.decode(encoding='UTF-8',errors='strict'), np.uint8)
    authToken = r['auth']
    with open('Cert/Database.pem', 'r') as f:
        key = ''.join([i[:-1] for i in f.readlines()])
    if key == authToken:
        if r['request'] == 'get':
            # decode image
            try:
                with open('Database/loginCreds.json') as f:
                    response = json.load(f)

            # encode response using jsonpickle
                response_pickled = json.dumps(response, ensure_ascii=False).encode('utf-8')

                return Response(response=response_pickled, status=200, mimetype="application/json")
            except Exception as e:
                print(e)

            # do some fancy processing here....

            # build a response dict to send back to client
            
        else:
            with open('Database/loginCreds.json', 'w') as f:
                json.dump(r['info'], f)
                print(r['info'])
                response_pickled = json.dumps({'status': 'Succces'}, ensure_ascii=False).encode('utf-8')
                return Response(response=response_pickled, status=200, mimetype="application/json")
    else:
        response_pickled = json.dumps({'status': 'Auth key Error'}, ensure_ascii=False).encode('utf-8')
        return Response(response=response_pickled, status=400, mimetype="application/json")


# start flask app
app.run(host="192.168.1.102", port=15001)