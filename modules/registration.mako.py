# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 9
_modified_time = 1422273035.602224
_enable_loop = True
_template_filename = 'htdocs/registration.mako'
_template_uri = 'registration.mako'
_source_encoding = 'utf-8'
_exports = [u'body', u'title', u'headline', u'script', u'header', u'footer', u'css']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'base.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def body():
            return render_body(context._locals(__M_locals))
        parent = context.get('parent', UNDEFINED)
        def title():
            return render_title(context._locals(__M_locals))
        def headline():
            return render_headline(context._locals(__M_locals))
        def script():
            return render_script(context._locals(__M_locals))
        def header():
            return render_header(context._locals(__M_locals))
        def footer():
            return render_footer(context._locals(__M_locals))
        def css():
            return render_css(context._locals(__M_locals))
        __M_writer = context.writer()
        # SOURCE LINE 2
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'script'):
            context['self'].script(**pageargs)
        

        # SOURCE LINE 5
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'css'):
            context['self'].css(**pageargs)
        

        # SOURCE LINE 10
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'title'):
            context['self'].title(**pageargs)
        

        # SOURCE LINE 14
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'header'):
            context['self'].header(**pageargs)
        

        # SOURCE LINE 18
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'headline'):
            context['self'].headline(**pageargs)
        

        # SOURCE LINE 22
        __M_writer(u'\n\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'body'):
            context['self'].body(**pageargs)
        

        # SOURCE LINE 84
        __M_writer(u'\n\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'footer'):
            context['self'].footer(**pageargs)
        

        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def body():
            return render_body(context)
        __M_writer = context.writer()
        # SOURCE LINE 25
        __M_writer(u'\n\n    <h1>Static client credentials</h1>\n    <p>If the RP does not support dynamic client registration please generate static client credentials in order to receive\n        a client ID and client secret. Enter at least one redirect URI where the OP will send a response after\n        completing a authorization request.</p>\n\n        <hr>\n    <div class="row">\n        <span class="col-sm-3">\n            <br>\n            Redirect URI\'s\n        </span>\n\n        <div class="col-sm-3">\n            New element:\n            <form>\n                <div class="input-group">\n                    <input type="text" ng-model="new_redirect_uri.value" class="form-control">\n                    <span class="input-group-btn">\n                        <button class="btn btn-default btn-sm"\n                                ng-click="add_redirect_uri()">\n                            Add\n                        </button>\n                    </span>\n                </div>\n            </form>\n        </div>\n\n        <div class="col-sm-3">\n            Added elements:\n            <form ng-repeat="uri in redirect_uris">\n                <div class="input-group">\n                    <input type="text" ng-model="uri.value" class="form-control">\n                        <span class="input-group-btn">\n                            <button class="btn btn-danger btn-sm"\n                                    ng-click="remove_redirect_uri($index)">\n                                X\n                            </button>\n                        </span>\n                </div>\n            </form>\n        </div>\n\n        <div class="col-sm-3">\n        </div>\n    </div>\n\n    <button class="btn btn-default btn-sm"\n            ng-click="generate_client_credentials()">\n        Generate client credentials\n    </button>\n\n    <hr>\n\n    <a class="btn btn-primary btn-sm" href="/test_list">\n        Continue to test page\n    </a>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def title():
            return render_title(context)
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'\n    oictest application\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_headline(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def headline():
            return render_headline(context)
        __M_writer = context.writer()
        # SOURCE LINE 20
        __M_writer(u'\n    <div ng-controller="IndexCtrl">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_script(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def script():
            return render_script(context)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_header(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def header():
            return render_header(context)
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 16
        __M_writer(u'\n    ')
        # SOURCE LINE 17
        __M_writer(unicode(parent.header()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        def footer():
            return render_footer(context)
        __M_writer = context.writer()
        # SOURCE LINE 86
        __M_writer(u'\n    </div>\n\n    <script type="text/javascript" src="/static/registration.js"></script>\n\n    ')
        # SOURCE LINE 91
        __M_writer(unicode(parent.footer()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_css(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def css():
            return render_css(context)
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer(u'\n    <!-- Add more css imports here! -->\n    <link rel="stylesheet" type="text/css" href="/static/registration.css">\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


