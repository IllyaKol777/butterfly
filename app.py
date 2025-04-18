from flask import Flask, render_template, redirect, url_for, request, flash, session, redirect
from markupsafe import Markup
import requests


app = Flask(__name__)
app.secret_key = 'blablabla123465789qweqweqwe'

TELEGRAM_BOT_TOKEN = '8127039608:AAG1kI8fKtrP0n8ARRuUVzAbVMPFXrz74AQ'
ADMIN_IDS = [464299007, 979644158]

# 🧠 Інформація про психологів
CHAT_INFO = {
    '1': {'chat_id': 1072852815, 'name': 'Василенко Тетяна'},
    '2': {'chat_id': 2096649369, 'name': 'Гулей Тетяна'},
    '3': {'chat_id': 979644158, 'name': 'Оксана Моргоч'},
    '4': {'chat_id': 6190054025, 'name': 'Віталія Калин'},
    '5': {'chat_id': 5260639345, 'name': 'Глушко Олена'},
    '6': {'chat_id': 1108966285, 'name': 'Кривонос Тетяна'},
    '7': {'chat_id': 486188850, 'name': 'Євгенія Овсюхно'},
}

def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(url, data=payload)

# Дані для входу в адмінку (тимчасові, можна замінити на БД)
ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

publications = [
    {"id": 1, "title": "Як впоратися зі стресом", "content": "Стаття про стратегії подолання стресу..."},
    {"id": 2, "title": "5 порад для здорової психології", "content": "Ключові рекомендації для поліпшення ментального здоров'я..."}
]

@app.route('/send-form', methods=['POST'])
def send_form():
    data = request.form
    selected = data.get('psychologist')
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    time = data.get('time')
    comment = data.get('message') or "Без коментарів"

    psych_info = CHAT_INFO.get(selected)
    if not psych_info:
        return "Invalid psychologist ID", 400

    psych_name = psych_info['name']
    chat_id = psych_info['chat_id']

    message = f"""
<b>🧠 Нова заявка на консультацію</b>
👤 Ім'я: {name}
📧 Email: {email}
🗓 Дата: {date}
⏰ Час: {time}
🧑‍⚕️ Психолог: {psych_name}
💬 Коментар: {comment}
"""

    # 🔹 Надсилаємо психологу
    send_telegram_message(chat_id, message)

    # 🔹 Надсилаємо всім адміністраторам
    for admin_id in ADMIN_IDS:
        send_telegram_message(admin_id, message)

    return redirect('/')


@app.route('/')
def home():
    return render_template('index.html', title="Головна сторінка")

@app.route('/about')
def about():
    return render_template('about.html')

"""
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        if len(message) < 10:
            flash("Повідомлення має містити мінімум 10 символів", "danger")
        else:
            # Тут можна зберігати дані в базу або надсилати email
            flash("Ваше повідомлення успішно надіслано!", "success")
            return redirect(url_for('contact'))

    return render_template('feedback.html')
"""

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')

        if not all([name, email, message_text]):
            flash("Будь ласка, заповніть всі поля.", "error")
            return render_template('feedback.html')

        # 📨 Формуємо повідомлення
        message = f"""
<b>📬 Нове повідомлення з форми зворотного зв'язку</b>
👤 Ім'я: {name}
📧 Email: {email}
💬 Повідомлення: {message_text}
"""

        # Надсилаємо всім адміністраторам
        for admin_id in ADMIN_IDS:
            send_telegram_message(admin_id, message)

        flash("Дякуємо за звернення! Ми відповімо якнайшвидше.", "success")
        return render_template('feedback.html')

    return render_template('feedback.html')

