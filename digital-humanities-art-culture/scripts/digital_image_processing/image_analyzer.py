#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
图像分析工具
用于艺术作品的形式分析、风格识别、特征提取
"""

import numpy as np
import cv2
from PIL import Image
from skimage import color, filters, feature, texture
from skimage.measure import shannon_entropy
import matplotlib.pyplot as plt

class ImageAnalyzer:
    """图像分析器类"""
    
    def __init__(self, image_path):
        """
        初始化图像分析器
        
        Args:
            image_path (str): 图像文件路径
        """
        self.image_path = image_path
        self.image = None
        self.gray_image = None
        self.load_image()
    
    def load_image(self):
        """
        加载图像
        """
        try:
            self.image = cv2.imread(self.image_path)
            if self.image is None:
                raise Exception(f"无法加载图像: {self.image_path}")
            # 转换为RGB格式
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            # 创建灰度图像
            self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        except Exception as e:
            print(f"加载图像时出错: {e}")
    
    def analyze(self):
        """
        分析图像特征
        
        Returns:
            dict: 包含图像分析结果的字典
        """
        if self.image is None:
            return {"error": "图像未加载"}
        
        analysis = {
            "color_distribution": self._analyze_color_distribution(),
            "edge_density": self._analyze_edge_density(),
            "texture_features": self._analyze_texture(),
            "composition": self._analyze_composition(),
            "brightness": self._analyze_brightness(),
            "contrast": self._analyze_contrast(),
            "entropy": self._calculate_entropy()
        }
        
        return analysis
    
    def _analyze_color_distribution(self):
        """
        分析颜色分布
        
        Returns:
            dict: 颜色分布分析结果
        """
        # 计算颜色直方图
        r_hist = cv2.calcHist([self.image], [0], None, [256], [0, 256])
        g_hist = cv2.calcHist([self.image], [1], None, [256], [0, 256])
        b_hist = cv2.calcHist([self.image], [2], None, [256], [0, 256])
        
        # 计算颜色均值和标准差
        mean_r, std_r = cv2.meanStdDev(self.image[:, :, 0])
        mean_g, std_g = cv2.meanStdDev(self.image[:, :, 1])
        mean_b, std_b = cv2.meanStdDev(self.image[:, :, 2])
        
        # 转换为Lab色彩空间分析色彩特性
        lab_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2Lab)
        mean_l, std_l = cv2.meanStdDev(lab_image[:, :, 0])
        mean_a, std_a = cv2.meanStdDev(lab_image[:, :, 1])
        mean_b_lab, std_b_lab = cv2.meanStdDev(lab_image[:, :, 2])
        
        return {
            "mean_r": float(mean_r[0][0]),
            "mean_g": float(mean_g[0][0]),
            "mean_b": float(mean_b[0][0]),
            "std_r": float(std_r[0][0]),
            "std_g": float(std_g[0][0]),
            "std_b": float(std_b[0][0]),
            "mean_l": float(mean_l[0][0]),  # 亮度
            "mean_a": float(mean_a[0][0]),  # 红绿轴
            "mean_b_lab": float(mean_b_lab[0][0]),  # 蓝黄轴
            "std_l": float(std_l[0][0]),
            "std_a": float(std_a[0][0]),
            "std_b_lab": float(std_b_lab[0][0])
        }
    
    def _analyze_edge_density(self):
        """
        分析边缘密度
        
        Returns:
            float: 边缘密度值
        """
        # 使用Canny边缘检测
        edges = cv2.Canny(self.gray_image, 100, 200)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        return edge_density
    
    def _analyze_texture(self):
        """
        分析纹理特征
        
        Returns:
            dict: 纹理特征分析结果
        """
        # 使用灰度共生矩阵计算纹理特征
        try:
            from skimage.feature import greycomatrix, greycoprops
            
            # 计算灰度共生矩阵
            glcm = greycomatrix(self.gray_image // 8, distances=[5], angles=[0], levels=32, symmetric=True, normed=True)
            
            # 计算纹理特征
            contrast = greycoprops(glcm, 'contrast')[0, 0]
            dissimilarity = greycoprops(glcm, 'dissimilarity')[0, 0]
            homogeneity = greycoprops(glcm, 'homogeneity')[0, 0]
            energy = greycoprops(glcm, 'energy')[0, 0]
            correlation = greycoprops(glcm, 'correlation')[0, 0]
            
            return {
                "contrast": float(contrast),
                "dissimilarity": float(dissimilarity),
                "homogeneity": float(homogeneity),
                "energy": float(energy),
                "correlation": float(correlation)
            }
        except Exception as e:
            print(f"纹理分析出错: {e}")
            return {
                "contrast": 0.0,
                "dissimilarity": 0.0,
                "homogeneity": 0.0,
                "energy": 0.0,
                "correlation": 0.0
            }
    
    def _analyze_composition(self):
        """
        分析构图
        
        Returns:
            dict: 构图分析结果
        """
        # 计算图像的重心
        moments = cv2.moments(self.gray_image)
        if moments['m00'] != 0:
            center_x = moments['m10'] / moments['m00']
            center_y = moments['m01'] / moments['m00']
        else:
            center_x = self.gray_image.shape[1] / 2
            center_y = self.gray_image.shape[0] / 2
        
        # 计算三分法则分析
        height, width = self.gray_image.shape
        third_x = width / 3
        third_y = height / 3
        
        # 检查重心是否在三分法则的交点附近
        rule_of_thirds_score = 0
        for i in range(1, 3):
            for j in range(1, 3):
                intersection_x = i * third_x
                intersection_y = j * third_y
                distance = np.sqrt((center_x - intersection_x)**2 + (center_y - intersection_y)**2)
                if distance < min(width, height) / 10:
                    rule_of_thirds_score = 1.0
                    break
            if rule_of_thirds_score == 1.0:
                break
        
        return {
            "center_of_mass": {
                "x": float(center_x),
                "y": float(center_y)
            },
            "rule_of_thirds_score": rule_of_thirds_score,
            "aspect_ratio": width / height
        }
    
    def _analyze_brightness(self):
        """
        分析亮度
        
        Returns:
            float: 亮度值
        """
        return float(np.mean(self.gray_image)) / 255.0
    
    def _analyze_contrast(self):
        """
        分析对比度
        
        Returns:
            float: 对比度值
        """
        return float(np.std(self.gray_image)) / 255.0
    
    def _calculate_entropy(self):
        """
        计算图像熵
        
        Returns:
            float: 熵值
        """
        return float(shannon_entropy(self.gray_image))
    
    def enhance(self, brightness=1.0, contrast=1.0, saturation=1.0):
        """
        增强图像
        
        Args:
            brightness (float): 亮度调整因子
            contrast (float): 对比度调整因子
            saturation (float): 饱和度调整因子
            
        Returns:
            PIL.Image: 增强后的图像
        """
        if self.image is None:
            return None
        
        # 复制图像
        enhanced = self.image.copy()
        
        # 调整亮度和对比度
        enhanced = cv2.convertScaleAbs(enhanced, alpha=contrast, beta=(brightness - 1) * 128)
        
        # 调整饱和度
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_RGB2HSV)
        hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], saturation)
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        # 转换为PIL Image
        return Image.fromarray(enhanced)
    
    def style_transfer(self, style="impressionist"):
        """
        风格转换
        
        Args:
            style (str): 风格类型
            
        Returns:
            PIL.Image: 风格转换后的图像
        """
        if self.image is None:
            return None
        
        # 这里使用简单的滤镜模拟风格转换
        # 实际应用中可以使用更复杂的深度学习方法
        styled = self.image.copy()
        
        if style == "impressionist":
            # 印象派风格模拟
            blur = cv2.GaussianBlur(styled, (5, 5), 0)
            edges = cv2.Canny(self.gray_image, 50, 150)
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            styled = cv2.addWeighted(blur, 0.8, edges, 0.2, 0)
        
        elif style == "sketch":
            # 素描风格模拟
            inv_gray = 255 - self.gray_image
            blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
            sketch = cv2.divide(self.gray_image, 255 - blur, scale=256)
            styled = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
        
        elif style == "oil_painting":
            # 油画风格模拟
            blur = cv2.medianBlur(styled, 7)
            edges = cv2.Canny(self.gray_image, 100, 200)
            edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            styled = cv2.addWeighted(blur, 0.9, edges, 0.1, 0)
        
        elif style == "watercolor":
            # 水彩风格模拟
            blur = cv2.GaussianBlur(styled, (3, 3), 0)
            hsv = cv2.cvtColor(blur, cv2.COLOR_RGB2HSV)
            hsv[:, :, 1] = cv2.add(hsv[:, :, 1], 30)
            styled = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        
        # 转换为PIL Image
        return Image.fromarray(styled)
    
    def detect_faces(self):
        """
        检测人脸
        
        Returns:
            list: 人脸边界框列表
        """
        if self.image is None:
            return []
        
        try:
            # 加载预训练的人脸检测器
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(self.gray_image, 1.3, 5)
            
            # 转换为标准格式
            face_list = []
            for (x, y, w, h) in faces:
                face_list.append({
                    "x": x,
                    "y": y,
                    "width": w,
                    "height": h
                })
            
            return face_list
        except Exception as e:
            print(f"人脸检测出错: {e}")
            return []
    
    def segment_image(self):
        """
        图像分割
        
        Returns:
            numpy.ndarray: 分割后的图像
        """
        if self.image is None:
            return None
        
        # 使用简单的阈值分割
        _, segmented = cv2.threshold(self.gray_image, 127, 255, cv2.THRESH_BINARY)
        return segmented
    
    def extract_features(self):
        """
        提取图像特征
        
        Returns:
            numpy.ndarray: 特征向量
        """
        if self.image is None:
            return None
        
        # 计算HOG特征
        try:
            from skimage.feature import hog
            features, _ = hog(
                self.gray_image,
                orientations=9,
                pixels_per_cell=(8, 8),
                cells_per_block=(2, 2),
                block_norm='L2-Hys',
                visualize=True
            )
            return features
        except Exception as e:
            print(f"特征提取出错: {e}")
            return None
