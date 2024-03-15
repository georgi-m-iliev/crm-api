from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.internal import admin
from app.routers import auth, users
from app.models import Base
from app.database import engine, SessionLocal, Base


def get_application() -> FastAPI:
    """ Configure, start and return the application """

    # Creat the application
    application = FastAPI()

    # Create the database tables
    Base.metadata.create_all(bind=engine)

    # Mapping api routes
    application.include_router(auth.auth, prefix="/auth", tags=["auth"])
    application.include_router(users.users, prefix="/users", tags=["users"])

    # Add exception handlers
    # application.add_exception_handler(HTTPException, http_error_handler)

    # Allow cors
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Example of admin route
    # application.include_router(
    #     admin.router,
    #     prefix="/admin",
    #     tags=["admin"],
    #     dependencies=[Depends(get_token_header)],
    #     responses={418: {"description": "I'm a teapot"}},
    # )

    return application


app = get_application()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    """
    This middleware will create a new SessionLocal for each request,
     and add it to the request, then close it when request is finished.
    """
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
