import color_identification

from flask import Flask, request, jsonify
import os
import base64
from PIL import Image
import time
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

print("Uploads Folder Path : " + UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg'])

@app.route('/upload', methods=['POST'])
def post_example():
    if not request.headers.get('Content-type') is None:
        if(request.headers.get('Content-type').split(';')[0] == 'multipart/form-data'):
            if 'image' in request.files.keys():
                print("Request Body: " + str(request.files['image'].filename))
                file = request.files['image']
                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    return jsonify('no image received')
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result = color_identification.get_colors(color_identification.get_image("uploads\\" + filename), 3, True)
                return jsonify(result), 200
            else:
                return jsonify(get_status_code("Invalid body", "Please provide valid format for Image")), 415
        
        elif(request.headers.get('Content-type') == 'application/json'):
            if(request.data == b''):
                return jsonify(get_status_code("Invalid body", "Please provide valid format for Image")), 415
            else:
                body = request.get_json()
                if "image_string" in body.keys():
                    str_image = body['image_string']
                    # str_image = str_image.split(',')[1]
                    imgdata = base64.b64decode(str_image)
                    img = str(int(round(time.time() * 1000))) + "_image.jpg"
                    image_path = os.path.join(UPLOAD_FOLDER, img)
                    with open(image_path, 'wb') as f:
                        f.write(imgdata)

                    # image=Image.open(img)s
                    result = color_identification.get_colors(color_identification.get_image(image_path), 3, True)
                    return jsonify(result), 200
    else:
        return jsonify(get_status_code("Invalid Header", "Please provide valid header")), 401

def get_status_code(argument, message):
    res = {
        "error": {
            "code": argument,
            "message": message
        }
    }
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3004)


