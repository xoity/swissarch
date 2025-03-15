#!/usr/bin/env python3
# AUR utilities for SwissArch

import os
import subprocess
import logging
import shutil
import tempfile
import requests


logger = logging.getLogger("SwissArch")


def install_aur_helper(helper_name):
    """
    Install the specified AUR helper

    Args:
        helper_name (str): Name of the AUR helper to install (yay or paru)
    """
    try:
        # Check if the helper is already installed
        if shutil.which(helper_name):
            logger.info(f"{helper_name} is already installed.")
            return True

        logger.info(f"Installing {helper_name} AUR helper...")

        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)

            # Install necessary build tools
            subprocess.run(
                ["pacman", "-S", "--needed", "--noconfirm", "git", "base-devel"],
                check=True,
            )

            # Clone the repository based on which helper was chosen
            if helper_name == "yay":
                subprocess.run(
                    ["git", "clone", "https://aur.archlinux.org/yay.git"], check=True
                )
                os.chdir("yay")
            elif helper_name == "paru":
                subprocess.run(
                    ["git", "clone", "https://aur.archlinux.org/paru.git"], check=True
                )
                os.chdir("paru")
            else:
                logger.error(f"Unsupported AUR helper: {helper_name}")
                return False

            # Build and install
            subprocess.run(["makepkg", "-si", "--noconfirm"], check=True)

        # Verify installation
        if shutil.which(helper_name):
            logger.info(f"{helper_name} was successfully installed.")
            return True
        else:
            logger.error(f"Failed to install {helper_name}.")
            return False

    except Exception as e:
        logger.error(f"Error installing AUR helper: {str(e)}")
        return False


def search_aur(query):
    """
    Search for packages in AUR

    Args:
        query (str): Search query
    """
    try:
        logger.info(f"Searching AUR for '{query}'...")

        # Check if we have yay or paru installed
        helper = None
        for h in ["yay", "paru"]:
            if shutil.which(h):
                helper = h
                break

        if helper:
            # Use the installed helper to search AUR
            result = subprocess.run(
                [helper, "-Ss", query], capture_output=True, text=True
            )

            if result.returncode == 0:
                return result.stdout
            else:
                logger.warning(
                    f"AUR search returned non-zero exit code: {result.returncode}"
                )
                return result.stdout + "\n" + result.stderr
        else:
            url = f"https://aur.archlinux.org/rpc/?v=5&type=search&arg={query}"
            response = requests.get(url)
            data = response.json()

            if data["resultcount"] == 0:
                return f"No AUR packages found matching '{query}'"

            result = (
                f"Found {data['resultcount']} packages in AUR matching '{query}':\n\n"
            )
            for pkg in data["results"]:
                result += f"{pkg['Name']} {pkg['Version']}\n"
                result += f"    {pkg['Description']}\n\n"

            return result

    except Exception as e:
        logger.error(f"Error searching AUR: {str(e)}")
        return f"Error searching AUR: {str(e)}"


def install_aur_package(package_name, helper=None):
    """
    Install a package from AUR

    Args:
        package_name (str): Name of the package to install
        helper (str): Preferred AUR helper to use
    """
    try:
        logger.info(f"Installing AUR package: {package_name}")

        # If helper is specified, check if it's installed
        if helper and not shutil.which(helper):
            logger.warning(
                f"{helper} not found, will try to use any available AUR helper"
            )
            helper = None

        # Find an available AUR helper
        if not helper:
            for h in ["yay", "paru"]:
                if shutil.which(h):
                    helper = h
                    break

        # If we have a helper, use it
        if helper:
            result = subprocess.run(
                [helper, "-S", "--noconfirm", package_name], check=True
            )
            logger.info(f"{package_name} installed successfully using {helper}")
            return True
        else:
            # Fallback to manual AUR installation
            logger.warning("No AUR helper found, performing manual installation")

            with tempfile.TemporaryDirectory() as temp_dir:
                os.chdir(temp_dir)

                # Clone the AUR package repository
                subprocess.run(
                    ["git", "clone", f"https://aur.archlinux.org/{package_name}.git"],
                    check=True,
                )
                os.chdir(package_name)

                # Build and install the package
                subprocess.run(["makepkg", "-si", "--noconfirm"], check=True)

            logger.info(f"{package_name} installed successfully manually")
            return True

    except Exception as e:
        logger.error(f"Error installing AUR package: {str(e)}")
        return False
