from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional

from app.models.lead import Lead, LeadCreate, LeadUpdate, LeadResponse
from app.models.user import User
from app.services.lead_service import lead_service
from app.routes.auth import get_current_user

router = APIRouter(prefix="/leads", tags=["leads"])

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead: LeadCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new lead"""
    # Pass business_id from authenticated user to service
    return await lead_service.create_lead(lead, current_user.business_id)

@router.get("/", response_model=List[LeadResponse])
async def list_leads(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    current_user: User = Depends(get_current_user)
):
    """List all leads for the authenticated business"""
    return await lead_service.list_leads(
        business_id=current_user.business_id,
        status=status,
        limit=limit
    )

@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get a specific lead"""
    return await lead_service.get_lead(lead_id, current_user.business_id)

@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    lead_update: LeadUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a lead"""
    return await lead_service.update_lead(
        lead_id,
        current_user.business_id,
        lead_update
    )

@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: str,
    current_user: User = Depends(get_current_user)
):
    """Delete a lead"""
    await lead_service.delete_lead(lead_id, current_user.business_id)
    return None