from fastapi import FastAPI
from app.database import engine, Base
from app.routes import user_routes, ml_routes

from fastapi.routing import APIRoute


# ✅ Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ Attach route modules
app.include_router(user_routes.router, prefix="/users", tags=["Users"] )
app.include_router(ml_routes.router, prefix="/ml", tags=["ML"])



@app.on_event("startup")
def list_routes():
    print("\n🔍 Registered Routes:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"{route.path} [{','.join(route.methods)}]")