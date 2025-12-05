from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import logging
import json
import secrets
import datetime
try:
    import jwt
except Exception:
    jwt = None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')
JWT_EXP_DELTA_SECONDS = 60 * 60 * 24 * 7

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

@app.before_request
def handle_options():
    if request.method == 'OPTIONS':
        resp = app.make_response(('', 204))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return resp

db = SQLAlchemy(app)

logging.basicConfig(level=logging.DEBUG)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    saved_co = db.Column(db.Integer, default=0)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return jsonify({'message': 'Authentication required'}), 401
        user = User.query.filter_by(email=auth.username).first()
        if not user or not check_password_hash(user.password, auth.password):
            return jsonify({'message': 'Invalid credentials'}), 401
        g.user = user
        return f(*args, **kwargs)
    return decorated_function

def create_token_for_user(user: User):
    if jwt is None:
        raise RuntimeError('PyJWT is required for token creation')
    payload = {
        'sub': user.id,
        'name': user.name,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if jwt is None:
            return jsonify({'message': 'Server misconfiguration: JWT library not installed'}), 500
        auth_header = request.headers.get('Authorization', '')
        logging.debug(f"Authorization header received: {auth_header}")
        token = None
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1].strip()

        if not token:
            try:
                body = request.get_json(silent=True) or {}
            except Exception:
                body = {}
            user_name = body.get('user_name') if isinstance(body, dict) else None
            if user_name:
                logging.debug(f"Fallback auth using user_name: {user_name}")
                user = User.query.filter_by(name=user_name).first()
                if not user:
                    # create a local user placeholder if it doesn't exist
                    user = User(name=user_name, email=f"{user_name}@local", password=generate_password_hash('default'))
                    db.session.add(user)
                    db.session.commit()
                g.user = user
                # proceed without JWT
            else:
                return jsonify({'message': 'Authorization token required'}), 401
        else:
            try:
                data = jwt.decode(token, app.secret_key, algorithms=['HS256'])
                user_id = data.get('sub')
                user = User.query.get(user_id)
                if not user:
                    return jsonify({'message': 'Invalid token user'}), 401
                g.user = user
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expired'}), 401
            except Exception as e:
                logging.exception('JWT decode failed')
                try:
                    body = request.get_json(silent=True) or {}
                except Exception:
                    body = {}
                user_name = body.get('user_name') if isinstance(body, dict) else None
                if user_name:
                    logging.debug(f"Fallback auth after decode failure using user_name: {user_name}")
                    user = User.query.filter_by(name=user_name).first()
                    if not user:
                        user = User(name=user_name, email=f"{user_name}@local", password=generate_password_hash('default'))
                        db.session.add(user)
                        db.session.commit()
                    g.user = user
                else:
                    print(e)
                    return jsonify({'message': 'Invalid token'}), 401
        return f(*args, **kwargs)
    return decorated

# Read missions from points.json using explicit UTF-8 to avoid encoding issues on Windows
try:
    with open('points.json', 'r', encoding='utf-8', errors='replace') as f:
        missions = json.load(f).get('missions', [])
except Exception:
    logging.exception('Failed to load points.json with utf-8, falling back to default open')
    with open('points.json', 'r') as f:
        missions = json.load(f).get('missions', [])


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    invite_link = db.Column(db.String(120), unique=True, nullable=False)
    cached_score = db.Column(db.Integer, default=0)
    members = db.relationship('User', backref='team', lazy=True)


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    co2_reduction = db.Column(db.Integer, default=0)


class MissionCompletion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    __table_args__ = (
        db.UniqueConstraint('team_id', 'mission_id', name='uix_team_mission'),
        db.UniqueConstraint('user_id', 'mission_id', name='uix_user_mission'),
    )


def serialize_mission(m: Mission):
    return { 'id': m.id, 'name': m.name, 'description': m.description, 'co2_reduction': m.co2_reduction }


