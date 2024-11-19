from aiohttp import web 
from aiohttp.web_request import Request
import functools
from aiohttp.web_response import Response
from creating import DB_KEY, create_db_pool, destroy_db_pool

routes = web.RouteTableDef()

@routes.get('/products')
async def get_products(request: Request) -> Response:
    try:
        db = request.app[DB_KEY]
        products_query = 'select product_id, product_name from product;'
        result = await db.fetch(products_query)
        if result is not None:
            return web.json_response([dict(record) for record in result])
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()

app = web.Application()
app.on_startup.append(functools.partial(create_db_pool))
app.on_cleanup.append(destroy_db_pool)
app.add_routes(routes)
web.run_app(app, port= 8000)