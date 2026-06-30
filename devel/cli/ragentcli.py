import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="RAGENT Python Engine")

    parser.add_argument("-v", "--version", action="store_true", help="Version check")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("build", help="Verifikasi syntax kode dan buat folder build otomatis")

    create_parser = subparsers.add_parser("create_pkg", help="Buat paket baru + package(.xml)")
    create_parser.add_argument("package", help="Nama folder package")

    create_parser.add_argument(
        "depends", 
        nargs="*", 
        help="Daftar dependensi (bisa kosong, satu, atau banyak, dipisah spasi)"
    )

    remove_parser = subparsers.add_parser("remove_pkg", help="Hapus paket")
    remove_parser.add_argument("package", help="Nama folder package")

    args = parser.parse_args()

    if args.version:
        from agent._agtversion import agent_version_check
        agent_version_check()
    elif args.command == "build":
        from agent._build import build_workspace
        build_workspace()
    elif args.command == "create_pkg":
        from agent._create import create_package
        create_package(args.package, args.depends)
    elif args.command == "remove_pkg":
        from agent._remove import remove_package
        remove_package(args.package)
    else:
        parser.print_help()