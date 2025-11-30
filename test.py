import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a valid model from your list
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Generate content
resp = model.generate_content("Say hi!")
print(resp.text)
