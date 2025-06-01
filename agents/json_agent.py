import json
from pydantic import BaseModel, ValidationError

class OrderSchema(BaseModel):
    order_id: str
    customer: str
    items: list

class JSONAgent:
    def process(self, content):
        try:
            data = json.loads(content)
            validated = OrderSchema(**data)
            return {
                "status": "success",
                "data": validated.dict(),
                "anomalies": self._find_anomalies(validated)
            }
        except (json.JSONDecodeError, ValidationError) as e:
            return {"status": "error", "message": str(e)}
    
    def _find_anomalies(self, data):
        anomalies = []
        # Simple anomaly check - you can add more
        if len(data.items) == 0:
            anomalies.append("No items in order")
        return anomalies
