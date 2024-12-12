from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from app.routers import router
import logging

import sys
import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

sys.path.append(os.path.join(os.path.dirname(__file__)))

# local proxy
# os.environ["http_proxy"] = "http://127.0.0.1:10809"
# os.environ["https_proxy"] = "http://127.0.0.1:10809"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.middleware("http")
async def log_request(request: Request, call_next):
    # 记录请求信息
    logger.info(f"Path: {request.url.path}")
    logger.info(f"Headers: {dict(request.headers)}")
    logger.info(f"Query params: {dict(request.query_params)}")

    # 读取body
    body = await request.body()

    # 尝试以UTF-8解码body
    try:
        body_decoded = body.decode('utf-8')
        logger.info(f"Body: {body_decoded}")
    except UnicodeDecodeError:
        # 如果解码失败，则以十六进制形式打印原始字节
        logger.info(f"Body (raw bytes): {body.hex()}")

    # 继续处理请求
    response = await call_next(request)
    return response

app.include_router(router)