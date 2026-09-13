"""
Centralized texture manager — loads all HUD icon textures once from disk
and shares them across every UI component that needs them.

Usage:
    tm = TextureManager.get()
    tm.load_all()                          # call once at startup
    tm.tyres["SOFT"]                       # → arcade.Texture
    tm.weather["rain"]                     # → arcade.Texture
    tm.controls["play"]                    # → arcade.Texture
"""

import os
from typing import Dict
import arcade


class TextureManager:
    _instance: "TextureManager | None" = None

    @classmethod
    def get(cls) -> "TextureManager":
        if cls._instance is None:
            cls._instance = TextureManager()
        return cls._instance

    # ── public dict-like accessors ──────────────────────────────────────────
    tyres:   Dict[str, arcade.Texture] = {}
    weather: Dict[str, arcade.Texture] = {}
    controls: Dict[str, arcade.Texture] = {}

    def load_all(self, base_path: str = ".") -> None:
        """Load every icon folder once. Safe to call multiple times."""
        self.tyres   = self._load_folder(os.path.join(base_path, "images", "tyres"))
        self.weather = self._load_folder(os.path.join(base_path, "images", "weather"))
        self.controls = self._load_folder(os.path.join(base_path, "images", "controls"))

    # ── internal ────────────────────────────────────────────────────────────
    @staticmethod
    def _load_folder(path: str) -> Dict[str, arcade.Texture]:
        out: Dict[str, arcade.Texture] = {}
        if not os.path.isdir(path):
            return out
        for fn in os.listdir(path):
            if fn.lower().endswith((".png", ".jpg", ".jpeg")):
                name = os.path.splitext(fn)[0]
                out[name] = arcade.load_texture(os.path.join(path, fn))
        return out
