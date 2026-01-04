"""Router Agent implementation."""
import time
from typing import Dict, Any
from tools.llm.providers.factory import get_llm_provider
from tools.llm.prompts.router_prompts import get_classification_prompt, get_classification_schema
from tools.database.postgres import get_db_session
from tools.database.models.classification import Classification as ClassificationModel
from tools.database.models.ticket import Ticket
from app.models.classification import ClassificationResponse
from tools.monitoring.metrics import get_metrics_collector


class RouterAgent:
    """Router Agent - classifies tickets into categories."""
    
    def __init__(self):
        """Initialize Router Agent."""
        try:
            self.llm = get_llm_provider()
            self.metrics = get_metrics_collector()
        except Exception as e:
            import logging
            logging.error(f"Failed to initialize Router Agent: {e}")
            raise
    
    async def classify(self, ticket_id: str, ticket_text: str) -> ClassificationResponse:
        """
        Classify a ticket into a category.
        
        Args:
            ticket_id: Ticket ID
            ticket_text: Ticket text
            
        Returns:
            Classification result
        """
        start_time = time.time()
        
        try:
            # Get classification prompt
            prompt = get_classification_prompt(ticket_text)
            schema = get_classification_schema()
            
            # Call LLM
            result = await self.llm.generate_json(
                prompt=prompt,
                schema=schema,
                temperature=0.3  # Lower temperature for more consistent classification
            )
            
            # Create response
            classification = ClassificationResponse(
                ticket_id=ticket_id,
                category=result.get("category", "OTHER"),
                subcategory=result.get("subcategory"),
                confidence=result.get("confidence", 0.0),
                reason=result.get("reason")
            )
            
            # Save to database (non-blocking - continue even if DB is unavailable)
            try:
                await self._save_classification(ticket_id, classification)
            except Exception as db_error:
                # Log but don't fail the request if DB is unavailable
                import logging
                logging.warning(f"Failed to save classification to database: {db_error}")
            
            # Record metrics
            duration = time.time() - start_time
            self.metrics.record_agent_call("router", True, duration)
            
            return classification
            
        except Exception as e:
            duration = time.time() - start_time
            self.metrics.record_agent_call("router", False, duration)
            raise
    
    async def _save_classification(
        self,
        ticket_id: str,
        classification: ClassificationResponse
    ):
        """Save classification to database."""
        async for session in get_db_session():
            # Get ticket UUID
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                # Ticket might not exist yet, skip saving
                return
            
            # Create classification record
            db_classification = ClassificationModel(
                ticket_id=ticket.ticket_id,
                category=classification.category,
                subcategory=classification.subcategory,
                confidence=classification.confidence,
                reason=classification.reason,
                agent_version="1.0.0"
            )
            
            session.add(db_classification)
            await session.commit()
            break

