#!/usr/bin/env python
# -*- coding: utf-8  -*-
import os
import six
import inspect
import importlib
import functools

from tornado.util import import_object
from tornado.web import RequestHandler

from .exception import JsonError
from .utils.encrypter import RSAEncrypter
from .settings_manager import settings
from .handler import BaseHandler
from .utils.func import md5


def get_modules(package="."):
    """
    获取包名下所有非__init__的模块名
    """
    modules = []
    files = os.listdir(package)
    for file in files:
        if not file.startswith('_'):
            name, ext = os.path.splitext(file)
            modules.append('.' + name)
    # endfor
    return modules

async def get_handlers(app_name):
    """ 自动加载特定APP里面的handler """
    namespace = f'{settings.ROOT_PATH}/applications/{app_name}/handlers/'
    modules = get_modules(namespace)
    # 将包下的所有模块，逐个导入，并调用其中的函数
    package = f'applications.{app_name}.handlers'
    handlers = {}
    for module in modules:
        if not module:
            continue
        if module.startswith('..'):
            continue
        try:
            module = importlib.import_module(module, package)
        except Exception as e:
            continue
        for attr in dir(module):
            if attr.startswith('_'):
                continue
            if not attr.endswith('Handler'):
                continue
            handler = getattr(module, attr)
            params = inspect.getmembers(handler, lambda f: callable(f) and hasattr(f, '_path'))
            for name, val in params:
                path = val._path if val._path.startswith('/') else rf'/{app_name}/{val._path}'
                path_md5 = val._path_md5
                method = val._method.lower()
                if len(handlers.keys())==0 or path_md5 in handlers.keys():
                    handler2 = handler
                else:
                    handler2 = type(path_md5, (handler,), {})
                # endif
                setattr(handler2, method, val)
                # print('handler2', method, name, path, path_md5, handler2, len(handlers.keys()), path_md5 in handlers.keys())
                handlers[path_md5] = (path, handler2)
        # endfor
    # endfor
    return list(handlers.values())

def get(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._path_md5 = md5(path)
        _wrapper._method = 'get'
        return _wrapper
    return wrapper

def post(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._path_md5 = md5(path)
        _wrapper._method = 'post'
        return _wrapper
    return wrapper

def put(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._path_md5 = md5(path)
        _wrapper._method = 'put'
        return _wrapper
    return wrapper

def head(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._path_md5 = md5(path)
        _wrapper._method = 'head'
        return _wrapper
    return wrapper

def delete(*dargs, **dkargs):
    """
    """
    def wrapper(method):
        path = dargs[0]
        @functools.wraps(method)
        def _wrapper(*args, **kargs):
            return method(*args, **kargs)
        _wrapper._path = path
        _wrapper._path_md5 = md5(path)
        _wrapper._method = 'delete'
        return _wrapper
    return wrapper
