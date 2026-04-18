# 🤝 贡献指南

感谢你对 knowledge-organizer 技能的兴趣！

## 📋 如何贡献

### 1. Fork 仓库

点击 GitHub 上的 Fork 按钮。

### 2. 克隆仓库

```bash
git clone https://github.com/YOUR_USERNAME/knowledge-organizer.git
cd knowledge-organizer
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
```

### 4. 开发和测试

```bash
# 运行测试
python3 test-skill.py

# 确保代码质量
# 添加你的测试
```

### 5. 提交更改

```bash
git add .
git commit -m "feat: add your feature description"
```

### 6. 推送到 Fork

```bash
git push origin feature/your-feature-name
```

### 7. 创建 Pull Request

在 GitHub 上创建 Pull Request。

---

## 📝 提交信息规范

使用以下前缀：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具相关

示例：
```
feat: add jieba tokenization support
fix: resolve path loading issue
docs: update README with security notes
```

---

## 🔒 安全注意事项

### ❌ 不要提交

- `config.json` - 包含公司路径
- 任何包含公司名、人名的文件
- 内部文档和报告

### ✅ 可以提交

- `skill.py` - 通用代码
- `config.json.example` - 配置模板
- 文档文件（SKILL.md, README.md 等）
- 测试文件

---

## 💡 改进建议

### 短期改进

- [ ] 集成 jieba 分词
- [ ] 添加缓存机制
- [ ] 性能优化

### 长期改进

- [ ] LLM 接口自动化
- [ ] 自动同步机制
- [ ] 知识图谱可视化

欢迎提出你的想法！

---

## 📞 联系方式

- GitHub Issues: https://github.com/YOUR_USERNAME/knowledge-organizer/issues
- Email: your-email@example.com

---

*Powered by 小蟹 🦀*
