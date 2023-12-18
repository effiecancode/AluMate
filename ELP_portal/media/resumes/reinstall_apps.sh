#!/bin/bash

# Get a list of all installed packages
installed_packages=$(dpkg --get-selections | awk '{print $1}')

# Reinstall each package using the package manager (apt in this case)
for package in $installed_packages; do
    sudo apt-get install --reinstall --yes "$package"
done
