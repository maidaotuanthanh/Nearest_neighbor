from fastapi import FastAPI
from routes.order_routes import order

import uvicorn

app = FastAPI()
app.include_router(order)


@app.get("/")
async def home():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8002, reload=True, workers=2)