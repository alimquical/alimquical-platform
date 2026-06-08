"""Generate PWA icons for Alimquical using Pillow."""
import os
from PIL import Image, ImageDraw, ImageFont


def create_icon(size: int, output_path: str) -> None:
    img = Image.new("RGBA", (size, size), (21, 101, 192, 255))
    draw = ImageDraw.Draw(img)

    # Background gradient effect - darker border
    for i in range(size // 4):
        alpha = int(30 * (1 - i / (size // 4)))
        draw.ellipse(
            [i, i, size - i - 1, size - i - 1],
            outline=(13, 71, 161, alpha),
            width=2,
        )

    # Draw "A" letter
    cx, cy = size // 2, size // 2
    letter_size = size * 0.55
    thickness = max(size // 20, 4)

    # Left leg
    draw.line(
        [(cx - letter_size * 0.4, cy + letter_size * 0.45),
         (cx, cy - letter_size * 0.45)],
        fill=(255, 255, 255, 255),
        width=thickness,
    )
    # Right leg
    draw.line(
        [(cx + letter_size * 0.4, cy + letter_size * 0.45),
         (cx, cy - letter_size * 0.45)],
        fill=(255, 255, 255, 255),
        width=thickness,
    )
    # Cross bar
    bar_y = cy + letter_size * 0.05
    draw.line(
        [(cx - letter_size * 0.25, bar_y),
         (cx + letter_size * 0.25, bar_y)],
        fill=(255, 255, 255, 255),
        width=thickness,
    )

    # AI accent dot - top right
    dot_cx = int(cx + letter_size * 0.45)
    dot_cy = int(cy - letter_size * 0.45)
    dot_r = max(size // 12, 6)
    draw.ellipse(
        [dot_cx - dot_r, dot_cy - dot_r, dot_cx + dot_r, dot_cy + dot_r],
        fill=(66, 165, 245, 255),
    )

    # Sparkle inside dot
    draw.ellipse(
        [dot_cx - dot_r // 3, dot_cy - dot_r // 3, dot_cx + dot_r // 3, dot_cy + dot_r // 3],
        fill=(255, 255, 255, 200),
    )

    img.save(output_path, "PNG")
    print(f"  [OK] {output_path} ({size}x{size})")


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icons_dir = os.path.join(base_dir, "frontend", "public", "icons")
    os.makedirs(icons_dir, exist_ok=True)

    print("Generating PWA icons (Pillow)...")
    create_icon(192, os.path.join(icons_dir, "icon-192.png"))
    create_icon(512, os.path.join(icons_dir, "icon-512.png"))

    # Verify
    print("\nVerification:")
    for name in ["icon-192.png", "icon-512.png"]:
        path = os.path.join(icons_dir, name)
        with Image.open(path) as im:
            print(f"  {name}: {im.size[0]}x{im.size[1]}px, mode={im.mode}, {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
