# coding=utf-8

'''
总结 ctypes 和 cffi  :
 1 bytes string 都能无 copy 的从 python 传递给 cpp
    其中 cffi 传递起来更简单

 2 读取 cpp 中提供的地址 或者创建内存提供给 cpp 写
    都是 cffi 简单

 有关字符串无拷贝获取内存地址系列已经移到另一个项目了 https://github.com/fooofei/py_string_address

'''

import os
import sys
import ctypes
from  io_in_out import io_print
from  io_in_out import io_in_arg

curpath = os.path.dirname(os.path.realpath(__file__))
curpath = io_in_arg(curpath)

from cpp_python_ctypes import bytes_string_address
from cpp_python_ctypes import text_string_address


def change_value_int(ins):
    io_print(u'test_func_change_value_int')
    v = 2
    io_print(u'python_python->pass value {0} to cpp'.format(v))
    r = ins.change_value_int(v)
    io_print(u'python_python->return value from cpp {0}'.format(r[1]))
    io_print('')


def pass_python_bytes_string(ins):
    ##
    io_print(u'test_func_pass_python_bytes_string')
    v = 'this is string in python pass_python_bytes_string'

    addr = bytes_string_address(v)
    io_print(u'python_print->address by ctypes api {0}'.format(hex(addr)))

    # check

    assert (v
            == ctypes.string_at(addr, len(v))
            )
    io_print('python_print->pass bytes string to cpp [{0}]{1}'.format(len(v), v))
    r = ins.pass_python_bytes_string(v)
    io_print('')


def pass_python_unicode_string(ins):
    ##
    io_print(u'test_func_pass_python_unicode_string')
    v = u'this is string in python pass_python_unicode_string'
    io_print(u'python_print->pass unicode string to cpp [{0}]{1}'.format(len(v), v))

    addr = text_string_address(v)
    io_print(u'python_print->address by ctypes api {0}'.format(hex(addr)))

    if not (addr == 0):
        assert (v
                == ctypes.wstring_at(addr, len(v))
                )

    ins.pass_python_unicode_string(v)

    if not (addr == 0):
        ins.pass_python_unicode_string2(addr, len(v))

    io_print('')

    ##
    io_print(u'test_func_pass_python_unicode_string_chs')
    v = u'这是来自 Python 的字符串，用中文表示，长度27'
    io_print(u'python_print->pass unicode string to cpp [{0}]{1}'.format(len(v), v))
    addr = text_string_address(v)

    io_print(u'python_print->address by ctypes api {0}'.format(hex(addr)))

    if not (addr == 0):
        assert (v
                == ctypes.wstring_at(addr, len(v))
                )

    ins.pass_python_unicode_string(v)
    if not (addr == 0):
        r = ins.pass_python_unicode_string2(addr, len(v))
    io_print('')


def out_memory_python_noalloc(ins):
    ##
    io_print(u'test_func_out_memory_python_noalloc')
    r = ins.out_memory_python_noalloc()
    io_print(u'python_print->out memory [{0}]{1}'.format(len(r[1]), r[1]))

    addr = bytes_string_address(r[1])

    io_print(u'python_print->这里有字符串内存拷贝')
    io_print(u'python_print->address result {0}'.format(hex(addr)))

    io_print('')


def out_memory_python_alloc(ins):
    ##
    io_print(u'test_func_out_memory_python_alloc')
    r = ins.out_memory_python_alloc()
    io_print(u'python_print->out memory [{0}]{1}'.format(len(r[1]), r[1]))
    io_print('')


def out_unicode_string(ins):
    io_print(u'test_out_unicode_string')
    r = ins.out_memoryw()
    io_print(u'python_print->out memoryw [{0}]{1}'.format(len(r[1]), r[1]))

    addr = text_string_address(r[1])
    io_print(u'python_print->return unicode address {0}'.format(hex(addr)))

    io_print('')


def cpp_python_framework(ins):
    # ffi 的 cast 就不能把 string 转换


    ##
    io_print('test_func_empty')
    ins.empty()
    io_print('')

    change_value_int(ins)
    pass_python_bytes_string(ins)
    pass_python_unicode_string(ins)
    out_memory_python_noalloc(ins)
    out_memory_python_alloc(ins)

    io_print(u'test_func_address_read')
    ins.address_read()
    io_print(u'')

    out_unicode_string(ins)


def entry():
    from cpp_python_ctypes import CppExportStructure

    a = {u'win32': u'cpp_python.dll',
         u'linux': u'libcpp_python.so',
         u'darwin': u'libcpp_python.dylib'}
    n = filter(sys.platform.startswith, a.keys())
    assert (len(n) == 1)
    n = a.get(n[0])
    if not n:
        raise ValueError('not found right name')

    p = os.path.join(curpath, n)
    # p = os.path.join(curpath,u'cmake-build-debug',u'libcpp_python.dylib')
    # p = r'D:\Visual_Studio_Projects\cpp_python_vs\Debug\cpp_python_vs.dll'




    ins = CppExportStructure()
    ins.loadlib(p)
    io_print(u'test ctypes..............................')
    cpp_python_framework(ins)

    is_has_cffi = False
    try:
        import cffi
        is_has_cffi = True
    except ImportError:
        pass

    if is_has_cffi:
        from cpp_python_cffi import CffiExportStructure
        ins = CffiExportStructure()
        ins.load_lib(p)
        assert (ins.valid)
        io_print(u'test cffi..............................')
        cpp_python_framework(ins)


if __name__ == '__main__':
    entry()
