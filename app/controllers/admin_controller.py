# app/controllers/admin_controller.py
from flask_login import login_required
from app import app
from flask import render_template, jsonify
from app.models.user_model import Users
from datetime import datetime, timedelta
from sqlalchemy import func

@app.route('/admin/stats')
@login_required
def admin_stats():
    # Obtener fecha actual y hace un mes
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    # Todos los usuarios
    users = Users.query.all()
    
    # Consultar usuarios registrados en el último mes
    users_last_month = Users.query.filter(Users.registered_on.between(start_date, end_date)).count()

    # Consultar total de usuarios
    total_users = Users.query.count()

    # Consultar usuarios activos (supongamos que tienes un campo "active" en el modelo User)
    active_users = Users.query.filter_by(active=True).count()
    
    print(users_last_month)
    print(total_users)
    print(active_users)

    return render_template('admin/stats.html', users=users, users_last_month=users_last_month, total_users=total_users, active_users=active_users)
