from flask import Flask, render_template, session, request, redirect, url_for, send_file, flash
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
                                     

def generate_math_captcha():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    captcha_text = f"{a} + {b} = ?"
    answer = a + b
    return captcha_text, str(answer)


def generate_text_captcha(length=5):
    letters = string.ascii_uppercase
    captcha_text = ''.join(random.choice(letters) for _ in range(length))
    return captcha_text, captcha_text


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/captcha', methods=['GET', 'POST'])
def captcha():
    if request.method == 'POST':
        user_input = request.form.get('captcha')
        expected = session.get('captcha_answer')
        if user_input and expected and user_input.strip().upper() == expected.strip().upper():
            flash("CAPTCHA пройден успешно!", "success")
        else:
            flash("Неверный ответ CAPTCHA. Попробуйте снова.", "error")
        captcha_type = random.choice(['math', 'text'])
        if captcha_type == 'math':
            captcha_text, answer = generate_math_captcha()
        else:
            captcha_text, answer = generate_text_captcha()
        session['captcha_text'] = captcha_text
        session['captcha_answer'] = answer
        return redirect(url_for('captcha'))
    else:
        captcha_type = random.choice(['math', 'text'])
        if captcha_type == 'math':
            captcha_text, answer = generate_math_captcha()
        else:
            captcha_text, answer = generate_text_captcha()
        session['captcha_text'] = captcha_text
        session['captcha_answer'] = answer
        return render_template('captcha.html')


@app.route('/captcha_image')
def captcha_image():
    captcha_text = session.get('captcha_text', 'ERROR')
    width, height = 200, 70
    image = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) / 2
    text_y = (height - text_height) / 2
    draw.text((text_x, text_y), captcha_text, fill=(0, 0, 0), font=font)

    for _ in range(5):
        start = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([start, end], fill=(0, 0, 0), width=1)

    buf = BytesIO()
    image.save(buf, 'PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)