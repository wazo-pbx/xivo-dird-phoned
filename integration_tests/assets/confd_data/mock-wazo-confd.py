# -*-coding: utf-8-*-
# Copyright 2016-2020 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

port = int(sys.argv[1])

API_VERSION = '1.1'

extensions_features_data = {
    'items': [
        {'feature': 'phoneprogfunckey', 'exten': '_*735.'},
        {'feature': 'enablednd', 'exten': '*25'},
        {'feature': 'fwdunc', 'exten': '_*21.'},
        {'feature': 'fwdrna', 'exten': '_*22.'},
        {'feature': 'fwdbusy', 'exten': '_*23.'},
        {'feature': 'incallfilter', 'exten': '*27'},
    ],
}

user_lines = {
    '123': [{'endpoint_sip': {'name': 'line-123'}}],
    '123-sccp': [{'endpoit_sccp': {'name': 'line-123-sccp'}}],
}

devices = {
    'device-yealink': {'vendor': 'yealink'},
    'device-cisco': {'vendor': 'cisco'},
    'device-unknown-vendor': {'vendor': 'unknown-vendor'},
    'device-empty-vendor': {'vendor': ''},
}

_requests = []


@app.before_request
def log_request():
    global _requests

    if request.path.startswith('/_'):
        return

    log = {
        'method': request.method,
        'path': request.path,
        'query': request.args.items(multi=True),
        'body': request.data,
        'json': request.json,
        'headers': dict(request.headers),
    }
    _requests.append(log)


@app.route('/_requests', methods=['GET'])
def list_requests():
    return jsonify({'requests': _requests})


@app.route('/_reset', methods=['POST'])
def reset_requests():
    global _requests
    _requests = []
    return '', 204


@app.route('/{}/extensions/features'.format(API_VERSION), methods=['GET'])
def extensions_features():
    return jsonify(extensions_features_data)


@app.route('/{}/users/<user_uuid>'.format(API_VERSION), methods=['GET'])
def user_uuid_get(user_uuid):
    return jsonify(
        {'id': user_uuid, 'uuid': user_uuid, 'lines': user_lines.get(user_uuid)}
    )


@app.route(
    '/{}/users/<user_uuid>/services/<service_name>'.format(API_VERSION), methods=['PUT']
)
def user_service_put(user_uuid, service_name):
    return '', 204


@app.route('/{}/lines'.format(API_VERSION), methods=['GET'])
def lines_get():
    search = request.args.get('search', None)
    body = None
    if search != 'no-result':
        body = {
            'items': [
                {
                    'id': 0,
                    'name': search,
                    'endpoint_sip': {'id': 0, 'name': search, 'username': search},
                    'device_id': 'device-{}'.format(search),
                }
            ],
            'total': 1,
        }
    else:
        body = {
            'items': [],
            'total': 0,
        }

    return jsonify(body)


@app.route('/{}/devices/<device_name>'.format(API_VERSION), methods=['GET'])
def device_get(device_name):
    if device_name in devices:
        return jsonify(devices[device_name])
    else:
        return '', 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port, debug=True)
