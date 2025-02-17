#!/usr/bin/env python3
from argparse import ArgumentParser
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template
from controller.main_controller import cb

app = Flask(__name__)
app.register_blueprint(cb)

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    try:
        arg_parser = ArgumentParser(
            usage='Usage: python ' + __file__ + ' [--port ] [--help]'
        )
        arg_parser.add_argument('-p', '--port', default=12020, help='port')
        arg_parser.add_argument('-d', '--debug', default=False, help='debug')
        options = arg_parser.parse_args()
        app.run(debug=options.debug, port=options.port, threaded=True) 
        # When 'Ctrl+C' is pressed, the program destroy() will be executed.
    except KeyboardInterrupt:
        print('Ctrl+Cで終了')
