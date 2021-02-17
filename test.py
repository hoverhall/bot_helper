import time
import asyncio

def a():
    print("a")


def b():
    print("b")


def c():
    print("c")


ts = time.time()

operation_stack = [
    {"timestamp": ts + 30, "operation": a},
    {"timestamp": ts + 10, "operation": b},
    {"timestamp": ts + 40, "operation": c}
]


async def stack_reducer():
    while True:
        for i in operation_stack:
            if time.time() >= i["timestamp"]:
                i["operation"]()
                operation_stack.remove(i)
        if len(operation_stack) == 0:
            break

asyncio.run(stack_reducer())