import os

GOOGLE_API_KEY = "AIzaSyDV3ekXPf9rQOxhx-nHaiYrpMF8KIBQ340"
# Add other LLM keys here if needed

def setEnvironment():
    varDict = globals().items()
    for key, value in varDict:
        if "API" in key or "ID" in key:
            os.environ[ key ] = value