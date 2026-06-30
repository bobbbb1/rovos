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

def create_package(pkg_name, depends):
    """Membuat folder package baru dan menghasilkan package.xml"""
    
    # 1. VALIDASI UTAMA: Folder 'src' WAJIB ADA
    if not os.path.exists(WS_SRC_PATH) or not os.path.isdir(WS_SRC_PATH):
        print("[\033[91mERROR\033[0m] Gagal! Folder '\033[93msrc\033[0m' tidak ditemukan di workspace ini.")
        print(f"         Pastikan Anda berada di direktori workspace yang benar: {WS_PATH}")
        sys.exit(1)

    # Tentukan path target package
    pkg_path = os.path.join(WS_SRC_PATH, pkg_name)

    # 2. VALIDASI DUPLIKASI: Cek apakah package sudah ada
    if not os.path.exists(pkg_path):
        print(f"[\033[94mCREATE\033[0m] Target Workspace: {WS_PATH}")
        print(f"[\033[94mCREATE\033[0m] Started Create Package '{pkg_name}'...")
    else:
        print(f"[\033[91mERROR\033[0m] Package '{pkg_name}' sudah ada di: {WS_SRC_PATH}")
        return

    # 3. PROSES PEMBUATAN FOLDER & XML
    try:
        # Buat folder package langsung
        os.makedirs(pkg_path, exist_ok=True)
        
        # Panggil fungsi generator XML
        generate_pkg_xml(pkg_path, depends)
        print(f"[\033[92mSUCCESS\033[0m] Package '{pkg_name}' berhasil dibuat!")

    except Exception as e:
        print(f"[\033[91mERROR\033[0m] Gagal membuat package: {e}")
        sys.exit(1)
    

def generate_pkg_xml(pkg_path, depends, silent=False):
    """
    Generator XML untuk package baru (Menggunakan List agar berurutan)
    """
    pkg_name = os.path.basename(pkg_path)
    target_xml_file = os.path.join(pkg_path, "package.xml")

    if not silent:
        print(f"[\033[94mMSG\033[0m] [{pkg_name}] Generating package.xml...")

    # Menggunakan List [] supaya urutan XML dari atas ke bawah konsisten
    xml_lines = [
        '<?xml version="1.0"?>',
        '<package format="3">',
        f'  <name>{pkg_name}</name>',
        '  <version>1.0.0</version>',
        f'  <description>Package {pkg_name}</description>',
        '  <maintainer email="mars@rovos.com">mars</maintainer>',
        '  <license>MIT</license>',
        ''
    ]

    # Tambahkan dependensi jika dimasukkan oleh user
    for depend in depends:
        xml_lines.append(f'  <depend>{depend}</depend>')

    xml_lines.append('')
    xml_lines.append('</package>')

    # Tulis string list tersebut ke dalam file package.xml murni
    try:
        with open(target_xml_file, "w") as f:
            f.write("\n".join(xml_lines))
    except Exception as e:
        print(f"[\033[91mERROR\033[0m] Gagal menulis file package.xml: {e}")
        raise e