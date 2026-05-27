import os
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ──────────────────────────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────────────────────────
homedir    = os.getenv('HOME')
repo_root  = os.path.join(homedir, 'toolboxes/votc-langorth')

csv_path        = os.path.join(homedir, 'Downloads/VOT_chinese_words.csv')
backgrounds_dir = os.path.join(homedir, 'toolboxes/BfLoc/stimuli/scrambled')
transbg_ff_dir  = os.path.join(repo_root, 'DATA/CN_material/Transbg_CN_FF')

zh_font_path = '/Library/Fonts/MacKTGB2312.ttf'
en_font_path = '/Library/Fonts/Arial Unicode.ttf'

ch_rw_dir  = os.path.join(repo_root, 'CH_RW')
ch_sc_dir  = os.path.join(repo_root, 'CH_SC')
en_rw_dir  = os.path.join(repo_root, 'EN_RW')
en_sc_dir  = os.path.join(repo_root, 'EN_SC')
en_ff_dir  = os.path.join(repo_root, 'EN_FF')
ch_ff_dir  = os.path.join(repo_root, 'CH_FF')
lang_sc_dir = os.path.join(repo_root, 'Lang_SC')

# ──────────────────────────────────────────────────────────────────
# Georgian substitution table (same as gen_FF-list_from_RW-list.py)
# ──────────────────────────────────────────────────────────────────
LATIN_TO_GEO = {
    'a': 'ა', 'e': 'ე', 'i': 'ი', 'o': 'ო', 'u': 'უ',
    'b': 'ბ', 'd': 'დ', 'f': 'ფ', 'g': 'გ', 'h': 'ჰ',
    'j': 'ჯ', 'k': 'კ', 'l': 'ლ', 'm': 'მ', 'n': 'ნ',
    'p': 'პ', 'q': 'ქ', 'r': 'რ', 's': 'ს', 't': 'ტ',
    'w': 'წ', 'x': 'ხ', 'z': 'ზ',
}

def to_geo(word):
    return ''.join(LATIN_TO_GEO.get(c.lower(), c) for c in word)

# ──────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────
def load_word_list(path):
    words = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            zh = parts[0].strip("'")
            en = parts[1].strip("'")
            words.append((zh, en))
    return words

def get_image_files(directory):
    supported = {'.jpeg', '.jpg', '.png', '.bmp', '.gif'}
    return [os.path.join(directory, fname)
            for fname in os.listdir(directory)
            if os.path.splitext(fname)[1].lower() in supported]

def get_font(font_path, text, max_width, start_size=225, min_size=40):
    """Return the largest TrueType font that renders text within max_width."""
    size = start_size
    while size >= min_size:
        fnt = ImageFont.truetype(font_path, size)
        bbox = fnt.getbbox(text)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            return fnt
        size -= 10
    return ImageFont.truetype(font_path, min_size)

# ──────────────────────────────────────────────────────────────────
# Image creators
# ──────────────────────────────────────────────────────────────────
def create_word_on_bg(bg_path, output_path, word, fnt):
    """White word centered on a scrambled grayscale background."""
    bg = Image.open(bg_path)          # 1024×1024 L (grayscale)
    draw = ImageDraw.Draw(bg)
    bbox = draw.textbbox((0, 0), word, font=fnt)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    W, H = bg.size
    # Subtract bbox origin to correct for font bearing offset
    draw.text(
        ((W - w) / 2 - bbox[0], (H - h) / 2 - bbox[1]),
        word, font=fnt,
        fill=255, stroke_width=2, stroke_fill=255
    )
    bg.save(output_path, 'JPEG')


