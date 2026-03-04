# Release v1.0.1 - API端点修复与格式更新

## 🎉 重大更新

### 🔧 API端点修复
修复了所有火山引擎API端点以匹配官方规范：
- **图像生成**: `/images/generate` → `/images/generations`
- **视觉理解**: `/chat/completions` → `/responses`
- **视频生成**: `/videos/generate` → `/contents/generations/tasks`

### 📝 请求格式更新
所有API调用格式已更新为官方最新规范：
- **图像生成**: 添加 `response_format` 和 `n` 参数
- **视觉理解**: `messages` 格式 → `input` 格式
- **视频生成**: 文本命令参数嵌入

### 📚 文档完善
- 更新所有示例代码
- 完善故障排查指南
- 添加迁移指南
- 更新API参考文档

### 🧪 破坏性变更
- 移除旧的端点路径
- 更新请求格式

## 📦 影响范围
- ✅ 图像生成功能 (Seedream 4.0)
- ✅ 视觉理解功能 (Seed Vision 1.6)
- ✅ 视频生成功能 (Seedance 1.5)
- ✅ 所有文档和示例
- ✅ 测试代码

## 🔗 GitHub Commit
- Commit: 69a2b80
- Files: 5 changed
- Author: Sisyphus <sisyphus@ohmyopen.code>

## 📦 升级指南
如果您使用旧版本，请：
1. 更新到最新版本
2. 检查API端点配置
3. 更新请求格式
4. 参考 CHANGE.list.md 了解详细变更

