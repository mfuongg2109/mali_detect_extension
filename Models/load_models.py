import pandas as pd
from joblib import load
from concurrent.futures import ThreadPoolExecutor

from Environment.path import *
from Extract_features.ExtractFeatures_NamLe import feature_extraction


def load_model(model_path):
    # warning loading XGB
    try:
        model = load(model_path)
        print('success')
        return model
    except Exception as e:
        print(f'Error: {e}')
        return 'Error'


def predict(model, url):
    features = feature_extraction(url)

    feature_names = ['use_of_ip_address', 'abnormal_url', 'google_index', 'count-www', 'count@',
                     'count_dir', 'count_embed_domian', 'short_url', 'count-https',
                     'count-http', 'count%', 'count?', 'count-', 'count=', 'url_length',
                     'hostname_length', 'sus_url', 'fd_length', 'tld_length', 'count-digits',
                     'count-letters']

    features_df = pd.DataFrame([features], columns=feature_names)
    prediction = model.predict(features_df)
    if prediction[0] == 1:
        return 1
    else:
        return 0

def predict_all_model(models, url):
    with ThreadPoolExecutor(max_workers = len(models)) as executor:
        futures = [executor.submit(predict, model, url) for model in models]
        results = [future.result() for future in futures]

        result = sum(results) / len(results)
        if result >= 0.5:
            return True
        else:
            return False

if __name__ == '__main__':
    url = ''

    model_path = [AdaBoost, DecisionTree, KNN, LDA, RandomForest]
    models = [load_model(path) for path in model_path]
    result = predict_all_model(models, url)
    print(result)


