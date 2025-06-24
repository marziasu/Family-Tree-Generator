import io, random, requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, ImageFilter
import math


# ── 1️⃣  base tree যাতে trunk+branches আছে
base_tree_path = "base_tree.png"       # ← এখানে আপনার লোকাল PNG (টার্গেট) দিন
base_img = Image.open(base_tree_path).convert("RGBA")

# ── 2️⃣  তিনটি profile ছবির URL
image_urls = [
    "https://randomuser.me/api/portraits/men/1.jpg",
    "https://randomuser.me/api/portraits/women/2.jpg",
    "https://randomuser.me/api/portraits/men/3.jpg",
    "https://randomuser.me/api/portraits/men/10.jpg",
    "https://randomuser.me/api/portraits/women/12.jpg",
    "https://randomuser.me/api/portraits/men/25.jpg",
    "https://randomuser.me/api/portraits/women/30.jpg",
    "https://randomuser.me/api/portraits/men/40.jpg",
    "https://randomuser.me/api/portraits/women/45.jpg",
    "https://randomuser.me/api/portraits/men/50.jpg",
    "https://randomuser.me/api/portraits/women/55.jpg",
    "https://randomuser.me/api/portraits/men/60.jpg",
    "https://randomuser.me/api/portraits/women/65.jpg",
    "https://randomuser.me/api/portraits/men/1.jpg",
    "https://randomuser.me/api/portraits/women/2.jpg",
    "https://randomuser.me/api/portraits/men/3.jpg",
    "https://randomuser.me/api/portraits/men/10.jpg",
    "https://randomuser.me/api/portraits/women/12.jpg",
    "https://randomuser.me/api/portraits/men/25.jpg",
    "https://randomuser.me/api/portraits/women/30.jpg",
    "https://randomuser.me/api/portraits/men/40.jpg",
    "https://randomuser.me/api/portraits/women/45.jpg",
    "https://randomuser.me/api/portraits/men/50.jpg",
    "https://randomuser.me/api/portraits/women/55.jpg",
    "https://randomuser.me/api/portraits/men/60.jpg",
    "https://randomuser.me/api/portraits/women/65.jpg",
    "https://randomuser.me/api/portraits/men/1.jpg",
    "https://randomuser.me/api/portraits/women/2.jpg",
    "https://randomuser.me/api/portraits/men/3.jpg",
    "https://randomuser.me/api/portraits/men/10.jpg",
    "https://randomuser.me/api/portraits/women/12.jpg",
    "https://randomuser.me/api/portraits/men/25.jpg",
    "https://randomuser.me/api/portraits/women/30.jpg",
    "https://randomuser.me/api/portraits/men/40.jpg",
    "https://randomuser.me/api/portraits/women/45.jpg",
    "https://randomuser.me/api/portraits/men/50.jpg",
    "https://randomuser.me/api/portraits/women/55.jpg",
    "https://randomuser.me/api/portraits/men/60.jpg",
    "https://randomuser.me/api/portraits/women/65.jpg",
    "https://randomuser.me/api/portraits/men/1.jpg",
    "https://randomuser.me/api/portraits/women/2.jpg",
    "https://randomuser.me/api/portraits/men/3.jpg",
    "https://randomuser.me/api/portraits/men/10.jpg",
    "https://randomuser.me/api/portraits/women/12.jpg",
    "https://randomuser.me/api/portraits/men/25.jpg",
    "https://randomuser.me/api/portraits/women/30.jpg",
    "https://randomuser.me/api/portraits/men/40.jpg",
    "https://randomuser.me/api/portraits/women/45.jpg",
    "https://randomuser.me/api/portraits/men/50.jpg",
    "https://randomuser.me/api/portraits/women/55.jpg",
    "https://randomuser.me/api/portraits/men/60.jpg",
    "https://randomuser.me/api/portraits/women/65.jpg"
]
circle_size = 30  # px ব্যাসার্ধ
# ── helper: download + circular‑crop
def circle_crop(url, size):
    img = Image.open(io.BytesIO(requests.get(url, timeout=20).content)).convert("RGBA")
    img = ImageOps.fit(img, (size, size))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size-1, size-1), fill=255)
    circled = Image.new("RGBA", (size, size))
    circled.paste(img, (0, 0), mask=mask)
    return circled

# ── 3️⃣ Detect random leaf-like edge positions
def find_safe_edge_positions(img, required_count, circle_size, y_max_ratio=0.6):
    radius = circle_size // 2
    min_distance = circle_size  # Minimum center-to-center distance to avoid touching

    grayscale = img.convert("L").filter(ImageFilter.FIND_EDGES)
    bw = grayscale.point(lambda x: 255 if x > 40 else 0, mode='1')

    edge_pixels = [
        (x, y) for y in range(int(img.height * y_max_ratio))
               for x in range(img.width)
               if bw.getpixel((x, y)) == 255
    ]

    # Filter out those near the image edges
    safe_pixels = [
        (x, y) for (x, y) in edge_pixels
        if (radius <= x < img.width - radius) and (radius <= y < img.height - radius)
    ]

    # Select non-overlapping positions
    selected_positions = []
    for candidate in random.sample(safe_pixels, len(safe_pixels)):
        too_close = any(
            math.hypot(candidate[0] - existing[0], candidate[1] - existing[1]) < min_distance
            for existing in selected_positions
        )
        if not too_close:
            selected_positions.append(candidate)
        if len(selected_positions) == required_count:
            break

    return selected_positions

if __name__ == "__main__":
    positions = find_safe_edge_positions(base_img, required_count=len(image_urls), circle_size=circle_size)
    print(f"Found edge positions: {positions}")
    print(f"Requested: {len(image_urls)} → Got: {len(positions)}")


    # ── overlay
    canvas = base_img.copy()
    for url, (x, y) in zip(image_urls, positions):
        profile = circle_crop(url, circle_size)
        canvas.paste(profile, (x - circle_size//2, y - circle_size//2), profile)

    out_path = Path("family_tree_final.png")
    canvas.save(out_path)
    print(f"✅ Saved → {out_path.absolute()}")
