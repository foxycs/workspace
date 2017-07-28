# coding:utf-8
import importlib

import functools
import inspect
import os

import time
import unittest

import HTMLTestRunner

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def check_and_format_test_data_list(test_data_list):
    format_test_data = {}
    for i in test_data_list:
        # 分离并检查class_str, func_name
        rsplit_str = i[0].rsplit('.', maxsplit=1)
        if len(rsplit_str) != 2:
            raise ValueError('数据有误， 请检查： {}'.format(i[0]))
        class_str, func_name = rsplit_str
        # 分离并检查module_str, class_name
        rsplit_str = class_str.rsplit('.', maxsplit=1)
        if len(rsplit_str) != 2:
            raise ValueError('数据有误， 请检查： {}'.format(class_str))
        module_str, class_name = rsplit_str
        # 引入模块
        imp_module = importlib.import_module(module_str)
        # 获取类
        test_class = getattr(imp_module, class_name)
        # 获取方法
        func_obj = getattr(test_class, func_name)
        # 验证方法参数
        arg_spec = inspect.getargspec(func_obj)
        if len(arg_spec.args) < 1:
            raise ValueError('测试方法不为类的实例方法，或参数不对')
        data_args_set = set(i[1].keys())
        data_args_set.add('self')
        if arg_spec.keywords:
            assert set(arg_spec.args).issubset(data_args_set), '参数不对'
        else:
            assert set(arg_spec.args) == data_args_set, '参数不对'
        data_list = [test_class, func_obj, i[1]]
        # 以class_str为key，为每个测试类组装数据字典
        if format_test_data.get(class_str):
            format_test_data[class_str].append(data_list)
        else:
            format_test_data[class_str] = [data_list]
    return format_test_data


def test_suite_factory(data_list):
    test_class = data_list[0][0]
    # 一条用例 (用到了闭包)
    def case_factory(func, test_data):
        @functools.wraps(func)
        def function(self):
            print('args: %s' % test_data)
            start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print('start_time: %s\n##############################' % start_time)
            try:
                self.instance
            except:
                print('************************\n*该类的__init__方法执行报错*\n************************')
            func(self.instance, **test_data)
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            print('##############################\nend_time: %s' % end_time)

        return function

    # 建空的测试类
    class TestCase(unittest.TestCase):
        pass

    TestCase.__module__ = "这里可设置模块名"
    TestCase.__name__ = test_class.__doc__

    @classmethod
    def setUpClass(cls):
        try:
            cls.instance = test_class()
        except Exception as err:
            print(err)
        try:
            cls.instance.set_up_class()
        except Exception as err:
            pass
    @classmethod
    def tearDownClass(cls):
        try:
            cls.instance.tear_down_class()
        except:
            pass

    def setUp(self):
        try:
            self.instance.set_up()
        except:
            pass

    def tearDown(self):
        try:
            self.instance.tear_down()
        except:
            pass

    # 往空测试类里插入方法
    n = 0
    for i in data_list:
        setattr(TestCase, 'test_%03.f' % n, case_factory(i[1], i[2]))
        n += 1
    # 插入初始化和清理方法
    setattr(TestCase, 'setUpClass', setUpClass)
    setattr(TestCase, 'tearDownClass', tearDownClass)
    setattr(TestCase, 'setUp', setUp)
    setattr(TestCase, 'tearDown', tearDown)
    return TestCase


def execute_test(test_data_list):
    try:
        formated_data_dict = check_and_format_test_data_list(test_data_list)
    except Exception as err:
        print(err)
        return
    all_suite = unittest.TestSuite()
    for i in formated_data_dict:
        suite = unittest.TestLoader().loadTestsFromTestCase(test_suite_factory(formated_data_dict[i]))
        all_suite.addTest(suite)
    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    report_file = os.path.join(BASE_DIR, 'report', 'report_%s.html' % now)
    fp = open(report_file, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='TestReport', description='用例执行情况:')
    r = runner.run(all_suite)
    fp.close()
    result = dict(runner.getReportAttributes(r))
    return result


if __name__ == '__main__':
    test_data_list = [
        ['test_file1.TestClass.test_case1', {}],
        ['test_file1.TestClass.test_case2', {'a': 1, 'b': 2}],
        ['test_file1.TestClass.test_case2', {'a': 3, 'b': 4}],
        ['test_folder.test_file2.TestClass.test_case1', {'a': 3, 'b': 4, 'A': '这是A', 'B': '这是B'}],
    ]
    result = execute_test(test_data_list)
    print(result)
