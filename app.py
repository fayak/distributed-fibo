from flask import Flask, jsonify
import asyncio
import aiohttp
import requests
import os

app = Flask(__name__)

ENDPOINT = os.environ.get("ENDPOINT", None)

@app.route("/")
def hello_world():
    return "Hello, world!\n"

@app.route("/whoami")
def whoami():
    return os.environ.get('HOSTNAME', 'No hostname set') + "\n"

@app.route("/version")
def version():
    return "1.7.0\n"

@app.route("/health")
def health():
    return "ok"

@app.route("/readiness")
def readiness():
    try:
        r = requests.get(f"{ENDPOINT}/fibo/2").text
        assert r == "1\n"
    except Exception as e:
        print(e)
        return f"ko: {str(e)}", 500
    return "ok"

@app.route("/fibo/<n_>")
def fibo_(n_):
    n = int(n_)
    if n < 0:
        return 0
    elif n <= 1:
        return jsonify(n)
    else:
        if ENDPOINT is None:
            raise ValueError("ENDPOINT env var is not defined !")
        val = asyncio.run(parallel_distributed_fibo([n - 1, n - 2]))
        return jsonify(val)


async def get(url, session, retry=15):
    if retry == 0:
        raise Exception("Could not find remote peer")
    try:
        async with session.get(url=url) as response:
            resp = await response.json()
            return resp
    except Exception as e:
        return await get(url, session, retry - 1)


async def parallel_distributed_fibo(ns):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*(get(f"{ENDPOINT}/fibo/{str(n)}", session) for n in ns))
    return sum(ret)

