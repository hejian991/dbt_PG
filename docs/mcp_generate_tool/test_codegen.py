#!/usr/bin/env python3
"""
测试 dbt MCP Codegen 工具
这个脚本演示如何使用 dbt-hejian991-remote MCP 的 codegen 工具自动生成 dbt 项目文件

注意：根据文档，codegen 工具默认是禁用的。
要启用它们，需要设置环境变量 DISABLE_DBT_CODEGEN=false
"""

import os
import sys

def test_generate_source():
    """
    测试 generate_source 工具
    从数据库 schema 创建 source YAML 定义
    
    示例用法：
    - 输入：数据库 schema 名称和表名
    - 输出：YAML 格式的 source 定义
    """
    print("=" * 80)
    print("测试 1: generate_source - 从数据库生成 source YAML")
    print("=" * 80)
    print()
    print("说明：此工具可以从数据库 schema 自动生成 source YAML 定义")
    print("用途：避免手动编写 sources.yml 文件")
    print()
    print("示例：假设我们有一个 'raw' schema，包含 'customers', 'orders', 'payments' 表")
    print()
    print("预期输出格式：")
    print("""
version: 2

sources:
  - name: raw
    description: "Raw data from source systems"
    tables:
      - name: customers
        columns:
          - name: id
            description: ""
          - name: first_name
            description: ""
          - name: last_name
            description: ""
      
      - name: orders
        columns:
          - name: id
            description: ""
          - name: user_id
            description: ""
          - name: order_date
            description: ""
          - name: status
            description: ""
      
      - name: payments
        columns:
          - name: id
            description: ""
          - name: order_id
            description: ""
          - name: payment_method
            description: ""
          - name: amount
            description: ""
    """)
    print()

def test_generate_model_yaml():
    """
    测试 generate_model_yaml 工具
    为现有 dbt 模型生成文档 YAML
    
    示例用法：
    - 输入：模型名称（如 'stg_customers'）
    - 输出：包含所有列名、数据类型和描述占位符的 YAML
    """
    print("=" * 80)
    print("测试 2: generate_model_yaml - 为现有模型生成文档 YAML")
    print("=" * 80)
    print()
    print("说明：此工具可以为已存在的 dbt 模型自动生成文档 YAML")
    print("用途：快速为模型添加文档框架，避免手动列出所有列")
    print()
    print("示例：为 'customers' 模型生成 YAML")
    print()
    print("预期输出格式：")
    print("""
version: 2

models:
  - name: customers
    description: ""
    columns:
      - name: customer_id
        data_type: integer
        description: ""
      
      - name: first_name
        data_type: varchar
        description: ""
      
      - name: last_name
        data_type: varchar
        description: ""
      
      - name: first_order_date
        data_type: date
        description: ""
      
      - name: most_recent_order_date
        data_type: date
        description: ""
      
      - name: number_of_orders
        data_type: bigint
        description: ""
      
      - name: total_order_amount
        data_type: numeric
        description: ""
    """)
    print()

def test_generate_staging_model():
    """
    测试 generate_staging_model 工具
    从 sources 创建 staging SQL 模型
    
    示例用法：
    - 输入：source 名称和表名
    - 输出：完整的 staging 模型 SQL 代码
    """
    print("=" * 80)
    print("测试 3: generate_staging_model - 从 source 生成 staging 模型")
    print("=" * 80)
    print()
    print("说明：此工具可以从 source 自动生成 staging 模型的 SQL 代码")
    print("用途：快速创建符合最佳实践的 staging 模型模板")
    print()
    print("示例：为 'raw.customers' source 生成 staging 模型")
    print()
    print("预期输出格式：")
    print("""
with source as (

    select * from {{ source('raw', 'customers') }}

),

renamed as (

    select
        id as customer_id,
        first_name,
        last_name

    from source

)

select * from renamed
    """)
    print()

def print_usage_instructions():
    """打印使用说明"""
    print()
    print("=" * 80)
    print("如何在实际项目中使用 Codegen 工具")
    print("=" * 80)
    print()
    print("1. 确保已安装 dbt-codegen 包")
    print("   在 packages.yml 中添加：")
    print("""
packages:
  - package: dbt-labs/codegen
    version: 0.12.1
    """)
    print()
    print("   然后运行: dbt deps")
    print()
    print("2. 设置环境变量启用 codegen 工具")
    print("   export DISABLE_DBT_CODEGEN=false")
    print()
    print("3. 通过 MCP 客户端（如 Claude、Cursor）使用工具")
    print("   - 在 AI 对话中请求生成 source 或模型文件")
    print("   - AI 会调用相应的 codegen 工具")
    print("   - 自动生成的代码可以直接保存到项目中")
    print()
    print("4. 实际命令示例（如果直接使用 dbt-codegen）：")
    print()
    print("   生成 source:")
    print("   dbt run-operation generate_source --args '{\"schema_name\": \"raw\"}'")
    print()
    print("   生成 model yaml:")
    print("   dbt run-operation generate_model_yaml --args '{\"model_names\": [\"customers\"]}'")
    print()
    print("   生成 staging model:")
    print("   dbt run-operation generate_staging_model --args '{\"source_name\": \"raw\", \"table_name\": \"customers\"}'")
    print()

def check_codegen_package():
    """检查是否安装了 dbt-codegen 包"""
    print("=" * 80)
    print("检查 dbt-codegen 包安装状态")
    print("=" * 80)
    print()
    
    packages_file = "/Users/hj/code/test_agent2.0/dbt_pg/packages.yml"
    
    if os.path.exists(packages_file):
        print(f"✓ 找到 packages.yml 文件")
        with open(packages_file, 'r') as f:
            content = f.read()
            if 'codegen' in content:
                print("✓ dbt-codegen 包已在 packages.yml 中配置")
                print()
                print("文件内容：")
                print(content)
            else:
                print("✗ packages.yml 中未找到 dbt-codegen 包")
                print()
                print("需要添加以下内容到 packages.yml：")
                print("""
packages:
  - package: dbt-labs/codegen
    version: 0.12.1
                """)
    else:
        print(f"✗ 未找到 packages.yml 文件")
        print()
        print("需要创建 packages.yml 文件并添加：")
        print("""
packages:
  - package: dbt-labs/codegen
    version: 0.12.1
        """)
    print()

def main():
    """主函数"""
    print()
    print("*" * 80)
    print("dbt MCP Codegen 工具测试脚本")
    print("*" * 80)
    print()
    print("这个脚本演示了 dbt-hejian991-remote MCP 服务器提供的三个 codegen 工具：")
    print("1. generate_source - 生成 source YAML 定义")
    print("2. generate_model_yaml - 生成模型文档 YAML")
    print("3. generate_staging_model - 生成 staging 模型 SQL")
    print()
    print("注意：这些工具需要：")
    print("- 安装 dbt-codegen 包（dbt deps）")
    print("- 设置环境变量 DISABLE_DBT_CODEGEN=false")
    print()
    
    # 检查 codegen 包
    check_codegen_package()
    
    # 运行测试
    test_generate_source()
    test_generate_model_yaml()
    test_generate_staging_model()
    
    # 打印使用说明
    print_usage_instructions()
    
    print("=" * 80)
    print("测试完成")
    print("=" * 80)
    print()

if __name__ == "__main__":
    main()

