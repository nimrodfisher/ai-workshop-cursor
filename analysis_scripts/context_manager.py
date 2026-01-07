"""
Context Manager - Combines schema from GitHub + user input + real-time data checks
"""

import yaml
import requests
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
from datetime import datetime


class ContextManager:
    """
    Manages analysis context from multiple sources:
    1. Schema definitions from GitHub repo
    2. User input/questions
    3. Real-time data checks
    """
    
    def __init__(self, github_owner: str, github_repo: str):
        self.github_owner = github_owner
        self.github_repo = github_repo
        self.schema_context: Dict[str, Any] = {}
        self.user_context: Dict[str, Any] = {}
        self.data_context: Dict[str, Any] = {}
        self.context_mapping: Dict[str, str] = {}
        
    def load_schema_from_github(self, schema_file: str = "schema.yml") -> Dict[str, Any]:
        """
        Load schema context from GitHub repo
        """
        try:
            url = f"https://raw.githubusercontent.com/{self.github_owner}/{self.github_repo}/main/{schema_file}"
            response = requests.get(url)
            if response.status_code == 200:
                self.schema_context = yaml.safe_load(response.text)
                return self.schema_context
            else:
                print(f"Warning: Could not load schema from GitHub (status {response.status_code})")
                return {}
        except Exception as e:
            print(f"Error loading schema from GitHub: {e}")
            return {}
    
    def load_schema_from_local(self, schema_path: str) -> Dict[str, Any]:
        """Load schema from local file"""
        try:
            with open(schema_path, 'r') as f:
                self.schema_context = yaml.safe_load(f)
            return self.schema_context
        except Exception as e:
            print(f"Error loading local schema: {e}")
            return {}
    
    def add_user_context(self, question: str, clarifications: List[str] = None):
        """Add user input context"""
        self.user_context = {
            'question': question,
            'clarifications': clarifications or [],
            'timestamp': str(datetime.now())
        }
    
    def add_data_context(self, table_name: str, metadata: Dict[str, Any]):
        """Add real-time data context from database checks"""
        if 'tables' not in self.data_context:
            self.data_context['tables'] = {}
        
        self.data_context['tables'][table_name] = {
            **metadata,
            'checked_at': str(datetime.now())
        }
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        Get comprehensive table information from all context sources
        """
        info = {
            'name': table_name,
            'schema_info': None,
            'data_info': None,
            'synonyms': [],
            'relationships': []
        }
        
        # Get from schema context
        if 'models' in self.schema_context:
            for model in self.schema_context['models']:
                if model.get('name') == table_name:
                    info['schema_info'] = model
                    info['synonyms'] = model.get('synonyms', [])
                    break
        
        # Get from data context
        if 'tables' in self.data_context and table_name in self.data_context['tables']:
            info['data_info'] = self.data_context['tables'][table_name]
        
        # Get relationships
        if 'relationships' in self.schema_context:
            for rel in self.schema_context['relationships']:
                if rel.get('from_model') == table_name or rel.get('to_model') == table_name:
                    info['relationships'].append(rel)
        
        return info
    
    def map_user_question_to_schema(self, question: str) -> Dict[str, Any]:
        """
        Map user question to schema elements using synonyms and descriptions
        """
        mapping = {
            'tables': [],
            'columns': [],
            'metrics': [],
            'time_dimensions': []
        }
        
        question_lower = question.lower()
        
        # Check for table matches
        if 'models' in self.schema_context:
            for model in self.schema_context['models']:
                table_name = model.get('name', '')
                synonyms = model.get('synonyms', [])
                description = model.get('description', '')
                
                # Check if question mentions table or synonyms
                if (table_name.lower() in question_lower or
                    any(syn.lower() in question_lower for syn in synonyms) or
                    any(word in description.lower() for word in question_lower.split())):
                    mapping['tables'].append({
                        'name': table_name,
                        'confidence': 'high' if table_name.lower() in question_lower else 'medium',
                        'synonyms': synonyms,
                        'description': description
                    })
        
        # Check for metric matches
        if 'common_metrics' in self.schema_context:
            for metric in self.schema_context['common_metrics']:
                metric_name = metric.get('name', '')
                synonyms = metric.get('synonyms', [])
                
                if (metric_name.lower() in question_lower or
                    any(syn.lower() in question_lower for syn in synonyms)):
                    mapping['metrics'].append({
                        'name': metric_name,
                        'calculation': metric.get('calculation', ''),
                        'synonyms': synonyms
                    })
        
        # Check for common business questions
        if 'common_business_questions' in self.schema_context:
            for q in self.schema_context['common_business_questions']:
                question_text = q.get('question', '')
                synonyms = q.get('synonyms', [])
                
                if (any(syn.lower() in question_lower for syn in synonyms) or
                    any(word in question_text.lower() for word in question_lower.split()[:5])):
                    mapping['query_pattern'] = q.get('query_pattern', '')
                    mapping['matched_question'] = question_text
        
        return mapping
    
    def get_query_suggestions(self, question: str) -> List[str]:
        """Get query suggestions based on context"""
        suggestions = []
        
        mapping = self.map_user_question_to_schema(question)
        
        if mapping.get('query_pattern'):
            suggestions.append(f"Use query pattern: {mapping['query_pattern']}")
        
        if mapping['tables']:
            table_names = [t['name'] for t in mapping['tables']]
            suggestions.append(f"Consider tables: {', '.join(table_names)}")
        
        if mapping['metrics']:
            metric_names = [m['name'] for m in mapping['metrics']]
            suggestions.append(f"Relevant metrics: {', '.join(metric_names)}")
        
        return suggestions
    
    def build_context_summary(self) -> str:
        """Build a comprehensive context summary for analysis"""
        summary_parts = []
        
        # Schema context
        if self.schema_context:
            summary_parts.append("## Schema Context")
            if 'models' in self.schema_context:
                summary_parts.append(f"Available tables: {len(self.schema_context['models'])}")
            if 'common_metrics' in self.schema_context:
                summary_parts.append(f"Defined metrics: {len(self.schema_context['common_metrics'])}")
        
        # User context
        if self.user_context:
            summary_parts.append("\n## User Context")
            summary_parts.append(f"Question: {self.user_context.get('question', 'N/A')}")
            if self.user_context.get('clarifications'):
                summary_parts.append(f"Clarifications: {len(self.user_context['clarifications'])} needed")
        
        # Data context
        if self.data_context.get('tables'):
            summary_parts.append("\n## Data Context")
            for table_name, info in self.data_context['tables'].items():
                row_count = info.get('row_count', 'unknown')
                summary_parts.append(f"{table_name}: {row_count:,} rows")
        
        return "\n".join(summary_parts)
    
    def save_context_mapping(self, filepath: str):
        """Save context mapping to file"""
        mapping = {
            'schema_context': self.schema_context,
            'user_context': self.user_context,
            'data_context': self.data_context,
            'context_mapping': self.context_mapping
        }
        with open(filepath, 'w') as f:
            json.dump(mapping, f, indent=2, default=str)
    
    def load_context_mapping(self, filepath: str):
        """Load context mapping from file"""
        with open(filepath, 'r') as f:
            mapping = json.load(f)
        self.schema_context = mapping.get('schema_context', {})
        self.user_context = mapping.get('user_context', {})
        self.data_context = mapping.get('data_context', {})

