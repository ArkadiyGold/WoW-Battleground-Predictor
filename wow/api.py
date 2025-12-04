import pandas as pd
from flask import Flask, request, jsonify
import joblib
import xgboost
import os

app = Flask(__name__)

# Загрузка модели и данных
current_dir = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(current_dir, 'model', 'battlegrounds_model.pkl'))
feature_columns = joblib.load(os.path.join(current_dir, 'model', 'model_features.pkl'))
class_efficiency = joblib.load(os.path.join(current_dir, 'model', 'class_efficiency.pkl'))

def prepare_input(data):
    faction = data['Faction']
    char_class = data['Class']
    role = data['Rol']
    be = 1 if data['BE'] == 'Yes' else 0

    # Получаем среднюю эффективность
    avg_eff = class_efficiency.get((faction, char_class), 0.0)

    input_dict = {
        'Faction': [faction],
        'Class': [char_class],
        'Rol': [role],
        'BE': [be],
        'avg_efficiency': [avg_eff]
    }
    df_input = pd.DataFrame(input_dict)
    input_encoded = pd.get_dummies(df_input, columns=['Faction', 'Class', 'Rol'], drop_first=True)

    # Выравниваем колонки
    for col in feature_columns:
        if col not in input_encoded.columns:
            input_encoded[col] = 0
    return input_encoded[feature_columns]

@app.route('/model_info', methods=['GET'])
def model_info():
    return jsonify({
        'model_name': 'RandomForestClassifier',
        'features': feature_columns,
        'accuracy': 0.63,
        'description': 'Предсказывает шанс победы в поле боя на основе фракции, класса, роли и бонусного ивента.'
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        X = prepare_input(data)
        proba = model.predict_proba(X)[0]
        prediction = int(model.predict(X)[0])
        return jsonify({
            'win': prediction,
            'probability': float(proba[1])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=3000, debug=True)