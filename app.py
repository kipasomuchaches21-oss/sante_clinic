import os

from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# ─── Демо-данные ───────────────────────────────────────────────────
DOCTORS = [
    {"id": 1, "slug": "ivanova-elena", "name": "Иванова Елена Сергеевна",
     "position": "Главный врач, дерматолог-косметолог", "degree": "К.м.н.",
     "experience": "15 лет", "photo": None, "gender": "female",
     "specialization": "Дерматология, косметология",
     "services": [1, 3], "bio": "Ведущий специалист клиники с многолетним опытом."},
    {"id": 2, "slug": "petrov-alexander", "name": "Петров Александр Иванович",
     "position": "Хирург-ортопед", "degree": "Д.м.н., профессор",
     "experience": "22 года", "photo": None, "gender": "male",
     "specialization": "Ортопедия, хирургия",
     "services": [2], "bio": "Доктор медицинских наук, автор 40+ научных работ."},
    {"id": 3, "slug": "sokolova-marina", "name": "Соколова Марина Владимировна",
     "position": "Терапевт, эндокринолог", "degree": "К.м.н.",
     "experience": "12 лет", "photo": None, "gender": "female",
     "specialization": "Терапия, эндокринология",
     "services": [1, 2], "bio": "Специалист в области эндокринологии и терапии."},
]

SERVICES = [
    {"id": 1, "slug": "terapiya", "title": "Терапия", "category": "medicine",
     "icon": "🫀", "description": "Комплексная диагностика и лечение внутренних болезней.",
     "full_desc": "Наши терапевты проводят полную диагностику, назначают лечение и сопровождают пациента на каждом этапе выздоровления."},
    {"id": 2, "slug": "ortopediya", "title": "Ортопедия", "category": "medicine",
     "icon": "🦴", "description": "Лечение заболеваний опорно-двигательного аппарата.",
     "full_desc": "Современные методы лечения и реабилитации при заболеваниях суставов, позвоночника и костей."},
    {"id": 3, "slug": "laser-cosmetology", "title": "Лазерная косметология", "category": "cosmetology",
     "icon": "✨", "description": "Лазерные процедуры для омоложения и улучшения кожи.",
     "full_desc": "Используем лазеры последнего поколения для эффективного и безопасного лечения кожных проблем."},
    {"id": 4, "slug": "injection-cosmetology", "title": "Инъекционная косметология", "category": "cosmetology",
     "icon": "💉", "description": "Ботулинотерапия, контурная пластика, мезотерапия.",
     "full_desc": "Инъекционные методики коррекции возрастных изменений и несовершенств кожи."},
]

REVIEWS = [
    {"id": 1, "slug": "review-1", "name": "Анна Михайлова", "profession": "Маркетолог",
     "gender": "female", "text": "Прекрасная клиника! Врачи внимательные, оборудование современное. Особенно хочу отметить Иванову Елену — настоящий профессионал своего дела.", "rating": 5,
     "date": "2024-01-15", "show_on_main": True, "tags": ["Клиника", "Косметология"]},
    {"id": 2, "slug": "review-2", "name": "Дмитрий Соколов", "profession": "Инженер",
     "gender": "male", "text": "Обратился с болью в спине. Петров Александр Иванович поставил точный диагноз и назначил эффективное лечение. Уже через месяц забыл о проблеме.", "rating": 5,
     "date": "2024-02-03", "show_on_main": True, "tags": ["Ортопедия", "Врач"]},
    {"id": 3, "slug": "review-3", "name": "Светлана Козлова", "profession": "Учитель",
     "gender": "female", "text": "Хожу в эту клинику уже 3 года. Всегда довольна качеством обслуживания. Чистота, уют, профессионализм — всё на высшем уровне.", "rating": 5,
     "date": "2024-03-10", "show_on_main": True, "tags": ["Клиника"]},
]

