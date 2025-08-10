import os
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

# Get the MongoDB URI from environment variables for security
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "attendance_db")

class AsyncDatabase:
    """
    A singleton class to manage the asynchronous MongoDB connection.
    This ensures that only one client is created and shared across the application.
    """
    _client: Optional[AsyncIOMotorClient] = None
    _db = None

    @classmethod
    async def connect(cls):
        """Initializes the MongoDB client and database connection."""
        if cls._client is None:
            # Use AsyncIOMotorClient for non-blocking database operations
            cls._client = AsyncIOMotorClient(MONGO_URI)
            cls._db = cls._client[DATABASE_NAME]
            print("MongoDB connection established.")

    @classmethod
    async def close(cls):
        """Closes the MongoDB client connection."""
        if cls._client:
            cls._client.close()
            cls._client = None
            print("MongoDB connection closed.")

    @classmethod
    def get_db(cls):
        """Returns the database instance."""
        if cls._db is None:
            raise ConnectionError("Database connection not established. Call connect() first.")
        return cls._db

