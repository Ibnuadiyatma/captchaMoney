#!/data/data/com.termux/files/usr/bin/bash
# ==========================================
# Setup environment
pkg install python make wget termux-exec clang libjpeg-turbo freetype -y

# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install dependencies with progress
echo "📦 Menginstall dependensi Python..."
pip install requests pycryptodome colorama rich termcolor --progress-bar on

# Install Pillow dengan flag build yang sesuai untuk Termux
CFLAGS="-O2" LDFLAGS="-lm" pip install Pillow --no-cache-dir --progress-bar on

echo "perizinan termux...."
termux-setup-storage
termux-media-scan

echo "============Instalasi selesai=============="