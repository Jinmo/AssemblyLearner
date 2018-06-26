#!/usr/bin/env python

# Example for using the shared library from python
# Will work with either python 2 or python 3
# Requires cmark library to be installed

import os
import platform
import re
import sys
import traceback
from ctypes import CDLL, c_char_p, c_void_p, c_long
from pygments import highlight
from pygments.formatters import HtmlFormatter, ClassNotFound
from pygments.lexers import get_lexer_by_name

sysname = platform.system()

if sysname == 'Darwin':
    libname = "libcmark-gfm.dylib"
    extname = "libcmark-gfmextensions.dylib"
elif sysname == 'Windows':
    os.environ['PATH'] += ';C:/Python27/DLLs'
    libname = "cmark-gfm.dll"
    extname = "cmark-gfmextensions.dll"
else:
    libname = "/usr/local/lib/libcmark-gfm.so"
    extname = "/usr/local/lib/libcmark-gfmextensions.so"

cmark = CDLL(libname)
cmark_ext = CDLL(extname)

cmark.cmark_render_html.restype = c_char_p
cmark.cmark_node_get_literal.restype = c_char_p

opts = 1 << 11  # defaults
opts |= 1 << 3
extensions = ('tagfilter', 'autolink', 'table', 'strikethrough')
cmark_ext.core_extensions_ensure_registered()
cmark.cmark_iter_next.restype = \
    cmark.cmark_get_default_mem_allocator.restype = \
    cmark.cmark_node_get_fence_info.restype = \
    cmark.cmark_iter_get_node.restype = \
    cmark.cmark_parser_finish.restype = \
    cmark.cmark_get_default_mem_allocator.restype = \
    cmark.cmark_parser_new_with_mem.restype = \
    cmark.cmark_find_syntax_extension.restype = \
    cmark.cmark_iter_new.restype = \
    cmark.cmark_iter_next.restype = \
    cmark.cmark_parser_new_with_mem.restype = \
    cmark.cmark_node_new.restype = c_void_p
alloc = cmark.cmark_get_default_mem_allocator()
parser = cmark.cmark_parser_new_with_mem(opts, c_void_p(alloc))
formatter = HtmlFormatter()
for ext in extensions:
    ext = cmark.cmark_find_syntax_extension(c_char_p(ext))
    assert ext != 0
    cmark.cmark_parser_attach_syntax_extension(c_void_p(parser), c_char_p(ext))


def highlight_code(node):
    x = cmark.cmark_iter_new(c_void_p(node))
    while True:
        ev_type = cmark.cmark_iter_next(c_void_p(x))
        if ev_type == 1:
            break
        cur = cmark.cmark_iter_get_node(c_void_p(x))
        node_type = cmark.cmark_node_get_type(c_void_p(cur))
        fence_info = cmark.cmark_node_get_fence_info(c_void_p(cur))
        if node_type == 0x8005:
            if fence_info:
                fence_info = c_char_p(fence_info).value
            else:
                fence_info = ''
            syntax = re.match(r'^([^=]+)', fence_info)
            if syntax:
                syntax = syntax.group()
            if not syntax:
                syntax = 'text'
            content = c_char_p(cmark.cmark_node_get_literal(c_void_p(cur))).value
            try:
                lexer = get_lexer_by_name(syntax)
            except ClassNotFound:
                lexer = get_lexer_by_name('text')
            highlighted = highlight(content, lexer, formatter)
            custom_node = cmark.cmark_node_new(c_void_p(0x8007))
            cmark.cmark_node_set_on_enter(c_void_p(custom_node), c_char_p(highlighted.encode('utf-8')))
            cmark.cmark_node_replace(c_void_p(cur), c_void_p(custom_node))
            cmark.cmark_node_free(c_void_p(cur))


def markdown(text, len, opts):
    cmark.cmark_parser_feed(parser, c_char_p(text), len)
    node = cmark.cmark_parser_finish(parser)
    highlight_code(node)
    # print 'highlight completed!'
    html = c_char_p(cmark.cmark_render_html(c_void_p(node), opts, c_void_p(cmark.cmark_parser_get_syntax_extensions(parser))))
    html = html.value
    html = html.replace('<table', '<table class="ui table"')
    html = html.replace('<hr />', '<div class="ui divider"></div>')
    return html


def render(text):
    if sys.version_info >= (3, 0):
        textbytes = text.encode('utf-8')
        textlen = len(textbytes)
        result = markdown(textbytes, textlen, opts).decode('utf-8')
    else:
        textbytes = text.encode('utf-8')
        textlen = len(textbytes)
        result = markdown(textbytes, textlen, opts).decode('utf-8')
    return result
