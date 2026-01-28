from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict
import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Mock Data Model
class Item(BaseModel):
    description: str
    cost: float

class ProposalData(BaseModel):
    client_name: str
    project_title: str
    date: str
    items: Dict[str, List[Item]]
    total: float
    notes: Optional[str] = None

# Default Mock Data
default_proposal = ProposalData(
    client_name="Future client",
    project_title="Next-Gen Web Platform",
    date=datetime.date.today().strftime("%B %d, %Y"),
    items={
        "Design & Discovery": [
            Item(description="UX/UI Design System", cost=4500.00),
            Item(description="User Research & Prototyping", cost=2000.00),
        ],
        "Development": [
            Item(description="Frontend Development (React/Next.js)", cost=8500.00),
            Item(description="Backend Integration & API Setup", cost=6000.00),
        ],
        "Infrastructure": [
            Item(description="Cloud Infrastructure & Deployment", cost=2500.00),
        ]
    },
    total=23500.00,
    notes="This proposal is valid for 14 days. We look forward to working with you to build something extraordinary."
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Renders the proposal with default mock data for demonstration.
    """
    return templates.TemplateResponse("proposal.html", {"request": request, "data": default_proposal})

@app.post("/generate", response_class=HTMLResponse)
async def generate_proposal(request: Request, data: ProposalData):
    """
    Accepts JSON data and renders the proposal template with it.
    Useful for n8n to call via POST.
    """
    return templates.TemplateResponse("proposal.html", {"request": request, "data": data})
