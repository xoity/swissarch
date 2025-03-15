#!/usr/bin/env python3
# SwissArch - Swiss Army Knife for Arch Linux
# An all-in-one tool for Arch Linux system management and customization

import os
import sys
import argparse
import logging

# Import modules
try:
    from modules.pacman_utils import setup_pacman, update_system, install_packages
    from modules.aur_utils import install_aur_helper, search_aur
    from modules.pentest_tools import install_blackarch, install_pentest_tools
    from modules.system_utils import check_system_info, backup_system, optimize_system
    from modules.ui_utils import (
        print_banner,
        print_status,
        get_user_input,
        show_menu,
        confirm_action,
    )
except ImportError:
    print("Error: Required modules not found. Setting up directory structure...")
    # Create module directories if they don't exist
    os.makedirs("modules", exist_ok=True)
    print("Please run the script again after the modules are created.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("swissarch.log"), logging.StreamHandler()],
)
logger = logging.getLogger("SwissArch")


def check_root():
    """Check if the script is run with root privileges"""
    if os.geteuid() != 0:
        logger.warning(
            "Some functions require root privileges. Run with sudo for full functionality."
        )
        return False
    return True


def main():
    """Main function to run the SwissArch tool"""
    parser = argparse.ArgumentParser(
        description="SwissArch - Swiss Army Knife for Arch Linux",
        epilog="Use --help with any subcommand for more information",
    )

    # Main arguments
    parser.add_argument("--version", action="version", version="SwissArch 1.0.0")
    parser.add_argument(
        "--no-color", action="store_true", help="Disable colored output"
    )

    # Subparsers for different functionality groups
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Pacman utilities
    pacman_parser = subparsers.add_parser("pacman", help="Pacman utilities")
    pacman_parser.add_argument(
        "--setup", action="store_true", help="Setup pacman with optimizations"
    )
    pacman_parser.add_argument(
        "--update", action="store_true", help="Update system packages"
    )
    pacman_parser.add_argument(
        "--install", nargs="+", help="Install specified packages"
    )
    pacman_parser.add_argument(
        "--enable-ilovecady",
        action="store_true",
        help='Enable the "ILoveCandy" option in pacman.conf',
    )

    # AUR utilities
    aur_parser = subparsers.add_parser("aur", help="AUR utilities")
    aur_parser.add_argument(
        "--install-helper", choices=["yay", "paru"], help="Install specified AUR helper"
    )
    aur_parser.add_argument("--search", help="Search for packages in AUR")

    # BlackArch and pentesting tools
    pentest_parser = subparsers.add_parser("pentest", help="Pentesting tools")
    pentest_parser.add_argument(
        "--setup-blackarch", action="store_true", help="Setup BlackArch repository"
    )
    pentest_parser.add_argument(
        "--install-tools",
        choices=["basic", "full", "custom"],
        help="Install pentesting tools (basic/full/custom set)",
    )

    # System utilities
    system_parser = subparsers.add_parser("system", help="System utilities")
    system_parser.add_argument(
        "--info", action="store_true", help="Show system information"
    )
    system_parser.add_argument("--backup", help="Backup system to specified location")
    system_parser.add_argument(
        "--optimize", action="store_true", help="Apply system optimizations"
    )

    args = parser.parse_args()

    # Show banner
    print_banner()

    # If no arguments provided, show interactive menu
    if len(sys.argv) == 1 or not args.command:
        show_menu()
        return

    # Handle commands
    if args.command == "pacman":
        if args.setup:
            if confirm_action(
                "Pacman Configuration Setup",
                "This will modify your pacman configuration to enable color,\n"
                f"{'enable ILoveCandy progress bar, ' if args.enable_ilovecady else ''}"
                "and optimize parallel downloads.\n"
                "A backup of your original configuration will be created.",
            ):
                setup_pacman(enable_ilovecady=args.enable_ilovecady)
        if args.update:
            if confirm_action(
                "System Update",
                "This will update all packages on your system.\n"
                "It will download and install the latest versions of all packages.\n"
                "Your system may restart services during this process.",
            ):
                update_system()
        if args.install:
            if confirm_action(
                f"Install Packages: {', '.join(args.install)}",
                "This will install the specified packages on your system.\n"
                "Required dependencies will also be installed automatically.",
            ):
                install_packages(args.install)

    elif args.command == "aur":
        if args.install_helper:
            if confirm_action(
                f"Install AUR Helper: {args.install_helper}",
                "This will install the selected AUR helper on your system.\n"
                "This includes downloading and building the package from AUR.\n"
                "Required build dependencies will also be installed.",
            ):
                install_aur_helper(args.install_helper)
        if args.search:
            search_aur(args.search)

    elif args.command == "pentest":
        if args.setup_blackarch:
            if confirm_action(
                "Install BlackArch Repository",
                "This will add the BlackArch repository to your system.\n"
                "BlackArch contains thousands of security tools and packages.\n"
                "This will modify your pacman configuration files.",
            ):
                install_blackarch()
        if args.install_tools:
            if args.install_tools == "full":
                confirm_msg = "Install Full Penetration Testing Suite"
                details = (
                    "This will install a comprehensive set of penetration testing tools.\n"
                    "This requires significant disk space (5GB+) and download time.\n"
                    "The installation may take 30+ minutes depending on your system."
                )
                default = "no"
            else:
                confirm_msg = (
                    f"Install {args.install_tools.title()} Penetration Testing Tools"
                )
                details = (
                    "This will install selected penetration testing tools.\n"
                    "This may require significant disk space and download time."
                )
                default = "yes"

            if confirm_action(confirm_msg, details, default):
                install_pentest_tools(args.install_tools)

    elif args.command == "system":
        if args.info:
            check_system_info()
        if args.backup:
            if confirm_action(
                "Backup System Configuration",
                f"This will create a backup of your system configuration in:\n"
                f"{args.backup}\n"
                f"Files backed up include system configs like pacman.conf, fstab,\n"
                f"and important user config files like .bashrc and .config files.",
            ):
                backup_system(args.backup)
        if args.optimize:
            if confirm_action(
                "Optimize System",
                "This will perform various system optimizations:\n"
                "- Clean package cache\n"
                "- Remove orphaned packages\n"
                "- Enable fstrim service\n"
                "- Optimize swap settings\n"
                "- Update mirrorlist\n"
                "These changes will improve system performance and disk usage.",
            ):
                optimize_system()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        sys.exit(1)
