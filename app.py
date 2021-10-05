from flask import Flask, render_template, jsonify, request
from bson.objectid import ObjectId

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.seongil


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/memo', methods=['GET'])
def listing():
    memos = list(db.memos.find({}))
    for m in memos:
        mongo_id = m['_id']
        m['_id'] = str(mongo_id)
    return jsonify({'all_memos': memos})


@app.route('/memo', methods=['POST'])
def saving():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']

    doc = {
        'title': title_receive,
        'content': content_receive,
    }

    memo = db.memos.insert_one(doc)
    return jsonify({'msg': '저장이 완료되었습니다!'})


@app.route('/memo/edit', methods=['POST'])
def edit():
    memo_id = ObjectId(request.form['memo_id'])
    newtitle = request.form['title_give']
    newcontent = request.form['content_give']
    print(db.memos.find_one({'_id': memo_id}))
    db.memos.update_one({'_id': memo_id}, {'$set': {'title': newtitle, 'content': newcontent}})
    return jsonify({'msg': '수정이 완료되었습니다!'})


@app.route('/memo/delete', methods=['POST'])
def delete():
    memo_id = ObjectId(request.form['memo_id'])
    print(memo_id)
    db.memos.delete_one({'_id': memo_id})
    return jsonify({'msg': '삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)