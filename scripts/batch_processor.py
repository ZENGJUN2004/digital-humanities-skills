#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
数字人文技能库批处理器

这个脚本可以批量处理文件夹中的文本文件，并将结果保存到输出文件夹
"""

from digital_humanities import DigitalHumanities
import os
import json
import time

class BatchProcessor:
    """
    批处理器类，用于处理文件夹中的多个文本文件
    """
    
    def __init__(self):
        """
        初始化批处理器
        """
        self.dh = DigitalHumanities()
        print("批处理器初始化完成")
    
    def process_folder(self, input_folder: str, output_folder: str, file_extensions: list = ['.txt', '.md', '.csv']) -> dict:
        """
        处理文件夹中的所有文本文件
        
        Args:
            input_folder: 输入文件夹路径
            output_folder: 输出文件夹路径
            file_extensions: 要处理的文件扩展名列表
            
        Returns:
            批处理结果统计
        """
        # 检查输入文件夹是否存在
        if not os.path.exists(input_folder):
            return {"error": f"输入文件夹不存在: {input_folder}"}
        
        # 创建输出文件夹
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
        
        # 统计信息
        stats = {
            "total_files": 0,
            "processed_files": 0,
            "failed_files": 0,
            "start_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": None,
            "files": []
        }
        
        print(f"开始处理文件夹: {input_folder}")
        print(f"输出结果将保存到: {output_folder}")
        print("=" * 80)
        
        # 遍历输入文件夹中的文件
        for root, dirs, files in os.walk(input_folder):
            for file_name in files:
                # 检查文件扩展名
                if any(file_name.endswith(ext) for ext in file_extensions):
                    stats["total_files"] += 1
                    file_path = os.path.join(root, file_name)
                    
                    print(f"\n处理文件: {file_name}")
                    print("-" * 40)
                    
                    try:
                        # 读取文件内容
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 处理文件内容
                        result = self.process_file(content, file_name)
                        
                        # 保存结果
                        output_file = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_result.json")
                        with open(output_file, 'w', encoding='utf-8') as f:
                            json.dump(result, f, ensure_ascii=False, indent=2)
                        
                        stats["processed_files"] += 1
                        stats["files"].append({
                            "file_name": file_name,
                            "status": "success",
                            "output_file": output_file
                        })
                        
                        print(f"✓ 处理成功，结果保存到: {output_file}")
                        
                    except Exception as e:
                        stats["failed_files"] += 1
                        stats["files"].append({
                            "file_name": file_name,
                            "status": "failed",
                            "error": str(e)
                        })
                        
                        print(f"✗ 处理失败: {str(e)}")
        
        stats["end_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        print("=" * 80)
        print("批处理完成")
        print(f"总文件数: {stats['total_files']}")
        print(f"成功处理: {stats['processed_files']}")
        print(f"处理失败: {stats['failed_files']}")
        print(f"开始时间: {stats['start_time']}")
        print(f"结束时间: {stats['end_time']}")
        
        # 保存统计信息
        stats_file = os.path.join(output_folder, "batch_processing_stats.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"统计信息保存到: {stats_file}")
        
        return stats
    
    def process_file(self, content: str, file_name: str) -> dict:
        """
        处理单个文件内容
        
        Args:
            content: 文件内容
            file_name: 文件名
            
        Returns:
            处理结果
        """
        # 根据文件大小进行处理
        if len(content) > 1000000:  # 1MB以上的大文件
            # 对于大文件，我们可以分段处理
            chunks = self._split_content(content, chunk_size=500000)
            results = []
            
            for i, chunk in enumerate(chunks):
                request = {
                    "description": f"处理文件 {file_name} 的第 {i+1} 部分",
                    "text": chunk
                }
                result = self.dh.process_request(request)
                results.append({
                    "chunk": i+1,
                    "result": result
                })
            
            return {
                "file_name": file_name,
                "file_size": len(content),
                "is_large_file": True,
                "chunks_processed": len(chunks),
                "results": results
            }
        else:
            # 对于小文件，直接处理
            request = {
                "description": f"处理文件 {file_name}",
                "text": content
            }
            result = self.dh.process_request(request)
            
            return {
                "file_name": file_name,
                "file_size": len(content),
                "is_large_file": False,
                "result": result
            }
    
    def _split_content(self, content: str, chunk_size: int = 500000) -> list:
        """
        将大文本分割成小块
        
        Args:
            content: 要分割的文本
            chunk_size: 每块的大小
            
        Returns:
            文本块列表
        """
        chunks = []
        for i in range(0, len(content), chunk_size):
            chunks.append(content[i:i+chunk_size])
        return chunks

def main():
    """
    主函数
    """
    processor = BatchProcessor()
    
    # 示例用法
    input_folder = "d:\\myapp\\skills\\数字人文技能\\assets"
    output_folder = "d:\\myapp\\skills\\数字人文技能\\output"
    
    print("数字人文技能库批处理器")
    print("=" * 80)
    print(f"输入文件夹: {input_folder}")
    print(f"输出文件夹: {output_folder}")
    print("=" * 80)
    
    # 开始批处理
    result = processor.process_folder(input_folder, output_folder)
    
    if "error" in result:
        print(f"错误: {result['error']}")
    else:
        print("批处理成功完成！")

if __name__ == "__main__":
    main()
