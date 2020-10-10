# references

## Advantages and disadvantages of cooperative multitasking (Python GIL single thread asyncio is that)
- `https://brandongaille.com/9-cooperative-multitasking-advantages-and-disadvantages/`

## function color
- `https://lukasa.co.uk/2016/07/The_Function_Colour_Myth/`
    - things not marked with "async" might be async, e.g. event loop implementation before Python 3.5

## event loop implementation in Python
- `https://lukasa.co.uk/2016/07/The_Function_Colour_Myth/`

## thoughts on async API design after "async/await"
- `https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-in-a-post-asyncawait-world/`
- talk: `https://www.youtube.com/watch?v=oLkfnc_UMcE`
    - Bad: disrespecting causality causes bugs
        - e.g. spawning a new logical thread (for callback etc.) of execution
            - causing "read data after socket closed"
    - Python asyncio is callback + async/await, hybrid system

## concurrency from the ground up
- talk: `https://www.youtube.com/watch?v=MCs5OvhV9S4`

## callbacks vs promises
- https://stackoverflow.com/questions/22539815/arent-promises-just-callbacks
    - inversion of control
    - with promise, you can control when to handle the result/exception; with callback passed into a function, you have to specify how to handle the result/exception there at once

## magic behind generator
- https://hackernoon.com/the-magic-behind-python-generator-functions-bc8eeea54220

### notes
- `yield` causes state explosion
- there's no control over how long a task can run. Task gives up control voluntarily via `yield`
- scheduling new task via `create_task` or `ensure_future` breaks causality
- backpressure?
    - `transport.write` just buffers the data to write later (sync call). has to call drain/pause etc. in stream app

```
  # demonstrates pdb can't do anything for classes and functions implemented in C modules
  /mnt/fsmnt/pterodragon/Documents/dev/python_project/tcp_echo_server.py(27)<module>()
     26
---> 27 asyncio.run(main())
     28

  /home/pterodragon/.pyenv/versions/3.8.2/lib/python3.8/asyncio/runners.py(43)run()
     42         loop.set_debug(debug)
1--> 43         return loop.run_until_complete(main)
     44     finally:

  /home/pterodragon/.pyenv/versions/3.8.2/lib/python3.8/asyncio/base_events.py(595)run_until_complete()
    594         new_task = not futures.isfuture(future)
2-> 595         future = tasks.ensure_future(future, loop=self)
    596         if new_task:

  /home/pterodragon/.pyenv/versions/3.8.2/lib/python3.8/asyncio/tasks.py(661)ensure_future()
    660             loop = events.get_event_loop()
--> 661         task = loop.create_task(coro_or_future)
    662         if task._source_traceback:

  /home/pterodragon/.pyenv/versions/3.8.2/lib/python3.8/asyncio/base_events.py(431)create_task()
    430         if self._task_factory is None:
3-> 431             task = tasks.Task(coro, loop=self, name=name)
    432             if task._source_traceback:

> /home/pterodragon/.pyenv/versions/3.8.2/lib/python3.8/asyncio/base_events.py(1877)get_debug()
   1876
-> 1877     def get_debug(self):
   1878         return self._debug  # ??????
```

```
fut->fut_loop is _UnixSelectorEventLoop
```

```
Traceback (most recent call first):
  File "/mnt/fsmnt/pterodragon/Documents/github/cpython/Lib/selectors.py", line 349, in __init__
    self._selector = self._selector_cls()
  File "/mnt/fsmnt/pterodragon/Documents/github/cpython/Lib/asyncio/selector_events.py", line 58, in __init__
    selector = selectors.DefaultSelector()
  File "/mnt/fsmnt/pterodragon/Documents/github/cpython/Lib/asyncio/unix_events.py", line 54, in __init__
    super().__init__(selector)
  File "/mnt/fsmnt/pterodragon/Documents/github/cpython/Lib/asyncio/events.py", line 656, in new_event_loop
    return self._loop_factory()
  File "/mnt/fsmnt/pterodragon/Documents/github/cpython/Lib/asyncio/events.py", line 758, in new_event_loop
    return get_event_loop_policy().new_event_loop()
  File "/mnt/fsmnt/pterodragon/Documents/github/cpython/Lib/asyncio/runners.py", line 295, in run
  File "../../dev/python_project/tcp_echo_server.py", line 27, in <module>
    asyncio.run(main())
```
#### to use Python implementation of `asyncio` instead of C implementation
- remove the "asyncio" line in `./Modules/Setup`
- remove `Modules/_asynciomodule.c`
- `./configure` again
- `make`