@app.route('/psychologists')
def psychologists():
    psychologists_data = [
        {"id": 1, "name": "Василенко Тетяна", "specialty": "Практикуючий психолог", "image": "1.jpg", "rating": 5.0, "reviews": 135},
        {"id": 2, "name": "Гулей Тетяна", "specialty": "Сертифікований гештальт терапевт", "image": "2.jpg", "rating": 5.0, "reviews": 135},
        {"id": 3, "name": "Оксана Моргоч", "specialty": "Практичний психолог в гештальт підході", "image": "3.jpg", "rating": 5.0, "reviews": 135},
        {"id": 4, "name": "Віталія Калин", "specialty": "Арт, гештальт-терапевт", "image": "4.jpg", "rating": 5.0, "reviews": 135},
        {"id": 5, "name": "Глушко Олена", "specialty": "Психолог консультант", "image": "5.jpg", "rating": 5.0, "reviews": 135},
        {"id": 6, "name": "Кривонос Тетяна", "specialty": "Практикуючий психолог", "image": "6.jpg", "rating": 5.0, "reviews": 135},
        {"id": 7, "name": "Євгенія Овсюхно", "specialty": "Психолог в гештальт підході", "image": "7.jpg", "rating": 5.0, "reviews": 135},
    ]
    return render_template('psychologists.html', psychologists=psychologists_data)


