import hashlib
import hmac
import base64
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode
from fastapi import FastAPI, Request, Header, HTTPException
import httpx

import os

from alibabacloud_openapi_util.client import Client as OpenApiUtilClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_util import models as util_models

app = FastAPI()

async def forward_request(endpoint:str, access_key:str, secret_key:str, action:str, original_request: Request,version:str = '2015-12-15'):
    """转发请求到阿里云并返回响应"""
    # 获取原始请求参数
    params = dict(original_request.query_params)
    body = await original_request.body()
    request_path = original_request.url.path
    request_method = original_request.method
    request_queries = parse_qs(original_request.url.query)
    request_queries = {k: v[0] for k, v in request_queries.items()}
    
    config = open_api_models.Config(
            access_key_id=access_key,
            access_key_secret=secret_key
        )
    config.endpoint = endpoint
    client = OpenApiClient(config)
    params = open_api_models.Params(
        # 接口名称,
        action=action,
        # 接口版本,
        version=version,
        # 接口协议,
        protocol='HTTPS',
        # 接口 HTTP 方法,
        method=request_method,
        auth_type='AK',
        style='RPC',
        # 接口 PATH,
        pathname='/',
        # 接口请求体内容格式,
        req_body_type='json',
        # 接口响应体内容格式,
        body_type='json'
    )
    # query params
    if request_method == 'GET' or request_method == 'DELETE':
        # GET/DELETE 请求没有请求体
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(request_queries),
        )
    else:
        # POST/PUT 请求
        request = open_api_models.OpenApiRequest(
            query=OpenApiUtilClient.query(request_queries),
            body=body
        )
    # runtime options
    runtime = util_models.RuntimeOptions()
    # 直接返回响应
    return await client.call_api_async(params, request, runtime)

@app.api_route("/", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(
    request: Request,
    access_key: str = Header(None),
    secret_key: str = Header(None),
    endpoint: str = Header(None),
    action: str = Header(None),
    version: str = Header(None),
):
    """通用代理端点"""
    if not endpoint:
        raise HTTPException(status_code=400, detail="Missing endpoint header")
    # 验证Authorization Header
    if not access_key or not secret_key:
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    
    
    
    # 转发请求
    content = await forward_request(endpoint, access_key, secret_key,action, request, version)
    
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)