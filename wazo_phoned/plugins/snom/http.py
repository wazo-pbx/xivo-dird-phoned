# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from wazo_phoned.plugin_helpers.client.http import ClientInput, ClientLookup


class Input(ClientInput):
    content_type = 'text/xml; charset=utf-8'
    template = 'snom_input.jinja'


class Lookup(ClientLookup):
    content_type = 'text/xml; charset=utf-8'
    template = 'snom_results.jinja'
