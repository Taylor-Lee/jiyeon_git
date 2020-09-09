from bson import ObjectId
from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

# from flask.ext.sqlalchemy import SQLAlchemy
userDB = SQLAlchemy()

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)
# db가 두 개 별개로 존재 할 수 있는지 확인 필요 / python 파일을 두 개 만들어야 하는지

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('obo_project.html')


@app.route('/makver')
def makver():
    return render_template('obo_project(makver)2.html')


@app.route('/searchver')
def searchver():
    return render_template('obo_project(searchver).html')


# @app.route('/login')
# def login():
#     return render_template('obo_project_login.html')


# @app.route('/loginver', methods=['GET', 'POST'])
# def loginver():
#     if request.method == 'GET':
#         return render_template('/login')
#     else:
#         name = request.form['name']
#         password = request.form['password']
#         try:
#             data = userinfo.query.filter_by(name=name, password=password).first()
#             if data is not None:
#                 session['logged_in'] = True
#                 return redirect(url_for('/'))
#             else:
#                 return 'Dont Login'
#         except:
#             return "Dont Login"
#
#
# @app.route('/logoutver')
# def logout():
#     # """Logout Form"""
#     session['logged_in'] = False
#     return redirect(url_for('/'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('obo_project_register.html')
    else:
        name_receive = request.form['name_give']
        password_receive = request.form['password_give']
        email_address_receive = request.form['email_address_give']
        userinfo = {
            'name': name_receive,
            'password': password_receive,
            'email_address': email_address_receive
        }

    if not ('name' and 'password' and 'email_address'):
        return render_template('/register')
    db.userinfo.insert_one(userinfo)

    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'all_userinfo': 'userinfo', 'msg': '정상적으로 아이디가 생성되었습니다!'})


@app.route('/makenewroom', methods=['POST'])
def make_new_room():
    # lecture_name (강의 제목)
    lecture_name_receive = request.form['lecture_name_give']
    # lecturer_name (강사 성함)
    lecturer_name_receive = request.form['lecturer_name_give']
    # lecture_image (강의 이미지)
    lecture_image_receive = request.form['lecture_image_give']
    # lecture_category (카테고리)
    lecture_category_receive = request.form['lecture_category_give']
    # mate_number (희망 수강 인원)
    mate_number_receive = request.form['mate_number_give']
    # lecture_link (강의 링크)
    lecture_link_receive = request.form['lecture_link_give']
    # owner_short_comment (방지기 한마디)
    owner_short_comment_receive = request.form['owner_short_comment_give']
    # owner_long_comment (소개 및 다짐글)
    owner_long_comment_receive = request.form['owner_long_comment_give']

    # DB에 삽입할 lectures 만들기
    lectures = {
        'lecture_name': lecture_name_receive,
        'lecturer_name': lecturer_name_receive,
        'lecture_image': lecture_image_receive,
        'lecture_category': lecture_category_receive,
        'mate_number': mate_number_receive,
        'lecture_link': lecture_link_receive,
        'owner_short_comment': owner_short_comment_receive,
        'owner_long_comment': owner_long_comment_receive
    }

    db.lectures.insert_one(lectures)
    lectures = list(db.lectures.find({'_id': False}))
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'all_lectures': 'lectures', 'msg': '방이 성공적으로 생성되었습니다!'})


@app.route('/enternewroom', methods=['POST'])
def enter_new_room():
    # purchase_proof_picture (구매 내역 인증 사진)
    purchase_proof_receive = request.form['purchase_proof_give']
    # participant_long_comment (참여자 한 마디)
    participant_long_comment_receive = request.form['participant_long_comment_give']

    # DB에 삽입할 participant_data 만들기
    participant_data = {
        'purchase_proof': purchase_proof_receive,
        'participant_long_comment': participant_long_comment_receive
    }

    room = db.lectures.find_one({"_id": ObjectId("5f4e3604f0fcaf7731a4a797")})
    if room["participants"] is None:
        room["participants"] = [ participant_data ]
    else:
        room["participants"].append(participant_data)

    db.lectures.update_one({"_id": ObjectId("5f4e3604f0fcaf7731a4a797")}, {"$push": {"participants": participant_data}})

    # db.participant.insert_one(participant_data)
    # lectures = list(db.participant_data.find({'_id': False}))
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'all_participant_data': 'participant_data', 'msg': '성공적으로 신청되었습니다!'})


@app.route('/shownewroom', methods=['GET'])
def show_new_room():
    # return render_template('obo_project.html')
    result = list(db.lectures.find({}))
    for room in result:
        room['_id'] = str(room['_id'])

    return jsonify({'result': 'success', 'lectures': result})

@app.route('/show_each_room', methods=['GET'])
def show_each_room():
    room_id = request.args.get('room_id')

    result = list(db.lectures.find({"_id": ObjectId(room_id)}))
    for room in result:
        room['_id'] = str(room['_id'])

    return jsonify({'result': 'success', 'lecture': result[0]})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
