from typing import List, Optional
from datetime import datetime

from app.models.lead import Lead, LeadCreate, LeadUpdate, LeadResponse
from app.database.dynamodb import db
from app.utils.exceptions import NotFoundException

class LeadService:
    def __init__(self):
        self.db = db
    
    async def create_lead(self, lead_create: LeadCreate, business_id: str) -> Lead:
        """Create a new lead"""
        # Create Lead object with business_id from authenticated user
        lead_dict = lead_create.dict()
        lead_dict['business_id'] = business_id
        
        lead = Lead(**lead_dict)
        lead_data = lead.dict()
        
        # Convert datetime to ISO string for DynamoDB
        lead_data['created_at'] = lead.created_at.isoformat()
        lead_data['updated_at'] = lead.updated_at.isoformat()
        
        await self.db.create_lead(lead_data)
        return lead
    
    async def get_lead(self, lead_id: str, business_id: str) -> Lead:
        """Get a lead by ID"""
        lead_data = await self.db.get_lead(lead_id, business_id)
        
        if not lead_data:
            raise NotFoundException(f"Lead {lead_id} not found")
        
        return Lead(**lead_data)
    
    async def list_leads(
        self,
        business_id: str,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Lead]:
        """List leads for a business"""
        leads_data = await self.db.list_leads(business_id, status, limit)
        return [Lead(**lead) for lead in leads_data]
    
    async def update_lead(
        self,
        lead_id: str,
        business_id: str,
        lead_update: LeadUpdate
    ) -> Lead:
        """Update a lead"""
        # Verify lead exists
        await self.get_lead(lead_id, business_id)
        
        # Prepare updates
        updates = lead_update.dict(exclude_unset=True)
        
        updated_data = await self.db.update_lead(lead_id, business_id, updates)
        return Lead(**updated_data)
    
    async def delete_lead(self, lead_id: str, business_id: str) -> bool:
        """Delete a lead"""
        # Verify lead exists
        await self.get_lead(lead_id, business_id)
        
        return await self.db.delete_lead(lead_id, business_id)

lead_service = LeadService()
