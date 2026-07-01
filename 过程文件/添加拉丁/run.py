# run_simple.py
import pandas as pd
import os
import re

print("开始处理...")

# 检查文件是否存在
if not os.path.exists('pages.xlsx'):
    print("错误: 找不到 pages.xlsx")
    exit()

if not os.path.exists('names.xlsx'):
    print("错误: 找不到 names.xlsx")
    exit()

# 创建日志文件
log_file = open('processing_log.txt', 'w', encoding='utf-8')
log_file.write("开始处理数据\n")

try:
    # 读取names.xlsx创建字典
    print("正在读取names.xlsx...")
    names_df = pd.read_excel('names.xlsx')
    name_dict = {}
    for idx, row in names_df.iterrows():
        chinese = str(row.iloc[0]).strip()
        latin = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
        if chinese and chinese != 'nan':
            name_dict[chinese] = latin
    
    print(f"成功加载 {len(name_dict)} 个名称映射")
    log_file.write(f"成功加载 {len(name_dict)} 个名称映射\n")
    
    # 读取pages.xlsx
    print("正在读取pages.xlsx...")
    xl_file = pd.ExcelFile('pages.xlsx')
    sheet_names = xl_file.sheet_names
    print(f"找到 {len(sheet_names)} 个工作表: {sheet_names}")
    
    # 创建新的Excel文件
    with pd.ExcelWriter('pages_updated.xlsx') as writer:
        for sheet_name in sheet_names:
            print(f"处理工作表: {sheet_name}")
            log_file.write(f"\n处理工作表: {sheet_name}\n")
            
            df = pd.read_excel(xl_file, sheet_name=sheet_name)
            
            # 检查是否已有拉丁名
            has_latin = False
            for value in df.iloc[:, 0]:
                if pd.notna(value) and re.search(r'[a-zA-Z]', str(value)):
                    has_latin = True
                    break
            
            if has_latin:
                print(f"  - 跳过（已有拉丁名）")
                log_file.write(f"跳过（已有拉丁名）\n")
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                continue
            
            # 处理没有拉丁名的工作表
            unmatched = []
            for idx in range(len(df)):
                original_name = str(df.iloc[idx, 0])
                if original_name == 'nan' or pd.isna(df.iloc[idx, 0]):
                    continue
                
                latin_name = name_dict.get(original_name.strip())
                if latin_name:
                    df.iloc[idx, 0] = original_name + latin_name
                else:
                    unmatched.append((idx+1, original_name))
            
            if unmatched:
                log_file.write(f"未匹配的数据:\n")
                for row_num, name in unmatched:
                    log_file.write(f"  第{row_num}行 {name}\n")
                print(f"  - 有 {len(unmatched)} 个未匹配项")
            
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    print("处理完成！")
    print("输出文件: pages_updated.xlsx")
    print("日志文件: processing_log.txt")
    
except Exception as e:
    print(f"发生错误: {e}")
    import traceback
    traceback.print_exc()
    log_file.write(f"错误: {e}\n")
    log_file.write(traceback.format_exc())

log_file.close()