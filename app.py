from flask import Flask, render_template, request, redirect, url_for
import random
import csv
import os

app = Flask(__name__)

USED_CODES_FILE = 'used_codes.csv'
VALID_CODES_FILE = 'valid_codes.txt'

def load_valid_codes():
    if not os.path.exists(VALID_CODES_FILE):
        return set()
    with open(VALID_CODES_FILE, 'r') as f:
        return set(line.strip() for line in f.readlines())

def is_code_used(code):
    if not os.path.exists(USED_CODES_FILE):
        return False
    with open(USED_CODES_FILE, 'r') as f:
        return code in (line.strip() for line in f.readlines())

def mark_code_as_used(code):
    with open(USED_CODES_FILE, 'a') as f:
        f.write(code + '\n')

@app.route('/', methods=['GET', 'POST'])
def code_entry():
    error = None
    if request.method == 'POST':
        code = request.form['code'].strip().upper()
        valid_codes = load_valid_codes()
        if code not in valid_codes:
            error = 'このコードは無効です。'
        elif is_code_used(code):
            error = 'このコードは既に使用されています。'
        else:
            mark_code_as_used(code)
            return redirect(url_for('omikuji_result'))
    return render_template('index.html', error=error)

@app.route('/result')
def omikuji_result():
    top = random.randint(1, 6)
    bottom = random.randint(1, 6)
    return render_template('result.html', top=top, bottom=bottom)

if __name__ == '__main__':
    app.run(debug=True)
