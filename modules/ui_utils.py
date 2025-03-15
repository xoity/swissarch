#!/usr/bin/env python3
# UI utilities for SwissArch

import os
import sys
import logging
import shutil
from colorama import init, Fore

# Initialize colorama for cross-platform colored output
init(autoreset=True)

logger = logging.getLogger("SwissArch")

def print_banner():
    """
    Display the SwissArch banner
    """
    terminal_width = shutil.get_terminal_size().columns
    
    # Use a smaller banner if terminal is narrow
    if terminal_width < 80:
        banner = f"""
{Fore.GREEN}╔═══════════════════╗
{Fore.GREEN}║ {Fore.YELLOW}SwissArch {Fore.WHITE}v1.0.0 {Fore.GREEN}║
{Fore.GREEN}╚═══════════════════╝
{Fore.CYAN}The Swiss Army Knife for Arch Linux
"""
    else:
        banner = f"""
{Fore.GREEN}╔═══════════════════════════════════════════════════════════════════════════╗
{Fore.GREEN}║ {Fore.YELLOW} ____            _           {Fore.RED}   _             _        {Fore.GREEN} ║
{Fore.GREEN}║ {Fore.YELLOW}/ ___|_      __ (_) ___ ___ {Fore.RED}  / \\   _ __ ___| |__     {Fore.GREEN} ║
{Fore.GREEN}║ {Fore.YELLOW}\\___ \\ \\ /\\ / / | |/ __/ __| {Fore.RED} / _ \\ | '__/ __| '_ \\   {Fore.GREEN} ║
{Fore.GREEN}║ {Fore.YELLOW} ___) \\ V  V /  | |\\__ \\__ \\ {Fore.RED}/ ___ \\| | | (__| | | |  {Fore.GREEN} ║
{Fore.GREEN}║ {Fore.YELLOW}|____/ \\_/\\_/   |_||___/___/{Fore.RED}/_/   \\_\\_|  \\___|_| |_|  {Fore.GREEN} ║
{Fore.GREEN}║                                                                   {Fore.GREEN} ║
{Fore.GREEN}║            {Fore.CYAN}The Swiss Army Knife for Arch Linux - {Fore.WHITE}v1.0.0{Fore.GREEN}         ║
{Fore.GREEN}╚═══════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def print_status(message, status="info", newline=True):
    """
    Print a status message with appropriate formatting
    
    Args:
        message (str): Message to display
        status (str): Status type - info, success, warning, error
        newline (bool): Whether to print a newline after the message
    """
    prefix = ""
    color = ""
    
    if status == "info":
        prefix = "[*]"
        color = Fore.BLUE
    elif status == "success":
        prefix = "[+]"
        color = Fore.GREEN
    elif status == "warning":
        prefix = "[!]"
        color = Fore.YELLOW
    elif status == "error":
        prefix = "[✗]"
        color = Fore.RED
    elif status == "question":
        prefix = "[?]"
        color = Fore.CYAN
    else:
        prefix = "[-]"
        color = Fore.WHITE
    
    output = f"{color}{prefix} {message}"
    if newline:
        print(output)
    else:
        print(output, end="", flush=True)

def get_user_input(prompt, choices=None, default=None):
    """
    Get input from the user with validation
    
    Args:
        prompt (str): Prompt to display to the user
        choices (list): List of valid choices
        default (str): Default value if user just presses Enter
        
    Returns:
        str: User's choice
    """
    # Format the prompt with choices and default
    if choices:
        choices_str = "/".join(choices)
        if default:
            prompt = f"{prompt} [{choices_str}, default={default}]: "
        else:
            prompt = f"{prompt} [{choices_str}]: "
    elif default:
        prompt = f"{prompt} [default={default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        print_status(prompt, "question", newline=False)
        response = input().strip()
        
        # Use default if response is empty
        if not response and default:
            return default
            
        # Validate against choices if provided
        if choices:
            if response.lower() in [choice.lower() for choice in choices]:
                return response
            else:
                print_status(f"Please enter one of: {', '.join(choices)}", "error")
        else:
            # If no choices to validate against, return the response
            if response or not default:
                return response

def show_progress(total, current=0, prefix='Progress:', suffix='Complete', bar_length=50):
    """
    Display a progress bar
    
    Args:
        total (int): Total number of items
        current (int): Current progress
        prefix (str): Prefix string
        suffix (str): Suffix string
        bar_length (int): Length of the progress bar
    """
    percent = int(100 * (current / float(total)))
    filled_length = int(bar_length * current // total)
    bar = Fore.GREEN + '█' * filled_length + Fore.WHITE + '░' * (bar_length - filled_length)
    
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    
    if current == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

def show_menu():
    """
    Display the interactive menu and handle user choices
    """
    from modules.pacman_utils import setup_pacman, update_system, install_packages
    from modules.aur_utils import install_aur_helper, search_aur, install_aur_package
    from modules.pentest_tools import install_blackarch, install_pentest_tools, list_installed_pentest_tools
    from modules.system_utils import check_system_info, backup_system, optimize_system
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        
        print(f"{Fore.CYAN}╔═══════════════════════════════════════╗")
        print(f"{Fore.CYAN}║  {Fore.WHITE}SwissArch - Main Menu              {Fore.CYAN}║")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}1. {Fore.WHITE}System Information             {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}2. {Fore.WHITE}Package Management            {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}3. {Fore.WHITE}AUR Helper Installation        {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}4. {Fore.WHITE}BlackArch & Penetration Tools  {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}5. {Fore.WHITE}System Maintenance             {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}6. {Fore.WHITE}Backup & Restore               {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}0. {Fore.WHITE}Exit                           {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
        
        choice = get_user_input("Enter your choice", choices=["0", "1", "2", "3", "4", "5", "6"])
        
        # Handle main menu choices
        if choice == "0":
            print_status("Thank you for using SwissArch. Goodbye!", "success")
            sys.exit(0)
            
        elif choice == "1":
            # System Information
            info = check_system_info()
            print(info)
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            # Package Management submenu
            show_package_menu()
            
        elif choice == "3":
            # AUR Helper Installation
            helper = get_user_input("Choose an AUR helper to install", choices=["yay", "paru"])
            result = install_aur_helper(helper)
            if result:
                print_status(f"Successfully installed {helper}", "success")
            else:
                print_status(f"Failed to install {helper}", "error")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            # BlackArch & Penetration Tools submenu
            show_pentest_menu()
            
        elif choice == "5":
            # System Maintenance
            result = optimize_system()
            print(result)
            input("\nPress Enter to continue...")
            
        elif choice == "6":
            # Backup & Restore submenu
            show_backup_menu()

def show_package_menu():
    """
    Display the package management submenu
    """
    from modules.pacman_utils import setup_pacman, update_system, install_packages, search_pacman_packages
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        
        print(f"{Fore.CYAN}╔═══════════════════════════════════════╗")
        print(f"{Fore.CYAN}║  {Fore.WHITE}Package Management               {Fore.CYAN}║")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}1. {Fore.WHITE}Update System                  {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}2. {Fore.WHITE}Search Packages                {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}3. {Fore.WHITE}Install Packages               {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}4. {Fore.WHITE}Setup Pacman (ILoveCandy etc.) {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}0. {Fore.WHITE}Back to Main Menu              {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
        
        choice = get_user_input("Enter your choice", choices=["0", "1", "2", "3", "4"])
        
        if choice == "0":
            return
            
        elif choice == "1":
            # Update System
            print_status("Updating system packages...", "info")
            result = update_system()
            if result:
                print_status("System updated successfully", "success")
            else:
                print_status("Failed to update system", "error")
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            # Search Packages
            query = get_user_input("Enter search query")
            print_status(f"Searching for packages matching '{query}'...", "info")
            results = search_pacman_packages(query)
            print(results)
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            # Install Packages
            packages = get_user_input("Enter package names (space-separated)")
            pkg_list = packages.split()
            if pkg_list:
                result = install_packages(pkg_list)
                if result:
                    print_status("Packages installed successfully", "success")
                else:
                    print_status("Failed to install packages", "error")
            else:
                print_status("No packages specified", "warning")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            # Setup Pacman
            enable_candy = get_user_input("Enable ILoveCandy option?", choices=["yes", "no"], default="yes")
            enable_candy = enable_candy.lower() == "yes"
            
            parallel = get_user_input("Number of parallel downloads", default="5")
            try:
                parallel = int(parallel)
            except ValueError:
                parallel = 5
            
            result = setup_pacman(enable_ilovecady=enable_candy, parallel_downloads=parallel)
            if result:
                print_status("Pacman configuration updated successfully", "success")
            else:
                print_status("Failed to update pacman configuration", "error")
            input("\nPress Enter to continue...")

def show_pentest_menu():
    """
    Display the penetration testing tools submenu
    """
    from modules.pentest_tools import install_blackarch, install_pentest_tools, list_installed_pentest_tools
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        
        print(f"{Fore.CYAN}╔═══════════════════════════════════════╗")
        print(f"{Fore.CYAN}║  {Fore.WHITE}Penetration Testing Tools         {Fore.CYAN}║")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}1. {Fore.WHITE}Install BlackArch Repository    {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}2. {Fore.WHITE}Install Basic Pentest Tools     {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}3. {Fore.WHITE}Install Full Pentest Suite      {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}4. {Fore.WHITE}List Installed Pentest Tools    {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}0. {Fore.WHITE}Back to Main Menu               {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
        
        choice = get_user_input("Enter your choice", choices=["0", "1", "2", "3", "4"])
        
        if choice == "0":
            return
            
        elif choice == "1":
            # Install BlackArch Repository
            print_status("Installing BlackArch repository...", "info")
            result = install_blackarch()
            if result:
                print_status("BlackArch repository installed successfully", "success")
            else:
                print_status("Failed to install BlackArch repository", "error")
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            # Install Basic Pentest Tools
            print_status("Installing basic penetration testing tools...", "info")
            result = install_pentest_tools("basic")
            if result:
                print_status("Basic penetration testing tools installed successfully", "success")
            else:
                print_status("Failed to install penetration testing tools", "error")
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            # Install Full Pentest Suite
            print_status("Installing full penetration testing suite...", "info")
            print_status("This may take a while depending on your internet connection", "warning")
            confirm = get_user_input("Are you sure you want to continue? This will download a lot of packages", 
                                    choices=["yes", "no"], default="no")
            
            if confirm.lower() == "yes":
                result = install_pentest_tools("full")
                if result:
                    print_status("Full penetration testing suite installed successfully", "success")
                else:
                    print_status("Failed to install penetration testing suite", "error")
            else:
                print_status("Installation cancelled", "info")
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            # List Installed Pentest Tools
            print_status("Listing installed penetration testing tools...", "info")
            tool_list = list_installed_pentest_tools()
            print(tool_list)
            input("\nPress Enter to continue...")

def show_backup_menu():
    """
    Display the backup and restore submenu
    """
    from modules.system_utils import backup_system, restore_backup
    
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        
        print(f"{Fore.CYAN}╔═══════════════════════════════════════╗")
        print(f"{Fore.CYAN}║  {Fore.WHITE}Backup & Restore                  {Fore.CYAN}║")
        print(f"{Fore.CYAN}╠═══════════════════════════════════════╣")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}1. {Fore.WHITE}Backup System Configuration     {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}2. {Fore.WHITE}Restore from Backup             {Fore.CYAN}║")
        print(f"{Fore.CYAN}║  {Fore.YELLOW}0. {Fore.WHITE}Back to Main Menu               {Fore.CYAN}║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════╝")
        
        choice = get_user_input("Enter your choice", choices=["0", "1", "2"])
        
        if choice == "0":
            return
            
        elif choice == "1":
            # Backup System Configuration
            backup_dir = get_user_input("Enter backup directory path", default=str(os.path.join(os.path.expanduser("~"), "swissarch_backups")))
            print_status(f"Creating backup in {backup_dir}...", "info")
            result = backup_system(backup_dir)
            print(result)
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            # Restore from Backup
            backup_file = get_user_input("Enter path to backup file (.tar.gz)")
            if not os.path.exists(backup_file):
                print_status("Backup file not found", "error")
                input("\nPress Enter to continue...")
                continue
                
            restore_configs = get_user_input("Restore configuration files?", choices=["yes", "no"], default="yes")
            restore_configs = restore_configs.lower() == "yes"
            
            restore_pkgs = get_user_input("Restore installed packages?", choices=["yes", "no"], default="no")
            restore_pkgs = restore_pkgs.lower() == "yes"
            
            print_status("Restoring from backup...", "info")
            result = restore_backup(
                backup_file, 
                restore_configs=restore_configs,
                restore_packages=restore_pkgs
            )
            
            print(result)
            input("\nPress Enter to continue...")