from wintermute import APP
from flask import render_template


@APP.route('/')
def main():
    return render_template('index.html')
