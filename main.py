from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = 'a03abf780b226cbfdce0eb96f3edbeb29143076730be555b'  # Нужно для работы flash()

# Параметры для SMTP сервера (например, для Gmail)
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = ''  # Замените на свой email
SMTP_PASSWORD = ''  # Замените на свой ключ безопасности

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Обработка формы
@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    # Получаем данные из формы
    email = request.form['email']
    message = request.form['text']

    # Создаем письмо
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = SMTP_USER  # Замените на email получателя
    msg['Subject'] = f'Обратная связь от {email}'

    # Добавляем текст письма
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Отправляем письмо через SMTP сервер
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Начинаем шифрование
            server.login(SMTP_USER, SMTP_PASSWORD)
            text = msg.as_string()
            server.sendmail(email, SMTP_USER, text)  # Отправка письма
        flash('Письмо успешно отправлено!', 'success')  # Добавляем уведомление
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Ошибка при отправке: {e}', 'danger')  # Добавляем сообщение об ошибке
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
