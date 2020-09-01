from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('obo_project.html')


@app.route('/makver')
def makver():
    return render_template('obo_project(makver).html')


@app.route('/searchver')
def searchver():
    return render_template('obo_project(searchver).html')


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
        'lecture_image' : lecture_image_receive,
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


@app.route('/shownewroom', methods=['GET'])
def show_new_room():
    return render_template('obo_project.html')
    result = list(db.lectures.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
