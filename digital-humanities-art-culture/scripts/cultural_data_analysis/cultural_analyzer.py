#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
文化数据分析工具
用于文化现象的定量研究、数据可视化和网络分析
"""

import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy import stats
from collections import Counter
import json
import os

class CulturalAnalyzer:
    """文化数据分析器类"""
    
    def __init__(self, data):
        """
        初始化文化数据分析器
        
        Args:
            data (pd.DataFrame or str): 文化数据，可以是DataFrame或数据文件路径
        """
        if isinstance(data, str):
            # 从文件加载数据
            self.data = self._load_data(data)
        else:
            self.data = data
        
        self.scaler = StandardScaler()
    
    def _load_data(self, file_path):
        """
        从文件加载数据
        
        Args:
            file_path (str): 数据文件路径
            
        Returns:
            pd.DataFrame: 加载的数据
        """
        try:
            if file_path.endswith('.csv'):
                return pd.read_csv(file_path)
            elif file_path.endswith('.json'):
                return pd.read_json(file_path)
            elif file_path.endswith('.xlsx'):
                return pd.read_excel(file_path)
            else:
                raise Exception(f"不支持的文件格式: {file_path}")
        except Exception as e:
            print(f"加载数据时出错: {e}")
            return pd.DataFrame()
    
    def descriptive_statistics(self):
        """
        计算描述性统计
        
        Returns:
            dict: 描述性统计结果
        """
        if self.data.empty:
            return {"error": "数据为空"}
        
        # 计算数值型列的统计
        numeric_stats = self.data.describe().to_dict()
        
        # 计算分类列的统计
        categorical_stats = {}
        for col in self.data.select_dtypes(include=['object', 'category']).columns:
            categorical_stats[col] = {
                "unique_values": self.data[col].nunique(),
                "top_value": self.data[col].mode().iloc[0] if not self.data[col].mode().empty else None,
                "top_value_count": self.data[col].value_counts().iloc[0] if not self.data[col].value_counts().empty else 0,
                "value_counts": self.data[col].value_counts().to_dict()
            }
        
        # 计算缺失值
        missing_values = self.data.isnull().sum().to_dict()
        
        stats_result = {
            "numeric_stats": numeric_stats,
            "categorical_stats": categorical_stats,
            "missing_values": missing_values,
            "shape": {
                "rows": self.data.shape[0],
                "columns": self.data.shape[1]
            }
        }
        
        return stats_result
    
    def correlation_analysis(self):
        """
        计算相关性分析
        
        Returns:
            dict: 相关性分析结果
        """
        if self.data.empty:
            return {"error": "数据为空"}
        
        # 选择数值型列
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return {"error": "数值型列不足"}
        
        # 计算皮尔逊相关系数
        corr_matrix = self.data[numeric_cols].corr().to_dict()
        
        # 计算斯皮尔曼相关系数
        spearman_corr = self.data[numeric_cols].corr(method='spearman').to_dict()
        
        return {
            "pearson_correlation": corr_matrix,
            "spearman_correlation": spearman_corr
        }
    
    def network_analysis(self, node_col, edge_col):
        """
        网络分析
        
        Args:
            node_col (str): 节点列名
            edge_col (str): 边列名
            
        Returns:
            nx.Graph: 网络分析结果
        """
        if self.data.empty:
            return None
        
        if node_col not in self.data.columns or edge_col not in self.data.columns:
            print(f"列名不存在: {node_col} 或 {edge_col}")
            return None
        
        # 创建网络
        G = nx.Graph()
        
        # 添加节点和边
        for _, row in self.data.iterrows():
            node = row[node_col]
            edges = row[edge_col]
            
            # 处理边列可能是列表或字符串的情况
            if isinstance(edges, list):
                for edge in edges:
                    G.add_edge(node, edge)
            elif isinstance(edges, str):
                # 如果是逗号分隔的字符串
                for edge in edges.split(','):
                    edge = edge.strip()
                    if edge:
                        G.add_edge(node, edge)
        
        return G
    
    def cluster_analysis(self, n_clusters=3):
        """
        聚类分析
        
        Args:
            n_clusters (int): 聚类数量
            
        Returns:
            dict: 聚类分析结果
        """
        if self.data.empty:
            return {"error": "数据为空"}
        
        # 选择数值型列
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return {"error": "数值型列不足"}
        
        # 处理缺失值
        numeric_data = self.data[numeric_cols].dropna()
        if numeric_data.empty:
            return {"error": "处理缺失值后数据为空"}
        
        # 标准化数据
        scaled_data = self.scaler.fit_transform(numeric_data)
        
        # 执行K-means聚类
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(scaled_data)
        
        # 计算聚类中心
        cluster_centers = kmeans.cluster_centers_
        
        # 计算每个聚类的大小
        cluster_sizes = Counter(clusters)
        
        return {
            "clusters": clusters.tolist(),
            "cluster_centers": cluster_centers.tolist(),
            "cluster_sizes": dict(cluster_sizes),
            "columns": numeric_cols.tolist()
        }
    
    def time_series_analysis(self, time_col, value_col):
        """
        时间序列分析
        
        Args:
            time_col (str): 时间列名
            value_col (str): 值列名
            
        Returns:
            dict: 时间序列分析结果
        """
        if self.data.empty:
            return {"error": "数据为空"}
        
        if time_col not in self.data.columns or value_col not in self.data.columns:
            return {"error": "列名不存在"}
        
        # 确保时间列是 datetime 类型
        try:
            self.data[time_col] = pd.to_datetime(self.data[time_col])
        except Exception as e:
            return {"error": f"时间列转换失败: {e}"}
        
        # 按时间排序
        time_series_data = self.data[[time_col, value_col]].sort_values(time_col)
        
        # 计算基本统计
        time_stats = {
            "start_date": time_series_data[time_col].min().isoformat(),
            "end_date": time_series_data[time_col].max().isoformat(),
            "mean_value": time_series_data[value_col].mean(),
            "std_value": time_series_data[value_col].std(),
            "max_value": time_series_data[value_col].max(),
            "min_value": time_series_data[value_col].min(),
            "trend": self._calculate_trend(time_series_data[value_col])
        }
        
        return time_stats
    
    def _calculate_trend(self, values):
        """
        计算时间序列趋势
        
        Args:
            values (pd.Series): 值序列
            
        Returns:
            float: 趋势值
        """
        x = np.arange(len(values))
        slope, _, _, _, _ = stats.linregress(x, values)
        return slope
    
    def geographic_analysis(self, lat_col, lon_col, value_col=None):
        """
        地理空间分析
        
        Args:
            lat_col (str): 纬度列名
            lon_col (str): 经度列名
            value_col (str): 值列名（可选）
            
        Returns:
            dict: 地理空间分析结果
        """
        if self.data.empty:
            return {"error": "数据为空"}
        
        if lat_col not in self.data.columns or lon_col not in self.data.columns:
            return {"error": "经纬度列不存在"}
        
        # 计算地理中心
        mean_lat = self.data[lat_col].mean()
        mean_lon = self.data[lon_col].mean()
        
        # 计算地理范围
        min_lat = self.data[lat_col].min()
        max_lat = self.data[lat_col].max()
        min_lon = self.data[lon_col].min()
        max_lon = self.data[lon_col].max()
        
        geo_stats = {
            "center": {
                "latitude": mean_lat,
                "longitude": mean_lon
            },
            "bounding_box": {
                "min_latitude": min_lat,
                "max_latitude": max_lat,
                "min_longitude": min_lon,
                "max_longitude": max_lon
            },
            "points_count": len(self.data)
        }
        
        # 如果提供了值列，计算值的统计
        if value_col and value_col in self.data.columns:
            geo_stats["value_stats"] = {
                "mean": self.data[value_col].mean(),
                "std": self.data[value_col].std(),
                "max": self.data[value_col].max(),
                "min": self.data[value_col].min()
            }
        
        return geo_stats
    
    def sentiment_analysis(self, text_col):
        """
        情感分析
        
        Args:
            text_col (str): 文本列名
            
        Returns:
            dict: 情感分析结果
        """
        if self.data.empty:
            return {"error": "数据为空"}
        
        if text_col not in self.data.columns:
            return {"error": "文本列不存在"}
        
        # 简单的情感分析（基于关键词）
        positive_words = set(["好", "优秀", "精彩", "美丽", "喜欢", "赞", "棒", "完美", "出色", "满意", 
                            "good", "great", "excellent", "wonderful", "beautiful", "like", "love", "awesome", "perfect", "amazing"])
        negative_words = set(["坏", "糟糕", "差", "难看", "讨厌", "无聊", "失望", "垃圾", "恶心", "不满", 
                            "bad", "terrible", "awful", "ugly", "hate", "boring", "disappointed", "trash", "disgusting", "unhappy"])
        
        sentiments = []
        positive_counts = []
        negative_counts = []
        
        for text in self.data[text_col].astype(str):
            words = text.lower().split()
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            
            if positive_count > negative_count:
                sentiment = "positive"
            elif negative_count > positive_count:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            sentiments.append(sentiment)
            positive_counts.append(positive_count)
            negative_counts.append(negative_count)
        
        sentiment_counts = Counter(sentiments)
        
        return {
            "sentiments": sentiments,
            "sentiment_counts": dict(sentiment_counts),
            "positive_word_counts": positive_counts,
            "negative_word_counts": negative_counts,
            "average_positive_words": np.mean(positive_counts),
            "average_negative_words": np.mean(negative_counts)
        }
    
    def visualize(self, viz_type="histogram", x_col=None, y_col=None, **kwargs):
        """
        数据可视化
        
        Args:
            viz_type (str): 可视化类型
            x_col (str): x轴列名
            y_col (str): y轴列名
            **kwargs: 其他参数
            
        Returns:
            plotly.graph_objects.Figure: 可视化图表
        """
        if self.data.empty:
            return None
        
        try:
            if viz_type == "histogram":
                # 直方图
                if x_col:
                    fig = px.histogram(self.data, x=x_col, **kwargs)
                else:
                    fig = px.histogram(self.data, **kwargs)
            
            elif viz_type == "scatter":
                # 散点图
                if x_col and y_col:
                    fig = px.scatter(self.data, x=x_col, y=y_col, **kwargs)
                else:
                    return None
            
            elif viz_type == "bar":
                # 条形图
                if x_col and y_col:
                    fig = px.bar(self.data, x=x_col, y=y_col, **kwargs)
                else:
                    fig = px.bar(self.data, **kwargs)
            
            elif viz_type == "line":
                # 折线图
                if x_col and y_col:
                    fig = px.line(self.data, x=x_col, y=y_col, **kwargs)
                else:
                    return None
            
            elif viz_type == "pie":
                # 饼图
                if x_col:
                    fig = px.pie(self.data, names=x_col, **kwargs)
                else:
                    return None
            
            elif viz_type == "heatmap":
                # 热力图
                if x_col and y_col:
                    fig = px.density_heatmap(self.data, x=x_col, y=y_col, **kwargs)
                else:
                    return None
            
            elif viz_type == "box":
                # 箱线图
                if x_col and y_col:
                    fig = px.box(self.data, x=x_col, y=y_col, **kwargs)
                else:
                    fig = px.box(self.data, **kwargs)
            
            elif viz_type == "network":
                # 网络图
                if "node_col" in kwargs and "edge_col" in kwargs:
                    G = self.network_analysis(kwargs["node_col"], kwargs["edge_col"])
                    if G:
                        pos = nx.spring_layout(G)
                        edge_x = []
                        edge_y = []
                        for edge in G.edges():
                            x0, y0 = pos[edge[0]]
                            x1, y1 = pos[edge[1]]
                            edge_x.extend([x0, x1, None])
                            edge_y.extend([y0, y1, None])
                        
                        edge_trace = go.Scatter(
                            x=edge_x, y=edge_y,
                            line=dict(width=0.5, color='#888'),
                            hoverinfo='none',
                            mode='lines')
                        
                        node_x = []
                        node_y = []
                        for node in G.nodes():
                            x, y = pos[node]
                            node_x.append(x)
                            node_y.append(y)
                        
                        node_trace = go.Scatter(
                            x=node_x, y=node_y,
                            mode='markers',
                            hoverinfo='text',
                            marker=dict(
                                showscale=True,
                                colorscale='YlGnBu',
                                size=10,
                                colorbar=dict(
                                    thickness=15,
                                    title='Node Connections',
                                    xanchor='left',
                                    titleside='right'
                                )
                            )
                        )
                        
                        node_adjacencies = []
                        node_text = []
                        for node, adjacencies in enumerate(G.adjacency()):
                            node_adjacencies.append(len(adjacencies[1]))
                            node_text.append(f'{adjacencies[0]} - # of connections: {len(adjacencies[1])}')
                        
                        node_trace.marker.color = node_adjacencies
                        node_trace.text = node_text
                        
                        fig = go.Figure(data=[edge_trace, node_trace],
                                     layout=go.Layout(
                                         title='Network Graph',
                                         titlefont_size=16,
                                         showlegend=False,
                                         hovermode='closest',
                                         margin=dict(b=20,l=5,r=5,t=40),
                                         annotations=[ dict(
                                             text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                                             showarrow=False,
                                             xref="paper", yref="paper",
                                             x=0.005, y=-0.002 ) ],
                                         xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                         yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
                    else:
                        return None
            
            else:
                return None
            
            return fig
        except Exception as e:
            print(f"可视化出错: {e}")
            return None
    
    def export_analysis(self, analysis_result, output_path):
        """
        导出分析结果
        
        Args:
            analysis_result (dict): 分析结果
            output_path (str): 输出文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(analysis_result, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出分析结果出错: {e}")
            return False
