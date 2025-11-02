from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import mysql.connector

app = FastAPI()

# Load templates folder
templates = Jinja2Templates(directory="templates")

# ✅ Database connection function
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="imdb_movies",
        auth_plugin='mysql_native_password'
    )
# ✅ Home page (renders index.html)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Movies page (renders movies.html)
@app.get("/movies", response_class=HTMLResponse)
async def get_movies(request: Request, search: str = "", genre: str = ""):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM movies WHERE 1=1"
    params = []

    if search:
        query += " AND (Series_Title LIKE %s OR Director LIKE %s)"
        params.extend([f"%{search}%", f"%{search}%"])

    if genre:
        query += " AND Genre LIKE %s"
        params.append(f"%{genre}%")

    cursor.execute(query, params)
    movies = cursor.fetchall()

    conn.close()
    return templates.TemplateResponse(
        "movies.html",
        {"request": request, "movies": movies, "search": search, "genre": genre}
    )

# ✅ API check
@app.get("/api", response_class=HTMLResponse)
async def api_status():
    return {"message": "🎬 IMDB Movie API is running successfully!"}
