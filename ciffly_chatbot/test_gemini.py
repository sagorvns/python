"""Quick test to find available Gemini models"""
import os
from dotenv import load_dotenv

load_dotenv()

try:
    import google.generativeai as genai
    
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    
    print("Available Gemini models:")
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative approach with langchain...")
    
    from langchain_google_genai import ChatGoogleGenerativeAI
    
    # Try with gemini-1.5-flash (without models/ prefix)
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
        response = llm.invoke("Say 'Hello, Gemini works!'")
        print(f"\n✅ SUCCESS with gemini-1.5-flash!")
        print(f"Response: {response.content}")
    except Exception as e2:
        print(f"❌ Failed with gemini-1.5-flash: {e2}")