BLOG = [
    {"id": 1, "slug": "zdorove-serdca", "title": "Как сохранить здоровье сердца", "category": "article",
     "date": "2024-03-01", "author": "Иванова Елена Сергеевна",
     "preview": "Кардиологи рассказывают о простых правилах, которые помогут сохранить здоровье сердечно-сосудистой системы на долгие годы.",
     "text": "Здоровье сердца — основа долгой и активной жизни. Регулярные физические нагрузки, правильное питание и отказ от вредных привычек — ключевые факторы профилактики сердечно-сосудистых заболеваний.",
     "tags": ["Кардиология", "Профилактика"]},
    {"id": 2, "slug": "kosmetologiya-vesna", "title": "Весенний уход за кожей", "category": "article",
     "date": "2024-03-15", "author": "Иванова Елена Сергеевна",
     "preview": "С приходом весны кожа нуждается в особом уходе. Узнайте о главных процедурах сезона.",
     "text": "Весна — идеальное время для обновления косметологических процедур. Пилинги, лазерные процедуры и мезотерапия помогут коже засиять после зимы.",
     "tags": ["Косметология", "Уход за кожей"]},
    {"id": 3, "slug": "profilaktika-artrita", "title": "Профилактика артрита: советы ортопеда", "category": "news",
     "date": "2024-04-01", "author": "Петров Александр Иванович",
     "preview": "Артрит — одно из самых распространённых заболеваний. Как предотвратить его развитие?",
     "text": "Профилактика артрита включает в себя регулярные умеренные физические нагрузки, контроль веса и своевременное лечение травм суставов.",
     "tags": ["Ортопедия", "Профилактика"]},
]

SPECIALS = [
    {"id": 1, "slug": "kompleksnoe-obsledovanie", "title": "Комплексное обследование", "category": "special",
     "date": "2024-03-01", "preview": "Полная диагностика организма по специальной цене. Экономия до 40%.",
     "text": "Комплексное обследование включает: анализ крови, ЭКГ, УЗИ внутренних органов и консультацию терапевта.", "tags": ["Акция", "Диагностика"],
     "image": None, "price": "от 5 900 ₽"},
    {"id": 2, "slug": "laser-spring", "title": "Лазерные процедуры — весенняя акция", "category": "special",
     "date": "2024-04-01", "preview": "Скидка 30% на все лазерные процедуры в апреле.",
     "text": "Лазерное омоложение, удаление пигментации, фракционный лазер — все процедуры со скидкой 30% в течение апреля.", "tags": ["Акция", "Косметология"],
     "image": None, "price": "от 3 500 ₽"},
]

FAQ = [
    {"id": 1, "question": "Как записаться на приём?", "answer": "Вы можете записаться онлайн через форму на сайте, по телефону +7 (495) 123-45-67 или лично в регистратуре клиники.", "doctor": "Иванова Елена Сергеевна"},
    {"id": 2, "question": "Принимаете ли вы полисы ОМС?", "answer": "Да, наша клиника работает по полисам обязательного медицинского страхования. Уточните перечень услуг по ОМС у администратора.", "doctor": "Петров Александр Иванович"},
    {"id": 3, "question": "Есть ли у вас парковка?", "answer": "Да, рядом с клиникой есть платная парковка. Для наших пациентов предусмотрена скидка при предъявлении карты клиента.", "doctor": "Соколова Марина Владимировна"},
]

# ─── Маршруты ──────────────────────────────────────────────────────

@app.route('/')
def index():
    main_reviews = [r for r in REVIEWS if r['show_on_main']]
    return render_template('index.html', reviews=main_reviews, specials=SPECIALS[:2], doctors=DOCTORS[:3])

@app.route('/medicine')
def medicine():
    services = [s for s in SERVICES if s['category'] == 'medicine']
    return render_template('services.html', services=services, category='medicine', title='Медицинские услуги')

@app.route('/cosmetology')
def cosmetology():
    services = [s for s in SERVICES if s['category'] == 'cosmetology']
    return render_template('services.html', services=services, category='cosmetology', title='Косметология')

@app.route('/medicine/<slug>')
def medicine_detail(slug):
    service = next((s for s in SERVICES if s['slug'] == slug), None)
    if not service:
        return redirect(url_for('medicine'))
    related_doctors = [d for d in DOCTORS if service['id'] in d['services']]
    return render_template('service_detail.html', service=service, doctors=related_doctors, specials=SPECIALS)

@app.route('/cosmetology/<slug>')
def cosmetology_detail(slug):
    service = next((s for s in SERVICES if s['slug'] == slug), None)
    if not service:
        return redirect(url_for('cosmetology'))
    related_doctors = [d for d in DOCTORS if service['id'] in d['services']]
    return render_template('service_detail.html', service=service, doctors=related_doctors, specials=SPECIALS)

@app.route('/doctors')
def doctors():
    return render_template('doctors.html', doctors=DOCTORS)

@app.route('/doctors/<slug>')
def doctor_detail(slug):
    doctor = next((d for d in DOCTORS if d['slug'] == slug), None)
    if not doctor:
        return redirect(url_for('doctors'))
    doctor_services = [s for s in SERVICES if s['id'] in doctor['services']]
    return render_template('doctor_detail.html', doctor=doctor, services=doctor_services)

