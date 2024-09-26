from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.modules.sprintgoal import Base as SprintgoalBase  # Importing Base from modules
from app.routers import sprintgoal
from app.routers import team
from app.routers import sprint
from app.routers import sprintprogress
from app.routers import individualperformance
from app.routers import velocity
from app.routers import blockers
from app.routers import production_pipeline_releases

app = FastAPI(title="POC")
app.include_router(
    team.router,
    tags=["Team"],
    prefix="/Team"
),
app.include_router(
    sprint.router,
    tags=["Sprint"],
    prefix="/Sprint"
),
app.include_router(
    sprintgoal.router,
    tags=["Sprintgoal"],
    prefix="/Sprintgoal"
),
app.include_router(
    sprintprogress.router,
    tags=["Sprintprogress"],
    prefix="/Sprintprogress"
),
app.include_router(
    individualperformance.router,
    tags=["Individualperformance"],
    prefix="/Individualperformance"
),
app.include_router(
    velocity.router,
    tags=["Velocity"],
    prefix="/velocity"
),
app.include_router(
    blockers.router,
    tags=["Blockers"],
    prefix="/Blockers"
),
app.include_router(
    production_pipeline_releases.router,
    tags=["Productionpipeline"],
    prefix="/Productionpipeline"
),

SprintgoalBase.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",  # React app URL
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



