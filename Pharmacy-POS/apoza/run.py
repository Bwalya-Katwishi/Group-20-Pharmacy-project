import uvicorn

from apoza.config import settings

if __name__ == "__main__":
    uvicorn.run("apoza.main:app", host=settings.host, port=settings.port, reload=False)
