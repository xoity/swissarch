#!/usr/bin/env python3
# System utilities for SwissArch

import os
import subprocess
import logging
import shutil
import platform
import psutil
import datetime
import tarfile
import tempfile
from pathlib import Path

logger = logging.getLogger("SwissArch")


def check_system_info():
    """
    Collect and display system information
    """
    try:
        logger.info("Collecting system information...")

        system_info = {
            "Hostname": platform.node(),
            "Kernel": platform.release(),
            "Architecture": platform.machine(),
            "CPU": platform.processor(),
            "CPU Cores": psutil.cpu_count(logical=False),
            "CPU Logical Cores": psutil.cpu_count(logical=True),
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "Memory Total": f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            "Memory Used": f"{psutil.virtual_memory().used / (1024**3):.2f} GB",
            "Memory Free": f"{psutil.virtual_memory().free / (1024**3):.2f} GB",
            "Disk Usage": {},
        }

        # Get disk usage for all mounted partitions
        for partition in psutil.disk_partitions():
            if os.path.exists(partition.mountpoint):
                usage = psutil.disk_usage(partition.mountpoint)
                system_info["Disk Usage"][partition.mountpoint] = {
                    "Total": f"{usage.total / (1024**3):.2f} GB",
                    "Used": f"{usage.used / (1024**3):.2f} GB",
                    "Free": f"{usage.free / (1024**3):.2f} GB",
                    "Percent Used": f"{usage.percent}%",
                }

        # Get package counts
        try:
            pacman_count = subprocess.run(
                ["pacman", "-Q"], capture_output=True, text=True
            )
            system_info["Installed Packages"] = len(pacman_count.stdout.splitlines())
        except:
            system_info["Installed Packages"] = "Unknown"

        # Format and return the information
        result = "\n=== System Information ===\n"

        for key, value in system_info.items():
            if key != "Disk Usage":
                result += f"{key}: {value}\n"

        result += "\n=== Disk Usage ===\n"
        for mount, usage in system_info["Disk Usage"].items():
            result += f"{mount}:\n"
            for k, v in usage.items():
                result += f"  {k}: {v}\n"

        return result

    except Exception as e:
        logger.error(f"Error collecting system info: {str(e)}")
        return f"Error collecting system information: {str(e)}"


def backup_system(backup_path):
    """
    Create a backup of important system files

    Args:
        backup_path (str): Path where the backup will be stored
    """
    try:
        logger.info(f"Creating system backup at {backup_path}...")

        # Create timestamp for the backup
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"swissarch_backup_{timestamp}.tar.gz"
        full_backup_path = os.path.join(backup_path, backup_filename)

        # Create backup directory if it doesn't exist
        os.makedirs(backup_path, exist_ok=True)

        # List of important directories and files to back up
        backup_paths = [
            "/etc/pacman.conf",
            "/etc/pacman.d/mirrorlist",
            "/etc/fstab",
            "/etc/hosts",
            "/etc/hostname",
            "/etc/locale.conf",
            "/etc/mkinitcpio.conf",
            "/etc/default/grub",
        ]

        # Add home directory configuration files
        home = str(Path.home())
        for config_file in [
            ".bashrc",
            ".zshrc",
            ".vimrc",
            ".config/i3/config",
            ".config/sway/config",
            ".xinitrc",
            ".Xresources",
        ]:
            full_path = os.path.join(home, config_file)
            if os.path.exists(full_path):
                backup_paths.append(full_path)

        # Create backup tar.gz file
        with tarfile.open(full_backup_path, "w:gz") as tar:
            for path in backup_paths:
                if os.path.exists(path):
                    logger.info(f"Adding {path} to backup")
                    # Add the file with an appropriate internal path
                    if path.startswith(home):
                        arcname = os.path.join(
                            "home_config", os.path.relpath(path, home)
                        )
                    else:
                        arcname = path.lstrip("/")

                    tar.add(path, arcname=arcname)
                else:
                    logger.warning(f"Path {path} does not exist, skipping")

        # Include a list of installed packages
        pkg_list_file = os.path.join(backup_path, f"installed_packages_{timestamp}.txt")
        subprocess.run(["pacman", "-Q"], stdout=open(pkg_list_file, "w"), check=True)

        logger.info(f"System backup completed: {full_backup_path}")
        logger.info(f"Package list saved: {pkg_list_file}")

        return f"Backup completed successfully:\n- System files: {full_backup_path}\n- Package list: {pkg_list_file}"

    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return f"Backup failed: {str(e)}"


