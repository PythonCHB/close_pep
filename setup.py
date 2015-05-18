# setup.py for is
from distutils.core import setup, Extension

is_close_module = Extension('is_close_module',
                            sources=['is_close_module.c'])

setup(name='is_close',
      version='1.0',
      description='test case of is_close C function',
      ext_modules=[is_close_module]
      )
