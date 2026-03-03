"""
Configuration management for Volcengine API Skill.

Supports multi-level configuration: Environment > Project > Global > Defaults
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
import yaml


class ConfigManager:
    """
    Manages configuration with priority-based loading.
    
    Priority order (highest to lowest):
    1. Environment variables
    2. Project configuration (.volcengine/config.yaml)
    3. Global configuration (~/.volcengine/config.yaml)
    4. Default values
    """
    
    DEFAULT_CONFIG = {
        "api_key": None,
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "timeout": 30,
        "max_retries": 3,
        "output_dir": "./output",
        "default_image_width": 1024,
        "default_image_height": 1024,
        "default_video_duration": 5.0,
    }
    
    def __init__(
        self,
        project_root: Optional[Path] = None,
        config_dir: Optional[str] = ".volcengine"
    ):
        self.project_root = project_root or Path.cwd()
        self.config_dir = config_dir
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from all sources in priority order."""
        # Start with defaults
        self._config = self.DEFAULT_CONFIG.copy()
        
        # Load global config
        global_config_path = Path.home() / ".volcengine" / "config.yaml"
        if global_config_path.exists():
            self._load_yaml_config(global_config_path)
        
        # Load project config
        project_config_path = self.project_root / self.config_dir / "config.yaml"
        if project_config_path.exists():
            self._load_yaml_config(project_config_path)
        
        # Load environment variables (highest priority)
        self._load_env_config()
    
    def _load_yaml_config(self, config_path: Path) -> None:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    self._config.update(yaml_config)
        except Exception:
            # Silently ignore config file errors
            pass
    
    def _load_env_config(self) -> None:
        """Load configuration from environment variables."""
        env_mappings = {
            "ARK_API_KEY": "api_key",
            "VOLCENGINE_BASE_URL": "base_url",
            "VOLCENGINE_TIMEOUT": "timeout",
            "VOLCENGINE_MAX_RETRIES": "max_retries",
            "VOLCENGINE_OUTPUT_DIR": "output_dir",
        }
        
        for env_var, config_key in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                # Convert to appropriate type
                if config_key == "timeout":
                    value = int(value)
                elif config_key == "max_retries":
                    value = int(value)
                self._config[config_key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value (in memory only).
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self._config[key] = value
    
    def get_api_key(self) -> Optional[str]:
        """Get API key from configuration."""
        return self.get("api_key")
    
    def get_base_url(self) -> str:
        """Get API base URL."""
        return self.get("base_url")
    
    def get_timeout(self) -> int:
        """Get request timeout in seconds."""
        return self.get("timeout")
    
    def get_output_dir(self) -> Path:
        """Get output directory path."""
        output_dir = self.get("output_dir")
        path = Path(output_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    def to_dict(self) -> Dict[str, Any]:
        """Get all configuration as dictionary."""
        return self._config.copy()
    
    def save_project_config(self) -> None:
        """Save current configuration to project config file."""
        config_path = self.project_root / self.config_dir / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(self._config, f, default_flow_style=False)
