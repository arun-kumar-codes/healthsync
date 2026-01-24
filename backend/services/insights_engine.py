from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

router = APIRouter()

class HealthInsightRequest(BaseModel):
    user_id: str
    health_data: dict

class HealthInsightResponse(BaseModel):
    insights: str

# Initialize OpenAI with your API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key not found in environment variables.")

llm = OpenAI(api_key=openai_api_key)

# Define a prompt template for generating health insights
prompt_template = PromptTemplate(
    input_variables=["health_data"],
    template="Based on the following health data: {health_data}, provide personalized health insights."
)

insight_chain = LLMChain(llm=llm, prompt=prompt_template)

@router.post("/generate-insights", response_model=HealthInsightResponse)
async def generate_insights(request: HealthInsightRequest):
    try:
        # Validate user_id and health_data
        if not request.user_id or not isinstance(request.health_data, dict):
            raise HTTPException(status_code=400, detail="Invalid user_id or health_data.")

        # Generate insights using the LangChain
        insights = insight_chain.run(health_data=request.health_data)

        return HealthInsightResponse(insights=insights)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))