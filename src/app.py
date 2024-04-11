import logging
from flask import Flask, request
import requests
from models.plate_reader import PlateReader, InvalidImage
from image_provider_client import ImageProviderClient
import logging
import io
import shutil


app = Flask(__name__)
plate_reader = PlateReader.load_from_file(
    path='./model_weights/plate_reader_model.pth'
)
image_provider_client = ImageProviderClient(
    service_url='http://178.154.220.122:7777/images/'
    )

# <url>:8080/taskwo?img_ids=['9965', '10022']
# <url>:8080/taskwo : body: {"img_ids": [9965, 10022]}
# -> {"plate_codes": {"9965": "о101но750", "10022': "с181мв190"}}
@app.route('/tasktwo', methods=['POST'])
def tasktwo():
    if 'img_ids' not in request.json:
        return {'error': 'field "img_ids" not found'}, 400
    img_ids = request.json['img_ids']
    res = {}
    for img_id in img_ids:
        img_id = str(img_id)
        im = image_provider_client.get_image(img_id)
        if im is None:
            res[img_id] = None
        try:
            plate_code = plate_reader.read_text(im)
        except InvalidImage:
            res[img_id] = None
        res[img_id] = plate_code
    return {'plate_codes': res}, 200
        

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        return {'error': 'invalid image'}, 400

    return {'plate_number': res}, 200

# <url>:8080/taskone?img_id=9965
# <url>:8080/taskone : body: {"img_id": "9965"}
# -> {"plate_number": "о101но750"}
@app.route('/taskone', methods=['POST'])
def taskone():
    if 'img_id' not in request.json:
        return {'error': 'field "img_id" not found'}, 400
    img_id = request.json['img_id']
    im = image_provider_client.get_image(img_id)
    if im is None:
        return {'error': 'cant get image data'}, 404

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        return {'error': 'invalid image'}, 400

    return {'plate_number': res}, 200

@app.route('/')
def hello():
    user = request.args['user']
    return f'<h1 style="color:red;"><center>Hello {user}!</center></h1>'


# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route('/greeting', methods=['POST'])
def greeting():
    if 'user' not in request.json:
        return {'error': 'field "user" not found'}, 400

    user = request.json['user']
    return {
        'result': f'Hello {user}',
    }


# <url>:8080/readPlateNumber : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    im = request.get_data()
    im = io.BytesIO(im)

    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return {'error': 'invalid image'}, 400

    return {'plate_number': res}, 200


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)