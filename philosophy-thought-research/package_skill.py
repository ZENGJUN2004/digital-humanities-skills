#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
哲学与思想研究数字人文技能打包脚本
用于将技能文件打包成可分发的格式
"""

import os
import zipfile
import shutil
import json
from datetime import datetime

# 技能根目录
SKILL_ROOT = os.path.dirname(os.path.abspath(__file__))
# 打包输出目录
OUTPUT_DIR = os.path.join(SKILL_ROOT, "dist")
# 技能名称
SKILL_NAME = "philosophy-thought-research"

# 需要包含的文件和目录
INCLUDE_PATHS = [
    "SKILL.md",
    "scripts/",
    "test_skill.py",
    "assets/"
]

# 需要排除的文件和目录
EXCLUDE_PATHS = [
    "__pycache__",
    ".git",
    "dist",
    "venv",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.swp",
    "*.swo",
    "*~",
    ".DS_Store",
    "Thumbs.db"
]


def create_output_directory():
    """创建输出目录"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    else:
        # 清空输出目录
        for item in os.listdir(OUTPUT_DIR):
            item_path = os.path.join(OUTPUT_DIR, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


def should_exclude(path):
    """判断是否应该排除文件或目录"""
    for exclude_pattern in EXCLUDE_PATHS:
        if exclude_pattern in path:
            return True
    return False


def create_skill_zip():
    """创建技能ZIP包"""
    # 生成打包文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{SKILL_NAME}_{timestamp}.zip"
    zip_path = os.path.join(OUTPUT_DIR, zip_filename)
    
    # 创建ZIP文件
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 添加文件到ZIP
        for include_path in INCLUDE_PATHS:
            include_full_path = os.path.join(SKILL_ROOT, include_path)
            
            if os.path.isfile(include_full_path):
                # 添加单个文件
                arcname = os.path.relpath(include_full_path, SKILL_ROOT)
                if not should_exclude(arcname):
                    zipf.write(include_full_path, arcname)
                    print(f"添加文件: {arcname}")
            elif os.path.isdir(include_full_path):
                # 递归添加目录
                for root, dirs, files in os.walk(include_full_path):
                    # 过滤目录
                    dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]
                    
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, SKILL_ROOT)
                        if not should_exclude(arcname):
                            zipf.write(file_path, arcname)
                            print(f"添加文件: {arcname}")
    
    print(f"\n技能包已创建: {zip_path}")
    return zip_path


def create_skill_metadata():
    """创建技能元数据文件"""
    metadata = {
        "name": SKILL_NAME,
        "display_name": "哲学与思想研究数字人文技能",
        "version": "1.0.0",
        "description": "提供全面的哲学与思想研究工具，支持从文本分析到概念可视化的全方位研究与表达",
        "author": "Digital Humanities Team",
        "created_at": datetime.now().isoformat(),
        "dependencies": [
            "numpy",
            "pandas",
            "scikit-learn",
            "nltk",
            "spacy",
            "networkx",
            "matplotlib",
            "plotly",
            "dash",
            "textblob",
            "gensim",
            "pyvis"
        ],
        "categories": [
            "digital_humanities",
            "philosophy",
            "thought_research",
            "text_analysis",
            "visualization"
        ]
    }
    
    metadata_path = os.path.join(OUTPUT_DIR, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"元数据文件已创建: {metadata_path}")
    return metadata_path


def main():
    """主函数"""
    print("开始打包哲学与思想研究数字人文技能...")
    
    # 创建输出目录
    create_output_directory()
    
    # 创建技能ZIP包
    zip_path = create_skill_zip()
    
    # 创建技能元数据文件
    metadata_path = create_skill_metadata()
    
    print("\n打包完成！")
    print(f"技能包: {zip_path}")
    print(f"元数据: {metadata_path}")


if __name__ == "__main__":
    main()
