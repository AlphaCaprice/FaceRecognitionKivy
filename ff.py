from keras.preprocessing import image
from keras.applications.vgg16 import  preprocess_input, decode_predictions
import numpy as np
from keras.models import model_from_json

def select_sex(self, nameFile):
    json_file = open("m_model", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("m_model.h5")
    loaded_model.compile(loss="categorical_crossentropy",optimizer="SGD", metrics=["accuracy"])
    img = image.load_img(nameFile, target_size=(32, 32))
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis=0)
    x = preprocess_input(x)
    preds = loaded_model.predict(x)
    if preds[0][1] == 1:
        return 1
        # print "female"
    elif preds[0][0] == 1:
        return 0
        # print "male"
    # print(preds)
