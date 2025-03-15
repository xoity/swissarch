#!/usr/bin/env python3
# SwissArch - Swiss Army Knife for Arch Linux
# An all-in-one tool for Arch Linux system management and customization

import os
import sys
import argparse
import subprocess
import shutil
import logging
import getpass
from pathlib import Path
from datetime import datetime

# Import modules
try:
    from modules.pacman_utils import setup_pacman, update_system, install_packages
    from modules.aur_utils import install_aur_helper, search_aur
    from modules.pentest_tools import install_blackarch, install_pentest_tools
    from modules.system_utils import check_system_info, backup_system, optimize_system
    from modules.ui_utils import print_banner, print_status, get_user_input, show_menu
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
    handlers=[
        logging.FileHandler("swissarch.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SwissArch")

def check_root():
    """Check if the script is run with root privileges"""
    if os.geteuid() != 0:
        logger.warning("Some functions require root privileges. Run with sudo for full functionality.")
        return False
    return True

def main():
    """Main function to run the SwissArch tool"""
    parser = argparse.ArgumentParser(
        description="SwissArch - Swiss Army Knife for Arch Linux",
        epilog="Use --help with any subcommand for more information"
    )
    
    # Main arguments
    parser.add_argument('--version', action='version', version='SwissArch 1.0.0')
    parser.add_argument('--no-color', action='store_true', help='Disable colored output')
    
    # Subparsers for different functionality groups
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Pacman utilities
    pacman_parser = subparsers.add_parser('pacman', help='Pacman utilities')
    pacman_parser.add_argument('--setup', action='store_true', help='Setup pacman with optimizations')
    pacman_parser.add_argument('--update', action='store_true', help='Update system packages')
    pacman_parser.add_argument('--install', nargs='+', help='Install specified packages')
    pacman_parser.add_argument('--enable-ilovecady', action='store_true', 
                              help='Enable the "ILoveCandy" option in pacman.conf')
    
    # AUR utilities
    aur_parser = subparsers.add_parser('aur', help='AUR utilities')
    aur_parser.add_argument('--install-helper', choices=['yay', 'paru'], 
                           help='Install specified AUR helper')
    aur_parser.add_argument('--search', help='Search for packages in AUR')
    
    # BlackArch and pentesting tools
    pentest_parser = subparsers.add_parser('pentest', help='Pentesting tools')
    pentest_parser.add_argument('--setup-blackarch', action='store_true', 
                               help='Setup BlackArch repository')
    pentest_parser.add_argument('--install-tools', choices=['basic', 'full', 'custom'], 
                               help='Install pentesting tools (basic/full/custom set)')
    
    # System utilities
    system_parser = subparsers.add_parser('system', help='System utilities')
    system_parser.add_argument('--info', action='store_true', help='Show system information')
    system_parser.add_argument('--backup', help='Backup system to specified location')
    system_parser.add_argument('--optimize', action='store_true', 
                              help='Apply system optimizations')
    
    args = parser.parse_args()

    # Show banner
    print_banner()
    
    # If no arguments provided, show interactive menu
    if len(sys.argv) == 1 or not args.command:
        show_menu()
        return
    
    # Handle commands
    if args.command == 'pacman':
        if args.setup:
            setup_pacman(enable_ilovecady=args.enable_ilovecady)
        if args.update:
            update_system()
        if args.install:
            install_packages(args.install)
            
    elif args.command == 'aur':
        if args.install_helper:
            install_aur_helper(args.install_helper)
        if args.search:
            search_aur(args.search)
            
    elif args.command == 'pentest':
        if args.setup_blackarch:
            install_blackarch()
        if args.install_tools:
            install_pentest_tools(args.install_tools)
            
    elif args.command == 'system':
        if args.info:
            check_system_info()
        if args.backup:
            backup_system(args.backup)
        if args.optimize:
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