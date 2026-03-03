"""
Guide generator for Volcengine API Skill.

Provides contextual guidance for users.
"""

from typing import List, Dict, Any, Optional
from toolkit.models.base import TaskType
from toolkit.state_manager import StateManager


class GuideGenerator:
    """
    Generates contextual guidance for users.
    
    Features:
    - Initial welcome guide
    - Post-operation suggestions
    - Context-aware recommendations
    - User preference learning
    """
    
    @staticmethod
    def get_welcome_guide() -> str:
        """
        Get initial welcome guide.
        
        Returns:
            Welcome message with available features
        """
        return """
🎨 火山引擎API助手已就绪！

我可以帮您：

1. 生成图像
   - 文本生成图片（Seedream 4.0）
   - 图片编辑
   - 图生图

2. 生成视频
   - 文本生成视频（Seedance 1.5）
   - 图片生成视频
   - 控制镜头运动

3. 音频生成
   - 文本转语音（TTS）

4. 视觉理解
   - 图像内容分析
   - 对象检测

5. 任务管理
   - 查看生成进度
   - 下载结果
   - 管理历史记录

6. 配置设置
   - 设置API Key
   - 调整默认参数
   - 查看配置

请告诉我您想要做什么？
"""
    
    @staticmethod
    def get_post_operation_guide(
        task_type: TaskType,
        result: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Get guide after completing an operation.
        
        Args:
            task_type: Type of completed task
            result: Task result data
            
        Returns:
            Post-operation suggestions
        """
        guides = {
            TaskType.IMAGE_GENERATION: GuideGenerator._get_image_post_guide(result),
            TaskType.IMAGE_EDIT: GuideGenerator._get_image_post_guide(result),
            TaskType.VIDEO_T2V: GuideGenerator._get_video_post_guide(result),
            TaskType.VIDEO_I2V: GuideGenerator._get_video_post_guide(result),
            TaskType.AUDIO_TTS: GuideGenerator._get_audio_post_guide(result),
            TaskType.VISION_DETECTION: GuideGenerator._get_vision_post_guide(result),
        }
        
        return guides.get(task_type, "✅ 操作完成！\n\n还需要其他帮助吗？")
    
    @staticmethod
    def _get_image_post_guide(result: Optional[Dict[str, Any]]) -> str:
        """Get guide after image operation."""
        message = "✅ 图片生成成功！\n\n接下来您可以：\n"
        suggestions = [
            "1. 用这张图片生成视频",
            "2. 继续生成更多图片",
            "3. 编辑这张图片",
            "4. 查看生成历史",
            "5. 下载图片到本地",
        ]
        
        if result and result.get("url"):
            suggestions.append(f"6. 访问图片: {result['url']}")
        
        return message + "\n".join(suggestions) + "\n\n您想继续做什么？"
    
    @staticmethod
    def _get_video_post_guide(result: Optional[Dict[str, Any]]) -> str:
        """Get guide after video operation."""
        message = "✅ 视频生成成功！\n\n接下来您可以：\n"
        suggestions = [
            "1. 生成更多视频",
            "2. 调整视频参数",
            "3. 查看生成历史",
            "4. 下载视频到本地",
        ]
        
        if result and result.get("url"):
            suggestions.append(f"5. 访问视频: {result['url']}")
        
        return message + "\n".join(suggestions) + "\n\n您想继续做什么？"
    
    @staticmethod
    def _get_audio_post_guide(result: Optional[Dict[str, Any]]) -> str:
        """Get guide after audio operation."""
        return "✅ 音频生成成功！\n\n接下来您可以：\n1. 生成更多音频\n2. 查看生成历史\n3. 下载音频到本地\n\n您想继续做什么？"
    
    @staticmethod
    def _get_vision_post_guide(result: Optional[Dict[str, Any]]) -> str:
        """Get guide after vision operation."""
        return "✅ 图像分析完成！\n\n接下来您可以：\n1. 分析更多图片\n2. 生成相关图片\n3. 生成描述视频\n\n您想继续做什么？"
    
    @staticmethod
    def get_contextual_suggestions(
        state_manager: StateManager,
        current_context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        Get contextual suggestions based on user history.
        
        Args:
            state_manager: State manager with user history
            current_context: Current operation context
            
        Returns:
            List of suggestion strings
        """
        suggestions = []
        
        # Get user preferences
        default_model = state_manager.get_preference("default_model")
        if default_model:
            suggestions.append(f"使用默认模型: {default_model}")
        
        # Get recent operations
        recent_ops = state_manager.get_history(limit=5)
        if recent_ops:
            op_types = [op["operation"] for op in recent_ops]
            most_common = max(set(op_types), key=op_types.count)
            suggestions.append(f"继续{most_common}操作")
        
        # Context-specific suggestions
        if current_context:
            if current_context.get("has_image"):
                suggestions.append("用此图片生成视频")
            if current_context.get("has_video"):
                suggestions.append("提取视频帧")
        
        return suggestions[:3]  # Limit to top 3
