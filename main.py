from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from PIL import Image
import io
from typing import List
from generate_image import circle_crop, find_safe_edge_positions
import json
from pydantic import BaseModel

class ProfileRequest(BaseModel):
    image_urls: List[str]


app = FastAPI()

@app.post("/generate-family-tree")
async def generate_family_tree(
    profile_request: ProfileRequest
):
    image_urls = profile_request.image_urls
    base_img = Image.open("base_tree.png").convert("RGBA")
    circle_size = 30
    positions = find_safe_edge_positions(base_img, required_count=len(image_urls), circle_size=circle_size)

    canvas = base_img.copy()
    radius = circle_size // 2
    for url, (x, y) in zip(image_urls, positions):
        profile = circle_crop(url, circle_size)
        canvas.paste(profile, (x - radius, y - radius), profile)

    buffer = io.BytesIO()
    canvas.save(buffer, format="PNG")
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")