@app.route('/psychologist/<int:id>')
def psychologist_detail(id):
    psychologists_data = {
        1: {
            "name": "Василенко Тетяна",
            "specialty": "Практикуючий психолог",
            "bio": Markup("""
                Маю вищу державну освіту психолога, використовую в роботі гештальт підхід, маю сертифікат гейткіпера та спеціалізацію " Психосоматика тіла".<br>
                Проводжу консультації з питань:<br>
                - Проблемно-орієнтовані консультації<br>
                - Працюю з темою втрат та горя.<br>
                - Батьківсько-дитячі відносини.<br>
                - Консультації на прийняття рішень, самооцінка.<br>
                -Психосоматика.<br>
                -Вигорання,як професійне так і особисте.<br><br>
                Проводжу:<br>
                - Індивідуальні сесії для дорослих та дітей віком з 14 років.<br>
                - Консультації онлайн та офлайн<br>
                📞 Запис за телефоном: 093 395 68 60<br>
                inst: tatiana_yogatea<br>
                fb: Василенко Татьяна<br>
                Вартість консультації -1000грн за 50 хв.<br>
                Запрошую вас на консультацію, щоб разом знайти рішення для ваших проблем та відкрити нові можливості для зростання.
            """),
            "image": "1.jpg",
            "rating": 5.0,
            "reviews": 135,
            "video": None
        },
        2: {
            "name": "Гулей Тетяна",
            "specialty": "Сертифікований гештальт терапевт",
            "bio": Markup("""
                Досвід роботи: 2,5 роки<br>
                Спеціалізація : гештальт терапія з дітьми та сім’єю.<br>
                Напрями роботи:<br>
                розлучення, життя до, після і в моменті.<br>
                Конфлікти , батьківсько- дитячі стосунки.<br>
                Сепарація<br>
                Відновлення опори, ресурсів рухатись вперед.<br>
                Проживання горя, криз<br>
                Ідентичність, проявлення, самореалізація.<br>
                Формат сесій: змішаний, онлайн і очно м. Черніці<br>
                Вартість сесії 60хв/900гр
            """),
            "image": "2.jpg",
            "rating": 5.0,
            "reviews": 135,
            "video": "2.mp4"
        },
        3: {
            "name": "Оксана Моргоч",
            "specialty": "Практичний психолог в гештальт підході",
            "bio": Markup("""
                Досвід з 2018 р.<br>
                Працюю з підлітками та дорослими.<br>
                Теми: <br>
                Кризові періоди в житті (розлучення, переїзд, втрата).<br>
                Відносини в парі, батьківсько дитячі, колегіальні.<br>
                Депресія. Тривога. Панічні атаки. У супроводі разом з психіатром.<br>
                Сепарація, пошук себе і свого шляху.<br>
                Підліткова криза. Селфхарм. Суциїдальна поведінка.<br> 
                Пошук життєвий опор. Саморегуляція. <br>
                Працюю онлайн та офлайн м.Чернівці.<br>
                Ціна 1000 грн. 60 хв.
            """),
            "image": "3.jpg",
            "rating": 5.0,
            "reviews": 135,
            "video": "3.mp4"
        },
        4: {
            "name": "Віталія Калин",
            "specialty": "Арт, гештальт-терапевт",
            "bio": Markup("""
                Маю спеціалізацію  «Особливості психотерапії дітей та підлітків у гештальт підході ». Запрошую клієнтів у короткострокову чи довгострокову терапію.<br>
                Чуйна ,вмію слухати.<br>
                Можу бути корисною у темах :<br>
                🔸самооцінка та самоцінність<br>
                🔸особисті кордони<br>
                🔸відчуття власних потреб<br>
                🔸відносини<br>
                🔸тривожність та страхи<br>
                🔸сепарація<br>
                🔸почуття самотності<br>
                🔸почуття провини та сорому.<br>
                📌про дитячо- батьківські стосунки.<br>
                📌про партнерські стосунки<br>
                📌про жіночність та материнство<br>
                📌 Вікові кризи у дітей ,підлітків ,дорослих .<br>
                В роботі дотримуюсь етичного кодексу. Працюю з дітьми ,підлітками та дорослими .Онлай зустір .<br>
                Цінність сесії 1000грн/50хв.<br>
                0964731136 вайбер/вотцап.
            """),
            "image": "4.jpg",
            "rating": 5.0,
            "reviews": 135,
            "video": "4.mp4"
        },
        5: {
            "name": "Глушко Олена",
            "specialty": "Психолог консультант",
            "bio": Markup("""
                Клінічна спеціалізація в гештальт підході.<br> 
                Працюю з такими темами:<br> 
                Вимушена міграція, кризи пов'язані з нею та адаптація в нових умовах.<br> 
                Депресивні та тривожні стани, панічні атаки, надмірна емоційність чи відсутність емоцій, нав'язливі думки та дії.<br> 
                Почуття сорому, провини, сепарація та дослідження своєї ідентичності.<br> 
                Не працюю з дітьми, підлітками, військовими.<br> 
                Консультація онлайн, 900грн/20євро за 60хв
            """),
            "image": "5.jpg",
            "rating": 5.0,
            "reviews": 135,
            "video": None
        },
        6: {
            "name": "Кривонос Тетяна",
            "specialty": "Практикуючий психолог",
            "bio": Markup("""
                Запрошую Вас у короткострокову чи тривалу терапію.<br>
                Запити, з якими я працюю:<br>
                - Тема стосунків.<br>
                - Встановлення та відстоювання кордонів.<br>
                - Почуття сорому, провини.<br>
                - Проблеми з самооцінкою.<br>
                - Складнощі у дитячо-батьківських відносинах.<br>
                - Сепарація.<br>
                - Адаптація до змін (зміна місця проживання, роботи, пошук себе).<br>
                - Професійне вигорання.<br>
                - Страх публічних виступів.<br>
                - Розрив стосунків, розлучення.<br>
                Працюю з дорослими.<br>
                Не працюю:<br> 
                - з дітьми та підлітками;<br>
                - військовослужбовцями,<br>
                - людьми з залежностями.<br>
                Тривалість консультації 60 хв,<br>
                вартість 1000 грн,<br>
                консультація онлайн Zoom.<br>
                Запис на консультацію в телеграм або вайбер +38 095 530 63 59.
            """),
            "image": "6.jpg",
            "rating": 5.0,
            "reviews": 135,
            "video": None
        },
        7: {
            "name": "Євгенія Овсюхно",
            "specialty": "Психолог в гештальт підході",
            "bio": Markup("""
                Я мама двох підлітків. Вже 3 роки живу у Німеччині. Маю великий досвід у банківській сфері,<br>
                сфері бізнесу і вже як 13 років досвід дитячо-батьківських відносин.  Також працюю з темами :<br>
                - пошуку себе<br>
                - реалізації<br>
                - стосунки з собою та іншими<br>
                - партнерські стосунки<br>
                - дитячо-батьківські стосунки<br>
                - розлучення<br>
                - вихід з кризи<br>
                - еміграція та адаптація<br> 
                - гроші та фінанси<br>
                Запрошу до роботи он-лайн. +380674955992<br>
                Вартість сесії 1000 грн / 50 хв
            """),
            "image": "7.jpg",
            "rating": 5.0,
            "reviews": 135,
            "video": None
        }
    }

    psychologist = psychologists_data.get(id)
    if psychologist:
        return render_template('psychologist_detail.html', psychologist=psychologist)
    else:
        return "Психолог не знайдений", 404

