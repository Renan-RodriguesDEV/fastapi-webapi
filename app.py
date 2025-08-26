import uvicorn
from fastapi import FastAPI, status

from routes.auth import router as auth_router
from routes.users import router as user_router

app = FastAPI(
    title="My Bullet API",
    description="that API development with python",
    version="1.0.0",
)
app.include_router(user_router)
app.include_router(auth_router)


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"status": status.HTTP_200_OK, "message": "Hellow world!"}


if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
