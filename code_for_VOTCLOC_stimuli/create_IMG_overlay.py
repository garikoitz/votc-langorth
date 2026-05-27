"""
create_IMG_overlay.py

Reads Img2ID.csv to select the 80 matched PICTURE_*.png files, then overlays
them (intact and scrambled) onto unique scrambled backgrounds.

Outputs (in repo root):
  IMG_RI/IMG_RI-{INDEX}.jpg  – intact figure on background
  IMG_SC/IMG_SC-{INDEX}.jpg  – scrambled figure on background
"""

import csv
import os
import random
from pathlib import Path
import numpy as np
from PIL import Image

# ──────────────────────────────────────────────────────────────────
# CONFIGURATION
# ──────────────────────────────────────────────────────────────────
homedir = Path(os.getenv('HOME'))
repo_root = homedir / 'toolboxes/votc-langorth'

figures_dir   = repo_root / 'DATA/images_transparent'
scrambled_dir = homedir   / 'toolboxes/BfLoc/stimuli/scrambled'
img2id_csv    = repo_root / 'DATA/Img2ID.csv'
output_base   = repo_root

scale_factor = 1.8    # 1.5 (previous) × 1.2 = 1.8
tile_size    = 15     # scramble tile size in pixels

# ──────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────
def scramble_image(img: Image.Image, tile_px: int) -> Image.Image:
    img_w, img_h = img.size
    pad_w = (tile_px - img_w % tile_px) % tile_px
    pad_h = (tile_px - img_h % tile_px) % tile_px
    if pad_w or pad_h:
        padded = Image.new(img.mode, (img_w + pad_w, img_h + pad_h), (0, 0, 0, 0))
        padded.paste(img, (0, 0))
        work = padded
    else:
        work = img.copy()

    nw, nh = work.size
    nx, ny = nw // tile_px, nh // tile_px
    tiles = [work.crop((tx * tile_px, ty * tile_px,
                        (tx + 1) * tile_px, (ty + 1) * tile_px))
             for ty in range(ny) for tx in range(nx)]
    random.shuffle(tiles)
    out = Image.new(img.mode, (nw, nh), (0, 0, 0, 0))
    for idx, tile in enumerate(tiles):
        out.paste(tile, ((idx % nx) * tile_px, (idx // nx) * tile_px))
    return out.crop((0, 0, img_w, img_h))


def create_ri_overlay(bg_path, fig_path, out_path, scale):
    bg  = Image.open(bg_path).convert('RGB')
    W, H = bg.size
    fig = Image.open(fig_path).convert('RGBA')
    fig = fig.resize((int(fig.width * scale), int(fig.height * scale)),
                     Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    canvas.paste(fig, ((W - fig.width) // 2, (H - fig.height) // 2), fig)
    bg.paste(canvas, (0, 0), canvas)
    bg.convert('L').save(out_path, 'JPEG')


def create_sc_overlay(bg_path, fig_path, out_path, scale, tile_px):
    bg  = Image.open(bg_path).convert('RGB')
    W, H = bg.size
    fig = Image.open(fig_path).convert('RGBA')
    fig = fig.resize((int(fig.width * scale), int(fig.height * scale)),
                     Image.Resampling.LANCZOS)

    # Tight bounding box of non-transparent pixels + padding
    arr   = np.array(fig)
    nz    = np.argwhere(arr[:, :, 3] > 0)
    if len(nz):
        (y0, x0), (y1, x1) = nz.min(axis=0), nz.max(axis=0)
        pad = 20
        x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
        x1 = min(fig.width,  x1 + 1 + pad)
        y1 = min(fig.height, y1 + 1 + pad)
    else:
        x0, y0, x1, y1 = 0, 0, fig.width, fig.height

    bbox_region   = fig.crop((x0, y0, x1, y1))
    scrambled_box = scramble_image(bbox_region, tile_px)
    fig.paste(Image.new('RGBA', (x1 - x0, y1 - y0), (0, 0, 0, 0)), (x0, y0))
    fig.paste(scrambled_box, (x0, y0))

    canvas = Image.new('RGBA', (W, H), (255, 255, 255, 0))
    canvas.paste(fig, ((W - fig.width) // 2, (H - fig.height) // 2), fig)
    bg.paste(canvas, (0, 0), canvas)
    bg.convert('L').save(out_path, 'JPEG')


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────
def main():
    # Read CSV: INDEX → multipicID
    index_to_picid = {}
    with open(img2id_csv, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            index_to_picid[row['INDEX'].strip()] = row['multipicID'].strip()

    # Build ordered list of (index, fig_path), skip missing files
    entries = []
    for idx, picid in sorted(index_to_picid.items(), key=lambda x: int(x[0])):
        fig_path = figures_dir / f'PICTURE_{picid}.png'
        if fig_path.exists():
            entries.append((idx, fig_path))
        else:
            print(f'  WARNING: {fig_path.name} not found, skipping index {idx}')

    # Collect backgrounds and sample without replacement — same bg for RI & SC pair
    bg_paths = sorted(scrambled_dir.glob('*.jpg'))
    if len(bg_paths) >= len(entries):
        sampled_bgs = random.sample(bg_paths, len(entries))
    else:
        sampled_bgs = [random.choice(bg_paths) for _ in entries]

    # Output dirs
    ri_dir = output_base / 'IMG_RI'
    sc_dir = output_base / 'IMG_SC'
    ri_dir.mkdir(parents=True, exist_ok=True)
    sc_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {len(entries)} IMG stimuli  "
          f"(scale={scale_factor}, tile={tile_size}px) …")

    for (idx, fig_path), bg_path in zip(entries, sampled_bgs):
        ri_out = ri_dir / f'IMG_RI-{idx}.jpg'
        sc_out = sc_dir / f'IMG_SC-{idx}.jpg'
        create_ri_overlay(bg_path, fig_path, ri_out, scale_factor)
        create_sc_overlay(bg_path, fig_path, sc_out, scale_factor, tile_size)
        print(f'  [{idx:>2}]  {fig_path.name}  →  RI + SC')

    print(f'\nDone!\n  IMG_RI → {ri_dir}\n  IMG_SC → {sc_dir}')


if __name__ == '__main__':
    main()
