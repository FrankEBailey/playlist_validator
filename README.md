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
```

## Usage

### Basic Validation

Scan your music collection and show only broken playlists:

```bash
python playlist_validator.py ~/Music
```

Show all playlists (both valid and invalid):

```bash
python playlist_validator.py ~/Music --show-valid
```

Quick scan with minimal output:

```bash
python playlist_validator.py ~/Music --no-details
```

### Quarantine Broken Playlists

Move invalid playlists to a quarantine directory:

```bash
python playlist_validator.py ~/Music --quarantine ~/broken_playlists
```

Preview what would be moved without actually doing it:

```bash
python playlist_validator.py ~/Music --quarantine ~/broken_playlists --dry-run
```

Quarantine with minimal output:

```bash
python playlist_validator.py ~/Music --quarantine ~/broken_playlists --no-details
```

### Real-World Examples

Check a specific artist's folder:

```bash
python playlist_validator.py "~/Music/Pink Floyd" --show-valid
```

Clean up your entire collection and quarantine broken playlists:

```bash
python playlist_validator.py ~/Music --quarantine ~/Desktop/broken_playlists
```

Test run before making changes:

```bash
python playlist_validator.py ~/Music --quarantine ~/Desktop/broken_playlists --dry-run
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

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.