from app import app, db
import flask
from db_setup import init_db
from flask import Flask, render_template, request
import socket
from db_creator import Lottery
from sqlalchemy import or_, asc, func
from datetime import datetime
import json

init_db()

@app.route('/')
def run():
    #lottery = Lottery(name = 'test3', series = 'script 3', date = datetime.utcnow())
    #db.session.add(lottery)
    #db.session.commit()
    #query = db.session.query(Lottery)
    #q = query.all()
    return render_template('index.html')

@app.route('/result/<lottery_id>')
def result(lottery_id):
    query = db.session.query(Lottery).filter(Lottery.id.__eq__(lottery_id))
    return render_template('result_view.html', lottery=query.first())


@app.route('/page', methods = ['GET', 'POST'])
def paginate():
    search_value = request.form['search[value]']

    query = db.session.query(Lottery)
    total_count = query.count()

    if 'date' in request.form:
        date = request.form['date']
        if date.__len__() != 0:
            query = query.filter(Lottery.date.like(date))

    if search_value.__len__() != 0:
        query = query.filter(or_(Lottery.name.contains(search_value),
                                Lottery.series.contains(search_value)))
    filtered_count = query.count()

    if request.form['order[0][column]'] == '0':
        order_column = Lottery.date
    if request.form['order[0][column]'] == '1':
        order_column = Lottery.name
    if request.form['order[0][column]'] == '2':
        order_column = Lottery.series

    if request.form['order[0][dir]'] == 'asc':
        order_column = order_column.asc()
    else:
        order_column = order_column.desc()

    query = query.order_by(order_column)

    length = int(request.form['length'])
    start = int(request.form['start'])
    query = query.paginate(page=(start/length)+1, per_page=length, error_out=False, max_per_page=None)
    #print request.form
    result_dict = []
    for q in query.items:
        result_dict.append([q.date, q.name, q.series, q.id])
    data = {'draw': int(request.form['draw']),
            'recordsTotal': total_count,
            'recordsFiltered': filtered_count,
            'data': result_dict}

    return flask.jsonify(data)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def not_found(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = 8080
    sock.close()
    app.run(port=port)

if __name__ == '__main__':
    app.run()
