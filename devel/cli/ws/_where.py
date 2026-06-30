#!/usr/bin/env python3
import os
import sys

# =======================================================================
# [HARD PROTECTION: ENVIRONMENT VALIDATION]
# =======================================================================
if "ROVOS_WS_ACTIVE" not in os.environ:
    print("[\033[91mERROR\033[0m] Workspace Environment Not Activated!")
    print("-----------------------------------------------------------------------")
    sys.exit(1)

# =======================================================================
# [PATH CONFIGURATION] 
# =======================================================================
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
CLI_PATH = os.path.normpath(os.path.join(CUR_PATH, "..")) 
DEVEL_PATH = os.path.normpath(os.path.join(CLI_PATH, "..")) 

WS_PATH = os.getcwd() 
WS_SRC_PATH = os.path.join(WS_PATH, "src")

def where_package(pkg_name):
    """Mencari lokasi package dan mencetak path murninya"""
    
    # 1. VALIDASI UTAMA: Folder 'src' WAJIB ADA
    # Gunakan sys.stderr agar pesan error tidak sengaja terbaca sebagai path tujuan
    if not os.path.exists(WS_SRC_PATH) or not os.path.isdir(WS_SRC_PATH):
        print(f"[\033[91mERROR\033[0m] Folder 'src' tidak ditemukan di: {WS_PATH}", file=sys.stderr)
        sys.exit(1)

    # Tentukan path target package
    pkg_path = os.path.join(WS_SRC_PATH, pkg_name)

    # 2. VALIDASI KEBERADAAN PACKAGE
    if os.path.exists(pkg_path) and os.path.isdir(pkg_path):
        # Cetak path murni tanpa hiasan apa pun agar bisa ditangkap terminal dengan aman
        print(pkg_path)
    else:
        print(f"[\033[91mERROR\033[0m] Package '{pkg_name}' tidak ditemukan di: {WS_SRC_PATH}", file=sys.stderr)
        sys.exit(1)