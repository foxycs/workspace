# coding:utf-8
"""
这是第一个模块？？？
"""
class TestClass:
    """TestClass1"""
    def test_case1(self):
        """no args"""
        print('test_case1')

    def test_case2(self, a, b):
        """fixed args"""
        print('a: %s, b: %s' % (a, b))

    def set_up(self):
        print('这里是set up方法')

    def tear_down(self):
        print('这里是tear down方法')

    def set_up_class(self):
        print('这里是set up class方法')
        print('这个方法可能在测试报告里没有体现出来，但确实是执行了')

    def tear_down_class(self):
        print('这里是tear down class方法')
        print('这个方法可能在测试报告里没有体现出来，但确实是执行了')