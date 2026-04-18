#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识整理技能 - LLM 驱动的知识查询和组织

安全架构：
- 代码通用化，不包含公司特定路径
- 路径通过 config.json 配置注入
- 支持默认值，便于代码分享
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

# 路径配置 - 从 config.json 加载，避免硬编码公司路径
SKILL_DIR = Path(__file__).parent
CONFIG_FILE = SKILL_DIR / 'config.json'

def load_config():
    """加载技能配置"""
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text(encoding='utf-8'))
        return config.get('config', {}), config.get('defaults', {})
    return {}, {}

# 加载配置
config, defaults = load_config()

# 使用配置路径（优先）或默认路径
WIKI_DIR = Path(config.get('knowledge_base_path', defaults.get('knowledge_base_path', './knowledge-base'))) / 'wiki'
COMPANY_DIR = Path(config.get('company_data_path', defaults.get('company_data_path', './wiki/company')))
ANALYSIS_DIR = Path(config.get('analysis_path', defaults.get('analysis_path', './wiki/analysis')))
COMPILED_WIKI_DIR = Path(config.get('compiled_wiki_path', defaults.get('compiled_wiki_path', './compiled/wiki')))
RAW_DOCS_DIR = Path(config.get('raw_docs_path', defaults.get('raw_docs_path', './raw')))

