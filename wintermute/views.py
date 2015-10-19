from wintermute import APP
from flask import render_template
from flask import jsonify
from wintermute.ipam import IPNetwork


@APP.route('/')
def main():
    return render_template('index.html')


@APP.route('/api/helloworld/<network>/<mask>')
def helloworld(network='10.0.0.0', mask='/8'):
    prefix = network + "/" + mask
    x = IPNetwork(prefix, create=True)
    return jsonify({x.ip_network: None})
