import numpy as np

from PIL import Image
from flask import Flask, jsonify
from urllib import request
from io import BytesIO
from tensorflow import keras
from keras.preprocessing import image
from flask import request as req

import gc
gc.collect()
app = Flask(__name__)

@app.route('/predict/<crop>/<v_id>/<img_name>')
def predict(crop=None, v_id=None, img_name=None):
    gc.collect()
    url = "https://res.cloudinary.com/marcos-yash/image/upload/" + str(v_id) + "/" + str(img_name)
    res = request.urlopen(url).read()
    img = Image.open(BytesIO(res)).resize((64, 64))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = np.vstack([img])
    images = img / 255.0

    crop = str(crop)
    model = None
    result = None
    if crop == "Strawberry":
        model = keras.models.load_model('strawberryNew1.h5')
        classes = model.predict(images, batch_size=10)
        ar = np.array(classes[0]).tolist()
        max_value = max(ar)
        max_index = ar.index(max_value)

        if max_index == 0:
            result = {
                "Status": "Leaf Scorch",
                "Chances": ar[max_index] * 100,
                "Remedy": "Once common leaf spot develops on strawberry plants, the plants cannot be cured. If the disease is detected early, its development may be slowed using fungicides."
            }
            print(result)
        else:
            result = {
                "Status": "Healthy",
                "Chances": ar[max_index] * 100,
                "Remedy": "No Action Needed"
            }
    elif crop == "Cherry":
        model = keras.models.load_model('cherryCropNew.h5')
        classes = model.predict(images, batch_size=10)
        ar = np.array(classes[0]).tolist()
        max_value = max(ar)
        max_index = ar.index(max_value)

        if max_index == 0:
            result = {
                "Status": "Powdery Mildew",
                "Chances": ar[max_index] * 100,
                "Remedy": "Potassium bicarbonate is a contact fungicide which kills the powdery mildew spores quickly."
            }
            print(result)
        else:
            result = {
                "Status": "Healthy",
                "Chances": ar[max_index] * 100,
                "Remedy": "No Action Needed"
            }
    elif crop == "Corn":
        model = keras.models.load_model('maizeNew.h5')
        classes = model.predict(images, batch_size=10)
        ar = np.array(classes[0]).tolist()
        max_value = max(ar)
        max_index = ar.index(max_value)
        if max_index == 0:
            result = {
                "Status": "Gray Leaf Spot",
                "Chances": ar[max_index] * 100,
                "Remedy": "Foliar fungicides can be used to manage gray leaf spot outbreaks."
            }
        elif max_index == 1:
            result = {
                "Status": "Common Rust",
                "Chances": ar[max_index] * 100,
                "Remedy": "Immediately spray with a fungicide"
            }
        elif max_index == 2:
            result = {
                "Status": "Northern Leaf Blight",
                "Chances": ar[max_index] * 100,
                "Remedy": "Fungicide applications reduces Northern Corn Leaf Blight damage and protects yield"
            }
        else:
            result = {
                "Status": "Healthy",
                "Chances": ar[max_index] * 100,
                "Remedy": "No Action Needed"
            }
    gc.collect()
    keras.backend.clear_session()
    return jsonify(result)


@app.route("/")
def hello():
    gc.collect()
    return "Hello , it's Team S.A.Y"


if __name__ == "__main__":
    app.run()