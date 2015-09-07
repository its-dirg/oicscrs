#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import os

from oic.utils.client_management import CDB
from mako.lookup import TemplateLookup
from oic.utils.http_util import Response, NotFound, get_post

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

LOOKUP = TemplateLookup(directories=['templates', 'htdocs'],
                        input_encoding='utf-8', output_encoding='utf-8')


def registration(environ, start_response):
    resp = Response(template_lookup=LOOKUP, mako_template="registration.html")
    return resp(environ, start_response)


def generate_static_client_credentials(parameters):
    redirect_uris = parameters['redirect_uris']
    client_db_path = os.environ.get("OIDC_CLIENT_DB", "client_db")
    LOGGER.info("Updating db: {}".format(client_db_path))
    cdb = CDB(client_db_path)
    static_client = cdb.create(redirect_uris=redirect_uris, policy_uri="example.com",
                               logo_uri="example.com")
    LOGGER.info("Generated client credentials: %s", json.dumps(static_client))
    return static_client['client_id'], static_client['client_secret']


def application(environ, start_response):
    """
    :param environ: The HTTP application environment
    :param start_response: The application to run when the handling of the
        request is done
    :return: The response as a list of lines
    """
    path = environ.get('PATH_INFO', '').lstrip('/')

    if path == "":
        return registration(environ, start_response)
    elif path == "generate_client_credentials":
        post_data = get_post(environ)
        query_params = json.loads(post_data)
        client_id, client_secret = generate_static_client_credentials(query_params)
        resp = Response(json.dumps({"client_id": client_id, "client_secret": client_secret}),
                        headers=[('Content-Type', "application/json")])
        return resp(environ, start_response)

    return NotFound("'/" + path + "' not found")(environ, start_response)


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
