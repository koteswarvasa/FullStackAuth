
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.admin_routes import router as admin_router



from app.routes.auth_routes import router as auth_router

app = FastAPI(
    title="FullStackAuth API",
    description="Authentication and Authorization API",
    version="1.0.0"
)

# Allow requests from our React development server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)


@app.get("/")
def root():
    return {
        "message": "FullStackAuth API is running"
    }


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)