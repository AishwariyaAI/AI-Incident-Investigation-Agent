from groq import Groq
import os
from dotenv import load_dotenv

# -----------------------
# LOAD ENV VARIABLES
# -----------------------
load_dotenv()

# -----------------------
# INIT GROQ CLIENT
# -----------------------
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------
# ROOT CAUSE ANALYZER
# -----------------------
def analyze_root_cause(incident):

    prompt = f"""
    You are a senior Site Reliability Engineer (SRE).

    Analyze this incident:

    {incident}

    Provide:
    1. Root Cause
    2. Risk Level
    3. Fix Recommendation
    4. Prevention Strategy
    """

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content