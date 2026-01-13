/*
================================================================================
STANDARD VALIDATION QUERIES
================================================================================
Purpose: Standard SQL-based data quality and exploratory checks.
Author: Nimrod Fisher | AI Analytics Hub
Created: 2026-01-05
================================================================================
*/

-- @name: null_check
-- @description: Checks for null values in critical columns
-- @params: table_name, columns_list
SELECT 
    '{{table_name}}' as table_name,
    COUNT(*) as total_rows,
    {% for col in columns %}
    COUNT({{col}}) as non_null_{{col}},
    COUNT(*) - COUNT({{col}}) as null_{{col}},
    ROUND(100.0 * (COUNT(*) - COUNT({{col}})) / NULLIF(COUNT(*), 0), 2) as null_pct_{{col}}{% if not loop.last %},{% endif %}
    {% endfor %}
FROM {{table_name}};

-- @name: duplicate_check
-- @description: Checks for duplicate primary keys
-- @params: table_name, pk_column
SELECT 
    '{{table_name}}' as table_name,
    COUNT(*) as total_rows,
    COUNT(DISTINCT {{pk_column}}) as unique_{{pk_column}},
    COUNT(*) - COUNT(DISTINCT {{pk_column}}) as duplicate_count
FROM {{table_name}};

-- @name: enum_check
-- @description: Checks distribution of categorical values
-- @params: table_name, column_name
SELECT 
    {{column_name}},
    COUNT(*) as count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM {{table_name}}), 2) as percentage
FROM {{table_name}}
GROUP BY {{column_name}}
ORDER BY count DESC;

-- @name: date_range_check
-- @description: Checks date ranges and validity
-- @params: table_name, start_col, end_col
SELECT 
    '{{table_name}}' as table_name,
    MIN({{start_col}}) as min_start,
    MAX({{start_col}}) as max_start,
    COUNT(CASE WHEN {{start_col}} > {{end_col}} THEN 1 END) as invalid_date_sequence
FROM {{table_name}}
WHERE {{start_col}} IS NOT NULL AND {{end_col}} IS NOT NULL;

-- @name: numeric_stats
-- @description: Basic numeric statistics
-- @params: table_name, column_name
SELECT 
    '{{table_name}}' as table_name,
    '{{column_name}}' as column_name,
    MIN({{column_name}}) as min_val,
    MAX({{column_name}}) as max_val,
    AVG({{column_name}}) as avg_val,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY {{column_name}}) as median_val
FROM {{table_name}};






