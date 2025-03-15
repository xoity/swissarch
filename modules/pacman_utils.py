#!/usr/bin/env python3
# Pacman utilities for SwissArch

import os
import subprocess
import logging
import re

logger = logging.getLogger("SwissArch")

def setup_pacman(enable_ilovecady=False, parallel_downloads=5):
    """
    Setup and optimize pacman configuration
    """
    pacman_conf_path = "/etc/pacman.conf"
    try:
        logger.info("Setting up pacman configuration...")
        
        # Check if we have root permissions
        if os.geteuid() != 0:
            logger.error("Root privileges required to modify pacman configuration.")
            return False
            
        # Backup the original file
        backup_file = f"{pacman_conf_path}.backup"
        if not os.path.exists(backup_file):
            subprocess.run(["cp", pacman_conf_path, backup_file], check=True)
            logger.info(f"Created backup at {backup_file}")
        
        # Read the current pacman.conf
        with open(pacman_conf_path, 'r') as f:
            content = f.read()
        
        # Enable color
        content = re.sub(r'#Color', 'Color', content)
        
        # Enable ILoveCandy if requested
        if enable_ilovecady and "ILoveCandy" not in content:
            content = re.sub(r'# Misc options\n', '# Misc options\nILoveCandy\n', content)
            logger.info("Enabled ILoveCandy option in pacman")
        
        # Enable parallel downloads
        if "ParallelDownloads" not in content:
            content = re.sub(
                r'# Misc options\n',
                f'# Misc options\nParallelDownloads = {parallel_downloads}\n',
                content
            )
        
        # Save the modified content
        with open(pacman_conf_path, 'w') as f:
            f.write(content)
        
        logger.info("Pacman configuration updated successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup pacman: {str(e)}")
        return False

def update_system():
    """
    Update the system packages
    """
    try:
        logger.info("Updating system packages...")
        
        # Check if we have root permissions
        if os.geteuid() != 0:
            logger.error("Root privileges required to update the system.")
            return False
        
        # Update package databases and upgrade
        subprocess.run(["pacman", "-Syyu", "--noconfirm"], check=True)
        
        logger.info("System update completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to update system: {str(e)}")
        return False

def install_packages(package_list):
    """
    Install specified packages with pacman
    
    Args:
        package_list (list): List of packages to install
    """
    try:
        if not package_list:
            logger.error("No packages specified for installation")
            return False
            
        # Check if we have root permissions
        if os.geteuid() != 0:
            logger.error("Root privileges required to install packages.")
            return False
            
        logger.info(f"Installing packages: {', '.join(package_list)}")
        
        # Install the packages with noconfirm
        subprocess.run(["pacman", "-S", "--needed", "--noconfirm"] + package_list, check=True)
        
        logger.info("Packages installed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to install packages: {str(e)}")
        return False

def search_pacman_packages(query):
    """
    Search for packages using pacman
    
    Args:
        query (str): Search query
    """
    try:
        logger.info(f"Searching for packages matching '{query}'")
        
        # Run pacman search
        result = subprocess.run(
            ["pacman", "-Ss", query], 
            capture_output=True, 
            text=True,
            check=True
        )
        
        return result.stdout
        
    except Exception as e:
        logger.error(f"Failed to search packages: {str(e)}")
        return "Error searching packages"