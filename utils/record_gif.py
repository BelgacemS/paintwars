#!/usr/bin/env python3
"""
Enregistre un match Paint Wars et le sauvegarde en GIF.
Usage: python utils/record_gif.py [arena_id] [position] [config]
  arena_id  : 0-4 ou 0-9 avec config_Paintwars_eval (defaut: 0)
  position  : True/False (defaut: False)
  config    : config_Paintwars ou config_Paintwars_eval (defaut: config_Paintwars)
"""

import sys, os

_arena_id = int(sys.argv[1]) if len(sys.argv) > 1 else 0
_position = sys.argv[2] if len(sys.argv) > 2 else "False"
_config = sys.argv[3] if len(sys.argv) > 3 else "config_Paintwars"

frames = []
frame_count = [0]
frame_interval = 1  # capture chaque frame affichee

# Monkey-patch pygame.display.flip pour capturer les frames
import pygame
_original_flip = pygame.display.flip

def _capturing_flip():
    _original_flip()
    frame_count[0] += 1
    if frame_count[0] % frame_interval == 0:
        surface = pygame.display.get_surface()
        if surface:
            data = pygame.image.tobytes(surface, 'RGB')
            size = surface.get_size()
            frames.append((data, size))

pygame.display.flip = _capturing_flip

# Lancer la simulation depuis src/
src_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src')
os.chdir(src_dir)
sys.path.insert(0, src_dir)
sys.argv = ['tetracomposibot.py', _config, str(_arena_id), _position, '0']

exec(open('tetracomposibot.py').read())

# Assembler le GIF
from PIL import Image

images = []
for data, size in frames:
    img = Image.frombytes('RGB', size, data)
    images.append(img)

if images:
    output_dir = os.path.join('..', 'assets')
    os.makedirs(output_dir, exist_ok=True)
    output = os.path.join(output_dir, f'arena_{_arena_id}.gif')
    # on prend 1 frame sur 6 pour un GIF rapide et leger
    images_sampled = images[::6]
    images_sampled[0].save(
        output,
        save_all=True,
        append_images=images_sampled[1:],
        duration=40,
        loop=0,
        optimize=True
    )
    print(f"\nGIF sauvegarde : {output} ({len(images_sampled)} frames)")
else:
    print("Aucune frame capturee")
