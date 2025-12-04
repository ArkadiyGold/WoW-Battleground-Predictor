# app.py
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

API_URL = 'http://localhost:3000/predict'

@app.route('/')
def index():
    factions = ['Horde', 'Alliance']
    classes = ['Warrior', 'Hunter', 'Rogue', 'Shaman', 'Warlock', 'Paladin', 'Priest', 'Druid', 'Mage', 'Death Knight', 'Monk', 'Demon Hunter']
    return render_template('index.html', factions=factions, classes=classes)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        user_data = request.get_json()

        # Передаём данные в ML API
        response = requests.post(API_URL, json=user_data)
        result = response.json()

        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        # Генерация рекомендаций (только текст, без модели)
        message = "✅ Высокий шанс победы!" if result['win'] == 1 else "⚠️ Шанс победы низкий."
        probability = result['probability']

        # Простые рекомендации
        recs = []
        if user_data['BE'] == 'Yes':
            recs.append("✨ Бонусный ивент активен — это повышает шанс победы!")
        if user_data['Rol'] == 'heal':
            recs.append("💡 Идеальный отряд: 2–3 хилера + 5–6 DPS.")
        else:
            recs.append("💡 Убедитесь, что в отряде есть хотя бы 1 хилер.")

        return jsonify({
            'message': message,
            'probability': probability,
            'recommendations': recs
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000, debug=True)