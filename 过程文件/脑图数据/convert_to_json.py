import pandas as pd
import json

# 读取Excel文件
file_path = 'output-with.xlsx'
df = pd.read_excel(file_path)

# 初始化一个空的字典来存储最终的JSON数据
result = {}

# 遍历DataFrame的每一行
for index, row in df.iterrows():
    current_level = result
    for i, cell in enumerate(row[:-1]):  # 遍历到倒数第二列（物种中文名之前）
        if pd.isna(cell):  # 如果当前单元格为空，则跳过
            continue
        if cell not in current_level:
            current_level[cell] = {}
        current_level = current_level[cell]
    # 添加物种中文名
    if not pd.isna(row[-1]):
        current_level[row[-1]] = None  # 物种中文名作为叶子节点

# 将结果转换为JSON字符串
json_data = json.dumps(result, ensure_ascii=False, indent=4)

# 打印JSON数据
print(json_data)

# 保存到文件
with open('植物界-2025-47927-仅苔藓.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print("JSON数据已保存到文件：植物界-2025-47927-仅苔藓.json")