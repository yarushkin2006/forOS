import configparser
import sys
import argparse
from flask import Flask, jsonify, request
import json

# Дорогой студент, сдающий это задание, надеюсь тебе понравится игровая форма данной практической части
# Приложение запускается стадартным способом то есть python /путь/к/скрипту
# Но для корректной работы надо указать ещё в качестве агрументов путь к конфигурационному файлу
# Задание несложное, читай комментарии в коде, анализируй, перечитывай задания
# Ты справишься, удачи

strinfo = None
secret_code = "- --- .--. ... . -.-. .-. . - -.-. --- -.. ."
app = Flask(__name__)
apperror = Flask(__name__)
name = None

# Маршрут для получение секретного кода
@apperror.route("/secret", methods=["GET"])
def sh123s():
    try:
        ans = {}
        ans["secret_code"] = decode_from_morse(secret_code)
        return ans
    except Exception as e:
        return jsonify(message=f"NOT OK {e}"), 400

# Маршрут для получения результата экзамена
@app.route("/123", methods=["GET"])
def sh123():
    try:
        ans = {}
        # Результат данной части экзамена
        if strinfo == "- --- .--. ... . -.-. .-. . - -.-. --- -.. .- --- .--. ... . -.-. .-. . - -.-. --- -.. .":
            ans["name"] = name
            ans["comm"] = "молодец, вы настоящий шпион"
        else:
            ans["name"] = name
            ans["comm"] = "плохой шпион"
        return ans
    except Exception as e:
        return jsonify(message=f"NOT OK {e}"), 400

# Маршрут для установки имени студента, укажите как параметр на английском имя и фамилию через пробел
@app.route("/321/<names>", methods=["GET"])
def sh321(names):
    try:
        global strinfo
        global name
        name = names
        # Снять комментарий после того, как узнали секретный пароль
        #strinfo = "- --- .--. ... . -.-. .-. . - -.-. --- -.. .- --- .--. ... . -.-. .-. . - -.-. --- -.. ."
        return jsonify(message="OK"), 200
    except Exception as e:
        return jsonify(message=f"NOT OK {e}"), 400

# Путь к конфигурационному файлу
file_path = sys.argv[1]
secret = ".---- ..--- ...--"

MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.',
    'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..',
    'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-',
    'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.'
}
def encode_to_morse(text):
    return ' '.join(MORSE_CODE.get(char.upper(), '') for char in text if char.upper() in MORSE_CODE or char == ' ')
def decode_from_morse(morse_code):
    reversed_dict = {v: k for k, v in MORSE_CODE.items()}
    return ''.join(reversed_dict.get(code, '') for code in morse_code.split())

try:
    with open(file_path, 'r') as f:
        dt = json.load(f)
        f.close()
    password = dt['INFO']['password']
    try:
        with open(file_path, 'r') as f:
            dt = json.load(f)
            f.close()
        password = dt['CODE']['secret']
        if encode_to_morse(password) == secret_code:
            print("Вы запустили основной сервер")
            # Чтобы сервер работал извне добавьте перед портом первый параметр host="0.0.0.0" который сделает сервер доступным из интернета
            app.run(port=20000, debug=True)
        else:
            print("Пароль неверный")
    except:
        print("Вы запустили сервер для получения секретного кода")
        # Чтобы сервер работал извне добавьте перед портом первый параметр host="0.0.0.0" который сделает сервер доступным из интернета
        apperror.run(port=20001, debug=True)
except:
    # Видимо конфигурационный файл не указан или же нет INFO с password
    print("Что-то не так с конфигурационным файлом")
