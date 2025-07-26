#!/usr/bin/env python3
"""
Playlist Validator Tool

Recursively scans directories for playlist files (.pls, .m3u, .m3u8, .xspf, .asx, .wpl)
and validates them by checking if referenced audio files exist.

Usage:
    python playlist_validator.py /path/to/music/collection
"""

import os
import sys
import argparse
import shutil
from pathlib import Path
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import re
from typing import List, Tuple, Dict, Set

class PlaylistValidator:
    def __init__(self, music_root: str, quarantine_path: str = None):
        self.music_root = Path(music_root).resolve()
        self.quarantine_path = Path(quarantine_path).resolve() if quarantine_path else None
        self.playlist_extensions = {'.pls', '.m3u', '.m3u8', '.xspf', '.asx', '.wpl'}
        self.audio_extensions = {
            '.mp3', '.flac', '.wav', '.m4a', '.aac', '.ogg', '.wma', 
            '.ape', '.opus', '.aiff', '.dsf', '.dff', '.mpc', '.tta'
        }
        self.stats = {
            'playlists_found': 0,
            'valid_playlists': 0,
            'invalid_playlists': 0,
            'quarantined_playlists': 0,
            'total_tracks': 0,
            'valid_tracks': 0,
            'missing_tracks': 0
        }
        
    def find_playlists(self) -> List[Path]:
        """Recursively find all playlist files"""
        playlists = []
        for root, dirs, files in os.walk(self.music_root):
            for file in files:
                if Path(file).suffix.lower() in self.playlist_extensions:
                    playlists.append(Path(root) / file)
        return playlists
    
    def parse_m3u(self, playlist_path: Path) -> List[str]:
        """Parse M3U/M3U8 playlist files"""
        tracks = []
        try:
            with open(playlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        # Handle URL-encoded paths
                        if line.startswith('file://'):
                            line = unquote(line[7:])
                        tracks.append(line)
        except Exception as e:
            print(f"Error reading {playlist_path}: {e}")
        return tracks
    
    def parse_pls(self, playlist_path: Path) -> List[str]:
        """Parse PLS playlist files"""
        tracks = []
        try:
            with open(playlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line.lower().startswith('file'):
                        # Extract file path from File1=, File2=, etc.
                        if '=' in line:
                            file_path = line.split('=', 1)[1]
                            if file_path.startswith('file://'):
                                file_path = unquote(file_path[7:])
                            tracks.append(file_path)
        except Exception as e:
            print(f"Error reading {playlist_path}: {e}")
        return tracks
    
    def parse_xspf(self, playlist_path: Path) -> List[str]:
        """Parse XSPF (XML Shareable Playlist Format) files"""
        tracks = []
        try:
            tree = ET.parse(playlist_path)
            root = tree.getroot()
            
            # Handle namespaces
            ns = {'xspf': 'http://xspf.org/ns/0/'}
            if root.tag.startswith('{'):
                ns_uri = root.tag.split('}')[0][1:]
                ns = {'xspf': ns_uri}
            
            for track in root.findall('.//xspf:track', ns):
                location = track.find('xspf:location', ns)
                if location is not None and location.text:
                    file_path = location.text
                    if file_path.startswith('file://'):
                        file_path = unquote(file_path[7:])
                    tracks.append(file_path)
        except Exception as e:
            print(f"Error parsing XSPF {playlist_path}: {e}")
        return tracks
    
    def parse_wpl(self, playlist_path: Path) -> List[str]:
        """Parse WPL (Windows Media Player Playlist) files"""
        tracks = []
        try:
            tree = ET.parse(playlist_path)
            root = tree.getroot()
            
            for media in root.findall('.//media'):
                src = media.get('src')
                if src:
                    tracks.append(src)
        except Exception as e:
            print(f"Error parsing WPL {playlist_path}: {e}")
        return tracks
    
    def parse_asx(self, playlist_path: Path) -> List[str]:
        """Parse ASX (Advanced Stream Redirector) files"""
        tracks = []
        try:
            tree = ET.parse(playlist_path)
            root = tree.getroot()
            
            for entry in root.findall('.//entry'):
                ref = entry.find('ref')
                if ref is not None:
                    href = ref.get('href')
                    if href:
                        tracks.append(href)
        except Exception as e:
            print(f"Error parsing ASX {playlist_path}: {e}")
        return tracks
    
    def parse_playlist(self, playlist_path: Path) -> List[str]:
        """Parse playlist file based on extension"""
        ext = playlist_path.suffix.lower()
        
        if ext in ['.m3u', '.m3u8']:
            return self.parse_m3u(playlist_path)
        elif ext == '.pls':
            return self.parse_pls(playlist_path)
        elif ext == '.xspf':
            return self.parse_xspf(playlist_path)
        elif ext == '.wpl':
            return self.parse_wpl(playlist_path)
        elif ext == '.asx':
            return self.parse_asx(playlist_path)
        else:
            return []
    
    def resolve_track_path(self, track_path: str, playlist_dir: Path) -> Path:
        """Resolve track path relative to playlist location"""
        track_path = track_path.replace('\\', '/')  # Normalize path separators
        
        # If absolute path, use as is
        if os.path.isabs(track_path):
            return Path(track_path)
        
        # Try relative to playlist directory first
        relative_path = playlist_dir / track_path
        if relative_path.exists():
            return relative_path
        
        # Try relative to music root
        root_relative = self.music_root / track_path
        if root_relative.exists():
            return root_relative
        
        # Return the relative path for further checking
        return relative_path
    
    def validate_playlist(self, playlist_path: Path) -> Tuple[bool, List[str], List[str]]:
        """Validate a single playlist file"""
        tracks = self.parse_playlist(playlist_path)
        valid_tracks = []
        missing_tracks = []
        
        playlist_dir = playlist_path.parent
        
        for track in tracks:
            resolved_path = self.resolve_track_path(track, playlist_dir)
            
            if resolved_path.exists() and resolved_path.suffix.lower() in self.audio_extensions:
                valid_tracks.append(str(resolved_path))
            else:
                missing_tracks.append(track)
        
        is_valid = len(missing_tracks) == 0 and len(valid_tracks) > 0
        return is_valid, valid_tracks, missing_tracks
    
    def quarantine_playlist(self, playlist_path: Path) -> bool:
        """Move invalid playlist to quarantine directory"""
        if not self.quarantine_path:
            return False
            
        try:
            # Create quarantine directory if it doesn't exist
            self.quarantine_path.mkdir(parents=True, exist_ok=True)
            
            # Preserve directory structure in quarantine
            relative_path = playlist_path.relative_to(self.music_root)
            quarantine_dest = self.quarantine_path / relative_path
            
            # Create subdirectories in quarantine if needed
            quarantine_dest.parent.mkdir(parents=True, exist_ok=True)
            
            # Move the playlist file
            shutil.move(str(playlist_path), str(quarantine_dest))
            self.stats['quarantined_playlists'] += 1
            return True
            
        except Exception as e:
            print(f"Error quarantining {playlist_path}: {e}")
            return False
    
    def scan_and_validate(self, show_details=True, show_valid=False, dry_run=False):
        """Scan for playlists and validate them"""
        print(f"Scanning for playlists in: {self.music_root}")
        print(f"Looking for extensions: {', '.join(sorted(self.playlist_extensions))}")
        if self.quarantine_path:
            print(f"Quarantine directory: {self.quarantine_path}")
            if dry_run:
                print("DRY RUN MODE: No files will be moved")
        print("-" * 70)
        
        playlists = self.find_playlists()
        self.stats['playlists_found'] = len(playlists)
        
        if not playlists:
            print("No playlist files found!")
            return
        
        print(f"Found {len(playlists)} playlist files\n")
        
        for playlist_path in sorted(playlists):
            is_valid, valid_tracks, missing_tracks = self.validate_playlist(playlist_path)
            
            # Update statistics
            self.stats['total_tracks'] += len(valid_tracks) + len(missing_tracks)
            self.stats['valid_tracks'] += len(valid_tracks)
            self.stats['missing_tracks'] += len(missing_tracks)
            
            if is_valid:
                self.stats['valid_playlists'] += 1
                status = "✓ VALID"
                if show_valid:
                    print(f"{status}: {playlist_path.relative_to(self.music_root)}")
                    if show_details:
                        print(f"   Tracks: {len(valid_tracks)}")
            else:
                self.stats['invalid_playlists'] += 1
                status = "✗ INVALID"
                
                # Handle quarantine
                quarantine_action = ""
                if self.quarantine_path and not dry_run:
                    if self.quarantine_playlist(playlist_path):
                        quarantine_action = " [QUARANTINED]"
                    else:
                        quarantine_action = " [QUARANTINE FAILED]"
                elif self.quarantine_path and dry_run:
                    quarantine_action = " [WOULD QUARANTINE]"
                
                print(f"{status}: {playlist_path.relative_to(self.music_root)}{quarantine_action}")
                
                if show_details:
                    print(f"   Valid tracks: {len(valid_tracks)}")
                    print(f"   Missing tracks: {len(missing_tracks)}")
                    
                    if missing_tracks:
                        print("   Missing files:")
                        for missing in missing_tracks[:5]:  # Show first 5 missing
                            print(f"     - {missing}")
                        if len(missing_tracks) > 5:
                            print(f"     ... and {len(missing_tracks) - 5} more")
                
                print()
    
    def print_summary(self):
        """Print validation summary statistics"""
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Playlists found:     {self.stats['playlists_found']}")
        print(f"Valid playlists:     {self.stats['valid_playlists']}")
        print(f"Invalid playlists:   {self.stats['invalid_playlists']}")
        if self.quarantine_path:
            print(f"Quarantined:         {self.stats['quarantined_playlists']}")
        print(f"Total tracks:        {self.stats['total_tracks']}")
        print(f"Valid tracks:        {self.stats['valid_tracks']}")
        print(f"Missing tracks:      {self.stats['missing_tracks']}")
        
        if self.stats['playlists_found'] > 0:
            valid_pct = (self.stats['valid_playlists'] / self.stats['playlists_found']) * 100
            print(f"Playlist validity:   {valid_pct:.1f}%")
        
        if self.stats['total_tracks'] > 0:
            track_pct = (self.stats['valid_tracks'] / self.stats['total_tracks']) * 100
            print(f"Track validity:      {track_pct:.1f}%")

def main():
    parser = argparse.ArgumentParser(description='Validate playlist files in music collection')
    parser.add_argument('path', help='Path to music collection root directory')
    parser.add_argument('--no-details', action='store_true', 
                       help='Hide detailed information about invalid playlists')
    parser.add_argument('--show-valid', action='store_true',
                       help='Show valid playlists in output')
    parser.add_argument('--quarantine', type=str, metavar='PATH',
                       help='Move invalid playlists to this quarantine directory')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be quarantined without actually moving files')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist!")
        sys.exit(1)
    
    if not os.path.isdir(args.path):
        print(f"Error: Path '{args.path}' is not a directory!")
        sys.exit(1)
    
    if args.dry_run and not args.quarantine:
        print("Error: --dry-run can only be used with --quarantine")
        sys.exit(1)
    
    validator = PlaylistValidator(args.path, args.quarantine)
    validator.scan_and_validate(
        show_details=not args.no_details,
        show_valid=args.show_valid,
        dry_run=args.dry_run
    )
    validator.print_summary()

if __name__ == '__main__':
    main()