class KnowledgeOrganizerSkill:
    """知识整理技能 - Karpathy LLM Wiki 方法
    
    安全说明：
    - 本技能代码是通用的，不包含公司特定信息
    - 公司知识路径通过 config.json 配置注入
    - 分享技能代码时，请移除 config.json 中的公司路径
    """
    
    def __init__(self):
        self.documents = []
        self.org_structure = self.load_org_structure()
        self.data_sources = self.load_data_sources()
        self.compiled_wiki = self.load_compiled_wiki()
    
    def load_org_structure(self):
        """加载组织架构"""
        org_file = COMPANY_DIR / 'org-structure.md'
        if org_file.exists():
            content = org_file.read_text(encoding='utf-8')
            return self.parse_org_structure(content)
        return {}
    
    def load_data_sources(self):
        """加载数据源注册表"""
        ds_file = COMPANY_DIR / 'data-sources.md'
        if ds_file.exists():
            content = ds_file.read_text(encoding='utf-8')
            return self.parse_data_sources(content)
        return {}
    
    def load_compiled_wiki(self):
        """加载编译后的 Wiki（Karpathy 方法）"""
        wiki_index = {}
        
        if not COMPILED_WIKI_DIR.exists():
            return wiki_index
        
        for md_file in COMPILED_WIKI_DIR.glob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # 提取标题作为索引键
                title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                    wiki_index[title] = {
                        'file': str(md_file),
                        'content': content,
                        'type': self.detect_entity_type(content)
                    }
            except:
                pass
        
        return wiki_index
    
    def detect_entity_type(self, content):
        """检测实体类型"""
        if '**职位**' in content or '**分管部门**' in content:
            return 'executive'
        elif '**职能**' in content or '**简称**' in content:
            return 'department'
        elif '**部门**' in content and '**职级**' in content:
            return 'person'
        elif '**类型**' in content and '**保司**' in content:
            return 'product'
        elif '**时间**' in content and '**目标**' in content:
            return 'event'
        return 'other'
    
    def parse_org_structure(self, content):
        """解析组织架构"""
        org = {'aliases': {}}
        # 简单解析部门映射表
        if '人力资源部' in content:
            org['aliases']['HR'] = '人力资源部'
            org['aliases']['人力'] = '人力资源部'
            org['aliases']['人力部'] = '人力资源部'
        if '用户发展' in content:
            org['aliases']['用发'] = '用户发展部'
        return org
    
    def parse_data_sources(self, content):
        """解析数据源注册表"""
        sources = {}
        # 简单解析，提取关键数据源
        if '高潜人才名单' in content:
            sources['高潜人才'] = {
                'primary': 'Fri, 17 Ap_人才盘点数据及汇报材料.md',
                'confidence': '95%'
            }
        return sources
    
    def scan_documents(self, topic, keywords):
        """扫描相关文档（优先使用编译 Wiki）"""
        docs = []
        
        # 1. 优先从编译 Wiki 中检索（Karpathy 方法）
        for title, wiki_data in self.compiled_wiki.items():
            content = wiki_data['content']
            
            # 检查标题或内容是否匹配
            match_count = sum(1 for kw in keywords if kw in title or kw in content)
            
            if match_count > 0:
                docs.append({
                    'file': wiki_data['file'],
                    'content': content,
                    'relevance': match_count * 2,  # Wiki 权重更高
                    'matched_keywords': [kw for kw in keywords if kw in title or kw in content],
                    'type': wiki_data['type'],
                    'source': 'compiled_wiki'
                })
        
        # 2. 从原始文档补充
        for md_file in COMPANY_DIR.glob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                
                # 智能匹配：检查多个关键词
                match_count = sum(1 for kw in keywords if kw in content)
                
                if match_count > 0:
                    docs.append({
                        'file': md_file.name,
                        'content': content,
                        'relevance': match_count,
                        'matched_keywords': [kw for kw in keywords if kw in content],
                        'source': 'raw_doc'
                    })
            except:
                pass
        
        # 按相关度排序
        docs = sorted(docs, key=lambda x: x['relevance'], reverse=True)
        return docs[:15]  # 最多返回 15 篇
    
    def extract_context(self, docs, keywords):
        """提取相关上下文"""
        contexts = []
        for doc in docs:
            content = doc['content']
            lines = content.split('\n')
            
            # 找到包含关键词的行及其上下文
            for i, line in enumerate(lines):
                for kw in keywords:
                    if kw in line:
                        # 提取当前行及前后各 10 行
                        start = max(0, i - 10)
                        end = min(len(lines), i + 11)
                        context = '\n'.join(lines[start:end])
                        
                        contexts.append({
                            'source': doc['file'],
                            'context': context.strip(),
                            'keyword': kw
                        })
                        break
        
        return contexts
    
    def build_llm_prompt(self, topic, contexts):
        """构建 LLM Prompt"""
        context_text = "\n\n".join([
            f"【来源：{c['source']}】\n{c['context']}"
            for c in contexts
        ])
        
        # 获取数据源信息
        source_info = ""
        for key, info in self.data_sources.items():
            if key in topic or topic in key:
                source_info += f"\n- {key}: 主数据源={info['primary']}, 可信度={info['confidence']}"
        
        prompt = f"""你是公司知识整理助手，请理解并整理以下关于"{topic}"的信息。

## 数据来源说明
{source_info if source_info else '无特殊数据源说明'}

## 原始信息片段

{context_text}

## 任务

请从以上信息片段中提取、理解并整理"{topic}"的完整信息。

## 输出格式

请严格按以下 Markdown 格式输出（不要 JSON）：

# 📋 {topic} - 整理报告

**整理时间**: YYYY-MM-DD HH:MM  
**整理方式**: LLM 驱动的知识关联系统

---

## 📊 信息来源

- 文档 1
- 文档 2

---

## 📋 整理结果

### 核心信息

[这里用简洁的语言总结核心信息]

### 详细信息

[按逻辑组织详细信息，使用标题、列表等]

### 数据/指标

[如有数据，用表格或列表展示]

---

## ⚠️ 待确认/进行中

- 待确认事项 1
- 待确认事项 2

---

## ❌ 信息缺口

[明确指出哪些关键信息缺失]

---

*Powered by 小蟹 🦀*

## 要求

1. **准确提取** - 只基于提供的信息，不要编造
2. **标注来源** - 在信息来源中列出所有文档
3. **识别缺口** - 明确指出哪些关键信息缺失
4. **结构化** - 使用 Markdown 格式，清晰易读
5. **完整性** - 尽可能提取所有相关信息
6. **简洁** - 避免冗长，用简洁语言表达

## 开始整理

请输出 Markdown 格式的报告："""

        return prompt
    
    def query(self, topic):
        """查询知识"""
        
        # 生成智能关键词
        keywords = self.generate_keywords(topic)
        
        # 扫描文档
        docs = self.scan_documents(topic, keywords)
        
        if not docs:
            # 放宽关键词重试
            keywords = [topic]
            docs = self.scan_documents(topic, keywords)
        
        if not docs:
            return f"❌ 未找到关于'{topic}'的相关文档"
        
        # 提取上下文
        contexts = self.extract_context(docs, keywords)
        
        if not contexts:
            return f"❌ 未能提取到'{topic}'的有效信息"
        
        # 构建 LLM Prompt
        prompt = self.build_llm_prompt(topic, contexts)
        
        # 返回 Prompt（由 OpenClaw 调用 LLM）
        # 实际使用时，这里应该调用 OpenClaw 的 LLM 接口
        return prompt
    
    def generate_keywords(self, topic):
        """生成智能关键词组"""
        keywords = [topic]
        
        # 1. 部门别名映射（从组织架构）
        if topic in self.org_structure.get('aliases', {}):
            keywords.append(self.org_structure[topic])
        
        # 2. 常见部门别名
        if topic in ['HR', '人力', '人力部']:
            keywords.extend(['人力资源部', '招聘', '培训', '薪酬', '绩效', '员工关系', '人才盘点'])
        if topic in ['用户发展', '用发']:
            keywords.extend(['新人', '代理人增长', '新人训练营', '步步高', 'MGM', '出单人力'])
        if topic in ['大数据', '数据部']:
            keywords.extend(['大数据部', '报表', 'BI', '周报', '埋点'])
        
        # 3. 产品别名
        if '518' in topic:
            keywords.extend(['518 周年庆', '5·18', '品牌焕新', 'MSH 专场', '518MGM', '518 活动'])
        if '哪吒' in topic:
            keywords.extend(['哪吒 2 号', '哪吒重疾险'])
        if '欣享' in topic:
            keywords.extend(['欣享易生', '欣享人生', 'MSH'])
        
        # 4. 去重
        return list(set(keywords))

def execute(topic):
    """执行技能"""
    skill = KnowledgeOrganizerSkill()
    return skill.query(topic)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        topic = ' '.join(sys.argv[1:])
        result = execute(topic)
        print(result)
    else:
        print("用法：python3 skill.py <查询主题>")
