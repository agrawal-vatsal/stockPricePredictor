import joblib
import numpy as np
import requests
from django.contrib.staticfiles.storage import staticfiles_storage
from keras.models import model_from_yaml

url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&apikey=UDJE8XNW0DMMYVVC&symbol="

names = {
    'GOOGL': 'google',
    'MSFT': 'microsoft',
    'AAPL': 'apple'
}


def get_price_list(name):
    furl = url + name
    data = requests.get(furl)
    data = data.json()
    data = data['Time Series (Daily)']
    final_data = []
    for value in data.values():
        final_data.append(value['4. close'])
        if len(final_data) == 60:
            final_data = final_data[::-1]
            return final_data
    return final_data


def get_ndarray(array):
    array = np.array(array)
    array = array.reshape(1, 60, 1)
    return array


def scaled_list(name):
    path = staticfiles_storage.path(names[name] + "_scaler.save")
    scaler = joblib.load(path)
    array = get_price_list(name)
    array = np.array(array)
    array = scaler.transform(array.reshape(-1, 1))
    return get_ndarray(array)


def unscale(name, array):
    path = staticfiles_storage.path(names[name] + "_scaler.save")
    scaler = joblib.load(path)
    array = array.reshape(-1, 1)
    array = scaler.inverse_transform(array)
    return array


def get_stock_price(name):
    path = staticfiles_storage.path(names[name] + ".yaml")
    yaml_file = open(path, 'r')
    loaded_model_yaml = yaml_file.read()
    yaml_file.close()
    model = model_from_yaml(loaded_model_yaml)
    path = staticfiles_storage.path(names[name] + ".h5")
    model.load_weights(path)
    return unscale(name, model.predict(scaled_list(name)))
