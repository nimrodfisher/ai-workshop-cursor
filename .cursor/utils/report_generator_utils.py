"""
Reusable utilities for report generation
Ensures consistent path handling, profile image loading, and error handling
"""

import base64
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List


def get_workspace_root(start_path: Optional[Path] = None) -> Path:
    """
    Find workspace root by looking for .cursor directory.
    Works from any subdirectory in the workspace.
    
    Args:
        start_path: Starting path (defaults to current file's parent)
    
    Returns:
        Path to workspace root
    """
    if start_path is None:
        # Default to calling file's parent directory
        import inspect
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_file = frame.f_back.f_globals.get('__file__')
            if caller_file:
                start_path = Path(caller_file).parent
            else:
                start_path = Path.cwd()
        else:
            start_path = Path.cwd()
    
    current = Path(start_path).resolve()
    
    # Look for .cursor directory (workspace marker)
    while current != current.parent:
        if (current / ".cursor").exists():
            return current
        current = current.parent
    
    # Fallback: assume we're in workspace root if .cursor not found
    return Path.cwd().resolve()


def load_profile_image(workspace_root: Optional[Path] = None) -> str:
    """
    Load and encode profile image as base64.
    
    Args:
        workspace_root: Workspace root path (auto-detected if None)
    
    Returns:
        Base64 data URI string, or empty string if image not found
    """
    if workspace_root is None:
        workspace_root = get_workspace_root()
    
    profile_path = workspace_root / ".cursor" / "assets" / "photo.jpg"
    
    if profile_path.exists():
        try:
            with open(profile_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
                return f"data:image/jpeg;base64,{image_data}"
        except Exception as e:
            print(f"Warning: Could not load profile image: {e}")
            return ""
    else:
        print(f"Warning: Profile image not found at {profile_path}")
        return ""


def load_logo_image(workspace_root: Optional[Path] = None) -> str:
    """
    Load and encode Analytics Hub logo as base64.
    Tries multiple formats: .png, .jpg, .jpeg, .svg
    
    Args:
        workspace_root: Workspace root path (auto-detected if None)
    
    Returns:
        Base64 data URI string, or empty string if image not found
    """
    if workspace_root is None:
        workspace_root = get_workspace_root()
    
    assets_dir = workspace_root / ".cursor" / "assets"
    
    # Try common logo filenames and formats
    logo_paths = [
        assets_dir / "logo.png",
        assets_dir / "logo.jpg",
        assets_dir / "logo.jpeg",
        assets_dir / "logo.svg",
        assets_dir / "analytics-hub-logo.png",
        assets_dir / "analytics-hub-logo.jpg",
    ]
    
    for logo_path in logo_paths:
        if logo_path.exists():
            try:
                with open(logo_path, "rb") as f:
                    image_data = base64.b64encode(f.read()).decode()
                    # Determine MIME type from extension
                    ext = logo_path.suffix.lower()
                    mime_types = {
                        '.png': 'image/png',
                        '.jpg': 'image/jpeg',
                        '.jpeg': 'image/jpeg',
                        '.svg': 'image/svg+xml'
                    }
                    mime_type = mime_types.get(ext, 'image/png')
                    return f"data:{mime_type};base64,{image_data}"
            except Exception as e:
                print(f"Warning: Could not load logo image from {logo_path}: {e}")
                continue
    
    print(f"Warning: Logo image not found in {assets_dir}")
    return ""


def load_json_data(data_dir: Path, filename: str) -> List[Dict[str, Any]]:
    """
    Safely load JSON data from file.
    
    Args:
        data_dir: Directory containing JSON file
        filename: JSON filename
    
    Returns:
        List of dictionaries (or empty list if file not found/invalid)
    """
    file_path = data_dir / filename
    
    if not file_path.exists():
        print(f"Warning: Data file not found: {file_path}")
        return []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data]
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []


def ensure_output_dir(output_path: Path) -> Path:
    """
    Ensure output directory exists.
    
    Args:
        output_path: Full path to output file
    
    Returns:
        Path object (directory created if needed)
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return output_path


def safe_write_file(file_path: Path, content: str, encoding: str = 'utf-8') -> bool:
    """
    Safely write content to file with error handling.
    
    Args:
        file_path: Path to output file
        content: Content to write
        encoding: File encoding (default: utf-8)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        ensure_output_dir(file_path)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")
        return False


def format_percentage(value: Any, decimals: int = 2) -> str:
    """
    Format value as percentage string.
    
    Args:
        value: Numeric value
        decimals: Number of decimal places
    
    Returns:
        Formatted percentage string (e.g., "15.28%")
    """
    try:
        num = float(value)
        return f"{num:.{decimals}f}%"
    except (ValueError, TypeError):
        return str(value) if value else "N/A"


def format_currency(value: Any, symbol: str = "$", decimals: int = 2) -> str:
    """
    Format value as currency string.
    
    Args:
        value: Numeric value
        symbol: Currency symbol
        decimals: Number of decimal places
    
    Returns:
        Formatted currency string (e.g., "$110.18")
    """
    try:
        num = float(value)
        return f"{symbol}{num:.{decimals}f}"
    except (ValueError, TypeError):
        return str(value) if value else "N/A"


def get_analysis_folder_path(script_path: Path) -> Path:
    """
    Get analysis folder path from script location.
    Assumes script is in: analyses/YYYY-MM-DD_analysis-name/
    
    Args:
        script_path: Path to the generation script
    
    Returns:
        Path to analysis folder
    """
    return script_path.parent


def validate_data_files(data_dir: Path, required_files: List[str]) -> Dict[str, bool]:
    """
    Validate that required data files exist.
    
    Args:
        data_dir: Directory containing data files
        required_files: List of required filenames
    
    Returns:
        Dictionary mapping filename to exists status
    """
    results = {}
    for filename in required_files:
        file_path = data_dir / filename
        results[filename] = file_path.exists()
        if not results[filename]:
            print(f"Warning: Required data file missing: {filename}")
    return results


# Example usage pattern for report generators:
"""
from pathlib import Path
from .cursor.utils.report_generator_utils import (
    get_workspace_root,
    load_profile_image,
    load_json_data,
    ensure_output_dir,
    safe_write_file,
    get_analysis_folder_path
)

# In your report generation script:
script_path = Path(__file__)
analysis_folder = get_analysis_folder_path(script_path)
workspace_root = get_workspace_root(script_path)

# Load profile image
profile_b64 = load_profile_image(workspace_root)

# Load data
data_dir = analysis_folder / "data"
demographics = load_json_data(data_dir, "01_bug-reporters-demographics.json")

# Generate and save
output_path = analysis_folder / "deliverables" / "report.html"
safe_write_file(output_path, html_content)
"""

