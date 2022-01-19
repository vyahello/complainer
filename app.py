"""Main application runner."""
import uvicorn
from fastapi import FastAPI

from complainer.db import database
from complainer.resources.routes import api_router

app = FastAPI()
app.include_router(api_router)


@app.on_event('startup')
async def startup() -> None:
    """Start web app. Connect to DB."""
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    """Start web app. Disconnect from DB."""
    await database.disconnect()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
