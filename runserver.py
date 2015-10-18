import os
from wintermute import APP


def runserver():
    port = int(os.environ.get('PORT', 5000))
    APP.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    runserver()
