'''
from fastapi import FastAPI

app = FastAPI(
    title="Driver Fleet Reconciliation API",
    description="API for reconciling driver and fleet operational data",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

'''
'''
from fastapi import FastAPI

from app.api.routes.drivers import router as drivers_router
from app.api.routes.exceptions import router as exceptions_router
from app.api.routes.health import router as health_router
from app.api.routes.reconciliation import router as reconciliation_router
from app.api.routes.summaries import router as summaries_router

app = FastAPI(
    title="Driver Fleet Reconciliation API",
    description="API for reconciling driver and fleet operational data",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(drivers_router)
app.include_router(reconciliation_router)
app.include_router(summaries_router)
app.include_router(exceptions_router)
'''

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.drivers import router as drivers_router
from app.api.routes.exceptions import router as exceptions_router
from app.api.routes.health import router as health_router
from app.api.routes.reconciliation import router as reconciliation_router
from app.api.routes.summaries import router as summaries_router


app = FastAPI(
    title="Driver Fleet Reconciliation API",
    description="API for reconciling driver and fleet operational data",
    version="1.0.0",
)


app.include_router(health_router)
app.include_router(drivers_router)
app.include_router(reconciliation_router)
app.include_router(summaries_router)
app.include_router(exceptions_router)


# Serve the HTML frontend
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)