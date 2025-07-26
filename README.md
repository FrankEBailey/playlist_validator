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

### Linux/Unix
```bash
# Download the script
wget https://raw.githubusercontent.com/yourusername/playlist-validator/main/playlist_validator.py

# Make it executable (optional)
chmod +x playlist_validator.py
```

### Windows
```cmd
# Download using PowerShell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/yourusername/playlist-validator/main/playlist_validator.py" -OutFile "playlist_validator.py"

# Or download using curl (if available)
curl -o playlist_validator.py https://raw.githubusercontent.com/yourusername/playlist-validator/main/playlist_validator.py
```

### macOS
```bash
# Download the script (same as Linux)
curl -o playlist_validator.py https://raw.githubusercontent.com/yourusername/playlist-validator/main/playlist_validator.py

# Make it executable (optional)
chmod +x playlist_validator.py
```

## Usage

### Basic Validation

Scan your music collection and show only broken playlists:

**Linux/macOS:**
```bash
python playlist_validator.py ~/Music
```

**Windows:**
```cmd
python playlist_validator.py "C:\Users\%USERNAME%\Music"
# Or using forward slashes
python playlist_validator.py "C:/Users/%USERNAME%/Music"
```

Show all playlists (both valid and invalid):

**Linux/macOS:**
```bash
python playlist_validator.py ~/Music --show-valid
```

**Windows:**
```cmd
python playlist_validator.py "C:\Users\%USERNAME%\Music" --show-valid
```

Quick scan with minimal output:

**Linux/macOS:**
```bash
python playlist_validator.py ~/Music --no-details
```

**Windows:**
```cmd
python playlist_validator.py "C:\Users\%USERNAME%\Music" --no-details
```

### Quarantine Broken Playlists

Move invalid playlists to a quarantine directory:

**Linux/macOS:**
```bash
python playlist_validator.py ~/Music --quarantine ~/broken_playlists
```

**Windows:**
```cmd
python playlist_validator.py "C:\Users\%USERNAME%\Music" --quarantine "C:\Users\%USERNAME%\Desktop\broken_playlists"
```

Preview what would be moved without actually doing it:

**Linux/macOS:**
```bash
python playlist_validator.py ~/Music --quarantine ~/broken_playlists --dry-run
```

**Windows:**
```cmd
python playlist_validator.py "C:\Users\%USERNAME%\Music" --quarantine "C:\Users\%USERNAME%\Desktop\broken_playlists" --dry-run
```

### Platform-Specific Examples

**Linux:**
```bash
# Scan external drive
python playlist_validator.py /media/external_drive/Music --quarantine /home/user/broken_playlists

# Scan with spaces in path
python playlist_validator.py "/home/user/My Music Collection" --show-valid
```

**macOS:**
```bash
# Scan iTunes Music folder
python playlist_validator.py "~/Music/Music/Media.localized/Music" --show-valid

# Scan external drive
python playlist_validator.py "/Volumes/External Drive/Music" --quarantine ~/Desktop/broken_playlists
```

**Windows:**
```cmd
# Scan different drive
python playlist_validator.py "D:\Music Collection" --quarantine "C:\temp\broken_playlists"

# Scan iTunes folder
python playlist_validator.py "C:\Users\%USERNAME%\Music\iTunes\iTunes Media\Music" --show-valid

# Using UNC paths (network drives)
python playlist_validator.py "\\server\music" --quarantine "C:\quarantine"
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `path` | Path to your music collection (required) |
| `--quarantine PATH` | Move invalid playlists to specified directory |
| `--dry-run` | Preview quarantine actions without moving files |
| `--no-details` | Hide detailed information about missing files |
| `--show-valid` | Display valid playlists in output |

## Sample Output

### Basic Scan Output

```
Scanning for playlists in: /home/user/Music
Looking for extensions: .asx, .m3u, .m3u8, .pls, .wpl, .xspf
----------------------------------------------------------------------
Found 15 playlist files

