"""
create_IMG_overlay.py

Overlays intact (IMG_RI) and scrambled (IMG_SC) transparent picture PNGs
onto scrambled backgrounds.

Source figures: PICTURE_*.png  (RGBA, transparent background)
Outputs:
  <output_dir>/IMG_RI/PICTURE_<n>_RI.jpg  – intact figure on background
  <output_dir>/IMG_SC/PICTURE_<n>_SC.jpg  – scrambled figure on background
"""

import csv
import os
import random
from pathlib import Path
import numpy as np
from PIL import Image

# ---------------------------------------------------------------------------
# CONFIGURATION  –  edit these variables
# ---------------------------------------------------------------------------

homedir = Path(os.getenv('HOME'))

# Transparent PNG figures (RGBA)
figures_dir   = homedir / 'toolboxes/votc-langorth/DATA/images_transparent'

# Scrambled background JPGs
scrambled_dir = homedir / 'toolboxes/BfLoc/stimuli/scrambled'

# Output base directory (IMG_RI/ and IMG_SC/ will be created here)
output_base_dir = homedir / 'toolboxes/votc-langorth'

# Scale factor: 1.0 = original size, 1.5 = 50% bigger
scale_factor = 1.5

# Tile size for scrambling (pixels)
tile_size = 20

# Random seed for reproducibility (set to None for a different result each run)
random_seed = None

# CSV mapping file: column A = new INDEX, column D = original multipicID
img2id_csv = homedir / 'toolboxes/votc-langorth/DATA/Img2ID.csv'

# ---------------------------------------------------------------------------


def create_ri_overlay(background_path: Path,
                      figure_path: Path,
                      output_path: Path,
                      scale: float = 1.0) -> None:
    """
    Opens the background, loads the transparent figure (RGBA), scales it,
    centers it on a transparent canvas the same size as the background,
    then composites using the alpha mask so the background stays fully intact.
    Saves as JPG.
    """
    background = Image.open(background_path).convert('RGB')
    pic_w, pic_h = background.size

    figure = Image.open(figure_path).convert('RGBA')
    if scale != 1.0:
        figure = figure.resize(
            (int(figure.width * scale), int(figure.height * scale)),
            Image.Resampling.LANCZOS)

    fig_w, fig_h = figure.size
    overlay = Image.new('RGBA', (pic_w, pic_h), (255, 255, 255, 0))
    paste_x = (pic_w - fig_w) // 2
    paste_y = (pic_h - fig_h) // 2
    overlay.paste(figure, (paste_x, paste_y), figure)

    background.paste(overlay, (0, 0), overlay)
    background.save(output_path, quality=95)


def create_sc_overlay(background_path: Path,
                      figure_path: Path,
                      output_path: Path,
                      scale: float = 1.0,
                      tile_px: int = 10) -> None:
    """
    Scrambles ONLY the tight bounding box of non-transparent pixels in the
    figure (tile_px×tile_px blocks), pastes it back into the figure, then
    centers it on a transparent canvas the same size as the background and
    composites using the alpha mask so the background stays fully intact.
    Saves as JPG.
    """
    background = Image.open(background_path).convert('RGB')
    pic_w, pic_h = background.size

    figure = Image.open(figure_path).convert('RGBA')
    if scale != 1.0:
        figure = figure.resize(
            (int(figure.width * scale), int(figure.height * scale)),
            Image.Resampling.LANCZOS)

    # Find tight bounding box of non-transparent pixels, with padding
    fig_arr = np.array(figure)
    alpha = fig_arr[:, :, 3]
    non_transparent = np.argwhere(alpha > 0)
    if len(non_transparent) == 0:
        y_min, x_min, y_max, x_max = 0, 0, figure.height, figure.width
    else:
        (y_min, x_min) = non_transparent.min(axis=0)
        (y_max, x_max) = non_transparent.max(axis=0)
        y_max += 1
        x_max += 1

    # Expand bbox by padding pixels on all sides (clamped to image bounds)
    pad = 20
    x_min = max(0, x_min - pad)
    y_min = max(0, y_min - pad)
    x_max = min(figure.width,  x_max + pad)
    y_max = min(figure.height, y_max + pad)

    # Crop, scramble, clear original region, then paste scrambled back
    bbox_region = figure.crop((x_min, y_min, x_max, y_max))
    scrambled_bbox = scramble_image(bbox_region, tile_px)
    # Clear the bbox area first so no original pixels bleed through
    figure.paste(Image.new('RGBA', (x_max - x_min, y_max - y_min), (0, 0, 0, 0)), (x_min, y_min))
    figure.paste(scrambled_bbox, (x_min, y_min))

    fig_w, fig_h = figure.size
    overlay = Image.new('RGBA', (pic_w, pic_h), (255, 255, 255, 0))
    paste_x = (pic_w - fig_w) // 2
    paste_y = (pic_h - fig_h) // 2
    overlay.paste(figure, (paste_x, paste_y), figure)

    background.paste(overlay, (0, 0), overlay)
    background.save(output_path, quality=95)



