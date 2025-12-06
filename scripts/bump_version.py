#!/usr/bin/env python3
"""
Version bumping script for Foundry VTT module.
Updates version and download URL in module.json
"""

import json
import sys
import re
from pathlib import Path
from typing import Tuple


def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse a semantic version string into (major, minor, patch)"""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)$', version)
    if not match:
        raise ValueError(f"Invalid version format: {version}")
    return tuple(map(int, match.groups()))


def bump_version(current: str, bump_type: str) -> str:
    """Bump version based on type (major, minor, patch)"""
    major, minor, patch = parse_version(current)

    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")


def update_module_json(new_version: str, module_path: Path = Path("module.json")):
    """Update version and download URL in module.json"""

    # Read current module.json
    with open(module_path, 'r') as f:
        data = json.load(f)

    old_version = data.get('version', 'unknown')

    # Update version
    data['version'] = new_version

    # Update download URL if it exists
    if 'download' in data:
        # Extract the base URL pattern and replace version
        download_url = data['download']
        # Replace the version number in the download URL
        new_download = re.sub(
            r'/releases/download/[\d.]+/',
            f'/releases/download/{new_version}/',
            download_url
        )
        data['download'] = new_download

    # Write back to file with proper formatting
    with open(module_path, 'w') as f:
        json.dump(data, f, indent=2)
        f.write('\n')  # Add trailing newline

    return old_version, new_version, data.get('download')


def main():
    if len(sys.argv) != 2:
        print("Usage: ./bump-version.py [major|minor|patch|X.Y.Z]")
        print("\nExamples:")
        print("  ./bump-version.py patch    # 0.0.2 -> 0.0.3")
        print("  ./bump-version.py minor    # 0.0.2 -> 0.1.0")
        print("  ./bump-version.py major    # 0.0.2 -> 1.0.0")
        print("  ./bump-version.py 1.5.3    # Set to 1.5.3")
        sys.exit(1)

    module_path = Path("module.json")

    if not module_path.exists():
        print(f"Error: {module_path} not found")
        sys.exit(1)

    # Read current version
    with open(module_path, 'r') as f:
        data = json.load(f)

    current_version = data.get('version')
    if not current_version:
        print("Error: No version field found in module.json")
        sys.exit(1)

    arg = sys.argv[1]

    # Determine new version
    if re.match(r'^\d+\.\d+\.\d+$', arg):
        # Explicit version provided
        new_version = arg
    elif arg in ['major', 'minor', 'patch']:
        # Semantic version bump
        new_version = bump_version(current_version, arg)
    else:
        print(f"Error: Invalid argument '{arg}'")
        print("Must be 'major', 'minor', 'patch', or a version like '1.2.3'")
        sys.exit(1)

    # Update the file
    old_version, new_version, new_download = update_module_json(new_version, module_path)

    print(f"✓ Bumped version from {old_version} to {new_version}")
    print(f"✓ Updated download URL to: {new_download}")
    print("\nNext steps:")
    print(f"  git add module.json")
    print(f"  git commit -m 'chore: bump version to {new_version}'")
    print(f"  git push")


if __name__ == "__main__":
    main()
