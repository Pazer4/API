from flask import Flask,jsonify, abort, request
import json
from flask import make_response
import sqlite3

app = Flask(__name__)

class batch():
    barcode=None
    batchNumber=None
    theoreticalQty=None
    sortMethod=None

    def printing(self):
        print(f"barcode:{self.barcode}, batchNumber:{self.batchNumber}, "
              f"theoreticalQty:{self.theoreticalQty}, sortMethod:{self.sortMethod}")


@app.route('/tu/announce', methods=['POST'])
def announce():
    data_request = json.loads(request.data)
    global sort_metod_error, message

    data_batch=batch()
    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()


    try:
        data_batch.barcode=data_request["tu"]["barcode"]
    except:
        message = "no barcode"
        abort(400)
        message = None
    if not data_batch.barcode:
        message = "barcode is empty"
        abort(400)
        message = None


    try:
        data_batch.batchNumber=data_request["tu"]["batchNumber"]
    except:
        message = "no batchNumber"
        abort(400)
        message = None
    if not data_batch.batchNumber:
        message = "batchNumber is empty"
        abort(400)
        message = None


    try:
        data_batch.theoreticalQty=data_request["theoreticalQty"]
    except:
        message = "no theoreticalQty"
        abort(400)
        message = None
    if data_batch.theoreticalQty <= 0:
        message = "theoreticalQty less or equal 0"
        abort(400)
        message = None


    try:
        data_batch.sortMethod=data_request["sortMethod"]
    except:
        message = "no sortMethod"
        abort(400)
        message = None
    if data_batch.sortMethod == 0:
        message = "sortMethod equals 0"
        abort(400)
        message = None
    cursor.execute(f'SELECT "shoot" from shoots WHERE '
                   f'"primary ID MC"={data_batch.sortMethod} or "second ID MC"={data_batch.sortMethod}')
    if not cursor.fetchall():
        sort_metod_error=data_batch.sortMethod
        abort(404)
        sort_metod_error=0


    cursor.execute(f"insert into Save values ('"
                   f"{data_batch.barcode}','{data_batch.batchNumber}','{data_batch.theoreticalQty}','{data_batch.sortMethod}')")
    conn.commit()


    cursor.execute(f'select')




    return "",200

@app.route('/tu/remove', methods=['POST'])
def remove():
    global message
    data_request = json.loads(request.data)

    data_batch=batch()

    try:
        data_batch.barcode = data_request["tu"]["barcode"]
    except:
        message = "no barcode"
        abort(400)
        message = None

    try:
        data_batch.batchNumber = data_request["tu"]["batchNumber"]
        message_batchNumber = f" AND batchNumber='{data_batch.batchNumber}'"
    except:
        message_batchNumber=""

    conn = sqlite3.connect('DB.db')
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM Save where barcode='{data_batch.barcode}'+{message_batchNumber}")
    conn.commit()

    return "",200

@app.route('/batch/finished', methods=['POST'])
def finished():
    data_request = json.loads(request.data)

    data_batch=batch()

    try:
        data_batch.batchNumber = data_request["tu"]["batchNumber"]
    except:
        message = "no barcode"
        abort(400)
        message = None
    if not data_batch.batchNumber:
        message = "batchNumber is empty"
        abort(400)
        message = None

@app.errorhandler(400)
def bad_data(error):
    global message
    return make_response(jsonify({
                                    "message": "Invalid data",
                                    "errors":
                                    [{
                                        "path": "/tu/barcode",
                                        "message": message,
                                        "additionalProp1": {}
                                     }],
                                    "additionalProp1": {}
                                }), 400)

@app.errorhandler(404)
def not_found(error):
    global sort_metod_error
    return make_response(jsonify({'message': f'There is no chanel with sorting method {sort_metod_error}'}), 404)

@app.errorhandler(408)
def Request_timeout(error):
    return make_response(jsonify({'message': 'Operation aborted maximum request time of 30 seconds exceeded'}), 408)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'message': 'Invalid data'}), 500)

if __name__ == '__main__':
    app.run(debug=True)