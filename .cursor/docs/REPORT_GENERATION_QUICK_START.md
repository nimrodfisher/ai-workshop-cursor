# Report Generation Quick Start Guide

## What Changed

The template and guidelines have been updated to use utility functions that ensure reliable path handling and error management.

## Key Improvements

✅ **Automatic path resolution** - Works from any directory  
✅ **Profile image loading** - No more path issues  
✅ **Data validation** - Checks files exist before processing  
✅ **Error handling** - Clear messages when things go wrong  
✅ **UTF-8 encoding** - No Unicode errors on Windows  

## How to Use (3 Steps)

### Step 1: Copy Template

Copy `.cursor/examples/generate_html_report_template.py` to your analysis folder:

```
analyses/2026-01-02_your-analysis/
└── generate_html_report.py  (copied from template)
```

### Step 2: Customize Data Section

Update the data loading section:

```python
# List your required data files
required_files = [
    "01_bug-reporters-demographics.json",
    "02_bug-reporters-user-behavior.json",
]

# Validate files exist
validation_results = validate_data_files(data_dir, required_files)
if not all(validation_results.values()):
    print("Error: Missing required data files")
    sys.exit(1)

# Load your data
demographics = load_json_data(data_dir, "01_bug-reporters-demographics.json")
behavior = load_json_data(data_dir, "02_bug-reporters-user-behavior.json")
```

### Step 3: Run Script

```bash
# Windows
py generate_html_report.py

# Unix/Mac
python3 generate_html_report.py
```

## What the Utilities Handle Automatically

1. **Profile Image Path** - Finds `.cursor/assets/photo.jpg` automatically
2. **Workspace Root** - Detects workspace root from any directory
3. **Analysis Folder** - Resolves analysis folder from script location
4. **Output Directory** - Creates `deliverables/` folder if needed
5. **File Encoding** - Uses UTF-8 to prevent Unicode errors

## Common Patterns

### Loading Multiple Data Files

```python
data_files = {
    "demographics": "01_bug-reporters-demographics.json",
    "behavior": "02_bug-reporters-user-behavior.json",
}

data = {}
for key, filename in data_files.items():
    data[key] = load_json_data(data_dir, filename)
```

### Handling Missing Data Gracefully

```python
demographics = load_json_data(data_dir, "01_data.json")
if not demographics:
    print("Warning: No demographics data, using empty dataset")
    demographics = []
```

## Troubleshooting

**Issue:** "Could not import utility functions"  
**Solution:** Ensure `.cursor/utils/report_generator_utils.py` exists

**Issue:** Profile image not showing  
**Solution:** Check that `.cursor/assets/photo.jpg` exists in workspace root

**Issue:** "Missing required data files"  
**Solution:** Verify JSON files exist in `data/` folder with correct names

## Next Steps

After generating the HTML report:
1. Test it opens correctly in a browser
2. Verify profile image appears
3. Check all charts render properly
4. Then ask about interactive dashboard or PDF if needed






