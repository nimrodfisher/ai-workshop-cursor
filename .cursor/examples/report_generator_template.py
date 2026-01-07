"""
Template for generating branded HTML reports
Uses utility functions for reliable path handling and image loading

Copy this to your analysis folder and customize the data sections.
"""

import sys
from pathlib import Path

# Add workspace root to path to import utilities
workspace_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(workspace_root))

try:
    from .cursor.utils.report_generator_utils import (
    get_workspace_root,
    load_profile_image,
    load_json_data,
    safe_write_file,
    get_analysis_folder_path,
    validate_data_files
)
from datetime import datetime
import json

# ============================================================================
# SETUP: Paths and Configuration
# ============================================================================

script_path = Path(__file__)
analysis_folder = get_analysis_folder_path(script_path)
workspace_root = get_workspace_root(script_path)
data_dir = analysis_folder / "data"

# Validate required data files
required_files = [
    "01_bug-reporters-demographics.json",
    # Add your required files here
]
validation_results = validate_data_files(data_dir, required_files)

# ============================================================================
# LOAD DATA
# ============================================================================

# Load profile image (handles path resolution automatically)
profile_b64 = load_profile_image(workspace_root)

# Load your data files
demographics = load_json_data(data_dir, "01_bug-reporters-demographics.json")
# Add more data loading as needed

# ============================================================================
# PREPARE DATA FOR CHARTS/TABLES
# ============================================================================

# Example: Prepare chart data
role_data = {r['user_role']: float(r['bug_reporter_pct']) for r in demographics}

# ============================================================================
# GENERATE HTML CONTENT
# ============================================================================

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Analysis Title | Nimrod Fisher</title>
    <!-- Add your CSS and scripts here -->
</head>
<body>
    <div class="report-header">
        {f'<img src="{profile_b64}" alt="Profile" class="profile">' if profile_b64 else ''}
        <div class="header-content">
            <h1>Your Analysis Title</h1>
            <p>{datetime.now().strftime('%B %d, %Y')} • Nimrod Fisher | AI Analytics Hub</p>
        </div>
    </div>
    <!-- Add your report content here -->
</body>
</html>
"""

# ============================================================================
# SAVE REPORT
# ============================================================================

output_path = analysis_folder / "deliverables" / "report.html"
if safe_write_file(output_path, html_content):
    print(f"[SUCCESS] HTML report generated: {output_path.absolute()}")
else:
    print(f"[ERROR] Failed to generate report")
    sys.exit(1)

