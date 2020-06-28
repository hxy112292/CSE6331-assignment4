import os
import sqlite3
import numpy
import json

from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.errorhandler(404)
@app.route("/error404")
def page_not_found(error):
    return render_template('404.html', title='404')


@app.errorhandler(500)
@app.route("/error500")
def requests_error(error):
    return render_template('500.html', title='500')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_column_list():
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'quakes.db')
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute("select * from vc limit 1")
    fields = cursor.description
    column_list = []
    for field in fields:
        column = {'field': field[0], 'title': field[0], 'sortable': 'true'}
        column_list.append(column)
    # column = {'field': 'operate', 'title': 'Item Operate', 'clickToSelect': 'false', 'events': 'window.operateEvents',
    #           'formatter': 'operate'}
    # column_list.append(column)
    conn.commit()
    conn.close()
    return column_list


@app.route('/quake_num_mag', methods=['GET', 'POST'])
def quake_num_mag():
    data_list = []
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'quakes.db')
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    for i in numpy.arange(1, 7, 1):
        sql = "select count(*) from quakes where mag >= " + str(i) + " and mag <= " + str(i+1) + " and time " \
              "> (SELECT DATETIME('2020-06-11', '-2 day'))"
        cursor.execute(sql)
        data_list.append(cursor.fetchone()['count(*)'])
    conn.commit()
    conn.close()
    column_list = ["1-2", "2-3", "3-4", "4-5", "5-6", "6-7"]

    res = {"data_list": data_list, "column_list": column_list}
    return json.dumps(res)


@app.route('/quake_mag_depth', methods=['GET', 'POST'])
def quake_mag_depth():
    sql = "select mag as x, depth as y from quakes order by time desc limit 100"
    db = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'quakes.db')
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(sql)
    data_list = cursor.fetchall()
    conn.commit()
    conn.close()
    column_list = ["mag", "depth"]

    res = {"data_list": data_list, "column_list": column_list}
    return json.dumps(res)


port = int(os.getenv('PORT', '5002'))
app.run(host='0.0.0.0', port=port)