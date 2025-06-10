from dotenv import load_dotenv
import os

load_dotenv()

MCP_API_URL = os.getenv("MCP_API_URL", '')
API_BASE_URL = os.getenv("PAISA_API_BASE_URL", '')
