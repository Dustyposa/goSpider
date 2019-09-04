from starlette.applications import Starlette
from starlette.responses import JSONResponse

app = Starlette()


@app.route('/api', methods=["GET"])
async def hello_api(request) -> JSONResponse:
    """常规返回"""
    return JSONResponse({'Hello': 'World!'})


@app.route('/goods/{goods_id:int}', methods=["GET"])
async def query_goods(request) -> JSONResponse:
    """带id的路由"""
    return JSONResponse({"name": "cake", "id": request.path_params.get("goods_id")})


@app.exception_handler(404)
async def not_found(request, exc) -> JSONResponse:
    """404处理"""
    return JSONResponse(content={"msg": "no route"}, status_code=exc.status_code)
