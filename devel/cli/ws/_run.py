#!/usr/bin/env python3
import os
import sys
import json
import subprocess

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

CORE_ROOT_PATH = os.path.normpath(os.path.join(DEVEL_PATH, "..")) 
CORE_DEVEL_PATH = os.path.join(CORE_ROOT_PATH, "devel")
CORE_INSTALL_PATH = os.path.join(CORE_ROOT_PATH, "install")

WS_PATH = os.getcwd() 
WS_SRC_PATH = os.path.join(WS_PATH, "src")
WS_DEVEL_PATH = os.path.join(WS_PATH, "devel")
WS_BUILD_PATH = os.path.join(WS_PATH, "build")

def get_node_absolute_path(package, node_script, packages_cache):
    """Helper untuk mengambil path absolut dari suatu node script"""
    if package not in packages_cache:
        return None
    return os.path.normpath(os.path.join(packages_cache[package], package, node_script))

def run_node(package, node_script):
    """Menjalankan satu Node tunggal secara blocking"""
    cache_file = os.path.join(WS_BUILD_PATH, "workspace_cache.json")
    if not os.path.exists(cache_file):
        print(f"[\033[91mERROR\033[0m] Build folder not found! Please rebuild.")
        return

    with open(cache_file, "r") as f:
        packages = json.load(f)

    node_path = get_node_absolute_path(package, node_script, packages)
    if not node_path or not os.path.exists(node_path):
        print(f"[\033[91mERROR\033[0m] Script '{node_script}' not found in package '{package}'!")
        return

    print(f"[\033[94mRUN\033[0m] Running {node_script} from package...")
    try:
        subprocess.run([sys.executable, node_path], check=True)
    except (KeyboardInterrupt, subprocess.CalledProcessError):
        pass