def create_scrambled_word_on_bg(bg_path, output_path, word, fnt, tile_size=15):
    """
    Scramble the word bounding box with tile_size×tile_size pixel tiles
    and overlay it centered on the same scrambled background as the RW.
    Matches the logic in create_fLoc_jpg_from_wordlist.py.
    """
    bg = Image.open(bg_path)          # 1024×1024 L
    W, H = bg.size

    # Render word as white text on a transparent RGBA canvas
    txt = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)
    bbox = d.textbbox((0, 0), word, font=fnt)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (W - w) / 2
    ty = (H - h) / 2
    d.text((tx, ty), word, font=fnt, fill=(255, 255, 255),
           stroke_width=2, stroke_fill="white")

    # Crop just the text bounding box region
    placed_bbox = d.textbbox((tx, ty), word, font=fnt)
    txtbox = txt.crop(placed_bbox)

    # Tile and shuffle (10×10 px)
    num_tiles_x = w // tile_size
    num_tiles_y = h // tile_size
    tiles = [
        txtbox.crop((x * tile_size, y * tile_size,
                     (x + 1) * tile_size, (y + 1) * tile_size))
        for y in range(num_tiles_y)
        for x in range(num_tiles_x)
    ]
    random.shuffle(tiles)

    scrambled = Image.new("RGBA", (num_tiles_x * tile_size,
                                   num_tiles_y * tile_size), (255, 255, 255, 0))
    for i, tile in enumerate(tiles):
        gx = i % num_tiles_x
        gy = i // num_tiles_x
        scrambled.paste(tile, (gx * tile_size, gy * tile_size))

    # Composite onto background
    bg_rgb = bg.convert("RGB")
    bg_rgb.paste(scrambled, ((W - scrambled.width) // 2,
                             (H - scrambled.height) // 2), scrambled)
    bg_rgb.convert("L").save(output_path, "JPEG")


def create_ch_ff(bg_path, output_path, n_chars, ff_image_paths, gap=-3):
    """
    Tile n_chars randomly chosen Transbg_CN_FF images horizontally,
    centered on a scrambled grayscale background.
    """
    chosen = (random.sample(ff_image_paths, n_chars)
              if n_chars <= len(ff_image_paths)
              else random.choices(ff_image_paths, k=n_chars))

    imgs = [Image.open(p).convert('RGBA') for p in chosen]

    # Scale to 0.8 of original size
    imgs = [img.resize((int(img.width * 0.8), int(img.height * 0.8)),
                       Image.Resampling.LANCZOS) for img in imgs]

    # Uniform height: scale each image to match the tallest
    target_h = max(img.height for img in imgs)
    scaled = []
    for img in imgs:
        if img.height != target_h:
            ratio = target_h / img.height
            img = img.resize((int(img.width * ratio), target_h),
                             Image.Resampling.LANCZOS)
        scaled.append(img)

    total_w = sum(img.width for img in scaled) + gap * (n_chars - 1)

    bg = Image.open(bg_path).convert('RGB')
    W, H = bg.size

    # Scale down if the tiled row is wider than the canvas (minus margin)
    if total_w > W - 40:
        ratio = (W - 40) / total_w
        scaled = [img.resize((int(img.width * ratio), int(img.height * ratio)),
                              Image.Resampling.LANCZOS)
                  for img in scaled]
        total_w = sum(img.width for img in scaled) + gap * (n_chars - 1)
        target_h = max(img.height for img in scaled)

    x = (W - total_w) // 2
    y = (H - target_h) // 2

    for img in scaled:
        bg.paste(img, (x, y), img)
        x += img.width + gap

    bg.convert('L').save(output_path, 'JPEG')


# ──────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────
def main():
    for d in [ch_rw_dir, ch_sc_dir, en_rw_dir, en_sc_dir, en_ff_dir, ch_ff_dir]:
        os.makedirs(d, exist_ok=True)

    words     = load_word_list(csv_path)
    bg_paths  = get_image_files(backgrounds_dir)
    ff_images = get_image_files(transbg_ff_dir)

    canvas_width = 1024 - 80   # leave 40 px margin each side
    n = len(words)

    # Draw n unique backgrounds per category (without replacement).
    # CN_SC shares backgrounds with CH_RW; EN_SC shares with EN_RW.
    bg_ch_rw = random.sample(bg_paths, n)   # also used for CN_SC
    bg_en_rw = random.sample(bg_paths, n)   # also used for EN_SC
    bg_en_ff = random.sample(bg_paths, n)
    bg_ch_ff = random.sample(bg_paths, n)

    print(f"Generating {n} stimuli × 4 categories …")

    for idx, (zh_word, en_word) in enumerate(words):
        item_id  = idx + 1
        geo_word = to_geo(en_word)

        # CH_RW — Chinese real word (楷书 font, white) on scrambled bg
        zh_fnt = get_font(zh_font_path, zh_word, canvas_width)
        create_word_on_bg(
            bg_ch_rw[idx],
            os.path.join(ch_rw_dir, f'CH_RW-{item_id}.jpg'),
            zh_word, zh_fnt,
        )

        # CN_SC — scrambled version of CH_RW, same background
        create_scrambled_word_on_bg(
            bg_ch_rw[idx],
            os.path.join(ch_sc_dir, f'CH_SC-{item_id}.jpg'),
            zh_word, zh_fnt,
        )

        # EN_RW — English real word on scrambled bg
        en_rw_fnt = get_font(en_font_path, en_word, canvas_width)
        create_word_on_bg(
            bg_en_rw[idx],
            os.path.join(en_rw_dir, f'EN_RW-{item_id}.jpg'),
            en_word, en_rw_fnt,
        )

        # EN_SC — scrambled version of EN_RW, same background
        create_scrambled_word_on_bg(
            bg_en_rw[idx],
            os.path.join(en_sc_dir, f'EN_SC-{item_id}.jpg'),
            en_word, en_rw_fnt,
        )

        # EN_FF — English → Georgian letter-substitution on scrambled bg
        en_fnt = get_font(en_font_path, geo_word, canvas_width)
        create_word_on_bg(
            bg_en_ff[idx],
            os.path.join(en_ff_dir, f'EN_FF-{item_id}.jpg'),
            geo_word, en_fnt,
        )

        # CH_FF — N Transbg_CN_FF tiles (N = # of Chinese characters)
        create_ch_ff(
            bg_ch_ff[idx],
            os.path.join(ch_ff_dir, f'CH_FF-{item_id}.jpg'),
            len(zh_word), ff_images,
        )

        print(f"  [{item_id:02d}/80]  CH_RW:{zh_word}  "
              f"EN_FF:{geo_word}  CH_FF:{len(zh_word)} tile(s)")

    # Lang_SC — randomly draw 40 from CH_SC and 40 from EN_SC, mixed
    import shutil
    ch_sc_files = sorted([f for f in os.listdir(ch_sc_dir)
                          if f.endswith('.jpg') and 'online' not in f])
    en_sc_files = sorted([f for f in os.listdir(en_sc_dir) if f.endswith('.jpg')])
    pool = ([('CH_SC', f) for f in random.sample(ch_sc_files, 40)] +
            [('EN_SC', f) for f in random.sample(en_sc_files, 40)])
    random.shuffle(pool)
    os.makedirs(lang_sc_dir, exist_ok=True)
    for i, (src_dir, fname) in enumerate(pool):
        shutil.copy2(os.path.join(repo_root, src_dir, fname),
                     os.path.join(lang_sc_dir, f'Lang_SC-{i+1}.jpg'))
    print(f"  Lang_SC → {lang_sc_dir}  "
          f"(CH:{sum(1 for d,_ in pool if d=='CH_SC')}  "
          f"EN:{sum(1 for d,_ in pool if d=='EN_SC')})")

    print(f"\nDone!\n"
          f"  CH_RW → {ch_rw_dir}\n"
          f"  EN_FF → {en_ff_dir}\n"
          f"  CH_FF → {ch_ff_dir}")


if __name__ == '__main__':
    main()
