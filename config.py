import yaml
import os
from typing import Dict, Any, Optional, List

class ConfigManager:
    """
    Handles loading and accessing configuration from the YAML file.
    """
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """
        Loads the configuration from the YAML file.
        """
        config_path = os.path.join(os.path.dirname(__file__), "prompts.yaml")
        with open(config_path, "r") as file:
            self._config = yaml.safe_load(file)
    
    def get_persona(self, persona_type: str) -> Dict[str, Any]:
        """
        Get a specific persona configuration.
        
        Args:
            persona_type (str): The type of persona to retrieve
            
        Returns:
            Dict[str, Any]: The persona configuration
        """
        return self._config.get("personas", {}).get(persona_type, {})
    
    def get_prompt(self, prompt_type: str, prompt_name: str = "base") -> Optional[str]:
        """
        Get a specific prompt template.
        
        Args:
            prompt_type (str): The type of prompt (student_analysis, roadmap_creation, etc.)
            prompt_name (str): The name of the prompt within that type
            
        Returns:
            Optional[str]: The prompt template or None if not found
        """
        return self._config.get("prompts", {}).get(prompt_type, {}).get(prompt_name)
    
    def get_learning_style_info(self, learning_style: str) -> Dict[str, Any]:
        """
        Get learning style-specific information.
        
        Args:
            learning_style (str): The learning style name
            
        Returns:
            Dict[str, Any]: The learning style configuration
        """
        return self._config.get("learning_styles", {}).get(learning_style, {})
    
    def get_subject_category_info(self, category: str) -> Dict[str, Any]:
        """
        Get subject category information.
        
        Args:
            category (str): The subject category name
            
        Returns:
            Dict[str, Any]: The subject category configuration
        """
        return self._config.get("subject_categories", {}).get(category, {})
    
    def get_knowledge_level_info(self, level: str) -> Dict[str, Any]:
        """
        Get knowledge level information.
        
        Args:
            level (str): The knowledge level
            
        Returns:
            Dict[str, Any]: The knowledge level configuration
        """
        return self._config.get("knowledge_levels", {}).get(level, {})
    
    def get_all_subject_categories(self) -> List[str]:
        """
        Get list of all available subject categories.
        
        Returns:
            List[str]: List of subject category names
        """
        return list(self._config.get("subject_categories", {}).keys())
    
    def get_all_learning_styles(self) -> List[str]:
        """
        Get list of all available learning styles.
        
        Returns:
            List[str]: List of learning style names
        """
        return list(self._config.get("learning_styles", {}).keys())
    
    def get_all_knowledge_levels(self) -> List[str]:
        """
        Get list of all available knowledge levels.
        
        Returns:
            List[str]: List of knowledge level names
        """
        return list(self._config.get("knowledge_levels", {}).keys())
    
    def format_prompt(self, prompt_type: str, prompt_name: str = "base", **kwargs) -> Optional[str]:
        """
        Get and format a prompt template with variables.
        
        Args:
            prompt_type (str): The type of prompt
            prompt_name (str): The name of the prompt within that type
            **kwargs: Variables to insert into the template
            
        Returns:
            Optional[str]: The formatted prompt or None if template not found
        """
        template = self.get_prompt(prompt_type, prompt_name)
        if template:
            return template.format(**kwargs)
        return None
