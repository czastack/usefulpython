#!/usr/bin/env python3
"""
异步下载文件列表
"""

import argparse
import aiofiles
import aiohttp
import asyncio
import os
import traceback
from types import SimpleNamespace

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError as e:
    pass


async def fetch(context, url, savepath):
    context.cur += 1
    print('download {:03d} / {:03d}'.format(context.cur, context.count))

    if os.path.exists(savepath):
        print(savepath, 'exists')
        return

    timeout = aiohttp.ClientTimeout(total=2)
    try:
        print(f'start get: {url}')
        async with context.session.get(url, timeout=timeout) as response:
            data = await response.read()
            async with aiofiles.open(savepath, 'wb') as f:
                await f.write(data)

    except Exception as e:
        traceback.print_exc()


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help="下载列表文件")
    parser.add_argument('-p', '--parent', default='.', help="目标目录")
    args = parser.parse_args()
    parent = args.parent

    async with aiohttp.ClientSession() as session:
        context = SimpleNamespace(
            session=session,
            cur=0,
        )
        task_list = []
        with open(args.src) as src_file:
            for line in src_file.readlines():
                url, savepath = line.split()
                if parent != '.':
                    savepath = os.path.join(parent, savepath)
                task_list.append(fetch(context, url, savepath))

        context.count = len(task_list)
        sem = asyncio.Semaphore(20)
        async with sem:
            await asyncio.wait(task_list)


if __name__ == '__main__':
    asyncio.run(main())
