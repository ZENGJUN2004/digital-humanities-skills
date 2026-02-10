#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
艺术作品分析示例
演示数字图像处理模块的使用
"""

from scripts.digital_image_processing.image_analyzer import ImageAnalyzer
import os

# 示例图像路径（实际使用时需要替换为真实的图像路径）
sample_image_path = "path/to/artwork.jpg"

# 检查图像是否存在
if not os.path.exists(sample_image_path):
    print(f"警告: 示例图像不存在: {sample_image_path}")
    print("请替换为真实的艺术作品图像路径")
    # 使用一个假的图像路径，实际运行时会失败
    sample_image_path = "sample_artwork.jpg"

try:
    # 初始化图像分析器
    print("初始化图像分析器...")
    analyzer = ImageAnalyzer(sample_image_path)
    
    # 分析图像
    print("\n分析图像特征...")
    analysis = analyzer.analyze()
    
    if "error" in analysis:
        print(f"分析错误: {analysis['error']}")
    else:
        # 显示分析结果
        print("\n=== 图像分析结果 ===")
        
        # 颜色分布
        print("\n1. 颜色分布:")
        color_dist = analysis['color_distribution']
        print(f"   亮度均值: {color_dist['mean_l']:.2f}")
        print(f"   红绿轴均值: {color_dist['mean_a']:.2f}")
        print(f"   蓝黄轴均值: {color_dist['mean_b_lab']:.2f}")
        print(f"   亮度标准差: {color_dist['std_l']:.2f}")
        
        # 边缘密度
        print("\n2. 边缘密度:")
        print(f"   边缘密度: {analysis['edge_density']:.4f}")
        
        # 纹理特征
        print("\n3. 纹理特征:")
        texture = analysis['texture_features']
        print(f"   对比度: {texture['contrast']:.2f}")
        print(f"   能量: {texture['energy']:.2f}")
        print(f"   相关性: {texture['correlation']:.2f}")
        print(f"   均匀性: {texture['homogeneity']:.2f}")
        
        # 构图分析
        print("\n4. 构图分析:")
        composition = analysis['composition']
        center = composition['center_of_mass']
        print(f"   重心位置: ({center['x']:.2f}, {center['y']:.2f})")
        print(f"   三分法则得分: {composition['rule_of_thirds_score']}")
        print(f"   宽高比: {composition['aspect_ratio']:.2f}")
        
        # 亮度和对比度
        print("\n5. 亮度和对比度:")
        print(f"   亮度: {analysis['brightness']:.2f}")
        print(f"   对比度: {analysis['contrast']:.2f}")
        
        # 熵
        print("\n6. 图像熵:")
        print(f"   熵值: {analysis['entropy']:.2f}")
    
    # 增强图像
    print("\n增强图像...")
    enhanced_image = analyzer.enhance(brightness=1.2, contrast=1.1, saturation=1.1)
    if enhanced_image:
        output_path = "enhanced_artwork.jpg"
        enhanced_image.save(output_path)
        print(f"增强后的图像已保存为: {output_path}")
    
    # 风格转换
    print("\n应用风格转换...")
    styles = ["impressionist", "sketch", "oil_painting", "watercolor"]
    
    for style in styles:
        print(f"应用 {style} 风格...")
        styled_image = analyzer.style_transfer(style=style)
        if styled_image:
            output_path = f"{style}_style_artwork.jpg"
            styled_image.save(output_path)
            print(f"风格转换后的图像已保存为: {output_path}")
    
    # 人脸检测
    print("\n检测人脸...")
    faces = analyzer.detect_faces()
    if faces:
        print(f"检测到 {len(faces)} 个人脸")
        for i, face in enumerate(faces):
            print(f"人脸 {i+1}: 位置=({face['x']}, {face['y']}), 大小={face['width']}x{face['height']}")
    else:
        print("未检测到人脸")
    
    # 图像分割
    print("\n分割图像...")
    segmented = analyzer.segment_image()
    if segmented is not None:
        print(f"分割完成，分割结果形状: {segmented.shape}")
    
    # 提取特征
    print("\n提取图像特征...")
    features = analyzer.extract_features()
    if features is not None:
        print(f"特征提取完成，特征向量长度: {len(features)}")
        print(f"前10个特征值: {features[:10]}")
    
    print("\n=== 分析完成 ===")
    
except Exception as e:
    print(f"运行时错误: {e}")
    print("请确保已安装所有依赖项并提供有效的图像路径")

print("\n=== 使用说明 ===")
print("1. 替换 sample_image_path 为真实的艺术作品图像路径")
print("2. 确保已安装以下依赖项:")
print("   - numpy")
print("   - opencv-python")
print("   - Pillow")
print("   - scikit-image")
print("   - matplotlib")
print("3. 运行脚本查看分析结果")
