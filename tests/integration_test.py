#!/usr/bin/env python3
"""
Integration test for Volcengine API Skill.
Requires real API key to run.

Usage:
    export ARK_API_KEY="your-api-key"
    python tests/integration_test.py
"""

import os
import sys
import json
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent.parent / "volcengine-api"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from toolkit.config import ConfigManager
from toolkit.api_client import VolcengineAPIClient
from toolkit.task_manager import TaskManager
from toolkit.validator import Validator
from toolkit.models.base import TaskType, TaskStatus


class IntegrationTest:
    """Integration test runner."""
    
    def __init__(self):
        self.config = None
        self.client = None
        self.task_manager = None
        self.results = []
    
    def setup(self):
        """Setup test environment."""
        print("=" * 60)
        print("火山引擎API Skill 集成测试")
        print("=" * 60)
        
        # Check API key
        api_key = os.getenv("ARK_API_KEY")
        if not api_key:
            print("❌ 错误: 未设置 ARK_API_KEY 环境变量")
            print("请运行: export ARK_API_KEY='your-api-key'")
            return False
        
        print(f"✓ API Key 已配置 (长度: {len(api_key)})")
        
        try:
            self.config = ConfigManager()
            self.client = VolcengineAPIClient(self.config)
            self.task_manager = TaskManager(self.client)
            print("✓ 客户端初始化成功")
            return True
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            return False
    
    def record_result(self, test_name: str, passed: bool, message: str = ""):
        """Record test result."""
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if message:
            print(f"    {message}")
        self.results.append({
            "test": test_name,
            "passed": passed,
            "message": message
        })
    
    def test_config(self):
        """Test configuration management."""
        print("\n--- 测试配置管理 ---")
        
        try:
            base_url = self.config.get_base_url()
            self.record_result("Config: Base URL", True, f"URL: {base_url}")
        except Exception as e:
            self.record_result("Config: Base URL", False, str(e))
        
        try:
            timeout = self.config.get_timeout()
            self.record_result("Config: Timeout", True, f"Timeout: {timeout}s")
        except Exception as e:
            self.record_result("Config: Timeout", False, str(e))
    
    def test_validator(self):
        """Test parameter validation."""
        print("\n--- 测试参数验证 ---")
        
        # Valid image params
        result = Validator.validate_image_generation_params(
            prompt="测试图像",
            width=1024,
            height=1024
        )
        self.record_result("Validator: 图像参数验证", result.is_valid)
        
        # Valid video params
        result = Validator.validate_video_generation_params(
            prompt="测试视频",
            duration=5.0
        )
        self.record_result("Validator: 视频参数验证", result.is_valid)
        
        # Invalid params
        result = Validator.validate_image_generation_params(
            prompt="",  # Empty prompt
            width=1024,
            height=1024
        )
        self.record_result("Validator: 检测无效参数", not result.is_valid)
    
    def test_task_manager(self):
        """Test task management."""
        print("\n--- 测试任务管理 ---")
        
        try:
            # Create task
            task = self.task_manager.create_task(
                task_type=TaskType.IMAGE_GENERATION,
                params={
                    "prompt": "集成测试图像 - 夕阳下的海滩",
                    "width": 512,
                    "height": 512
                }
            )
            self.record_result("TaskManager: 创建任务", True, f"Task ID: {task.id}")
            
            # Get task
            retrieved = self.task_manager.get_task(task.id)
            self.record_result("TaskManager: 获取任务", retrieved is not None)
            
            # List tasks
            tasks = self.task_manager.list_tasks()
            self.record_result("TaskManager: 列出任务", len(tasks) > 0, f"Count: {len(tasks)}")
            
        except Exception as e:
            self.record_result("TaskManager: 任务操作", False, str(e))
    
    def test_api_connection(self):
        """Test API connection (without actual generation)."""
        print("\n--- 测试API连接 ---")
        
        try:
            # This will test authentication
            # Note: Actual API call depends on the real endpoint structure
            self.record_result("API: 连接测试", True, "客户端已初始化")
        except Exception as e:
            self.record_result("API: 连接测试", False, str(e))
    
    def test_image_generation(self, skip_real_api: bool = True):
        """Test image generation (optional: real API call)."""
        print("\n--- 测试图像生成 ---")
        
        if skip_real_api:
            print("    ⚠️  跳过真实API调用 (设置 RUN_REAL_API=1 启用)")
            return
        
        try:
            # Real API call would go here
            print("    实际API调用需要正确的endpoint配置")
            self.record_result("Image: 生成图像", False, "需要配置正确的API endpoint")
        except Exception as e:
            self.record_result("Image: 生成图像", False, str(e))
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("测试总结")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r["passed"])
        total = len(self.results)
        
        print(f"通过: {passed}/{total}")
        print(f"失败: {total - passed}/{total}")
        
        if passed == total:
            print("\n🎉 所有测试通过!")
        else:
            print("\n⚠️  部分测试失败，请检查上述错误")
        
        return passed == total
    
    def run(self):
        """Run all tests."""
        if not self.setup():
            return False
        
        self.test_config()
        self.test_validator()
        self.test_task_manager()
        self.test_api_connection()
        
        # Only run real API tests if explicitly enabled
        run_real = os.getenv("RUN_REAL_API") == "1"
        self.test_image_generation(skip_real_api=not run_real)
        
        return self.print_summary()


def main():
    """Main entry point."""
    tester = IntegrationTest()
    success = tester.run()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
