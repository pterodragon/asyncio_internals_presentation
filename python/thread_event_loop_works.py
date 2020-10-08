import asyncio
import threading


def task():
    print("task")


def run_loop_inside_thread(loop):
    loop.run_forever()


loop = asyncio.get_event_loop()
threading.Thread(target=run_loop_inside_thread, args=(loop,)).start()
loop.call_soon_threadsafe(task)  # prints "task"