def optimize_system():
    """
    Apply various system optimizations
    """
    try:
        logger.info("Applying system optimizations...")

        optimizations_applied = []

        # Check if running as root
        if os.geteuid() != 0:
            logger.error("Root privileges required for system optimization")
            return "Error: Root privileges required for system optimization"

        # 1. Clean package cache
        logger.info("Cleaning package cache...")
        subprocess.run(["pacman", "-Sc", "--noconfirm"], check=True)
        optimizations_applied.append("Cleaned package cache")

        # 2. Remove orphaned packages
        logger.info("Removing orphaned packages...")
        orphans = subprocess.run(["pacman", "-Qtdq"], capture_output=True, text=True)
        if orphans.stdout:
            # If there are orphans, remove them
            orphan_list = orphans.stdout.strip().split("\n")
            subprocess.run(["pacman", "-Rns", "--noconfirm"] + orphan_list, check=True)
            optimizations_applied.append(
                f"Removed {len(orphan_list)} orphaned packages"
            )
        else:
            optimizations_applied.append("No orphaned packages found")

        # 3. Enable systemd services for better performance
        services_to_enable = ["fstrim.timer"]
        for service in services_to_enable:
            try:
                subprocess.run(["systemctl", "enable", service], check=True)
                subprocess.run(["systemctl", "start", service], check=True)
                optimizations_applied.append(f"Enabled and started {service}")
            except subprocess.CalledProcessError:
                logger.warning(f"Could not enable {service}")

        # 4. Set up better swappiness value for better performance
        try:
            with open("/etc/sysctl.d/99-swappiness.conf", "w") as f:
                f.write("vm.swappiness=10\n")
            subprocess.run(["sysctl", "vm.swappiness=10"], check=True)
            optimizations_applied.append("Set vm.swappiness to 10")
        except:
            logger.warning("Could not set swappiness parameter")

        # 5. Update mirrorlist to get fastest mirrors
        try:
            if shutil.which("reflector"):
                logger.info("Updating mirrorlist with reflector...")
                subprocess.run(
                    [
                        "reflector",
                        "--latest",
                        "10",
                        "--protocol",
                        "https",
                        "--sort",
                        "rate",
                        "--save",
                        "/etc/pacman.d/mirrorlist",
                    ],
                    check=True,
                )
                optimizations_applied.append("Updated mirrorlist with fastest mirrors")
            else:
                logger.info("Reflector not installed, skipping mirrorlist update")
        except:
            logger.warning("Could not update mirrorlist")

        # Return summary
        result = "System optimizations applied:\n"
        for item in optimizations_applied:
            result += f"- {item}\n"

        return result

    except Exception as e:
        logger.error(f"Optimization failed: {str(e)}")
        return f"Optimization failed: {str(e)}"


def restore_backup(backup_file, restore_configs=True, restore_packages=False):
    """
    Restore system from a backup

    Args:
        backup_file (str): Path to the backup tar.gz file
        restore_configs (bool): Whether to restore configuration files
        restore_packages (bool): Whether to reinstall packages from the backup list
    """
    try:
        logger.info(f"Restoring from backup: {backup_file}")

        # Check if running as root for certain operations
        if restore_configs and os.geteuid() != 0:
            logger.error("Root privileges required to restore configuration files")
            return "Error: Root privileges required to restore configuration files"

        # Create temporary directory for extraction
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract the backup archive
            logger.info(f"Extracting backup to {temp_dir}")
            with tarfile.open(backup_file, "r:gz") as tar:
                tar.extractall(path=temp_dir)

            # Restore configuration files
            if restore_configs:
                logger.info("Restoring configuration files...")

                # Restore system configuration files
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        rel_path = os.path.relpath(os.path.join(root, file), temp_dir)

                        # Skip home_config directory as it's handled separately
                        if rel_path.startswith("home_config"):
                            continue

                        # Determine target path
                        target_path = os.path.join("/", rel_path)
                        target_dir = os.path.dirname(target_path)

                        # Create directory if it doesn't exist
                        os.makedirs(target_dir, exist_ok=True)

                        # Copy the file
                        logger.info(f"Restoring {target_path}")
                        shutil.copy2(os.path.join(root, file), target_path)

                # Restore home configuration files
                home_config_dir = os.path.join(temp_dir, "home_config")
                if os.path.isdir(home_config_dir):
                    home = str(Path.home())
                    for root, dirs, files in os.walk(home_config_dir):
                        for file in files:
                            src_path = os.path.join(root, file)
                            rel_path = os.path.relpath(src_path, home_config_dir)
                            target_path = os.path.join(home, rel_path)
                            target_dir = os.path.dirname(target_path)

                            # Create directory if it doesn't exist
                            os.makedirs(target_dir, exist_ok=True)

                            # Copy the file
                            logger.info(f"Restoring {target_path}")
                            shutil.copy2(src_path, target_path)

            # Restore packages if requested
            if restore_packages:
                # Find package list file in the same directory as backup_file
                backup_dir = os.path.dirname(backup_file)
                pkg_list_files = [
                    f
                    for f in os.listdir(backup_dir)
                    if f.startswith("installed_packages_") and f.endswith(".txt")
                ]

                if pkg_list_files:
                    # Use the most recent package list if multiple exist
                    pkg_list_file = os.path.join(backup_dir, sorted(pkg_list_files)[-1])
                    logger.info(f"Reinstalling packages from {pkg_list_file}")

                    # Read package list
                    with open(pkg_list_file, "r") as f:
                        packages = [line.split()[0] for line in f.readlines()]

                    # Reinstall packages in batches to avoid command line length limits
                    batch_size = 20
                    for i in range(0, len(packages), batch_size):
                        batch = packages[i : i + batch_size]
                        try:
                            logger.info(
                                f"Installing package batch {i // batch_size + 1}/{(len(packages) - 1) // batch_size + 1}"
                            )
                            subprocess.run(
                                ["pacman", "-S", "--needed", "--noconfirm"] + batch,
                                check=True,
                            )
                        except:
                            logger.warning(
                                f"Failed to install some packages in batch {i // batch_size + 1}"
                            )
                else:
                    logger.warning(
                        "No package list file found, skipping package restoration"
                    )

        logger.info("Backup restoration completed")
        return "Backup restoration completed successfully"

    except Exception as e:
        logger.error(f"Restoration failed: {str(e)}")
        return f"Restoration failed: {str(e)}"
