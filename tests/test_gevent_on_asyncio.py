import gevent

gevent.config.loop = "asyncio_gevent.gevent_loop.GeventLoop"

import gevent.monkey

gevent.monkey.patch_all(
    socket=False,
    dns=True,
    time=True,
    select=False,
    thread=True,
    os=True,
    ssl=True,
    subprocess=True,
    sys=True,
    aggressive=True,
    Event=True,
    builtins=True,
    signal=True,
    queue=True,
    contextvars=True,
)

import asyncio
import threading
import time

import asyncio_gevent

# test_asyncio_on_gevent_will_run_in_dummy_thread


def test_asyncio_on_gevent_will_run_in_dummy_thread_with_asyncio_run():
    assert threading.current_thread().name == "MainThread"

    result = asyncio.run(asyncio_on_gevent_will_run_in_dummy_thread_async("MainThread"))
    assert result == 42


def test_asyncio_on_gevent_will_run_in_dummy_thread_with_future_to_greenlet():
    assert threading.current_thread().name == "MainThread"

    greenlet = asyncio_gevent.future_to_greenlet(
        asyncio_on_gevent_will_run_in_dummy_thread_async("Dummy-2")
    )
    greenlet.start()
    greenlet.join()
    result = greenlet.get()
    assert result == 42


async def asyncio_on_gevent_will_run_in_dummy_thread_async(expected_name):
    assert threading.current_thread().name == expected_name
    return 42


# test_asyncio_on_gevent_supports_nested_async_calls


def test_asyncio_on_gevent_supports_nested_async_calls_with_asyncio_run():
    result = asyncio.run(asyncio_on_gevent_supports_nested_async_calls_1())
    assert result == 42


def test_asyncio_on_gevent_supports_nested_async_calls_with_future_to_greenlet():
    greenlet = asyncio_gevent.future_to_greenlet(
        asyncio_on_gevent_supports_nested_async_calls_1()
    )
    greenlet.start()
    greenlet.join()
    result = greenlet.get()
    assert result == 42


async def asyncio_on_gevent_supports_nested_async_calls_1():
    result = await asyncio_on_gevent_supports_nested_async_calls_2()
    assert result == 100
    return 42


async def asyncio_on_gevent_supports_nested_async_calls_2():
    result = await asyncio_on_gevent_supports_nested_async_calls_3()
    assert result == "it works"
    return 100


async def asyncio_on_gevent_supports_nested_async_calls_3():
    await asyncio.sleep(1)
    return "it works"


# test asyncio_on_gevent_supports_awaiting_greenlets


def test_asyncio_on_gevent_supports_awaiting_greenlets_with_asyncio_run():
    asyncio.run(asyncio_on_gevent_supports_awaiting_greenlets_1())


def test_asyncio_on_gevent_supports_awaiting_greenlets_with_future_to_greenlet():
    greenlet = asyncio_gevent.future_to_greenlet(
        asyncio_on_gevent_supports_awaiting_greenlets_1()
    )
    greenlet.start()
    greenlet.join()
    result = greenlet.get()
    assert result == None


async def asyncio_on_gevent_supports_awaiting_greenlets_1():
    current_thread = threading.current_thread()
    result = await asyncio_gevent.greenlet_to_future(
        gevent.spawn(asyncio_on_gevent_supports_awaiting_greenlets_2, current_thread)
    )
    assert result == 42


def asyncio_on_gevent_supports_awaiting_greenlets_2(parent_thread):
    assert threading.current_thread() != parent_thread

    time.sleep(1)

    return 42
