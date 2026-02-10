#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
打包语言与语言学研究技能为可分发的.skill文件
"""

import os
import zipfile
import shutil

# 定义路径
skill_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(os.path.dirname(skill_dir), "language-linguistics-research.skill")

# 需要包含的文件和目录
includes = [
    "SKILL.md",
    "scripts",
    "assets",
    "references"
]

# 排除的文件和目录
excludes = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "test_*.py",
    "package_skill.py"
]

def should_exclude(path):
    """检查路径是否应该被排除"""
    for exclude in excludes:
        if exclude in path:
            return True
    return False

def add_to_zip(zipf, base_dir, path):
    """将文件或目录添加到zip文件"""
    if should_exclude(path):
        return
    
    if os.path.isfile(path):
        arcname = os.path.relpath(path, base_dir)
        zipf.write(path, arcname)
        print(f"添加文件: {arcname}")
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            if should_exclude(root):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                if not should_exclude(file_path):
                    arcname = os.path.relpath(file_path, base_dir)
                    zipf.write(file_path, arcname)
                    print(f"添加文件: {arcname}")

print(f"打包技能到: {out_path}")
print("=" * 60)

# 创建zip文件
with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    for item in includes:
        item_path = os.path.join(skill_dir, item)
        if os.path.exists(item_path):
            add_to_zip(zipf, skill_dir, item_path)
        else:
            print(f"警告: {item} 不存在，跳过")

print("=" * 60)
print(f"技能打包完成: {out_path}")
print(f"文件大小: {os.path.getsize(out_path) / 1024:.2f} KB")
