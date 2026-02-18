import boto3
from boto3.dynamodb.conditions import Key, Attr
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DynamoDBClient:
    def __init__(self):
        environment = os.getenv("ENVIRONMENT", "production")
        region = os.getenv("AWS_REGION", "us-east-1")

        if environment in ("local", "test"):
            self.dynamodb = boto3.resource(
                "dynamodb",
                endpoint_url=os.getenv("DYNAMODB_ENDPOINT", "http://localhost:8000"),
                region_name=region,
                aws_access_key_id="dummy",
                aws_secret_access_key="dummy",
            )
        else:
            self.dynamodb = boto3.resource(
                "dynamodb",
                region_name=region
            )

        self.leads_table = self.dynamodb.Table(
            os.getenv("LEADS_TABLE_NAME", "leads")
        )
        self.users_table = self.dynamodb.Table(
            os.getenv("USERS_TABLE_NAME", "users")
        )
    
    # LEAD OPERATIONS
    async def create_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new lead"""
        try:
            self.leads_table.put_item(Item=lead_data)
            logger.info(f"Created lead: {lead_data['id']}")
            return lead_data
        except Exception as e:
            logger.error(f"Error creating lead: {str(e)}")
            raise
    
    async def get_lead(self, lead_id: str, business_id: str) -> Optional[Dict[str, Any]]:
        """Get a lead by ID and business_id"""
        try:
            response = self.leads_table.get_item(
                Key={'id': lead_id, 'business_id': business_id}
            )
            return response.get('Item')
        except Exception as e:
            logger.error(f"Error getting lead {lead_id}: {str(e)}")
            raise
    
    async def list_leads(
        self, 
        business_id: str, 
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """List leads for a business with optional status filter"""
        try:
            # Query using GSI on business_id
            kwargs = {
                'IndexName': 'business_id-created_at-index',
                'KeyConditionExpression': Key('business_id').eq(business_id),
                'Limit': limit,
                'ScanIndexForward': False  # Most recent first
            }
            
            if status:
                kwargs['FilterExpression'] = Attr('status').eq(status)
            
            response = self.leads_table.query(**kwargs)
            return response.get('Items', [])
        except Exception as e:
            logger.error(f"Error listing leads for business {business_id}: {str(e)}")
            raise
    
    async def update_lead(
    self, 
    lead_id: str, 
    business_id: str, 
    updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a lead"""
        try:
            # Build update expression with attribute name mapping for reserved keywords
            update_parts = ["updated_at = :updated_at"]
            expr_values = {':updated_at': datetime.utcnow().isoformat()}
            expr_names = {}
            
            # DynamoDB reserved keywords that need ExpressionAttributeNames
            reserved_keywords = {'status', 'name', 'data', 'timestamp'}
            
            for key, value in updates.items():
                if value is not None:
                    # Check if attribute name is a reserved keyword
                    if key.lower() in reserved_keywords:
                        # Use ExpressionAttributeNames for reserved keywords
                        expr_names[f'#{key}'] = key
                        update_parts.append(f"#{key} = :{key}")
                    else:
                        # Use attribute name directly
                        update_parts.append(f"{key} = :{key}")
                    
                    expr_values[f":{key}"] = value
            
            update_expr = "SET " + ", ".join(update_parts)
            
            # Build the update_item parameters
            update_params = {
                'Key': {
                    'id': lead_id,
                    'business_id': business_id
                },
                'UpdateExpression': update_expr,
                'ExpressionAttributeValues': expr_values,
                'ReturnValues': 'ALL_NEW'
            }
            
            # Only add ExpressionAttributeNames if we have any
            if expr_names:
                update_params['ExpressionAttributeNames'] = expr_names
            
            response = self.leads_table.update_item(**update_params)
            
            updated_item = response.get('Attributes')
            if not updated_item:
                logger.error(f"Update returned no attributes for lead {lead_id}")
                raise Exception(f"Failed to update lead {lead_id}")
            
            logger.info(f"Updated lead: {lead_id}")
            return updated_item
        except Exception as e:
            logger.error(f"Error updating lead {lead_id}: {str(e)}")
            raise
    
    async def delete_lead(self, lead_id: str, business_id: str) -> bool:
        """Delete a lead"""
        try:
            self.leads_table.delete_item(
                Key={'id': lead_id, 'business_id': business_id}
            )
            logger.info(f"Deleted lead: {lead_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting lead {lead_id}: {str(e)}")
            raise
    
    # USER OPERATIONS
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            self.users_table.put_item(Item=user_data)
            logger.info(f"Created user: {user_data['email']}")
            return user_data
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            response = self.users_table.query(
                IndexName='email-index',
                KeyConditionExpression=Key('email').eq(email)
            )
            items = response.get('Items', [])
            return items[0] if items else None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {str(e)}")
            raise

# Singleton instance
_db_instance: Optional[DynamoDBClient] = None

def get_db() -> DynamoDBClient:
    """Get singleton database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = DynamoDBClient()
    return _db_instance

# For backward compatibility
db = get_db()