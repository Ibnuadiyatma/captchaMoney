#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# ======================================================
# 🎨 Warna terminal
def merah(text): return f"\033[91m{text}\033[0m"
def hijau(text): return f"\033[92m{text}\033[0m"
def kuning(text): return f"\033[93m{text}\033[0m"
def biru(text): return f"\033[94m{text}\033[0m"
def ungu(text): return f"\033[95m{text}\033[0m"
def cyan(text): return f"\033[96m{text}\033[0m"
def abu(text): return f"\033[90m{text}\033[0m"

# ======================================================
# 🧹 Bersihkan layar
def clear():
    os.system("clear" if os.name != "nt" else "cls")

# ======================================================
# 🏷️ Header tampilan utama
def header():
    print(cyan("╔═══════════════════════════════════════╗"))
    print(cyan("║           🤖 CAPTCHA BOT v3.0          ║"))
    print(cyan("║         Created by AbyazTech           ║"))
    print(cyan("╚═══════════════════════════════════════╝\n"))