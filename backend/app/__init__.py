from flask import Flask, request, jsonify
from config import get_db_connection
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route('/')
def home():
    conn = get_db_connection()
    conn.close()
    return 'Bienvenido a greenGo'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password_hash = data['password_hash']
    hashed_password = generate_password_hash(password_hash)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING user_id", (name, email, hashed_password))
        user_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Usuario registrado con éxito', 'user_id': user_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/plant_tree', methods=['POST'])
def plant_tree():
    data = request.form
    user_id = data['user_id']
    location = data['location']
    photo_before = data['photo_before'].read()
    photo_during = data['photo_during'].read()
    photo_after = data['photo_after'].read()

    tree_type = data['tree_type']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO planted_trees (user_id, location, photo_before, photo_during, photo_after, tree_type) VALUES (%s, %s, %s, %s, %s, %s) RETURNING tree_id", (user_id, location, photo_before, photo_during, photo_after, tree_type))
        tree_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Árbol plantado con éxito', 'arbol_id': tree_id }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/missions', methods=['GET'])
def get_missions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM missions")
        missions = cursor.fetchall()
        cursor.close()
        conn.close()

        mission_list = []
        for mission in missions:
            mission_dict = {
                'mission_id': mission[0],
                'description': mission[1],
                'points': mission[2],
                'date': mission[3].strftime('%Y-%m-%d')
            }
            mission_list.append(mission_dict)

        return jsonify(mission_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def create_app():
    return app