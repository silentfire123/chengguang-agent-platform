# test_async_sample.py
import asyncio

async def async_add(x, y):
    await asyncio.sleep(0.1)  # 模拟异步操作，比如网络I/O
    return x + y
import pytest

@pytest.mark.asyncio
async def test_async_add():
    print('异步测试...')
    result = await async_add(1, 2)
    assert result == 3