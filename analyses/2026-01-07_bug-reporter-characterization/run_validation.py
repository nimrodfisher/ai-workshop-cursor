"""
Phase 1: Data Validation & Sanity Checks
Bug Reporter Characterization Analysis
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'analysis_scripts'))

from analysis_framework import AnalysisFramework
import json
from datetime import datetime

def main():
    print("=" * 80)
    print("PHASE 1: DATA VALIDATION & SANITY CHECKS")
    print("=" * 80)
    print()
    
    # Initialize framework
    framework = AnalysisFramework()
    framework.connect()
    
    print("✓ Connected to database")
    print()
    
    # Tables to validate
    tables_to_validate = ['support_tickets', 'users', 'accounts', 'events']
    
    validation_results = {}
    
    for table in tables_to_validate:
        print(f"\n{'=' * 80}")
        print(f"Validating: {table}")
        print('=' * 80)
        
        # Run sanity checks
        results = framework.sanity_checker.run_checks(table)
        validation_results[table] = results
        
        # Display results
        print(f"\nTotal Checks: {results['summary']['total_checks']}")
        print(f"✓ Passed: {results['summary']['passed_checks']}")
        print(f"⚠ Warnings: {results['summary']['warnings']}")
        print(f"✗ Failed: {results['summary']['failed_checks']}")
        
        if results['checks']:
            print("\nCheck Details:")
            for check in results['checks']:
                status_icon = "✓" if check['status'] == 'pass' else "⚠" if check['status'] == 'warning' else "✗"
                print(f"  {status_icon} {check['check_name']}: {check['message']}")
                if check.get('details'):
                    for key, value in check['details'].items():
                        print(f"      - {key}: {value}")
    
    # Save validation results
    output_file = os.path.join(os.path.dirname(__file__), 'data', '00_validation_results.json')
    with open(output_file, 'w') as f:
        json.dump(validation_results, f, indent=2, default=str)
    
    print(f"\n{'=' * 80}")
    print(f"✓ Validation results saved to: {output_file}")
    print('=' * 80)
    
    # Identify bug-related categories
    print(f"\n{'=' * 80}")
    print("IDENTIFYING BUG-RELATED CATEGORIES")
    print('=' * 80)
    
    category_query = """
    SELECT 
        category,
        COUNT(*) as ticket_count,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_of_total
    FROM support_tickets
    WHERE category IS NOT NULL
    GROUP BY category
    ORDER BY ticket_count DESC;
    """
    
    cursor = framework.connection.cursor()
    cursor.execute(category_query)
    categories = cursor.fetchall()
    cursor.close()
    
    print("\nSupport Ticket Categories:")
    print("-" * 60)
    bug_categories = []
    for cat, count, pct in categories:
        print(f"  {cat}: {count} tickets ({pct}%)")
        # Identify bug-related categories
        if cat and any(keyword in cat.lower() for keyword in ['bug', 'technical', 'error', 'issue', 'problem', 'defect']):
            bug_categories.append(cat)
    
    print(f"\n✓ Identified bug-related categories: {bug_categories}")
    
    # Save bug categories for later use
    bug_info = {
        'bug_categories': bug_categories,
        'all_categories': [{'category': cat, 'count': count, 'percentage': pct} for cat, count, pct in categories],
        'identified_at': datetime.now().isoformat()
    }
    
    bug_file = os.path.join(os.path.dirname(__file__), 'data', '00_bug_categories.json')
    with open(bug_file, 'w') as f:
        json.dump(bug_info, f, indent=2)
    
    print(f"✓ Bug categories saved to: {bug_file}")
    
    # Summary
    print(f"\n{'=' * 80}")
    print("VALIDATION SUMMARY")
    print('=' * 80)
    
    total_checks = sum(r['summary']['total_checks'] for r in validation_results.values())
    total_passed = sum(r['summary']['passed_checks'] for r in validation_results.values())
    total_warnings = sum(r['summary']['warnings'] for r in validation_results.values())
    total_failed = sum(r['summary']['failed_checks'] for r in validation_results.values())
    
    print(f"\nOverall Results:")
    print(f"  Total Checks: {total_checks}")
    print(f"  ✓ Passed: {total_passed}")
    print(f"  ⚠ Warnings: {total_warnings}")
    print(f"  ✗ Failed: {total_failed}")
    
    if total_failed == 0:
        print(f"\n✓ DATA QUALITY: READY FOR ANALYSIS")
    else:
        print(f"\n⚠ DATA QUALITY: NEEDS ATTENTION")
    
    print('=' * 80)
    
    framework.close()
    return validation_results, bug_categories

if __name__ == "__main__":
    main()




