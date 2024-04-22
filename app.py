from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Process
from main import main
from db import Match, DatabaseHandler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/football_matches'
db = SQLAlchemy(app)
db_handler = DatabaseHandler(app.config['SQLALCHEMY_DATABASE_URI'])
parser_process = Process()


def run_parser(date):
    main(date=date)


@app.route('/', methods=['GET', 'POST'])
def index():
    global parser_process
    if request.method == 'POST':
        action = request.form['action']
        if action == 'start':
            date = int(request.form['date'])
            if -7 <= date <= 7 and (parser_process is None or not parser_process.is_alive()):
                parser_process = Process(target=run_parser, args=(date,))
                parser_process.start()
        elif action == 'stop':
            if parser_process and parser_process.is_alive():
                parser_process.terminate()
                parser_process.join()  # Wait for the process to terminate
                parser_process = None
    matches = db_handler.get_records_by_user_id(Match)
    return render_template('index.html', matches=matches, parser_running=parser_process and parser_process.is_alive())


if __name__ == '__main__':
    app.run(debug=True)
