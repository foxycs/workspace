## 使用说明

* 运行环境： python3.x
* demo，数据都写在了test_engine的最下面了，正式用时，可保存到csv/xls/或数据库，并可保存更多的用例信息，可往__doc__/__name__/__module__中赋值
* 用例要求：测试方法必须为类的实例方法，可加参数。
* 有4个特殊方法，set_up/set_up_class/tear_down/tear_down_class
* 执行测试

    git clone git@code.csdn.net:zbwill/test_engine.git
    cd test_engine
    python test_emgine.py
