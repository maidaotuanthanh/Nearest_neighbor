from fastapi import FastAPI
from routes.order_routes import order
from routes.layout_routes import layout
from routes.picking_routes import picking
import uvicorn

app = FastAPI()
app.include_router(order)
app.include_router(layout)
app.include_router(picking)

@app.get("/")
async def home():
    return {"message": "Hello World"}


@app.get("/route_picking")
async def route_picking():
    return {"message": "Route Picking"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8002, reload=True, workers=2)