@app.route('/publications')
def publications():
    publications_data = [
        {"id": 1, "title": "Що таке психотравма?", "content": "Психотравма або дитяча травма  або психутравмуюча ситуація чи подія. Простими словами про складне..."},
        {"id": 2, "title": "Саморегуляція. Що то за звір?", "content": "Травма формується коли є надто травматична подія і психіка не може її обробити..."},
    ]
    return render_template('publications.html', publications=publications_data)

@app.route('/publish/<int:id>')
def publication_detail(id):
    publications_data = {
        1: {"title": "Що таке психотравма?", "content": """
Психотравма або дитяча травма  або психутравмуюча ситуація чи подія<br>
Простими словами про складне.<br>
Що то таке? <br>
Як відбувається зцілення?<br>
Як впливає на життя, відносини , самосприйняття та здатність як дорослий задовільнити свої потреби ( налаштування безпеки, побудови відносин, і самореалізації)<br>
Травма формується коли є надто травматична подія і психіка не може її обробити. Тут якщо про дітей потрібно стійка психіка дорослих, щоб прожити разом складні почуття. З різних причин  підтримки немає ( батьки незрілі і можуть ляпнути напртклад " Що ти ниєш? Чи " Я твої роки вже  корову пасла і 3 братів доглядала". Тощо.<br>
Відбувається фіксація бо не прожиті почуття і формується травма. Потім спрацьовує тригер подібна ситуація в сьогоденні і понеслося всі переживання які були заблоковані в першій ситуації.<br>
Зрозуміло що сьогодні це впливає на життя і самосприйняття. Тут тривога, сором, вина, злість яка буде направлена в себе.<br>
Зцілення :<br>
Ми травмуємося об людей і зцілення також відбувається з людьми.<br>
Зцілення відбувається через проживання тих заблокованих почуттів. Закрити  славнозвісний гештальт ( незавершену ситуацію).<br>
1 етап: не усвідомлення місця травми, болі, і ми діємо шаблонно<br>
2 етап. Соціальні маски і захистні стратегії поведінки . Уникнення травмуючих подій.<br>
3 етап .переживання тупіка і безсилля. Усвідомлення болю, травми.<br>
4 етап.утрииаггя напруги яка накопилося за роки і відчуття зараз зірвуся.<br>
5 етап вихід енергії болю через плач, крик, злість, навіть сміх.<br> 
Полегшення і відчуття кулька здулася. І відновлюється глибокий контакт з собою , тілом.<br>
Якщо травмування відбулося в стосунках з батьками. То дана травма буде проявлятися в побудові відносин близьких, колегіальних, батьківсько дитячих.<br>
Видихаємо розумні слова закінчилися.)))<br>
Надія є це змінити і налаштувати контакт з собою. Це буває переважно боляче, але ваша психіка розумна штука яка вас захистить і ви візьмете і пройдете те що є для вас у даний момент виносимо.<br>
Цей шлях проходження даних етапів вартий того щоб бути вільним від напруження і болю .<br>
Змінити і бути вільним у проявах себе без сорому, страху і вини.<br>
Це бути живим, вільним, розслабленим.<br>
І жити то життя на повні груди.
            """, "date": "1 березня 2025"},
        2: {"title": "Саморегуляція. Що то за звір?", "content": """
Саморегуляція<br>
Що то за звір?<br>
Класна штука. Гарне самопочуття турбота про себе з любові і задовільнення вчасно своїх потреб.<br>
Тут все просто:<br>
Дує протягом закрий вікно, не готовий до поцілунку скажи, переїв спілкування з людьми усамітнення і відновлення, порушили кордони скажи, " Чувак ти стоїш на моєму пальці, болить, забери ногу". Відчуваєш голод йди їсти, не знаєш що? Слухай тіло воно тобі скаже, Втома- відпочинок. Вдох видих, вдох видих.<br>
Проблемка в тому, що довіра і чуттєвість забита і заблокована буває<br>
 І каркання з минулого: <br>
-Поки не заробив на обід то немаєш чого за стіл сідати.( Вина)<br>
- спати вдень коли купа роботи? ( Сором)<br>
- ти не причащався цього посту Аяяя( страх, провина, сором)<br>
- вікна до паски не помиті яка ти газдиня( сором )<br>
Жінка повинна ... Чоловік повинен... Діти повинні.... ( Вкладіть своє)<br>
То що ми бачимо маніпуляції  , тиск через вину, сором, страх. І про які тут потреби? Яка саморегуляція? <br>
Сумно адже так просто. Робити собі добре, турбуватися, любити себе. ..<br>
Але ж : егоїстично, не нормально, так всі жили, соромно за своє "я"( не дивно якщо соромили в сім'ї, школі і було бляха нажаль як норма). <br>
Тут багато можна співати про ситуації, сприйняття себе викривлене як наслідок цих пісень прекрасних людей що нас оточували. <br>
І на закуску. Це міняється. Помалу. Непросто. Але це нав'язування можна позбутися шляхом здобуття нового досвіду у стосунках з терапевтом як тренувальна база, а далі і і життя нести створенні нові нейронні зв'язки. Старі патерни відпадуть з часом . І в кінці кінців ми дорослі і ми можемо обирати чи по старому чи по новому) <br>
Так що будемо композиторами і напишемо разом нову мелодію . Під яку танцювати і рухатися в задоволення.
        """, "date": "20 лютого 2025"},
    }

    publication = publications_data.get(id)
    if publication:
        return render_template('publication_detail.html', publication=publication)
    else:
        return "Стаття не знайдена", 404

