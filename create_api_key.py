import asyncio

from app.providers.database import AsyncSessionLocal
from app.utils.api_key import create_api_key_record


async def main():
    name = input("Enter API Key name: ")
    
    async with AsyncSessionLocal() as session:
        api_key_record, key = await create_api_key_record(name, session)
        
        print("\n" + "="*60)
        print("✅ API Key created successfully!")
        print("="*60)
        print(f"ID:         {api_key_record.id}")
        print(f"Name:       {api_key_record.name}")
        print(f"Prefix:     {api_key_record.prefix}")
        print(f"Created:    {api_key_record.created_at}")
        print(f"Active:     {api_key_record.is_active}")
        print("="*60)
        print(f"\n🔑 API Key: {key}")
        print("\n⚠️  IMPORTANT: Save this key securely!")
        print("   This is the only time you'll see the full key.")
        print("="*60)
        print("\n📝 Example usage:")
        print(f'   curl -H "X-API-Key: {key}" http://your-domain.com/api/endpoint')
        print("\n💡 Note: Requests from localhost don't require API key during development")
        print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
