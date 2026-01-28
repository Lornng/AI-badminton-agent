from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import datetime
import uuid

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Mock Data Model
# Data Models
class ClientDetails(BaseModel):
    name: str
    email: str

class Product(BaseModel):
    category: str
    item: str
    description: str = ""
    # Specifications now holds everything including suitability, features, etc.
    specifications: Dict[str, Any] = {} 

class ProposalData(BaseModel):
    client_details: ClientDetails
    products: List[Product]
    total_package: str
    estimated_budget_range: str
    recommendation_notes: str

class N8NPayload(BaseModel):
    body: ProposalData

# In-memory storage for proposals (use a database in production)
proposals_db: Dict[str, Any] = {}

# Default Mock Data
default_proposal = ProposalData(
    client_details=ClientDetails(
        name="Jian",
        email="jensen@aligned.au"
    ),
    products=[
        Product(
            category="Racket",
            item="Yonex Astrox 88S Pro",
            description="Designed for front-court doubles players, offering excellent control and quick handling with a balanced feel. Features Rotational Generator System for power generation.",
            specifications={
                "balance": "Slightly head-heavy (perceived even balance)",
                "suitability": "Intermediate doubles play",
                "features": [
                    "Net play optimization",
                    "Quick handling for drives",
                    "Solid feel for consistent play"
                ]
            }
        ),
        Product(
            category="String",
            item="Yonex BG65 Titanium",
            description="Durable all-around string with solid feel. Recommended for balanced control and durability in doubles scenarios.",
            specifications={
                "type": "Synthetic multifilament",
                "characteristics": [
                    "High durability",
                    "Solid impact feel",
                    "Control-oriented"
                ]
            }
        ),
        Product(
            category="Stringing Service",
            item="Professional Stringing",
            description="",
            specifications={
                "tension": "25 lbs",
                "notes": "Balanced tension for intermediate players - optimal blend of power and control"
            }
        )
    ],
    total_package="Yonex Astrox 88S Pro racket strung with Yonex BG65 Titanium at 25 lbs",
    estimated_budget_range="$300-$400",
    recommendation_notes="This setup prioritizes versatility for doubles play, offering control at the net and power from the backcourt. Tension and string can be adjusted based on future performance feedback."
)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Renders the proposal with default mock data for demonstration.
    """
    return templates.TemplateResponse("proposal.html", {"request": request, "data": default_proposal})

@app.post("/generate")
async def generate_proposal(request: Request, payload: List[Dict[str, Any]]):
    """
    Accepts flexible JSON data from n8n, stores it, and returns a unique URL.
    Handles format: [{"output": {...}}] or just [{...}]
    """
    # Extract data - check if wrapped in 'output' key
    if payload and isinstance(payload, list) and len(payload) > 0:
        first_item = payload[0]
        # If data is wrapped in 'output', extract it
        data = first_item.get('output', first_item)
    else:
        data = payload
    
    # Generate unique ID
    proposal_id = str(uuid.uuid4())
    
    # Store the proposal (as dict)
    proposals_db[proposal_id] = data
    
    # Get the base URL from the request
    base_url = str(request.base_url).rstrip('/')
    proposal_url = f"{base_url}/proposal/{proposal_id}"
    
    return {"url": proposal_url, "proposal_id": proposal_id}

@app.get("/proposal/{proposal_id}", response_class=HTMLResponse)
async def view_proposal(request: Request, proposal_id: str):
    """
    View a generated proposal by its unique ID.
    """
    if proposal_id not in proposals_db:
        return templates.TemplateResponse("proposal.html", {
            "request": request,
            "data": default_proposal,
            "error": "Proposal not found"
        })
    
    # Get the stored data (now a dict)
    data = proposals_db[proposal_id]
    return templates.TemplateResponse("proposal.html", {"request": request, "data": data})