# Playlist Validator

A Python tool to scan and validate playlist files in your music collection, with support for quarantining broken playlists.

## Features

- **Multi-format support**: Validates `.pls`, `.m3u`, `.m3u8`, `.xspf`, `.asx`, and `.wpl` playlist files
- **Recursive scanning**: Searches through entire directory trees
- **Smart path resolution**: Handles absolute paths, relative paths, and URL-encoded file references
- **Comprehensive audio format detection**: Supports MP3, FLAC, WAV, M4A, AAC, OGG, WMA, and many more
- **Quarantine functionality**: Safely move invalid playlists to a separate directory while preserving folder structure
- **Detailed reporting**: Shows missing files, validity percentages, and comprehensive statistics
- **Dry-run mode**: Preview changes before moving files

## Use Cases

Perfect for music enthusiasts who have:
- Large music collections with automated file management
- Playlists broken by file renaming or moving
- Need to clean up their music library
- Want to identify which playlists are still functional after reorganizing files

## Installation

No installation required! Simply download `playlist_validator.py` and run it with Python 3.6+.

```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/playlist-validator/main/playlist_validator.py

# Make it executable (optional)
chmod +x playlist_validator.py