def serialize_team(team: Team):
    return {
        'id': team.id,
        'name': team.name,
        'inviteLink': team.invite_link,
        'teamScore': sum([m.saved_co or 0 for m in team.members]),
        'members': [{'name': m.name, 'score': m.saved_co or 0, 'avatar': ''} for m in sorted(team.members, key=lambda x: x.saved_co or 0, reverse=True)]
    }


try:
    with app.app_context():
        db.create_all()
        try:
            import sqlite3
            conn = sqlite3.connect('data.db')
            cur = conn.cursor()
            cur.execute("PRAGMA table_info('user')")
            cols = [r[1] for r in cur.fetchall()]
            if 'saved_co' not in cols:
                cur.execute("ALTER TABLE user ADD COLUMN saved_co INTEGER DEFAULT 0")
                conn.commit()
            conn.close()
        except Exception:
            logging.exception('Migration check failed')
        try:
            existing = {m.id for m in Mission.query.all()}
            for mm in missions:
                mid = mm.get('id')
                if mid in existing:
                    mobj = Mission.query.get(mid)
                    mobj.name = mm.get('name')
                    mobj.description = mm.get('description')
                    mobj.co2_reduction = mm.get('co2_reduction')
                else:
                    mobj = Mission(id=mid, name=mm.get('name'), description=mm.get('description'), co2_reduction=mm.get('co2_reduction'))
                    db.session.add(mobj)
            db.session.commit()
        except Exception:
            logging.exception('Failed to sync missions from points.json')
except Exception:
    logging.exception('Auto migration failed on import')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        if not data or not data.get('name') or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing fields'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'User already exists'}), 400
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        token = create_token_for_user(new_user)
        return jsonify({'message': 'User registered successfully', 'token': token, 'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email}}), 201
    except Exception as e:
        logging.exception("Error in /register endpoint")
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': 'Missing fields'}), 400
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        token = create_token_for_user(user)
        return jsonify({'message': 'Login successful', 'token': token, 'user': {'id': user.id, 'name': user.name, 'email': user.email}}), 200
    except Exception as e:
        logging.exception('Error in /login')
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

@app.route('/add-user', methods=['POST'])
@jwt_required
def add_user():
    data = request.json
    if not data or not data.get('email') or not data.get('name'):
        return jsonify({'message': 'Missing fields'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User already exists'}), 400
    new_user = User(name=data['name'], email=data['email'], password=generate_password_hash('default', method='pbkdf2:sha256'), team_id=g.user.id)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added to team'}), 201

@app.route('/users', methods=['GET'])
@jwt_required
def get_users():
    if not g.user.team:
        return jsonify([])
    members = g.user.team.members
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'saved_co': u.saved_co} for u in members])


@app.route('/api/user/name/<string:name>', methods=['GET'])
def get_user_by_name(name):
    user = User.query.filter_by(name=name).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    resp = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'saved_co': user.saved_co
    }
    if user.team:
        resp['team'] = serialize_team(user.team)
    else:
        resp['team'] = None
    return jsonify(resp), 200


@app.route('/api/tribe/create', methods=['POST'])
def api_create_tribe():
    try:
        data = request.json
        owner_name = data.get('owner_name')
        tribe_name = data.get('name')
        if not owner_name or not tribe_name:
            return jsonify({'message': 'Missing fields'}), 400
        owner = User.query.filter_by(name=owner_name).first()
        if not owner:
            owner = User(name=owner_name, email=f"{owner_name}@local", password=generate_password_hash('default'))
            db.session.add(owner)
            db.session.commit()

        invite = secrets.token_urlsafe(6)
        while Team.query.filter_by(invite_link=invite).first():
            invite = secrets.token_urlsafe(6)

        team = Team(name=tribe_name, invite_link=invite)
        db.session.add(team)
        db.session.commit()

        owner.team_id = team.id
        db.session.add(owner)
        db.session.commit()

        return jsonify(serialize_team(team)), 201
    except Exception as e:
        logging.exception('Error in /api/tribe/create')
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


