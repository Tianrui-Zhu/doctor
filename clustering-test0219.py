import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# --------------------------------------------
# 步骤1：从Excel读取数据
# --------------------------------------------
def read_excel_data(file_path):
    """
    从Excel中读取样本数据
    输入参数：
        file_path: Excel文件路径
    返回：
        samples: 样本关键词集合列表（每个元素为一个样本的关键词集合）
        sample_names: 样本名称列表
    """
    # 读取Sheet1的A-L列数据（假设第一行是标题）
    df = pd.read_excel(file_path, sheet_name='sheet1', header=0, usecols='B:L')
    
    samples = []
    sample_names = []
    for index, row in df.iterrows():
        # B列为样本名称
        sample_names.append(row[0])
        # C-L列（即数据中的第1到10列）为关键词，转换为集合
        keywords = set(row[1:11].dropna().astype(str).values)
        samples.append(keywords)
    
    return samples, sample_names

# --------------------------------------------
# 步骤2：计算距离矩阵
# --------------------------------------------
def calculate_distance_matrix(samples):
    """
    计算所有样本间的距离矩阵
    输入参数：
        samples: 样本关键词集合列表
    返回：
        distance_matrix: 距离矩阵（numpy数组）
    """
    n = len(samples)
    distance_matrix = np.zeros((n, n))
    
    # 遍历所有样本对
    for i in range(n):
        for j in range(i+1, n):
            # 计算共同关键词数量
            common = len(samples[i] & samples[j])
            # 距离 = 10 - 共同关键词数量
            distance = 10 - common
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance  # 对称填充
    
    return distance_matrix

# --------------------------------------------
# 步骤3：执行层次聚类
# --------------------------------------------
def hierarchical_clustering(distance_matrix, method='single'):
    """
    执行层次聚类
    输入参数：
        distance_matrix: 距离矩阵
        method: 聚类方法（'single'表示最小距离法）
    返回：
        linkage_matrix: 聚类连接矩阵
    """
    # 将距离矩阵压缩为condensed格式（scipy要求输入）
    condensed_dist = distance_matrix[np.triu_indices(len(distance_matrix), k=1)]
    
    # 执行层次聚类
    linkage_matrix = linkage(condensed_dist, method=method)
    
    return linkage_matrix

# --------------------------------------------
# 步骤4：绘制树状图
# --------------------------------------------
def plot_dendrogram(linkage_matrix, labels, figsize=(15, 30)):
    """
    绘制树状图
    输入参数：
        linkage_matrix: 聚类连接矩阵
        labels: 样本名称标签列表
        figsize: 图像尺寸
    """
    plt.figure(figsize=figsize)
    dendrogram(
        linkage_matrix,
        labels=labels,
        orientation='left',  # 横向显示
        leaf_font_size=4,    # 调整标签字体大小
    )
    plt.title('Hierarchical Clustering Dendrogram (Single Linkage)')
    plt.xlabel('Distance')
    plt.grid(False)
    plt.tight_layout()
    plt.show()

# --------------------------------------------
# 主程序
# --------------------------------------------
if __name__ == "__main__":
    # 参数设置
    excel_path = r"D:\study\python-test\试验20250217.xlsx"  # 修改为你的Excel文件路径
    
    # 1. 读取数据
    samples, sample_names = read_excel_data(excel_path)
    
    # 2. 计算距离矩阵
    print("正在计算距离矩阵...")
    distance_matrix = calculate_distance_matrix(samples)
    
    # 3. 执行聚类
    print("正在执行层次聚类...")
    linkage_matrix = hierarchical_clustering(distance_matrix, method='average')
    #方法有single，complete，average，ward，centroid等

    # 4. 绘制树状图
    print("生成树状图...")
    plot_dendrogram(linkage_matrix, sample_names, figsize=(20, 20))  # 增大图像尺寸