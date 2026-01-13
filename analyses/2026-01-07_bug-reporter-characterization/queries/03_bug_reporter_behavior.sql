/*
================================================================================
QUERY: Bug Reporter Behavioral Patterns - Before and After First Bug Report
================================================================================
Business Question: What specific behaviors precede bug reporting?
Author: AI Analytics
Created: 2026-01-07
Last Modified: 2026-01-07
-----
DESCRIPTION:
  Analyzes the behavioral patterns of bug reporters in the 7 days before and after
  their first bug report. Identifies triggering events and post-report behavior changes.

DEPENDENCIES:
  - support_tickets: To identify first bug ticket per user
  - users: For user information
  - events: For behavioral event tracking

OUTPUT:
  - user_id: User identifier
  - first_bug_ticket_date: Date of first bug report
  - days_from_signup_to_bug: Days from user creation to first bug
  - events_before_bug: Count of events in 7 days before bug report
  - events_after_bug: Count of events in 7 days after bug report
  - event_types_before: Event types used before bug
  - event_types_after: Event types used after bug
  - most_recent_event_before_bug: Last event type before bug report
  - hours_since_last_event: Hours from last event to bug report

NOTES:
  - Only includes users who have opened bug tickets
  - Time window: 7 days before and after first bug ticket
  - Helps identify if specific events/patterns trigger bug reporting
================================================================================
*/

WITH first_bug_tickets AS (
    -- Get the first bug ticket for each user
    SELECT 
        opened_by as user_id,
        MIN(opened_at) as first_bug_date,
        COUNT(*) as total_bug_tickets
    FROM support_tickets
    WHERE category = 'bug'
        AND opened_by IS NOT NULL
    GROUP BY opened_by
),

user_bug_context AS (
    -- Add user context to first bug tickets
    SELECT 
        fbt.user_id,
        u.role,
        u.created_at as user_created_at,
        fbt.first_bug_date,
        fbt.total_bug_tickets,
        EXTRACT(EPOCH FROM (fbt.first_bug_date - u.created_at)) / 86400 as days_from_signup_to_bug
    FROM first_bug_tickets fbt
    JOIN users u ON fbt.user_id = u.id
),

events_before_bug AS (
    -- Events in 7 days BEFORE first bug
    SELECT 
        ubc.user_id,
        COUNT(e.id) as events_before,
        COUNT(DISTINCT e.event_type) as unique_types_before,
        STRING_AGG(DISTINCT e.event_type, ', ' ORDER BY e.event_type) as event_types_before,
        MAX(e.occurred_at) as last_event_before_bug
    FROM user_bug_context ubc
    LEFT JOIN events e ON ubc.user_id = e.user_id
        AND e.occurred_at < ubc.first_bug_date
        AND e.occurred_at >= ubc.first_bug_date - INTERVAL '7 days'
    GROUP BY ubc.user_id
),

events_after_bug AS (
    -- Events in 7 days AFTER first bug
    SELECT 
        ubc.user_id,
        COUNT(e.id) as events_after,
        COUNT(DISTINCT e.event_type) as unique_types_after,
        STRING_AGG(DISTINCT e.event_type, ', ' ORDER BY e.event_type) as event_types_after
    FROM user_bug_context ubc
    LEFT JOIN events e ON ubc.user_id = e.user_id
        AND e.occurred_at > ubc.first_bug_date
        AND e.occurred_at <= ubc.first_bug_date + INTERVAL '7 days'
    GROUP BY ubc.user_id
),

last_event_details AS (
    -- Get details of the most recent event before bug
    SELECT DISTINCT ON (ubc.user_id)
        ubc.user_id,
        e.event_type as last_event_type,
        EXTRACT(EPOCH FROM (ubc.first_bug_date - e.occurred_at)) / 3600 as hours_since_last_event
    FROM user_bug_context ubc
    LEFT JOIN events e ON ubc.user_id = e.user_id
        AND e.occurred_at < ubc.first_bug_date
    ORDER BY ubc.user_id, e.occurred_at DESC
)

-- Final output
SELECT 
    ubc.user_id,
    ubc.role,
    ubc.first_bug_date,
    ROUND(ubc.days_from_signup_to_bug::numeric, 2) as days_from_signup_to_bug,
    ubc.total_bug_tickets,
    COALESCE(ebb.events_before, 0) as events_before_bug,
    COALESCE(eab.events_after, 0) as events_after_bug,
    COALESCE(ebb.unique_types_before, 0) as unique_types_before,
    COALESCE(eab.unique_types_after, 0) as unique_types_after,
    ebb.event_types_before,
    eab.event_types_after,
    led.last_event_type,
    ROUND(led.hours_since_last_event::numeric, 2) as hours_since_last_event
FROM user_bug_context ubc
LEFT JOIN events_before_bug ebb ON ubc.user_id = ebb.user_id
LEFT JOIN events_after_bug eab ON ubc.user_id = eab.user_id
LEFT JOIN last_event_details led ON ubc.user_id = led.user_id
ORDER BY ubc.first_bug_date;