@app.route('/reviews')
def reviews():
    tag = request.args.get('tag')
    filtered = REVIEWS
    if tag:
        filtered = [r for r in REVIEWS if tag in r.get('tags', [])]
    return render_template('reviews.html', reviews=filtered, current_tag=tag)

@app.route('/reviews/<slug>')
def review_detail(slug):
    review = next((r for r in REVIEWS if r['slug'] == slug), None)
    if not review:
        return redirect(url_for('reviews'))
    return render_template('review_detail.html', review=review)

@app.route('/faq')
def faq():
    return render_template('faq.html', faqs=FAQ)

@app.route('/blog')
def blog():
    tag = request.args.get('tag')
    filtered = BLOG
    if tag:
        filtered = [b for b in BLOG if tag in b.get('tags', [])]
    return render_template('blog.html', posts=filtered, current_tag=tag)

@app.route('/blog/<slug>')
def blog_detail(slug):
    post = next((p for p in BLOG if p['slug'] == slug), None)
    if not post:
        return redirect(url_for('blog'))
    others = [p for p in BLOG if p['slug'] != slug][:3]
    return render_template('blog_detail.html', post=post, others=others)

@app.route('/special')
def special():
    return render_template('special.html', specials=SPECIALS)

@app.route('/special/<slug>')
def special_detail(slug):
    sp = next((s for s in SPECIALS if s['slug'] == slug), None)
    if not sp:
        return redirect(url_for('special'))
    others = [s for s in SPECIALS if s['slug'] != slug][:2]
    return render_template('special_detail.html', special=sp, others=others)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/search')
def search():
    q = request.args.get('q', '').lower()
    results = []
    if q:
        for s in SERVICES:
            if q in s['title'].lower():
                results.append({'title': s['title'], 'url': f"/{s['category']}/{s['slug']}", 'section': 'Услуги'})
        for d in DOCTORS:
            if q in d['name'].lower():
                results.append({'title': d['name'], 'url': f"/doctors/{d['slug']}", 'section': 'Врачи'})
        for p in BLOG:
            if q in p['title'].lower() or q in p['preview'].lower():
                results.append({'title': p['title'], 'url': f"/blog/{p['slug']}", 'section': 'Блог'})
    return render_template('search.html', results=results, query=q)

@app.route('/api/search')
def api_search():
    q = request.args.get('q', '').lower()
    results = []
    if len(q) >= 2:
        for s in SERVICES:
            if q in s['title'].lower():
                results.append({'title': s['title'], 'url': f"/{s['category']}/{s['slug']}", 'section': 'Услуги'})
        for d in DOCTORS:
            if q in d['name'].lower():
                results.append({'title': d['name'], 'url': f"/doctors/{d['slug']}", 'section': 'Врачи'})
        for p in BLOG:
            if q in p['title'].lower():
                results.append({'title': p['title'], 'url': f"/blog/{p['slug']}", 'section': 'Блог'})
    return jsonify(results[:6])

@app.route('/api/appointment', methods=['POST'])
def api_appointment():
    data = request.json
    print(f"[ЗАПИСЬ НА ПРИЁМ] {data}")
    return jsonify({'status': 'ok', 'message': 'Заявка принята! Мы свяжемся с вами в ближайшее время.'})

@app.route('/api/callback', methods=['POST'])
def api_callback():
    data = request.json
    print(f"[ОБРАТНЫЙ ЗВОНОК] {data}")
    return jsonify({'status': 'ok', 'message': 'Заявка принята! Мы перезвоним вам в течение 15 минут.'})

@app.route('/api/review', methods=['POST'])
def api_review():
    data = request.json
    print(f"[НОВЫЙ ОТЗЫВ] {data}")
    return jsonify({'status': 'ok', 'message': 'Спасибо! Ваш отзыв отправлен на модерацию.'})

# Редиректы согласно ТЗ
@app.route('/diagnoz')
@app.route('/diagnoz/<path:p>')
def redirect_diagnoz(p=None): return redirect('/', 301)

@app.route('/napravlenia')
def redirect_napravlenia(): return redirect('/medicine', 301)

@app.route('/uslugi')
@app.route('/uslugi/<path:p>')
def redirect_uslugi(p=None): return redirect('/medicine', 301)

@app.route('/klinika')
def redirect_klinika(): return redirect('/about', 301)

@app.route('/news')
@app.route('/news/<path:p>')
def redirect_news(p=None): return redirect('/blog', 301)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    print("Sante Clinic запущена → http://localhost:5000")
    # app.run(debug=True, port=5000)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