def scramble_image(img: Image.Image, tile_px: int) -> Image.Image:
    """
    Scramble `img` by shuffling tile_px x tile_px pixel blocks.
    The image is first expanded to the next multiple of tile_px (by wrapping
    from the opposite edge) so that no remainder strips are left unscrambled,
    then cropped back to the original size after shuffling.
    """
    img_w, img_h = img.size

    # Pad to next multiple of tile_px so there are no leftover strips
    pad_w = (tile_px - img_w % tile_px) % tile_px
    pad_h = (tile_px - img_h % tile_px) % tile_px
    if pad_w or pad_h:
        padded = Image.new(img.mode, (img_w + pad_w, img_h + pad_h), (0, 0, 0, 0))
        padded.paste(img, (0, 0))
        work = padded
    else:
        work = img.copy()

    work_w, work_h = work.size
    num_tiles_x = work_w // tile_px
    num_tiles_y = work_h // tile_px

    tiles = [
        work.crop((tx * tile_px, ty * tile_px,
                   (tx + 1) * tile_px, (ty + 1) * tile_px))
        for ty in range(num_tiles_y)
        for tx in range(num_tiles_x)
    ]
    random.shuffle(tiles)

    scrambled = Image.new(img.mode, (work_w, work_h), (0, 0, 0, 0))
    for idx, tile in enumerate(tiles):
        tx = idx % num_tiles_x
        ty = idx // num_tiles_x
        scrambled.paste(tile, (tx * tile_px, ty * tile_px))

    # Crop back to original size
    return scrambled.crop((0, 0, img_w, img_h))


def main():
    if random_seed is not None:
        random.seed(random_seed)

    # Collect transparent PNG figures and background files
    fig_paths = sorted(figures_dir.glob('PICTURE_*.png'))
    bg_paths  = sorted(scrambled_dir.glob('*.jpg'))

    if not fig_paths:
        raise FileNotFoundError(f"No PICTURE_*.png files found in {figures_dir}")
    if not bg_paths:
        raise FileNotFoundError(f"No background JPGs found in {scrambled_dir}")

    # Sample one background per figure without replacement (cycle if needed)
    if len(bg_paths) >= len(fig_paths):
        sampled_bgs = random.sample(bg_paths, len(fig_paths))
    else:
        sampled_bgs = [bg_paths[random.randint(0, len(bg_paths) - 1)]
                       for _ in fig_paths]

    # Create output dirs
    out_ri_dir = output_base_dir / 'IMG_RI'
    out_sc_dir = output_base_dir / 'IMG_SC'
    out_ri_dir.mkdir(parents=True, exist_ok=True)
    out_sc_dir.mkdir(parents=True, exist_ok=True)

    for i, (fig_path, bg_path) in enumerate(zip(fig_paths, sampled_bgs)):
        stem = fig_path.stem   # e.g. "PICTURE_100"

        # ---- Intact figure overlaid on background ----
        ri_out = out_ri_dir / f'{stem}_RI.jpg'
        create_ri_overlay(bg_path, fig_path, ri_out, scale=scale_factor)

        # ---- Scrambled figure overlaid on background ----
        sc_out = out_sc_dir / f'{stem}_SC.jpg'
        create_sc_overlay(bg_path, fig_path, sc_out, scale=scale_factor, tile_px=tile_size)

        print(f'[{i+1}/{len(fig_paths)}]  {fig_path.name}  ->  RI: {ri_out.name}  |  SC: {sc_out.name}')

    # --- Rename files using Img2ID.csv mapping ---
    # Build dict: multipicID (str) -> INDEX (str)
    id_map = {}
    with open(img2id_csv, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            id_map[row['multipicID'].strip()] = row['INDEX'].strip()

    renamed = 0
    for pic_id, new_idx in id_map.items():
        ri_old = out_ri_dir / f'PICTURE_{pic_id}_RI.jpg'
        sc_old = out_sc_dir / f'PICTURE_{pic_id}_SC.jpg'
        ri_new = out_ri_dir / f'IMG_RI-{new_idx}.jpg'
        sc_new = out_sc_dir / f'IMG_SC-{new_idx}.jpg'
        if ri_old.exists():
            ri_old.rename(ri_new)
            renamed += 1
        if sc_old.exists():
            sc_old.rename(sc_new)
            renamed += 1

    print(f'Renamed {renamed} files using {img2id_csv.name}')
    print(f'\nDone!  Outputs saved to: {output_base_dir}')


if __name__ == '__main__':
    main()
