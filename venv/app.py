from flask import Flask,jsonify, abort, request
import json
from flask import make_response

app = Flask(__name__)

class batch():
    barcode=-99
    batchNumber=-99
    theoreticalQty=-99
    sortMethod=-99

    def printing(self):
        print(f"barcode:{self.barcode}, batchNumber:{self.batchNumber}, theoreticalQty:{self.theoreticalQty}, sortMethod:{self.sortMethod}")


@app.route('/tu/announce', methods=['POST'])
def announce():
    data_request = json.loads(request.data)
    global sort_metod

    data_batch=batch()
    data_batch.barcode=data_request["tu"]["barcode"]
    data_batch.batchNumber=data_request["tu"]["batchNumber"]

    data_batch.theoreticalQty=data_request["theoreticalQty"]
    data_batch.sortMethod=data_request["sortMethod"]

    sort_metod = 30
    abort(404)

    return "",201
@app.route('/batch/finished', methods=['POST'])
def finished():
    data_request = json.loads(request.data)


@app.errorhandler(400)
def bad_data(error):
    return make_response(jsonify({
                                    "message": "Invalid data",
                                    "errors":
                                    [{
                                        "path": "/tu/barcode",
                                        "message": "expected a minimum length of 1",
                                        "additionalProp1": {}
                                     }],
                                    "additionalProp1": {}
                                }), 400)

@app.errorhandler(404)
def not_found(error):
    global sort_metod
    return make_response(jsonify({'message': f'There is no chanel with sorting method {sort_metod}'}), 404)

@app.errorhandler(408)
def Request_timeout(error):
    return make_response(jsonify({'message': 'Operation aborted maximum request time of 30 seconds exceeded'}), 408)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'message': 'Invalid data'}), 500)

if __name__ == '__main__':
    app.run(debug=True)