@app.route('/api/tribe/join', methods=['POST'])
def api_join_tribe():
    try:
        data = request.json
        invite = data.get('invite')
        user_name = data.get('user_name')
        if not invite or not user_name:
            return jsonify({'message': 'Missing fields'}), 400
        team = Team.query.filter_by(invite_link=invite).first()
        if not team:
            return jsonify({'message': 'Invalid invite code'}), 404
        user = User.query.filter_by(name=user_name).first()
        if not user:
            user = User(name=user_name, email=f"{user_name}@local", password=generate_password_hash('default'))
            db.session.add(user)
            db.session.commit()

        user.team_id = team.id
        db.session.add(user)
        db.session.commit()

        return jsonify(serialize_team(team)), 200
    except Exception as e:
        logging.exception('Error in /api/tribe/join')
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


@app.route('/api/tribe/<string:invite>', methods=['GET'])
def api_get_tribe(invite):
    team = Team.query.filter_by(invite_link=invite).first()
    if not team:
        return jsonify({'message': 'Tribe not found'}), 404
    return jsonify(serialize_team(team)), 200


@app.route('/missions', methods=['GET'])
def get_missions():
    db_missions = Mission.query.order_by(Mission.id).all()
    return jsonify([serialize_mission(m) for m in db_missions]), 200


@app.route('/missions/<int:mission_id>/complete', methods=['POST'])
@jwt_required
def complete_mission(mission_id):
    mission = Mission.query.get(mission_id)
    if not mission:
        return jsonify({'message': 'Mission not found'}), 404
    try:
        if not hasattr(g, 'user') or g.user is None:
            logging.debug(f"complete_mission: g has attributes: {dir(g)}")
            return jsonify({'message': 'No authenticated user (g.user missing)'}), 401
        logging.debug(f"complete_mission: g.user type={type(g.user)} repr={repr(g.user)}")

        # Determine if team completion should be checked
        team_id = g.user.team_id
        # If user belongs to a team ensure the team hasn't already completed this mission
        if team_id:
            existing = MissionCompletion.query.filter_by(team_id=team_id, mission_id=mission_id).first()
            if existing:
                return jsonify({'message': 'This mission has already been completed by your team.'}), 400
            # record team completion
            completion = MissionCompletion(mission_id=mission_id, team_id=team_id, user_id=g.user.id)
            db.session.add(completion)
        else:
            # No team: ensure the user hasn't already completed this mission
            existing = MissionCompletion.query.filter_by(user_id=g.user.id, mission_id=mission_id).first()
            if existing:
                return jsonify({'message': 'You have already completed this mission.'}), 400
            completion = MissionCompletion(mission_id=mission_id, user_id=g.user.id)
            db.session.add(completion)

        # Update user's saved CO2 and persist
        g.user.saved_co = (g.user.saved_co or 0) + (mission.co2_reduction or 0)
        db.session.add(g.user)
        db.session.commit()

        team_payload = serialize_team(g.user.team) if g.user.team else None
        return jsonify({'message': f'Mission {mission_id} completed!', 'saved_co': g.user.saved_co, 'team': team_payload}), 200
    except Exception as e:
        logging.exception('Error completing mission')
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

@app.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    try:
        users = User.query.order_by(User.saved_co.desc()).limit(10).all()
        return jsonify([{'name': u.name, 'saved_co': u.saved_co} for u in users]), 200
    except Exception as e:
        logging.exception('Error fetching leaderboard')
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        try:
            res = db.session.execute("PRAGMA table_info('user')").fetchall()
            cols = [r[1] for r in res]
            if 'saved_co' not in cols:
                db.session.execute("ALTER TABLE user ADD COLUMN saved_co INTEGER DEFAULT 0")
                db.session.commit()
        except Exception:
            logging.exception('Migration check failed')
    app.run(debug=True)

