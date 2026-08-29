import os
from supabase import create_client

# Creating supabase client to communicate to it directly
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)