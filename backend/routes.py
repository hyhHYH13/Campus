from flask import Flask, request, jsonify
from app import app, db
from models import *
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

# 初始化数据库
try:
    with app.app_context():
        db.create_all()
        # 创建默认管理员用户
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(username='admin', password='admin123', name='管理员', email='admin@example.com', role='admin')
            db.session.add(admin)
            db.session.commit()
except Exception as e:
    print(f"数据库初始化错误: {e}")

# 登录
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'role': user.role
            }
        })
    return jsonify({'message': '用户名或密码错误'}), 401

# 获取当前用户信息
@app.route('/api/user/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'role': user.role
    })

# 修改密码
@app.route('/api/user/change-password', methods=['POST'])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if user.password != old_password:
        return jsonify({'message': '旧密码错误'}), 400
    
    user.password = new_password
    db.session.commit()
    return jsonify({'message': '密码修改成功'})

# 用户管理
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at
    } for user in users])

@app.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    user = User(
        username=data.get('username'),
        password=data.get('password'),
        name=data.get('name'),
        email=data.get('email'),
        role=data.get('role')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '用户创建成功'})

@app.route('/api/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get(id)
    data = request.get_json()
    user.username = data.get('username')
    user.name = data.get('name')
    user.email = data.get('email')
    user.role = data.get('role')
    if data.get('password'):
        user.password = data.get('password')
    db.session.commit()
    return jsonify({'message': '用户更新成功'})

@app.route('/api/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': '用户删除成功'})

# 轮播图管理
@app.route('/api/carousels', methods=['GET'])
def get_carousels():
    carousels = Carousel.query.filter_by(status=True).order_by(Carousel.order).all()
    return jsonify([{
        'id': carousel.id,
        'title': carousel.title,
        'image_url': carousel.image_url,
        'link': carousel.link
    } for carousel in carousels])

@app.route('/api/carousels/admin', methods=['GET'])
@jwt_required()
def get_all_carousels():
    carousels = Carousel.query.order_by(Carousel.order).all()
    return jsonify([{
        'id': carousel.id,
        'title': carousel.title,
        'image_url': carousel.image_url,
        'link': carousel.link,
        'order': carousel.order,
        'status': carousel.status
    } for carousel in carousels])

@app.route('/api/carousels', methods=['POST'])
@jwt_required()
def create_carousel():
    data = request.get_json()
    carousel = Carousel(
        title=data.get('title'),
        image_url=data.get('image_url'),
        link=data.get('link'),
        order=data.get('order', 0),
        status=data.get('status', True)
    )
    db.session.add(carousel)
    db.session.commit()
    return jsonify({'message': '轮播图创建成功'})

@app.route('/api/carousels/<int:id>', methods=['PUT'])
@jwt_required()
def update_carousel(id):
    carousel = Carousel.query.get(id)
    data = request.get_json()
    carousel.title = data.get('title')
    carousel.image_url = data.get('image_url')
    carousel.link = data.get('link')
    carousel.order = data.get('order')
    carousel.status = data.get('status')
    db.session.commit()
    return jsonify({'message': '轮播图更新成功'})

