#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
import sys
from exceptions import Exception
from exceptions import OSError
from exceptions import KeyboardInterrupt

from beaker.middleware import SessionMiddleware
from dirg_util.http_util import HttpHandler
from oic.utils.http_util import *
from oic.utils.client_management import CDB

from response_encoder import ResponseEncoder

__author__ = 'rohe0002'

from mako.lookup import TemplateLookup

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

URLMAP = {}
NAME = "oicscr"
OAS = None

HEADER = "---------- %s ----------"

# ----------------------------------------------------------------------------

#noinspection PyUnusedLocal
def css(environ, start_response, session):
    try:
        _info = open(environ["PATH_INFO"]).read()
        resp = Response(_info)
    except (OSError, IOError):
        resp = NotFound(environ["PATH_INFO"])

    return resp(environ, start_response)

# ----------------------------------------------------------------------------

def wsgi_wrapper(environ, start_response, func, session, trace):
    kwargs = extract_from_request(environ)
    trace.request(kwargs["request"])
    args = func(**kwargs)

    try:
        resp, state = args
        trace.reply(resp.message)
        return resp(environ, start_response)
    except TypeError:
        resp = args
        trace.reply(resp.message)
        return resp(environ, start_response)
    except Exception as err:
        LOGGER.error("%s" % err)
        trace.error("%s" % err)
        raise

# ----------------------------------------------------------------------------

def static_file(path):
    try:
        os.stat(path)
        return True
    except OSError:
        return False

#noinspection PyUnresolvedReferences
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

URLS = [
    (r'.+\.css$', css),
]

# ----------------------------------------------------------------------------

ROOT = './'

LOOKUP = TemplateLookup(directories=[ROOT + 'templates', ROOT + 'htdocs'],
                        module_directory=ROOT + 'modules',
                        input_encoding='utf-8', output_encoding='utf-8')

# ----------------------------------------------------------------------------

def registration(environ, start_response):
    resp = Response(mako_template="registration.mako",
                    template_lookup=LOOKUP,
                    headers=[])
    return resp(environ, start_response)

def generate_static_client_credentials(parameters):
    redirect_uris = parameters['redirect_uris']
    cdb = CDB(config.CLIENT_DB)
    static_client = cdb.create(redirect_uris=redirect_uris, policy_uri="example.com",logo_uri="example.com")
    return static_client['client_id'], static_client['client_secret']


def application(environ, start_response):
    """
    :param environ: The HTTP application environment
    :param start_response: The application to run when the handling of the
        request is done
    :return: The response as a list of lines
    """
    global OAS
    session = environ['beaker.session']
    path = environ.get('PATH_INFO', '').lstrip('/')
    http_helper = HttpHandler(environ, start_response, session, LOGGER)
    response_encoder = ResponseEncoder(environ=environ, start_response=start_response)
    parameters = http_helper.query_dict()

    if path == "robots.txt":
        return static(environ, start_response, "static/robots.txt")

    if path.startswith("static/"):
        return static(environ, start_response, path)
    elif path.startswith("_static/"):
        return static(environ, start_response, path)


    elif path == "":
        return registration(environ, start_response)
    elif path == "generate_client_credentials":
        client_id, client_secret = generate_static_client_credentials(parameters)
        return response_encoder.returnJSON(json.dumps({"client_id": client_id, "client_secret": client_secret}))



# ----------------------------------------------------------------------------


if __name__ == '__main__':
    import argparse
    import importlib
    from cherrypy import wsgiserver
    from cherrypy.wsgiserver import ssl_pyopenssl

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', dest='port', default=80, type=int)
    parser.add_argument(dest="config")
    args = parser.parse_args()

    session_opts = {
        'session.type': 'memory',
        'session.cookie_expires': True,
        'session.auto': True,
        'session.timeout': 900
    }

    sys.path.insert(0, ".")
    config = importlib.import_module(args.config)

    # Setup the web server
    SRV = wsgiserver.CherryPyWSGIServer(('0.0.0.0', args.port),
                                        SessionMiddleware(application,
                                                          session_opts))
    https = ""
    if config.baseurl.startswith("https"):
        https = " using HTTPS"
        SRV.ssl_adapter = ssl_pyopenssl.pyOpenSSLAdapter(
            config.SERVER_CERT, config.SERVER_KEY, config.CERT_CHAIN)

    LOGGER.info("OC server starting listening on port:%s%s" % (args.port,
                                                               https))
    print "OC server starting listening on port:%s%s" % (args.port, https)
    try:
        SRV.start()
    except KeyboardInterrupt:
        SRV.stop()
