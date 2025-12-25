from mcp.server.fastmcp import FastMCP
import httpx

mcp = FastMCP("Agentic Agent Server")

@mcp.tool()
async def get_weather(lat: float, lon: float):
    """Get current weather."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json().get("current_weather", {})
        return f"Temperature: {data.get('temperature')}°C, Windspeed: {data.get('windspeed')}km/h"

@mcp.tool()
async def get_mystery_books(count: int = 2):
    """Fetch mystery book recommendations from Open Library."""
    url = "https://openlibrary.org/subjects/mystery.json?limit=10"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        works = resp.json().get("works", [])
        books = [f"'{w['title']}' by {w['authors'][0]['name']}" for w in works[:count]]
        return " | ".join(books)

@mcp.tool()
async def get_joke():
    """Get a safe one-liner."""
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://v2.jokeapi.dev/joke/Any?safe-mode&type=single")
        return resp.json().get("joke", "Why did the AI cross the road? To reach the other data center.")

@mcp.tool()
async def get_dog_photo():
    """Get a random dog image URL."""
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://dog.ceo/api/breeds/image/random")
        return resp.json().get("message", "No dogs found.")

@mcp.tool()
async def get_trivia():
    """Get one mystery-themed trivia question."""
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://opentdb.com/api.php?amount=1&category=10&type=multiple")
        data = resp.json()["results"][0]
        return f"Question: {data['question']} | Correct Answer: {data['correct_answer']}"

if __name__ == "__main__":
    mcp.run(transport="stdio")