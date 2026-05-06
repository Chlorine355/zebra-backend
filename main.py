from fastapi import FastAPI
from auth.routes import router as auth_router
from users.routes import router as users_router
from reports.routes import router as reports_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])

@app.get("/")
def read_root():
    return {"message": "Go to /docs for Swagger"}