@app.route('/booking', methods=['GET', 'POST'])
def booking():
    psychologists_data = [
        {"id": 1, "name": "Наталія Салівон"},
        {"id": 2, "name": "Гулей Тетяна"},
        {"id": 3, "name": "Оксана Моргоч"},
        {"id": 4, "name": "Шевчук Оксана"},
        {"id": 5, "name": "Глушко Олена"},
    ]

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        psychologist_id = request.form['psychologist']
        date = request.form['date']
        time = request.form['time']
        message = request.form.get('message', '')

        # Тут можна обробити дані (записати в базу)
        return f"Записано: {name}, email: {email}, до психолога {psychologist_id} на {date} о {time}. Коментар: {message}"

    return render_template('booking.html', psychologists=psychologists_data)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
            session['admin_logged_in'] = True
            flash("Вхід успішний!", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Неправильний логін або пароль", "danger")

    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash("Увійдіть в систему для доступу", "warning")
        return redirect(url_for('admin_login'))

    psychologists_data = [
        {"id": 1, "name": "Анна Коваленко", "specialty": "Сімейний психолог"},
        {"id": 2, "name": "Олег Василенко", "specialty": "Клінічний психолог"},
        {"id": 3, "name": "Марія Дорошенко", "specialty": "Дитячий психолог"},
    ]

    publications_data = [
        {"id": 1, "title": "Як подолати стрес?"},
        {"id": 2, "title": "Психологічні техніки для зниження тривожності"},
        {"id": 3, "title": "Як покращити відносини в сім'ї?"},
    ]

    return render_template('admin_dashboard.html', psychologists=psychologists_data, publications=publications_data)

# Додавання психолога
@app.route('/admin/add_psychologist')
def add_psychologist():
    return "Форма додавання психолога"

# Редагування психолога
@app.route('/admin/edit_psychologist/<int:id>')
def edit_psychologist(id):
    return f"Редагування психолога з ID {id}"

# Видалення психолога
@app.route('/admin/delete_psychologist/<int:id>')
def delete_psychologist(id):
    flash("Психолога успішно видалено", "success")
    return redirect(url_for('admin_dashboard'))

# Додавання публікації
@app.route('/admin/add_publication')
def add_publication():
    return "Форма додавання публікації"

# Редагування публікації
@app.route('/admin/edit_publication/<int:id>')
def edit_publication(id):
    return f"Редагування публікації з ID {id}"

# Видалення публікації
@app.route('/admin/delete_publication/<int:id>')
def delete_publication(id):
    flash("Публікацію успішно видалено", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Ви вийшли з системи", "info")
    return redirect(url_for('admin_login'))

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)