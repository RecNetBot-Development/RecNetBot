import asyncio

class AsyncQueue:
    def __init__(self, max_threads: int):
        self.queue = asyncio.Queue()
        self.max = max_threads
        self.tasks = []
 
    def append(self, item):
        self.queue.put_nowait(item)

    async def drain(self):
        for _ in range(self.max): self.worker()
        await self.queue.join()
        for task in self.tasks: task.cancel()
        await asyncio.gather(*self.tasks, return_exceptions = True)
            

    def task(self, func):
        self.task = func

    def worker(self):
        queue = self.queue
        async def task():
            while True:
                item = await queue.get()
                await self.task(item)
                queue.task_done()
        self.tasks.append(asyncio.create_task(task()))

async def run_in_queue(func, iter, **kwargs):
    data = []
    threads = round((0.4*len(iter))**.5)
    Queue = AsyncQueue(threads)
    @Queue.task
    async def task(item):
        result = await func(item, **kwargs)
        data.append(result)
    for item in iter: Queue.append(item)
    await Queue.drain()
    return data