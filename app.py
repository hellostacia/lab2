from flask import Flask, render_template, request, make_response

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/url-params')
def url_params():
    return render_template('url_params.html', args=request.args)


@app.route('/headers')
def headers():
    return render_template('headers.html', headers=request.headers)


@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html', cookies=request.cookies))
    if 'demo_cookie' not in request.cookies:
        response.set_cookie('demo_cookie', 'cookie_value')
    return response


@app.route('/auth-form', methods=['GET', 'POST'])
def auth_form():
    form_data = None
    if request.method == 'POST':
        form_data = request.form
    return render_template('auth_form.html', form_data=form_data)


def normalize_phone(phone: str):
    allowed = set('0123456789 +-().')
    if any(ch not in allowed for ch in phone):
        return None, 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'

    digits = ''.join(ch for ch in phone if ch.isdigit())
    stripped = phone.strip()
    needs_11_digits = stripped.startswith('+7') or stripped.startswith('8')
    required_count = 11 if needs_11_digits else 10

    if len(digits) != required_count:
        return None, 'Недопустимый ввод. Неверное количество цифр.'

    phone_body = digits[1:] if required_count == 11 else digits
    result = f'8-{phone_body[0:3]}-{phone_body[3:6]}-{phone_body[6:8]}-{phone_body[8:10]}'
    return result, None


@app.route('/phone', methods=['GET', 'POST'])
def phone():
    phone_value = ''
    error = None
    normalized = None
    if request.method == 'POST':
        phone_value = request.form.get('phone', '')
        normalized, error = normalize_phone(phone_value)
    return render_template('phone.html', phone=phone_value, error=error, normalized=normalized)


if __name__ == '__main__':
    app.run(debug=True)
