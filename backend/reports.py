# reports.py
from flask import Blueprint, jsonify
from sqlalchemy import text
from app import db

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')

@reports_bp.route('/shipments/today')
def get_today_shipments():
    try:
        rows = db.session.execute(text("SELECT * FROM v_shipments_today"))
        return jsonify([dict(r) for r in rows])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