# Code dive
## `Task`
- bound to an event loop

1. `task.Task`
2. C `_asyncio_Task___init___impl` -> `task_call_step_soon` -> `call_soon`
3. `loop.call_soon` -> `loop._call_soon` 
4. `self._ready.append(handle)`

## Event loop
From python docs
```
Event loops use cooperative scheduling: an event loop runs one Task at a time. While a Task awaits for the completion of a Future, the event loop runs other Tasks, callbacks, or performs IO operations.
```

## `_UnixSelectorEventLoop`

The loop style doesn't affect coroutines, but rather how the fds are polled

## loop run
Some part is implemented in C, `Lib/asyncio/task.py` `def __step` demonstrates the code in C
1. `loop.run_until_complete(...)` -> `loop.run_forever()`
2. `self._run_once()`
`self._scheduled` ? `loop.call_at` never called in the app, so irrelevant
3. `handle._run()`
4. `self._context.run(self._callback, *self._args)`
### stepping a coroutine (generator)
5. C `context_run` -> C `TaskStepMethWrapper_call` -> C `task_step` -> C `task_step_impl`
6a. C `result = _PyGen_Send((PyGenObject*)coro, Py_None);`
6b. C `if (result == NULL)` (generator returns None / StopException raised)
6c. C `res = future_set_result((FutureObj*)task, o);`

(6a.) demonstrates that stepping means "continuing" a generator

## `asyncio.run(...)`

1. `loop.run_until_complete(main)`
2. finalize
    - `_cancel_all_tasks(loop)`
    - `loop.run_until_complete(loop.shutdown_asyncgens())`

## What does `self._run_once()` do?

- there's a queue (FIFO) `self._ready`
- run tasks in order until all are done
- tasks that are spawned/suspended get put back to the queue in order

demo: `python/run_once_demo.py`

## asyncio.Future
- bound to an event loop
- `yield from fut` (`await fut`) will yield itself if it's not done
    - when done, it yields the result
    - future is added back to the event loop when `Futurer.set_result` is called

### asyncio.Future.set_result
1. C `_asyncio_Future_set_result` -> `future_set_result` -> `future_schedule_callbacks` -> `call_soon`
2. loop.call_soon

demo: `python/await_generator_future.py`
also change the selector timeout to be always 0

## Task vs Future
- pretty much the same
- C `TaskObj` contains `FutureObj_HEAD`
- `Task` is a coroutine wrapped in a `Future`


## self pipe
https://github.com/dask/distributed/issues/3223

"""
Well, this is a "self-pipe" meant to wake up the IO loop thread from other threads or from a signal, for example when adding a callback. Normally this mechanism isn't used when a callback is added from regular async code (i.e. called from the IO loop thread itself), but perhaps Tornado's compatibility layer doesn't make a difference between the two situations?

You'll have to trace the calls to _write_to_self to find out a bit more.
"""
https://zhuanlan.zhihu.com/p/38575715 (Chinese)
In `selectors.py:468`, the poll will block if the self pipe isn't written into

demo: `python/thread_event_loop.py`, `python/thread_event_loop_works.py`
```
fd_event_list = self._selector.poll(timeout, max_ev)
```


# talk
https://www.slideshare.net/saghul/asyncio-internals

# Others
in `base_events.py`

```
ntodo = len(self._ready)
for i in range(ntodo):
```

why not `for e in self._ready` -> because during the iteration, things can be added to the deque

--
`add_reader` `add_writer` => fd based