✗ INVALID: Rock/Classic Rock Hits.m3u
   Valid tracks: 8
   Missing tracks: 4
   Missing files:
     - ../Moved/Led Zeppelin - Stairway.mp3
     - Deep Purple - Smoke on the Water.flac
     - Queen - Bohemian Rhapsody.mp3
     - AC/DC - Back in Black.flac

✗ INVALID: Jazz/Smooth Jazz Collection.pls
   Valid tracks: 12
   Missing tracks: 2
   Missing files:
     - Miles Davis - Kind of Blue.flac
     - John Coltrane - Giant Steps.mp3

======================================================================
VALIDATION SUMMARY
======================================================================
Playlists found:     15
Valid playlists:     12
Invalid playlists:   3
Total tracks:        847
Valid tracks:        798
Missing tracks:      49
Playlist validity:   80.0%
Track validity:      94.2%
```

### Quarantine Mode Output

```
Scanning for playlists in: /home/user/Music
Looking for extensions: .asx, .m3u, .m3u8, .pls, .wpl, .xspf
Quarantine directory: /home/user/broken_playlists
----------------------------------------------------------------------
Found 15 playlist files

✗ INVALID: Rock/Classic Rock Hits.m3u [QUARANTINED]
   Valid tracks: 8
   Missing tracks: 4
   Missing files:
     - ../Moved/Led Zeppelin - Stairway.mp3
     - Deep Purple - Smoke on the Water.flac

✗ INVALID: Jazz/Smooth Jazz Collection.pls [QUARANTINED]
   Valid tracks: 12
   Missing tracks: 2

======================================================================
VALIDATION SUMMARY
======================================================================
Playlists found:     15
Valid playlists:     12
Invalid playlists:   3
Quarantined:         3
Total tracks:        847
Valid tracks:        798
Missing tracks:      49
Playlist validity:   80.0%
Track validity:      94.2%
```

### Dry Run Output

```
Scanning for playlists in: /home/user/Music
Looking for extensions: .asx, .m3u, .m3u8, .pls, .wpl, .xspf
Quarantine directory: /home/user/broken_playlists
DRY RUN MODE: No files will be moved
----------------------------------------------------------------------

✗ INVALID: Rock/Classic Rock Hits.m3u [WOULD QUARANTINE]
✗ INVALID: Jazz/Smooth Jazz Collection.pls [WOULD QUARANTINE]
```

## Supported Formats

### Playlist Formats
- **M3U/M3U8** - Most common playlist format
- **PLS** - Winamp/Shoutcast playlist format  
- **XSPF** - XML Shareable Playlist Format
- **WPL** - Windows Media Player playlists
- **ASX** - Advanced Stream Redirector

### Audio Formats
MP3, FLAC, WAV, M4A, AAC, OGG, WMA, APE, OPUS, AIFF, DSF, DFF, MPC, TTA

## How It Works

1. **Discovery**: Recursively scans directories for playlist files
2. **Parsing**: Extracts file paths from each playlist format
3. **Resolution**: Resolves relative and absolute paths, handles URL encoding
4. **Validation**: Checks if referenced audio files actually exist
5. **Reporting**: Shows detailed results and statistics
6. **Quarantine** (optional): Moves broken playlists while preserving directory structure

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

### Platform Notes

**Windows:**
- Supports both forward slashes (`/`) and backslashes (`\`) in paths
- Handles UNC paths for network drives (`\\server\share`)
- Works with Windows-style drive letters (`C:\`, `D:\`, etc.)
- Automatically handles Windows path length limitations

**macOS:**
- Full Unicode support for international characters in filenames
- Handles macOS-specific file attributes and resource forks
- Compatible with case-insensitive HFS+ and case-sensitive APFS filesystems
- Works with iTunes/Music app folder structures

**Linux:**
- Supports all filesystem types (ext4, btrfs, xfs, etc.)
- Handles symbolic links correctly
- Full Unicode filename support
- Works with mounted network filesystems (NFS, CIFS/SMB)

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.