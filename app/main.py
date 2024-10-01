from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.modules.sprintgoal import Base as SprintgoalBase  
from app.modules.individualperformance import Base as IndividualPerformanceBase
from app.modules.sprintprogress import Base as SprintProgress 
from app.routers import sprintgoal
from app.routers import team
from app.routers import sprint
from app.routers import sprintprogress
from app.routers import individualperformance
from app.routers import velocity
from app.routers import blockers
from app.routers import production_pipeline_releases
from app.routers import imageupload

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
# app.include_router(
#     imageupload.router,
#     tags=["ImageUpload"],
#     prefix="/ImageUpload"
# ),

SprintgoalBase.metadata.create_all(bind=engine)
IndividualPerformanceBase.metadata.create_all(bind=engine)
SprintProgress.metadata.create_all(bind=engine)
origins = [
    "http://localhost:3000", 
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



