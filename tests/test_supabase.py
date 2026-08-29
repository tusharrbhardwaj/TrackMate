from app.supabase import supabase

response = supabase.storage.from_("proofs").list()
print(response)