#!/usr/bin/env python3
"""Relay a local Linux client to the user's existing Windows HTTP proxy.

Use only for preparing public evaluation dependencies. The loopback service does
not inspect, log, or persist request bytes. Solver namespaces retain no network.
Windows proxy connections travel through stdin/stdout, avoiding host firewall or
system resolver changes. Stop this helper after dependency preparation.
"""

import argparse
import asyncio
import base64
import json
import signal
from pathlib import Path


async def serve(windows_port, linux_port):
    powershell = Path("/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe")
    if not powershell.is_file():
        raise RuntimeError("Windows interop is required for this local relay")
    source = (
        "$ErrorActionPreference='Stop';"
        f"$taskClient=[Net.Sockets.TcpClient]::new('127.0.0.1',{windows_port});"
        "$taskStream=$taskClient.GetStream();"
        "$taskUp=[Console]::OpenStandardInput().CopyToAsync($taskStream);"
        "$taskDown=$taskStream.CopyToAsync([Console]::OpenStandardOutput());"
        "[Threading.Tasks.Task]::WaitAny([Threading.Tasks.Task[]]@($taskUp,$taskDown))|Out-Null;"
        "$taskClient.Dispose();"
    )
    encoded = base64.b64encode(source.encode("utf-16le")).decode()

    async def relay(reader, writer):
        process = await asyncio.create_subprocess_exec(
            str(powershell),
            "-NoProfile",
            "-NonInteractive",
            "-EncodedCommand",
            encoded,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
        )

        async def upload():
            while data := await reader.read(1024 * 1024):
                process.stdin.write(data)
                await process.stdin.drain()

        async def download():
            while data := await process.stdout.read(1024 * 1024):
                writer.write(data)
                await writer.drain()

        tasks = [asyncio.create_task(upload()), asyncio.create_task(download())]
        try:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        finally:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            if process.returncode is None:
                process.terminate()
            await process.wait()
            writer.close()
            await writer.wait_closed()

    server = await asyncio.start_server(relay, "127.0.0.1", linux_port)
    print(
        json.dumps(
            {
                "loopback_port": server.sockets[0].getsockname()[1],
                "traffic_logging": False,
                "solver_network_access": False,
            }
        ),
        flush=True,
    )
    stopped = asyncio.Event()
    loop = asyncio.get_running_loop()
    for signum in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(signum, stopped.set)
    async with server:
        await stopped.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--windows-proxy-port", type=int, required=True)
    parser.add_argument("--linux-port", type=int, default=0)
    args = parser.parse_args()
    if not 0 < args.windows_proxy_port < 65536 or not 0 <= args.linux_port < 65536:
        parser.error("proxy ports must be valid local TCP ports")
    asyncio.run(serve(args.windows_proxy_port, args.linux_port))


if __name__ == "__main__":
    main()
