from fastapi import Request, HTTPException
from ..core.engine import ComplianceEngine
from ..core.context import ComplianceContext

class ComplianceMiddleware:
    def __init__(self, app, engine: ComplianceEngine):
        self.app = app
        self.engine = engine

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            # In a real middleware, you'd extract body here
            # This is a simplified example for demonstration
            pass 
        
        await self.app(scope, receive, send)

# Helper dependency for FastAPI endpoints
async def validate_compliance(request: dict, engine: ComplianceEngine):
    context = ComplianceContext(
        user_id=request.get("user_id", "anonymous"),
        content=request.get("prompt", ""),
        metadata=request.get("metadata", {})
    )
    report = engine.check(context)
    
    if not report.is_compliant:
        raise HTTPException(status_code=403, detail=report.message)
    
    return context