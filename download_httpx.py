#!/usr/bin/env python3
"""
异步下载文件列表
"""

import argparse
import aiofiles
import httpx
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
    print('download {} [{:03d} / {:03d}]'.format(savepath, context.cur, context.count))

    if os.path.exists(savepath):
        print(savepath, 'exists')
        return

    try:
        print(f'start get: {url}')
        response = await context.client.get(url)
        data = response.content
        async with aiofiles.open(savepath, 'wb') as f:
            await f.write(data)
    except Exception as e:
        traceback.print_exc()


async def download_list(items, save_dir='.'):
    """下载列表"""
    async with httpx.AsyncClient(http2=True) as client:
        context = SimpleNamespace(
            client=client,
            cur=0,
        )
        task_list = []
        for item in items:
            if isinstance(item, str):
                url = item
                filename = os.path.split(item)[1]
                qn = filename.find()
                if qn != -1:
                    filename = filename[:qn]
            else:
                url, savepath = item
            if save_dir != '.':
                savepath = os.path.join(save_dir, savepath)
            task_list.append(fetch(context, url, savepath))

        context.count = len(task_list)
        sem = asyncio.Semaphore(20)
        async with sem:
            await asyncio.wait(task_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', help="下载列表文件")
    parser.add_argument('-p', '--parent', default='.', help="目标目录")
    args = parser.parse_args()
    parent = args.parent

    items = []
    with open(args.src) as src_file:
        for line in src_file.readlines():
            line = line.strip()
            if line and not line.startswith('#'):
                url, savepath = line.split(maxsplit=1)
                items.append((url, savepath))
    # asyncio.run(main())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_list(items, parent))


if __name__ == '__main__':
    main()
