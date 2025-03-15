# SwissArch - Swiss Army Knife for Arch Linux

![SwissArch Logo](https://img.shields.io/badge/SwissArch-v1.0.0-blue)
![Python Version](https://img.shields.io/badge/Python-3.6%2B-green)
![License](https://img.shields.io/badge/License-MIT-brightgreen)

A comprehensive utility tool for Arch Linux system management and maintenance, offering an all-in-one solution for common administrative tasks.

## Features

- **Package Management**: Easily search, install, and update packages
- **AUR Helper Installation**: Simplify installation of yay or paru
- **BlackArch Integration**: Install BlackArch repository and penetration testing tools
- **System Information**: Quick access to detailed system information
- **System Maintenance**: Perform optimization and maintenance tasks
- **Backup and Restore**: Create and restore system configuration backups

## Installation

### Prerequisites
- Arch Linux or Arch-based distribution
- Python 3.6 or higher
- Required Python modules: colorama, psutil, requests

### Install Dependencies
```bash
sudo pacman -S python python-pip
pip install colorama psutil requests
```

### Install SwissArch
```bash
# Clone the repository
git clone https://github.com/yourusername/swissarch.git
cd swissarch

# Make the script executable
chmod +x swissarch.py
```

## Usage

SwissArch can be used in two ways:
1. **Interactive Mode**: Menu-driven interface for easier navigation
2. **Command Line Mode**: Direct commands for automation and scripting

### Interactive Mode

Simply run the script without arguments:
```bash
sudo ./swissarch.py
```

This will display the main menu with all available options.

### Command Line Mode

SwissArch supports various command-line arguments for direct access to specific functions:

#### General Options
```bash
./swissarch.py --version     # Display version information
./swissarch.py --no-color    # Disable colored output
```

#### System Information
```bash
./swissarch.py system --info
```

#### Package Management
```bash
# Update system
sudo ./swissarch.py pacman --update

# Install packages
sudo ./swissarch.py pacman --install package1 package2

# Setup pacman with optimizations
sudo ./swissarch.py pacman --setup --enable-ilovecady
```

#### AUR Utilities
```bash
# Install AUR helper
sudo ./swissarch.py aur --install-helper yay

# Search for packages in AUR
./swissarch.py aur --search package-name
```

#### Penetration Testing Tools
```bash
# Setup BlackArch repository
sudo ./swissarch.py pentest --setup-blackarch

# Install penetration testing tools (basic/full/custom)
sudo ./swissarch.py pentest --install-tools basic
```

#### System Maintenance
```bash
# Apply system optimizations
sudo ./swissarch.py system --optimize

# Backup system configuration
sudo ./swissarch.py system --backup /path/to/backup/dir
```

## Features in Detail

### Package Management
- **System Update**: Update all installed packages
- **Package Search**: Search for packages in repositories
- **Package Installation**: Install new packages
- **Pacman Configuration**: Optimize pacman settings

### AUR Helper Installation
- Automated installation of popular AUR helpers (yay, paru)
- Handles all dependencies and build requirements

### BlackArch & Penetration Tools
- Setup BlackArch repository for security tools
- Install basic or full penetration testing toolkit
- List installed security tools

### System Maintenance
- Clean package cache
- Remove orphaned packages
- Enable system services for performance
- Optimize swap settings
- Update mirrorlist for faster downloads

### Backup & Restore
- Backup important system configuration files
- Save list of installed packages
- Restore configurations and packages from backup

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- The Arch Linux community
- BlackArch project
- Contributors and testers

## Author

Mohammad Abukhader

---

**Note**: Some operations require root privileges. Always review what changes will be made to your system before confirming them.