@app.route('/api/carousels/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_carousel(id):
    carousel = Carousel.query.get(id)
    db.session.delete(carousel)
    db.session.commit()
    return jsonify({'message': '轮播图删除成功'})

# 公告管理
@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return jsonify([{
        'id': announcement.id,
        'title': announcement.title,
        'content': announcement.content,
        'author': announcement.author,
        'created_at': announcement.created_at
    } for announcement in announcements])

@app.route('/api/announcements', methods=['POST'])
@jwt_required()
def create_announcement():
    data = request.get_json()
    announcement = Announcement(
        title=data.get('title'),
        content=data.get('content'),
        author=data.get('author')
    )
    db.session.add(announcement)
    db.session.commit()
    return jsonify({'message': '公告创建成功'})

@app.route('/api/announcements/<int:id>', methods=['PUT'])
@jwt_required()
def update_announcement(id):
    announcement = Announcement.query.get(id)
    data = request.get_json()
    announcement.title = data.get('title')
    announcement.content = data.get('content')
    announcement.author = data.get('author')
    db.session.commit()
    return jsonify({'message': '公告更新成功'})

@app.route('/api/announcements/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_announcement(id):
    announcement = Announcement.query.get(id)
    db.session.delete(announcement)
    db.session.commit()
    return jsonify({'message': '公告删除成功'})

# 资讯分类管理
@app.route('/api/news-categories', methods=['GET'])
def get_news_categories():
    categories = NewsCategory.query.all()
    return jsonify([{
        'id': category.id,
        'name': category.name
    } for category in categories])

@app.route('/api/news-categories', methods=['POST'])
@jwt_required()
def create_news_category():
    data = request.get_json()
    category = NewsCategory(name=data.get('name'))
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': '分类创建成功'})

@app.route('/api/news-categories/<int:id>', methods=['PUT'])
@jwt_required()
def update_news_category(id):
    category = NewsCategory.query.get(id)
    data = request.get_json()
    category.name = data.get('name')
    db.session.commit()
    return jsonify({'message': '分类更新成功'})

@app.route('/api/news-categories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_news_category(id):
    category = NewsCategory.query.get(id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': '分类删除成功'})

# 疫情资讯管理
@app.route('/api/news', methods=['GET'])
def get_news():
    news = News.query.order_by(News.created_at.desc()).all()
    return jsonify([{
        'id': news_item.id,
        'title': news_item.title,
        'content': news_item.content,
        'category_id': news_item.category_id,
        'category_name': news_item.category.name,
        'author': news_item.author,
        'image_url': news_item.image_url,
        'created_at': news_item.created_at
    } for news_item in news])

@app.route('/api/news', methods=['POST'])
@jwt_required()
def create_news():
    data = request.get_json()
    news_item = News(
        title=data.get('title'),
        content=data.get('content'),
        category_id=data.get('category_id'),
        author=data.get('author'),
        image_url=data.get('image_url')
    )
    db.session.add(news_item)
    db.session.commit()
    return jsonify({'message': '资讯创建成功'})

@app.route('/api/news/<int:id>', methods=['PUT'])
@jwt_required()
def update_news(id):
    news_item = News.query.get(id)
    data = request.get_json()
    news_item.title = data.get('title')
    news_item.content = data.get('content')
    news_item.category_id = data.get('category_id')
    news_item.author = data.get('author')
    news_item.image_url = data.get('image_url')
    db.session.commit()
    return jsonify({'message': '资讯更新成功'})

@app.route('/api/news/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_news(id):
    news_item = News.query.get(id)
    db.session.delete(news_item)
    db.session.commit()
    return jsonify({'message': '资讯删除成功'})

# 疫情数据管理
@app.route('/api/covid-data', methods=['GET'])
def get_covid_data():
    data = CovidData.query.order_by(CovidData.date.desc()).all()
    return jsonify([{
        'id': item.id,
        'date': item.date,
        'confirmed': item.confirmed,
        'suspected': item.suspected,
        'recovered': item.recovered,
        'deaths': item.deaths,
        'campus_area': item.campus_area
    } for item in data])

@app.route('/api/covid-data', methods=['POST'])
@jwt_required()
def create_covid_data():
    data = request.get_json()
    covid_data = CovidData(
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
        confirmed=data.get('confirmed'),
        suspected=data.get('suspected'),
        recovered=data.get('recovered'),
        deaths=data.get('deaths'),
        campus_area=data.get('campus_area')
    )
    db.session.add(covid_data)
    db.session.commit()
    return jsonify({'message': '数据添加成功'})

@app.route('/api/covid-data/<int:id>', methods=['PUT'])
@jwt_required()
def update_covid_data(id):
    covid_data = CovidData.query.get(id)
    data = request.get_json()
    covid_data.date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    covid_data.confirmed = data.get('confirmed')
    covid_data.suspected = data.get('suspected')
    covid_data.recovered = data.get('recovered')
    covid_data.deaths = data.get('deaths')
    covid_data.campus_area = data.get('campus_area')
    db.session.commit()
    return jsonify({'message': '数据更新成功'})

@app.route('/api/covid-data/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_covid_data(id):
    covid_data = CovidData.query.get(id)
    db.session.delete(covid_data)
    db.session.commit()
    return jsonify({'message': '数据删除成功'})

# 健康填报
@app.route('/api/health-reports', methods=['GET'])
@jwt_required()
def get_health_reports():
    user_id = get_jwt_identity()
    reports = HealthReport.query.filter_by(user_id=user_id).order_by(HealthReport.created_at.desc()).all()
    return jsonify([{
        'id': report.id,
        'temperature': report.temperature,
        'symptoms': report.symptoms,
        'location': report.location,
        'health_status': report.health_status,
        'created_at': report.created_at
    } for report in reports])

@app.route('/api/health-reports/admin', methods=['GET'])
@jwt_required()
def get_all_health_reports():
    reports = HealthReport.query.order_by(HealthReport.created_at.desc()).all()
    return jsonify([{
        'id': report.id,
        'user_id': report.user_id,
        'user_name': report.user.name,
        'temperature': report.temperature,
        'symptoms': report.symptoms,
        'location': report.location,
        'health_status': report.health_status,
        'created_at': report.created_at
    } for report in reports])

@app.route('/api/health-reports', methods=['POST'])
@jwt_required()
def create_health_report():
    user_id = get_jwt_identity()
    data = request.get_json()
    report = HealthReport(
        user_id=user_id,
        temperature=data.get('temperature'),
        symptoms=data.get('symptoms'),
        location=data.get('location'),
        health_status=data.get('health_status')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': '健康填报成功'})

# 出入申请
@app.route('/api/entry-exit', methods=['GET'])
@jwt_required()
def get_entry_exit_applications():
    user_id = get_jwt_identity()
    applications = EntryExitApplication.query.filter_by(user_id=user_id).order_by(EntryExitApplication.created_at.desc()).all()
    return jsonify([{
        'id': app.id,
        'purpose': app.purpose,
        'start_time': app.start_time,
        'end_time': app.end_time,
        'destination': app.destination,
        'status': app.status,
        'created_at': app.created_at
    } for app in applications])

@app.route('/api/entry-exit/admin', methods=['GET'])
@jwt_required()
def get_all_entry_exit_applications():
    applications = EntryExitApplication.query.order_by(EntryExitApplication.created_at.desc()).all()
    return jsonify([{
        'id': app.id,
        'user_id': app.user_id,
        'user_name': app.user.name,
        'purpose': app.purpose,
        'start_time': app.start_time,
        'end_time': app.end_time,
        'destination': app.destination,
        'status': app.status,
        'created_at': app.created_at
    } for app in applications])

@app.route('/api/entry-exit', methods=['POST'])
@jwt_required()
def create_entry_exit_application():
    user_id = get_jwt_identity()
    data = request.get_json()
    application = EntryExitApplication(
        user_id=user_id,
        purpose=data.get('purpose'),
        start_time=datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S'),
        end_time=datetime.strptime(data.get('end_time'), '%Y-%m-%d %H:%M:%S'),
        destination=data.get('destination'),
        status='pending'
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'message': '申请提交成功'})

@app.route('/api/entry-exit/<int:id>/approve', methods=['PUT'])
@jwt_required()
def approve_entry_exit_application(id):
    application = EntryExitApplication.query.get(id)
    application.status = 'approved'
    db.session.commit()
    return jsonify({'message': '申请已批准'})

@app.route('/api/entry-exit/<int:id>/reject', methods=['PUT'])
@jwt_required()
def reject_entry_exit_application(id):
    application = EntryExitApplication.query.get(id)
    application.status = 'rejected'
    db.session.commit()
    return jsonify({'message': '申请已拒绝'})

# 动态上报
@app.route('/api/dynamic-reports', methods=['GET'])
@jwt_required()
def get_dynamic_reports():
    user_id = get_jwt_identity()
    reports = DynamicReport.query.filter_by(user_id=user_id).order_by(DynamicReport.created_at.desc()).all()
    return jsonify([{
        'id': report.id,
        'content': report.content,
        'location': report.location,
        'created_at': report.created_at
    } for report in reports])

@app.route('/api/dynamic-reports/admin', methods=['GET'])
@jwt_required()
def get_all_dynamic_reports():
    reports = DynamicReport.query.order_by(DynamicReport.created_at.desc()).all()
    return jsonify([{
        'id': report.id,
        'user_id': report.user_id,
        'user_name': report.user.name,
        'content': report.content,
        'location': report.location,
        'created_at': report.created_at
    } for report in reports])

@app.route('/api/dynamic-reports', methods=['POST'])
@jwt_required()
def create_dynamic_report():
    user_id = get_jwt_identity()
    data = request.get_json()
    report = DynamicReport(
        user_id=user_id,
        content=data.get('content'),
        location=data.get('location')
    )
    db.session.add(report)
    db.session.commit()
    return jsonify({'message': '动态上报成功'})

# 医务室信息
@app.route('/api/medical-offices', methods=['GET'])
def get_medical_offices():
    offices = MedicalOffice.query.all()
    return jsonify([{
        'id': office.id,
        'name': office.name,
        'location': office.location,
        'contact': office.contact,
        'capacity': office.capacity,
        'available': office.available
    } for office in offices])

@app.route('/api/medical-offices', methods=['POST'])
@jwt_required()
def create_medical_office():
    data = request.get_json()
    office = MedicalOffice(
        name=data.get('name'),
        location=data.get('location'),
        contact=data.get('contact'),
        capacity=data.get('capacity'),
        available=data.get('available')
    )
    db.session.add(office)
    db.session.commit()
    return jsonify({'message': '医务室创建成功'})

@app.route('/api/medical-offices/<int:id>', methods=['PUT'])
@jwt_required()
def update_medical_office(id):
    office = MedicalOffice.query.get(id)
    data = request.get_json()
    office.name = data.get('name')
    office.location = data.get('location')
    office.contact = data.get('contact')
    office.capacity = data.get('capacity')
    office.available = data.get('available')
    db.session.commit()
    return jsonify({'message': '医务室更新成功'})

@app.route('/api/medical-offices/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_medical_office(id):
    office = MedicalOffice.query.get(id)
    db.session.delete(office)
    db.session.commit()
    return jsonify({'message': '医务室删除成功'})

# 医务室分配
@app.route('/api/medical-assignments', methods=['GET'])
@jwt_required()
def get_medical_assignments():
    user_id = get_jwt_identity()
    assignments = MedicalOfficeAssignment.query.filter_by(user_id=user_id).order_by(MedicalOfficeAssignment.created_at.desc()).all()
    return jsonify([{
        'id': assignment.id,
        'medical_office_id': assignment.medical_office_id,
        'medical_office_name': assignment.medical_office.name,
        'start_time': assignment.start_time,
        'end_time': assignment.end_time,
        'reason': assignment.reason,
        'status': assignment.status,
        'created_at': assignment.created_at
    } for assignment in assignments])

@app.route('/api/medical-assignments/admin', methods=['GET'])
@jwt_required()
def get_all_medical_assignments():
    assignments = MedicalOfficeAssignment.query.order_by(MedicalOfficeAssignment.created_at.desc()).all()
    return jsonify([{
        'id': assignment.id,
        'user_id': assignment.user_id,
        'user_name': assignment.user.name,
        'medical_office_id': assignment.medical_office_id,
        'medical_office_name': assignment.medical_office.name,
        'start_time': assignment.start_time,
        'end_time': assignment.end_time,
        'reason': assignment.reason,
        'status': assignment.status,
        'created_at': assignment.created_at
    } for assignment in assignments])

@app.route('/api/medical-assignments', methods=['POST'])
@jwt_required()
def create_medical_assignment():
    user_id = get_jwt_identity()
    data = request.get_json()
    assignment = MedicalOfficeAssignment(
        user_id=user_id,
        medical_office_id=data.get('medical_office_id'),
        start_time=datetime.strptime(data.get('start_time'), '%Y-%m-%d %H:%M:%S'),
        end_time=datetime.strptime(data.get('end_time'), '%Y-%m-%d %H:%M:%S'),
        reason=data.get('reason'),
        status='pending'
    )
    db.session.add(assignment)
    db.session.commit()
    return jsonify({'message': '申请提交成功'})

@app.route('/api/medical-assignments/<int:id>/approve', methods=['PUT'])
@jwt_required()
def approve_medical_assignment(id):
    assignment = MedicalOfficeAssignment.query.get(id)
    assignment.status = 'approved'
    # 更新医务室可用床位
    office = assignment.medical_office
    office.available -= 1
    db.session.commit()
    return jsonify({'message': '申请已批准'})

@app.route('/api/medical-assignments/<int:id>/reject', methods=['PUT'])
@jwt_required()
def reject_medical_assignment(id):
    assignment = MedicalOfficeAssignment.query.get(id)
    assignment.status = 'rejected'
    db.session.commit()
    return jsonify({'message': '申请已拒绝'})

# 数据分析
@app.route('/api/analytics/covid-trend', methods=['GET'])
def get_covid_trend():
    data = CovidData.query.order_by(CovidData.date).all()
    dates = [item.date.strftime('%Y-%m-%d') for item in data]
    confirmed = [item.confirmed for item in data]
    recovered = [item.recovered for item in data]
    deaths = [item.deaths for item in data]
    return jsonify({
        'dates': dates,
        'confirmed': confirmed,
        'recovered': recovered,
        'deaths': deaths
    })

@app.route('/api/analytics/health-status', methods=['GET'])
def get_health_status():
    reports = HealthReport.query.all()
    healthy = len([r for r in reports if r.health_status == 'healthy'])
    abnormal = len([r for r in reports if r.health_status == 'abnormal'])
    return jsonify({
        'healthy': healthy,
        'abnormal': abnormal
    })

@app.route('/api/analytics/entry-exit-stats', methods=['GET'])
def get_entry_exit_stats():
    applications = EntryExitApplication.query.all()
    pending = len([a for a in applications if a.status == 'pending'])
    approved = len([a for a in applications if a.status == 'approved'])
    rejected = len([a for a in applications if a.status == 'rejected'])
    return jsonify({
        'pending': pending,
        'approved': approved,
        'rejected': rejected
    })