from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Це важливо для сесії

# Налаштування підключення до бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  # Вказуємо файл бази даних
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Вимикаємо відстеження змін, щоб зменшити використання пам'яті

db = SQLAlchemy(app)

# Створимо модель користувача
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Створення бази даних (це необхідно для створення таблиць, якщо їх ще немає)
with app.app_context():
    db.create_all()

# Головна сторінка
@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:  # Якщо користувач авторизований
        return render_template("site.html", username=session['username'])  # Виводимо головну сторінку
    return redirect(url_for('login'))  # Якщо не авторизований, редірект на сторінку входу

# Сторінка входу
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Перевіряємо наявність користувача в базі даних
        user = User.query.filter_by(username=username).first()
        
        if user and user.password == password:  # Перевіряємо логін і пароль
            session['username'] = user.username  # Зберігаємо ім'я користувача в сесії
            return redirect(url_for('index'))  # Переходимо на головну сторінку
        else:
            return "Невірний логін або пароль", 403  # Помилка, якщо логін або пароль неправильні

    return render_template('login.html')  # Якщо GET-запит, показуємо форму для входу

# Сторінка реєстрації
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Перевірка, чи вже є користувач з таким логіном
        if User.query.filter_by(username=username).first():
            return "Користувач з таким логіном вже існує", 400

        # Додаємо нового користувача до бази даних
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))  # Після реєстрації переходимо на сторінку входу

    return render_template('register.html')  # Якщо GET-запит, показуємо форму реєстрації

# Вихід із системи
@app.route('/logout')
def logout():
    session.pop('username', None)  # Видаляємо ім'я користувача з сесії
    return redirect(url_for('login'))  # Після виходу перенаправляємо на сторінку входу

if __name__ == '__main__':
    app.run(debug=True)









