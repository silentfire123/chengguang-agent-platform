# 文件 test_sample.py
def add(x, y):
    return x + y

# 以 test_ 开头的函数，就是测试函数
def test_add():
    # assert 断言，用来判断表达式是否为 True。 True代表测试通过
    print('嗨嗨嗨...')
    assert add(2, 3) == 5

def test_add_fail():
    assert add(2, 2) == 4  # 故意写错的断言，用来演示失败的测试
