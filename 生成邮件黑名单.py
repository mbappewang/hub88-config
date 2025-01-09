import pandas as pd
import os
import mysql.connector

def concat_xlsx(file_path, db_config, table_name):
    # 读取指定的xlsx文件
    df = pd.read_excel(file_path)
    print("读取xlsx文件完成")
    
    # 读取每列非首行的值
    values = []
    for col in df.columns:
        values.extend(df[col][1:].dropna().tolist())
    print(f"读取每列非首行的值{len(values)}个完成")
    
    # 连接数据库并获取account_id列数据
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = f"SELECT account_id FROM {table_name}"
    cursor.execute(query)
    db_values = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    print(f"连接数据库并获取account_id列数据{len(db_values)}个完成")
    
    # 合并数据并去重
    all_values = values + db_values
    unique_values = list(set(all_values))
    print(f"合并数据并去重{len(unique_values)}个完成")
    
    # 将所有值合并到一列中
    result_df = pd.DataFrame(unique_values, columns=['合并列'])
    print("将所有值合并到一列中完成")
    result_df = result_df.astype(str)
    # 获取原始文件名和路径
    base_name = os.path.basename(file_path)
    dir_name = os.path.dirname(file_path)
    new_file_name = f"合并_{os.path.splitext(base_name)[0]}.csv"
    new_file_path = os.path.join(dir_name, new_file_name)
    
    # 导出文件为CSV
    result_df.to_csv(new_file_path, index=False)
    print(f"文件已保存为: {new_file_path}")

# 示例调用
file_path = 'excel/截至1.8封号.xlsx' 
db_config = {
    'user': 'email_not',  
    'password': 'wintokens',  
    'host': '107.191.60.19',  
    'database': 'email_not'  
}
table_name = 'email_not'  
concat_xlsx(file_path, db_config, table_name)