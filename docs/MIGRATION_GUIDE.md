# 从旧版本迁移到 v1.0.1 指南

## 🔄 主要变更
### 1. API端点变更
| 功能 | 旧端点 | 新端点 | 变更原因 |
|------|--------|--------|----------|
| 图像生成 | `/images/generate` | `/images/generations` | 符合OpenAI API规范 |
| 视觉理解 | `/chat/completions` | `/responses` | 火山引擎专用端点 |
| 视频生成 | `/videos/generate` | `/contents/generations/tasks` | 官方规范 |

### 2. 请求格式变更
#### 图像生成
**旧格式**:
```python
{
    "prompt": "...",
    "size": "1024x1024"
}
```

**新格式**:
```python
{
    "model": "doubao-seedream-4-0-250828",
    "prompt": "...",
    "size": "1024x1024",
    "response_format": "url",  # 新增
    "n": 1                    # 新增
}
```
#### 视觉理解
**旧格式**:
```python
{
    "model": "doubao-seed-1-6-vision-250815",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "..."},
                {"type": "image_url", "image_url": {"url": "..."}}
            ]
        }
    ]
}
```
**新格式**:
```python
{
    "model": "doubao-seed-1-6-vision-250815",
    "input": [  # 改为 input
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "..."},  # 改为 input_text
                {"type": "input_image", "image_url": "..."}  # 改为 input_image
            ]
        }
    ]
}
```
#### 视频生成
**旧格式**:
```python
{
    "model": "doubao-seedance-1-5-pro-251215",
    "prompt": "...",
    "duration": 5
}
```
**新格式**:
```python
{
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
        {
            "type": "text",
            "text": "... --duration 5 --resolution 720p"  # 参数嵌入文本
        }
    ]
}
```
## 🚀 迁移步骤
### 1. 更新代码
```bash
# 拉取最新代码
git pull origin main

# 或者重新安装
pip install -r volcengine-api/requirements.txt
```
### 2. 检查配置
```python
# 检查API Key配置
from toolkit.config import ConfigManager
config = ConfigManager()
print(config.get_api_key())  # 应显示你的API Key

```
### 3. 更新请求代码
**图像生成**:
```python
from toolkit.api_client import VolcengineAPIClient

client = VolcengineAPIClient(config)
result = client.post("/images/generations", json={
    "model": "doubao-seedream-4-0-250828",
    "prompt": "your prompt",
    "size": "1024x1024",
    "response_format": "url",
    "n": 1
})
```
**视觉理解**:
```python
result = client.post("/responses", json={
    "model": "doubao-seed-1-6-vision-250815",
    "input": [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "描述这张图片"},
                {"type": "input_image", "image_url": "https://example.com/image.jpg"}
            ]
        }
    ]
}
```
**视频生成**:
```python
result = client.post("/contents/generations/tasks", json={
    "model": "doubao-seedance-1-5-pro-251215",
    "content": [
        {
            "type": "text",
            "text": "镜头缓缓移动 --duration 5"
        }
    ]
}
# 记录任务ID
task_id = result["id"]

# 查询任务状态
status = client.get(f"/contents/generations/tasks/{task_id}")
```
### 4. 测试验证
```bash
# 运行测试
python tests/full_feature_test.py

# 或运行示例
python examples/quickstart.py
```
## ⚠️ 注意事项
1. **API Key**: 确保已正确配置
2. **模型ID**: 使用正确的模型ID
3. **响应格式**: 图像生成需要 `response_format: "url"`
4. **参数格式**: 视频生成参数嵌入文本中
5. **异步任务**: 视频生成是异步的，需要轮询查询状态
## 📚 相关文档
- [API参考文档](./docs/api_reference.md)
- [变更日志](./change.list.md)
- [故障排查](./docs/troubleshooting.md)
- [完整示例](./examples/quickstart.py)
