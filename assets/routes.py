from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

@router.get('/image')
async def get_image(filename: str):
    image_path = Path(filename)
    if not image_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(image_path)