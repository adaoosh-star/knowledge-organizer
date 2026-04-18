#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试知识整理技能（集成编译 Wiki）
"""

import sys
sys.path.insert(0, '/home/admin/.openclaw/skills/knowledge-organizer')

from skill import KnowledgeOrganizerSkill

def test_skill():
    """测试技能"""
    print("=" * 60)
    print("🧪 测试知识整理技能（Karpathy LLM Wiki）")
    print("=" * 60)
    
    # 1. 初始化技能
    print("\n📦 初始化技能...")
    skill = KnowledgeOrganizerSkill()
    print(f"   ✅ 编译 Wiki 加载：{len(skill.compiled_wiki)} 个页面")
    
    # 2. 测试查询：人力资源部
    print("\n🔍 测试查询：人力资源部")
    docs = skill.scan_documents("人力资源部", ["人力资源部", "HR", "人力"])
    print(f"   ✅ 找到 {len(docs)} 篇相关文档")
    for i, doc in enumerate(docs[:3], 1):
        print(f"   {i}. {doc['file']} (相关度：{doc['relevance']}, 来源：{doc.get('source', 'unknown')})")
    
    # 3. 测试查询：高潜人才
    print("\n🔍 测试查询：高潜人才")
    docs = skill.scan_documents("高潜人才", ["高潜", "人才", "潜力"])
    print(f"   ✅ 找到 {len(docs)} 篇相关文档")
    for i, doc in enumerate(docs[:5], 1):
        print(f"   {i}. {doc['file']} (相关度：{doc['relevance']}, 来源：{doc.get('source', 'unknown')})")
    
    # 4. 测试查询：李哲
    print("\n🔍 测试查询：李哲")
    docs = skill.scan_documents("李哲", ["李哲", "CEO", "创始人"])
    print(f"   ✅ 找到 {len(docs)} 篇相关文档")
    for i, doc in enumerate(docs[:3], 1):
        print(f"   {i}. {doc['file']} (相关度：{doc['relevance']}, 来源：{doc.get('source', 'unknown')})")
    
    # 5. 统计
    print("\n" + "=" * 60)
    print("📊 统计")
    print("=" * 60)
    
    wiki_types = {}
    for title, data in skill.compiled_wiki.items():
        t = data['type']
        wiki_types[t] = wiki_types.get(t, 0) + 1
    
    print(f"   编译 Wiki 页面：{len(skill.compiled_wiki)} 个")
    for t, count in sorted(wiki_types.items()):
        print(f"   - {t}: {count} 个")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

if __name__ == '__main__':
    test_skill()
