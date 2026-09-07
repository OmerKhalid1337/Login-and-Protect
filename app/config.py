import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
PORT: int = int(os.getenv("PORT", "8000"))
HOST: str = os.getenv("HOST", "0.0.0.0")

def get_supabase_client() -> Client:
    """Initialize and return the Supabase client using environment variables."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "SUPABASE_URL and SUPABASE_KEY must be set in the .env file. "
            "Please check your .env configuration."
        )
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize a global supabase client instance
try:
    supabase: Client = get_supabase_client()
except ValueError:
    supabase = None  # type: ignore
