# 🔒 安全知识库技能配置说明

**更新时间**: 2026-04-19 03:05  
**安全级别**: ⚠️ 重要

---

## 🚨 安全问题修复

### 问题描述

在 2026-04-19 03:00 之前，`skill.py` 中存在**代码和知识混合**的问题：

```python
# ❌ 错误做法（已修复）
WIKI_DIR = Path('/home/admin/.openclaw/workspace/knowledge-base/wiki')
COMPANY_DIR = WIKI_DIR / 'company'
```

**风险**：
- 技能代码中硬编码了公司知识路径
- 分享技能时会暴露公司知识结构
- 违背"系统代码与公司知识分离"原则

---

## ✅ 修复方案

### 架构设计

```
┌─────────────────────────────────────────┐
│  skill.py (通用代码，可安全分享)          │
│  - 从 config.json 读取路径配置            │
│  - 不包含公司特定路径                    │
│  - 只有通用读取逻辑                      │
└─────────────────────────────────────────┘
                 ↓ 读取
┌─────────────────────────────────────────┐
│  config.json (私有配置，不应分享)         │
│  - 包含公司知识路径                      │
│  - 包含默认路径                          │
│  - 本地配置，不提交到 Git                │
└─────────────────────────────────────────┘┘
                 ↓ 注入
┌─────────────────────────────────────────┐
│  /workspace/knowledge-base/ (公司知识)    │
│  - 敏感数据，私有保存                    │
│  - 技能通过配置路径访问                   │
└─────────────────────────────────────────┘
```

---

## 📁 文件说明

### skill.py ✅

**通用代码，可安全分享**

```python
# 从 config.json 加载路径
config, defaults = load_config()

# 使用配置路径或默认路径
WIKI_DIR = Path(config.get('knowledge_base_path', 
                defaults.get('knowledge_base_path', './knowledge-base'))) / 'wiki'
```

**特点**：
- ✅ 不包含公司特定路径
- ✅ 从配置文件读取路径
- ✅ 有默认值便于分享
- ✅ 代码本身无敏感信息

---

### config.json ⚠️

**私有配置，不应分享**

```json
{
  "config": {
    "_comment": "路径配置 - 公司特定路径，不应分享或开源",
    "knowledge_base_path": "/home/admin/.openclaw/workspace/knowledge-base",
    "compiled_wiki_path": "/home/admin/.openclaw/workspace/knowledge-base/compiled/wiki",
    "company_data_path": "/home/admin/.openclaw/workspace/knowledge-base/wiki/company"
  },
  "defaults": {
    "_comment": "默认路径 - 用于代码分享时的默认值",
    "knowledge_base_path": "./knowledge-base",
    "compiled_wiki_path": "./compiled/wiki"
  }
}
```

**特点**：
- ⚠️ 包含公司知识路径
- ⚠️ 不应分享或开源
- ⚠️ 应加入 .gitignore
- ✅ 有默认值便于他人使用

---

## 🔐 安全最佳实践

### 1. Git 忽略配置

```bash
# .gitignore
skills/knowledge-organizer/config.json
```

**或者**提供配置模板：
```bash
# .gitignore
skills/knowledge-organizer/config.json
skills/knowledge-organizer/config.json.example  # ✅ 可以提交
```

---

### 2. 配置模板

创建 `config.json.example`（可安全分享）：

```json
{
  "name": "knowledge-organizer",
  "version": "1.0.0",
  "config": {
    "_comment": "复制为 config.json 并填入你的路径",
    "knowledge_base_path": "/path/to/your/knowledge-base",
    "compiled_wiki_path": "/path/to/your/compiled/wiki"
  },
  "defaults": {
    "knowledge_base_path": "./knowledge-base",
    "compiled_wiki_path": "./compiled/wiki"
  }
}
```

---

### 3. 环境变量（可选）

更安全的做法是使用环境变量：

```bash
# ~/.bashrc 或 ~/.zshrc
export KNOWLEDGE_BASE_PATH=/home/admin/.openclaw/workspace/knowledge-base
export COMPILED_WIKI_PATH=/home/admin/.openclaw/workspace/knowledge-base/compiled/wiki
```

```python
# skill.py 读取环境变量
import os
WIKI_DIR = Path(os.environ.get('KNOWLEDGE_BASE_PATH', './knowledge-base')) / 'wiki'
```

---

### 4. 文件权限

```bash
# 设置配置文件权限（仅所有者可读写）
chmod 600 skills/knowledge-organizer/config.json

# 设置知识目录权限
chmod 700 workspace/knowledge-base
```

---

## ✅ 安全检查清单

在分享技能代码前，请检查：

- [ ] `skill.py` 中没有硬编码公司路径
- [ ] `config.json` 已加入 `.gitignore`
- [ ] 或已提供 `config.json.example` 模板
- [ ] 默认路径是相对路径（如 `./knowledge-base`）
- [ ] 代码注释中没有泄露公司信息
- [ ] 测试使用默认路径能否正常运行

---

## 🔍 验证方法

### 验证 1：检查 skill.py

```bash
# 搜索是否有硬编码路径
grep -n "/home/admin" skills/knowledge-organizer/skill.py
# 应该无输出
```

### 验证 2：检查 config.json

```bash
# 查看配置
cat skills/knowledge-organizer/config.json | jq '.config'
# 应该看到公司路径（这是正常的，因为 config 是私有的）
```

### 验证 3：测试默认路径

```bash
# 临时重命名 config.json
mv skills/knowledge-organizer/config.json skills/knowledge-organizer/config.json.bak

# 测试技能（应使用默认路径）
python3 skills/knowledge-organizer/test-skill.py

# 恢复配置
mv skills/knowledge-organizer/config.json.bak skills/knowledge-organizer/config.json
```

---

## 📊 修复前后对比

| 项目 | 修复前 | 修复后 |
|------|--------|--------|
| skill.py 路径 | ❌ 硬编码公司路径 | ✅ 从配置读取 |
| config.json | ❌ 无配置 | ✅ 包含路径配置 |
| 代码可分享性 | ❌ 不可分享 | ✅ 可安全分享 |
| 知识隔离 | ❌ 混合 | ✅ 分离 |
| 安全风险 | 🔴 中 | 🟢 低 |

---

## 🎯 总结

### 核心原则

1. **代码通用化** - skill.py 不包含公司特定信息
2. **配置私有化** - config.json 包含公司路径，不分享
3. **默认值友好** - 他人使用时有合理的默认路径
4. **环境可移植** - 在不同环境中可轻松配置

### 安全级别

| 文件 | 安全级别 | 可否分享 |
|------|---------|---------|
| skill.py | 🟢 安全 | ✅ 可分享 |
| SKILL.md | 🟢 安全 | ✅ 可分享 |
| config.json | 🔴 敏感 | ❌ 不分享 |
| config.json.example | 🟢 安全 | ✅ 可分享 |

---

*Powered by 小蟹 🦀*  
*安全架构设计 - 2026-04-19*
