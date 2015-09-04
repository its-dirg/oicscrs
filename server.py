#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os
from urllib.parse import parse_qsl

from oic.utils.client_management import CDB
from mako.lookup import TemplateLookup
from oic.utils.http_util import Response, NotFound

__author__ = 'rohe0002'

LOGGER = logging.getLogger("")
LOGFILE_NAME = 'oicscr.log'
hdlr = logging.FileHandler(LOGFILE_NAME)
base_formatter = logging.Formatter(
    "%(asctime)s %(name)s:%(levelname)s %(message)s")

CPC = ('%(asctime)s %(name)s:%(levelname)s '
       '[%(client)s,%(path)s,%(cid)s] %(message)s')
cpc_formatter = logging.Formatter(CPC)

hdlr.setFormatter(base_formatter)
LOGGER.addHandler(hdlr)
LOGGER.setLevel(logging.DEBUG)

CLIENT_DB = "client_db"


# ----------------------------------------------------------------------------

# noinspection PyUnusedLocal
def css(environ, start_response, session):
    try:
        _info = open(environ["PATH_INFO"]).read()
        resp = Response(_info)
    except (OSError, IOError):
        resp = NotFound(environ["PATH_INFO"])

    return resp(environ, start_response)


def static_file(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False


# noinspection PyUnresolvedReferences
def static(environ, start_response, path):
    LOGGER.info("[static]sending: %s" % (path,))

    try:
        text = open(path).read()
        if path.endswith(".ico"):
            start_response('200 OK', [('Content-Type', "image/x-icon")])
        elif path.endswith(".html"):
            start_response('200 OK', [('Content-Type', 'text/html')])
        elif path.endswith(".json"):
            start_response('200 OK', [('Content-Type', 'application/json')])
        elif path.endswith(".txt"):
            start_response('200 OK', [('Content-Type', 'text/plain')])
        elif path.endswith(".css"):
            start_response('200 OK', [('Content-Type', 'text/css')])
        else:
            start_response('200 OK', [('Content-Type', 'text/plain')])
        return [text]
    except IOError:
        resp = NotFound()
        return resp(environ, start_response)


# ----------------------------------------------------------------------------

LOOKUP = TemplateLookup(directories=['templates', 'htdocs'],
                        input_encoding='utf-8', output_encoding='utf-8')


# ----------------------------------------------------------------------------

def registration(environ, start_response):
    resp = Response(template_lookup=LOOKUP, mako_template="registration.mako")
    return resp(environ, start_response)


def generate_static_client_credentials(parameters):
    redirect_uris = parameters['redirect_uris']
    cdb = CDB(CLIENT_DB)
    static_client = cdb.create(redirect_uris=redirect_uris, policy_uri="example.com",
                               logo_uri="example.com")
    return static_client['client_id'], static_client['client_secret']


def application(environ, start_response):
    """
    :param environ: The HTTP application environment
    :param start_response: The application to run when the handling of the
        request is done
    :return: The response as a list of lines
    """
    path = environ.get('PATH_INFO', '').lstrip('/')
    query_params = dict(parse_qsl(environ.get("QUERY_STRING")))

    if path.startswith("static/"):
        return static(environ, start_response, path)
    elif path.startswith("_static/"):
        return static(environ, start_response, path)
    elif path == "":
        return registration(environ, start_response)
    elif path == "generate_client_credentials":
        client_id, client_secret = generate_static_client_credentials(query_params)
        resp = Response(json.dumps({"client_id": client_id, "client_secret": client_secret}),
                        headers=[('Content-Type', "application/json")])
        return resp(environ, start_response)


# ----------------------------------------------------------------------------

def bytes_middleware(application):
    def response_as_bytes(environ, start_response):
        resp = application(environ, start_response)

        # encode the data if necessary
        data = resp[0]
        if isinstance(data, str):
            data = data.encode("utf-8")
        return [data]

    return response_as_bytes

wsgi = bytes_middleware(application)
