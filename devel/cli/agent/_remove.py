#!/usr/bin/env python3
import os
import sys
import shutil

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

def remove_package(pkg_name):
    """Hapus folder package beserta seluruh isinya secara permanen"""
    
    # 1. VALIDASI UTAMA: Folder 'src' WAJIB ADA
    if not os.path.exists(WS_SRC_PATH) or not os.path.isdir(WS_SRC_PATH):
        print("[\033[91mERROR\033[0m] Gagal! Folder '\033[93msrc\033[0m' tidak ditemukan di workspace ini.")
        print(f"         Pastikan Anda berada di direktori workspace yang benar: {WS_PATH}")
        sys.exit(1)

    # Tentukan path target package
    pkg_path = os.path.join(WS_SRC_PATH, pkg_name)

    # 2. VALIDASI KEBERADAAN PACKAGE
    if os.path.exists(pkg_path) and os.path.isdir(pkg_path):
        print(f"[\033[94mREMOVE\033[0m] Target Workspace: {WS_PATH}")
        print(f"[\033[94mREMOVE\033[0m] Started Remove Package '{pkg_name}'...")
    else:
        print(f"[\033[91mERROR\033[0m] Package '{pkg_name}' tidak ditemukan di: {WS_SRC_PATH}")
        return

    # 3. PROSES EKSEKUSI PENGHAPUSAN
    try:
        # shutil.rmtree akan menghapus folder package + package.xml + semua kode di dalamnya
        shutil.rmtree(pkg_path)

        print(f"[\033[92mSUCCESS\033[0m] Package '{pkg_name}' berhasil dihapus secara permanen!")

    except Exception as e:
        print(f"[\033[91mERROR\033[0m] Gagal menghapus package: {e}")
        sys.exit(1)