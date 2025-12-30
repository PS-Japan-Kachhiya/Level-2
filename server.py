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
        return f"Temperature: {data.get('temperature')}°C"

@mcp.tool()
async def get_books(count: int = 2):
    """Fetch  book recommendations from Open Library."""
    url = "https://openlibrary.org/search.json"
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
async def get_photo():
    """Get a random  image URL."""
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://dog.ceo/api/breeds/image/random")
        return resp.json().get("message", "No image found.")

@mcp.tool()
async def get_trivia():
    """Get one mystery-themed trivia question."""
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://opentdb.com/api.php?amount=1&category=10&type=multiple")
        data = resp.json()["results"][0]
        return f"Question: {data['question']} | Correct Answer: {data['correct_answer']}"
    

@mcp.tool()
async def resolve_city_to_latlon(city_name: str):
    """
    Convert city name to latitude/longitude
    and fetch weather using get_weather tool.
    """

    geo_url = (
        "https://geocoding-api.open-meteo.com/v1/search"
        f"?name={city_name}&count=1&language=en&format=json"
    )

    async with httpx.AsyncClient() as client:
        geo_resp = await client.get(geo_url)
        geo_data = geo_resp.json()

    if not geo_data.get("results"):
        return f"❌ Could not find a city named '{city_name}'."

    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]

    weather = await get_weather(lat, lon)

    full_name = f"{location['name']}, {location.get('country', '')}"
    return f"🌍 Weather for {full_name}: {weather}"

if __name__ == "__main__":
    mcp.run(transport="stdio")