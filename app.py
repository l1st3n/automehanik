from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Конфигурация электронной почты
EMAIL_ADDRESS = "sten25six@gmail.com"  # Замените на ваш адрес электронной почты
EMAIL_PASSWORD = "sktj yaxb kwyi zwwa"  # Замените на ваш пароль (или сгенерированный пароль приложения)
SMTP_SERVER = "smtp.gmail.com"  # Или другой SMTP-сервер
SMTP_PORT = 587  # Обычно 587 для TLS или 465 для SSL

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        message = request.form['message']

        # Формируем текст письма
        body = f"Имя: {name}\nТелефон: {phone}\nСообщение: {message}"
        msg = MIMEText(body)
        msg['Subject'] = "Новое сообщение с сайта АвтоМеханик"
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS  # Отправляем на тот же адрес, но можно изменить

        # Отправка письма
        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Защищенное соединение
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
            return redirect(url_for('success')) # Перенаправление на страницу успеха
        except Exception as e:
            print(f"Ошибка отправки: {e}")
            return render_template('error.html', error=str(e)) # Отображение страницы ошибки

    else:
        return "Что-то пошло не так!"

@app.route('/success')
def success():
    return render_template('success.html')

# Добавьте обработку ошибок (необязательно, но рекомендуется)
@app.route('/error')
def error():
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)