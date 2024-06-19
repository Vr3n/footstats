import uvicorn
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
