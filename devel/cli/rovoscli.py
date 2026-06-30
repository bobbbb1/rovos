import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ROVOS Python Engine")
    parser.add_argument("-v", "--version", action="store_true", help="Version check")
    parser.add_argument("-u", "--update", action="store_true", help="update package")

    subparsers = parser.add_subparsers(dest="command")
    
    run_parser = subparsers.add_parser("run", help="Jalankan satu file node robot (.py)")
    run_parser.add_argument("package", help="Nama folder package di src/")
    run_parser.add_argument("node", help="Nama file script .py target")

    launch_parser = subparsers.add_parser("launch", help="Jalankan skema multi-node dari file .launch.py")
    launch_parser.add_argument("package", help="Nama folder package di src/")
    launch_parser.add_argument("launch_file", help="Nama file .launch.py")

    where_parser = subparsers.add_parser("where", help="Mencari Package")
    where_parser.add_argument("package", help="Nama folder package di src/")

    args = parser.parse_args()

    if args.command == "run":
        from ws._run import run_node
        run_node(args.package, args.node)
    elif args.command == "launch":
        from ws._launch import launch_workspace
        launch_workspace(args.package, args.launch_file)
    elif args.command == "where":
        from ws._where import where_package
        where_package(args.package)
    elif args.version:
        from default._version import version_check
        version_check()
    elif args.update:
        from default._update import update_package
        update_package()
    else:
        parser.print_help()