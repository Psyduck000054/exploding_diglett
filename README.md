# Exploding Diglett!

Exploding Diglett! is my second Python project—a procedural map generator for a physical board game of the same name. It uses Perlin noise algorithms to create random, unique, and playable maps featuring diverse terrain types and special elements like dragons, runes, and regional anomalies. The generated maps are intended to be used as a reference during gameplay.

-- TECHNICAL HIGHLIGHTS --

+ Procedural terrain generation using fractal Perlin noise (multiple octaves with configurable roughness and scale)
+ Deterministic RNG based on SHA256 hashing, allowing reproducible maps from a seed value
+ Rich tile system with 7 terrain types: abyss, deep sea, shallow sea, beach, grassland, desert, badlands, and lava
+ Special 3×3 cell in-game features including dragons, rune chests/beacons, oases, mineshafts, fruit trees, coconut canopies, and sharks
+ Configurable parameters in "constants.py" for map size, spawn rates, separation distances, and more
+ Pygame visualization with rotational variants for tiles and proper layering of 3×3 objects

-- SETUP -- [Copy these lines into Terminal to install the source code]

git clone https://github.com/Psyduck000054/exploding_diglett.git
cd exploding_diglett
pip install -r requirements.txt

-- RUN --
Run main.py
