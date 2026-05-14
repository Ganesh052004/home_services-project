# ============================================================
# HomeFixr Backend — app.py
# Python Flask + MySQL (XAMPP MySQL only)
#
# HOW TO RUN:
#   1. Start XAMPP → only start MySQL (Apache NOT needed)
#   2. Open phpMyAdmin → run database_setup.sql
#   3. Open CMD → cd to this folder → python app.py
#   4. Open browser → http://localhost:5000
# ============================================================

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'homefixr'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ---- Serve HTML pages ----
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory('.', filename)

# ---- Register Worker ----
@app.route('/api/register_worker', methods=['POST'])
def register_worker():
    try:
        data = request.get_json()
        name       = data.get('name','').strip()
        phone      = data.get('phone','').strip()
        email      = data.get('email','').strip()
        category   = data.get('category','').strip()
        city       = data.get('city','').strip()
        experience = data.get('experience', 0)
        rate       = data.get('rate', 0)
        about      = data.get('about','').strip()
        if not all([name, phone, category, city, experience, rate]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workers (name, phone, email, category, city, experience, rate, about, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (name, phone, email, category, city, int(experience), int(rate), about, datetime.now()))
        conn.commit()
        wid = cursor.lastrowid
        cursor.close(); conn.close()
        return jsonify({'success': True, 'worker_id': wid})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ---- Search Workers ----
@app.route('/api/workers', methods=['GET'])
def get_workers():
    try:
        category = request.args.get('category','').strip()
        city     = request.args.get('city','').strip()
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM workers WHERE 1=1"
        params = []
        if category:
            query += " AND category = %s"; params.append(category)
        if city:
            query += " AND city LIKE %s"; params.append(f'%{city}%')
        query += " ORDER BY created_at DESC"
        cursor.execute(query, params)
        workers = cursor.fetchall()
        cursor.close(); conn.close()
        for w in workers:
            if w.get('created_at'): w['created_at'] = str(w['created_at'])
        return jsonify(workers)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ---- Book Service ----
@app.route('/api/book_service', methods=['POST'])
def book_service():
    try:
        data = request.get_json()
        cust_name        = data.get('cust_name','').strip()
        cust_phone       = data.get('cust_phone','').strip()
        cust_address     = data.get('cust_address','').strip()
        service_category = data.get('service_category','').strip()
        worker_name      = data.get('worker_name','').strip()
        booking_date     = data.get('booking_date','')
        booking_time     = data.get('booking_time','')
        description      = data.get('description','').strip()
        if not all([cust_name, cust_phone, cust_address, service_category, booking_date, booking_time, description]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (cust_name, cust_phone, cust_address, service_category,
              worker_name, booking_date, booking_time, description, status, created_at)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (cust_name, cust_phone, cust_address, service_category, worker_name,
              booking_date, booking_time, description, 'Pending', datetime.now()))
        conn.commit()
        bid = cursor.lastrowid
        cursor.close(); conn.close()
        return jsonify({'success': True, 'booking_id': bid})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ---- All Bookings ----
@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")
        bookings = cursor.fetchall()
        cursor.close(); conn.close()
        for b in bookings:
            for k in ['booking_date','created_at']:
                if b.get(k): b[k] = str(b[k])
        return jsonify(bookings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("")
    print("=" * 55)
    print("  HomeFixr is running!")
    print("  Open browser -> go to:  http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, port=5000)
