# WoW-Level-Predictor

Предсказание достиг ли персонаж в World of Warcraft максимального уровня (70) на основе расы, класса, зоны и наличия гильдии.

## Задача
Бинарная классификация:
- **Класс 1**: персонаж на уровне 70
- **Класс 0**: персонаж ниже 70 уровня

## Структура проекта
- `data/` — данные
- `models/` — обученная модель
- `notebooks/` — код обучения модели (Google Colab)
- `templates/index.html` — веб-интерфейс
- `installers.txt` — установщик библиотек
- `wowlvlapp.py` — Flask API

 ## Запуск
 
Копирование, установка и запуск:
 ```bash
 git clone https://github.com/ArkadiyGold/wow-level-predictor.git
 cd wow-level-predictor
 pip install -r installers.txt
 python wowlvlapp.py
 ```

Адрес сайта:
http://127.0.0.1:5000

Данные:
Основной источник датасета: https://www.kaggle.com/datasets/mylesoneill/warcraft-avatar-history?spm=a2ty_o01.29997173.0.0.6d355171LG4RNp
Информация о персонажах: wowah_data.csv
Справочник зон: zones.csv

Модель:
Алгоритм: RandomForestClassifier
Точность: 0.859825
Признаки: раса, класс, тип зоны, контролирующая фракция, рекомендуемый уровень зоны, наличие гильдии
