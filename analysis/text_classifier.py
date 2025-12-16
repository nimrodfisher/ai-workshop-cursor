"""
Text Classification Module
Uses LLM to classify text data and create new buckets for analysis
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import json


class TextClassifier:
    """
    Classifies text data using LLM based on user context
    """
    
    def __init__(self, llm_provider=None):
        """
        Initialize text classifier
        
        Args:
            llm_provider: Optional LLM provider (for future integration)
        """
        self.llm_provider = llm_provider
        self.classification_results: List[Dict[str, Any]] = []
    
    def classify_text_column(
        self,
        df: pd.DataFrame,
        column_name: str,
        user_context: str,
        classification_prompt: Optional[str] = None,
        num_categories: int = 5
    ) -> Dict[str, Any]:
        """
        Classify text column using LLM based on user context
        
        Args:
            df: DataFrame with text column
            column_name: Name of column to classify
            user_context: User's context/requirements for classification
            classification_prompt: Optional custom prompt
            num_categories: Expected number of categories
        
        Returns:
            Dictionary with classification results
        """
        if column_name not in df.columns:
            return {'error': f"Column '{column_name}' not found"}
        
        # Get unique values (sample if too many)
        unique_values = df[column_name].dropna().unique()
        if len(unique_values) > 100:
            unique_values = df[column_name].dropna().value_counts().head(100).index.tolist()
        
        # Create classification prompt
        if not classification_prompt:
            classification_prompt = self._create_classification_prompt(
                unique_values[:20],  # Sample
                user_context,
                num_categories
            )
        
        # For now, return structure (LLM integration would go here)
        # In production, this would call an LLM API
        result = {
            'column_name': column_name,
            'user_context': user_context,
            'classification_prompt': classification_prompt,
            'unique_values_count': len(unique_values),
            'sample_values': unique_values[:10].tolist(),
            'categories': self._suggest_categories(unique_values, user_context, num_categories),
            'note': 'LLM classification would be performed here based on user context'
        }
        
        self.classification_results.append(result)
        return result
    
    def _create_classification_prompt(
        self,
        sample_values: List[str],
        user_context: str,
        num_categories: int
    ) -> str:
        """Create classification prompt for LLM"""
        prompt = f"""
        Based on the user's context: "{user_context}"
        
        Classify the following text values into {num_categories} meaningful categories:
        
        Sample values:
        {json.dumps(sample_values[:20], indent=2)}
        
        Please:
        1. Create {num_categories} category names that make sense for this context
        2. Assign each value to a category
        3. Provide a mapping of value -> category
        
        Return the classification as JSON with:
        - categories: list of category names
        - mappings: dict of value -> category
        """
        return prompt
    
    def _suggest_categories(
        self,
        values: List[str],
        user_context: str,
        num_categories: int
    ) -> List[Dict[str, Any]]:
        """
        Suggest categories based on patterns (fallback when LLM not available)
        This is a simple heuristic - in production, use LLM
        """
        categories = []
        
        # Simple keyword-based categorization as fallback
        if 'error' in user_context.lower() or 'issue' in user_context.lower():
            categories = ['Error', 'Warning', 'Info', 'Other']
        elif 'sentiment' in user_context.lower():
            categories = ['Positive', 'Negative', 'Neutral', 'Mixed']
        elif 'priority' in user_context.lower():
            categories = ['High', 'Medium', 'Low', 'Critical']
        else:
            # Default categories
            categories = [f'Category {i+1}' for i in range(num_categories)]
        
        return [
            {
                'name': cat,
                'description': f'Category for {cat.lower()} items',
                'sample_values': []
            }
            for cat in categories
        ]
    
    def apply_classification(
        self,
        df: pd.DataFrame,
        column_name: str,
        classification_mapping: Dict[str, str]
    ) -> pd.DataFrame:
        """
        Apply classification mapping to DataFrame
        
        Args:
            df: DataFrame to classify
            column_name: Column to classify
            classification_mapping: Dict mapping original values to categories
        
        Returns:
            DataFrame with new classification column
        """
        df_classified = df.copy()
        new_column_name = f"{column_name}_classified"
        
        df_classified[new_column_name] = df_classified[column_name].map(
            classification_mapping
        ).fillna('Uncategorized')
        
        return df_classified
    
    def analyze_classified_data(
        self,
        df: pd.DataFrame,
        original_column: str,
        classified_column: str
    ) -> Dict[str, Any]:
        """
        Analyze data after classification
        
        Returns:
            Analysis of classified data
        """
        analysis = {
            'category_counts': df[classified_column].value_counts().to_dict(),
            'category_percentages': (df[classified_column].value_counts() / len(df) * 100).to_dict(),
            'total_classified': len(df[df[classified_column] != 'Uncategorized']),
            'uncategorized_count': len(df[df[classified_column] == 'Uncategorized']),
            'categories': list(df[classified_column].unique())
        }
        
        return analysis


def classify_with_llm(
    text_values: List[str],
    user_context: str,
    num_categories: int = 5
) -> Dict[str, str]:
    """
    Placeholder for LLM-based classification
    In production, this would call an LLM API (OpenAI, Anthropic, etc.)
    
    Args:
        text_values: List of text values to classify
        user_context: User's context for classification
        num_categories: Number of categories to create
    
    Returns:
        Dictionary mapping original values to categories
    """
    # This is a placeholder - actual implementation would:
    # 1. Call LLM API with classification prompt
    # 2. Parse LLM response
    # 3. Return mapping
    
    # For now, return a simple mapping structure
    return {
        value: f"Category_{hash(value) % num_categories + 1}"
        for value in text_values
    }

