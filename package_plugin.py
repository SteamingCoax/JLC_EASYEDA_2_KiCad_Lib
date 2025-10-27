#!/usr/bin/env python3
import os
import json
import hashlib
import zipfile
from pathlib import Path

def calculate_size_and_sha256(file_path):
    """Calculate file size and SHA256 hash."""
    sha256_hash = hashlib.sha256()
    file_size = 0
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256_hash.update(chunk)
            file_size += len(chunk)
    
    return file_size, sha256_hash.hexdigest()

def create_plugin_package(version):
    """Create a zip package of the plugin."""
    # Create zip file
    zip_name = f'easyeda2kicad_v{version}.zip'
    zip_path = Path('resources') / zip_name
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add plugin files
        plugin_dir = Path('plugin')
        for file_path in plugin_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(plugin_dir)
                zipf.write(file_path, arcname)
    
    return zip_path

def update_repository_json(zip_path, version):
    """Update repository.json with package information."""
    repo_path = Path('resources') / 'repository.json'
    
    # Calculate package size and hash
    size, sha256 = calculate_size_and_sha256(zip_path)
    
    # Read current repository.json
    with open(repo_path, 'r') as f:
        repo_data = json.load(f)
    
    # Update package information
    for repo in repo_data['packages']['repositories']:
        repo['download_sha256'] = sha256
        repo['download_size'] = size
        repo['install_size'] = size  # Uncompressed size will be larger
        repo['download_url'] = f'https://github.com/TousstNicolas/EasyEDA2KiCad/releases/download/v{version}/easyeda2kicad_v{version}.zip'
    
    # Write updated repository.json
    with open(repo_path, 'w') as f:
        json.dump(repo_data, f, indent=4)

def main():
    version = '1.0.0'  # Update this for new releases
    
    # Create plugin package
    zip_path = create_plugin_package(version)
    print(f'Created plugin package: {zip_path}')
    
    # Update repository.json
    update_repository_json(zip_path, version)
    print('Updated repository.json')
    
    print('Package created successfully!')
    print('Next steps:')
    print('1. Commit and push changes')
    print('2. Create a new release on GitHub')
    print(f'3. Upload {zip_path.name} to the release')
    print('4. Update the repository URL in KiCad Plugin and Content Manager:')
    print('   https://raw.githubusercontent.com/TousstNicolas/EasyEDA2KiCad/master/resources/repository.json')

if __name__ == '__main__':
    main()