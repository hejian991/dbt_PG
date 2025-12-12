#!/usr/bin/env python3
"""
dbt MCP Codegen 工具实际使用演示

本脚本展示如何通过 AI 助手（Claude、Cursor 等）使用 MCP codegen 工具来自动化生成 dbt 项目文件。

工作流程：
1. 安装 dbt-codegen 包
2. 设置环境变量启用 codegen 工具
3. 通过 AI 对话请求生成代码
4. 将生成的代码保存到项目文件中
"""

import os
import sys
import json

# 演示场景配置
DEMO_SCENARIOS = {
    "scenario_1": {
        "name": "从数据库生成 source 定义",
        "description": "为 PostgreSQL 中的 raw schema 生成 source YAML",
        "tool": "generate_source",
        "prompt": "请为 PostgreSQL 数据库中的 'raw' schema 生成 source 定义，包括 customers、orders 和 payments 表",
        "expected_file": "models/staging/sources.yml",
        "example_output": """version: 2

sources:
  - name: raw
    description: "Raw data from operational systems"
    database: postgres
    schema: raw
    tables:
      - name: customers
        description: "Raw customer data"
        columns:
          - name: id
            description: "Primary key"
            data_type: integer
          - name: first_name
            description: "Customer first name"
            data_type: varchar
          - name: last_name
            description: "Customer last name"
            data_type: varchar
      
      - name: orders
        description: "Raw order data"
        columns:
          - name: id
            description: "Primary key"
            data_type: integer
          - name: user_id
            description: "Foreign key to customers"
            data_type: integer
          - name: order_date
            description: "Date order was placed"
            data_type: date
          - name: status
            description: "Order status"
            data_type: varchar
      
      - name: payments
        description: "Raw payment data"
        columns:
          - name: id
            description: "Primary key"
            data_type: integer
          - name: order_id
            description: "Foreign key to orders"
            data_type: integer
          - name: payment_method
            description: "Method of payment"
            data_type: varchar
          - name: amount
            description: "Payment amount in cents"
            data_type: integer
"""
    },
    
    "scenario_2": {
        "name": "为现有模型生成文档",
        "description": "为 customers 模型生成完整的 YAML 文档",
        "tool": "generate_model_yaml",
        "prompt": "请为 'customers' 模型生成完整的 YAML 文档，包括所有列的数据类型和描述占位符",
        "expected_file": "models/schema.yml",
        "example_output": """version: 2

models:
  - name: customers
    description: "Customer dimension table with order aggregations"
    columns:
      - name: customer_id
        description: "Primary key - unique customer identifier"
        data_type: integer
        tests:
          - unique
          - not_null
      
      - name: first_name
        description: "Customer's first name"
        data_type: varchar
      
      - name: last_name
        description: "Customer's last name"
        data_type: varchar
      
      - name: first_order_date
        description: "Date of customer's first order"
        data_type: date
      
      - name: most_recent_order_date
        description: "Date of customer's most recent order"
        data_type: date
      
      - name: number_of_orders
        description: "Total count of orders placed by customer"
        data_type: bigint
      
      - name: total_order_amount
        description: "Lifetime total order amount in cents"
        data_type: numeric
"""
    },
    
    "scenario_3": {
        "name": "生成 staging 模型",
        "description": "从 raw.products source 生成 stg_products 模型",
        "tool": "generate_staging_model",
        "prompt": "请从 'raw' source 的 'products' 表生成一个 stg_products staging 模型",
        "expected_file": "models/staging/stg_products.sql",
        "example_output": """with source as (

    select * from {{ source('raw', 'products') }}

),

renamed as (

    select
        id as product_id,
        name as product_name,
        category as product_category,
        price as product_price,
        created_at,
        updated_at

    from source

)

select * from renamed
"""
    }
}


def print_scenario(scenario_key):
    """打印单个场景的详细信息"""
    scenario = DEMO_SCENARIOS[scenario_key]
    
    print(f"\n{'=' * 80}")
    print(f"场景: {scenario['name']}")
    print(f"{'=' * 80}\n")
    
    print(f"📝 描述: {scenario['description']}")
    print(f"🔧 工具: {scenario['tool']}")
    print(f"📁 目标文件: {scenario['expected_file']}")
    print()
    
    print("💬 对话提示词（向 AI 助手说）:")
    print("-" * 80)
    print(scenario['prompt'])
    print("-" * 80)
    print()
    
    print("📤 预期输出:")
    print("-" * 80)
    print(scenario['example_output'])
    print("-" * 80)
    print()


def print_setup_instructions():
    """打印设置说明"""
    print("\n" + "=" * 80)
    print("🚀 设置步骤")
    print("=" * 80 + "\n")
    
    print("步骤 1: 安装 dbt-codegen 包")
    print("-" * 80)
    print("已创建 packages.yml 文件，请运行:")
    print()
    print("  cd /Users/hj/code/test_agent2.0/dbt_pg")
    print("  dbt deps")
    print()
    
    print("步骤 2: 启用 codegen 工具")
    print("-" * 80)
    print("设置环境变量（codegen 工具默认禁用）:")
    print()
    print("  export DISABLE_DBT_CODEGEN=false")
    print()
    print("或在 MCP 配置中添加:")
    print("""
{
  "mcpServers": {
    "dbt": {
      "command": "uvx",
      "args": ["dbt-mcp"],
      "env": {
        "DISABLE_DBT_CODEGEN": "false"
      }
    }
  }
}
""")
    print()
    
    print("步骤 3: 确保 MCP 服务器正确配置")
    print("-" * 80)
    print("检查你的 MCP 客户端（Cursor/Claude）是否已连接到 dbt-hejian991-remote")
    print()


def print_workflow():
    """打印工作流程说明"""
    print("\n" + "=" * 80)
    print("🔄 使用工作流程")
    print("=" * 80 + "\n")
    
    print("方式 1: 通过 AI 对话（推荐）")
    print("-" * 80)
    print("""
1. 在 Cursor 或 Claude 中打开 dbt 项目
2. 使用上述场景中的提示词与 AI 对话
3. AI 会自动调用相应的 MCP codegen 工具
4. 生成的代码会直接显示在对话中
5. 确认后，AI 会将代码保存到指定文件
""")
    
    print("\n方式 2: 直接使用 dbt 命令")
    print("-" * 80)
    print("""
如果想直接使用 dbt-codegen（不通过 MCP）:

# 生成 source
dbt run-operation generate_source --args '{"schema_name": "raw", "database_name": "postgres"}'

# 生成 model yaml
dbt run-operation generate_model_yaml --args '{"model_names": ["customers"]}'

# 生成 staging model（需要先有 source 定义）
dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "customers"}'
""")


def create_example_conversation():
    """创建示例对话脚本"""
    print("\n" + "=" * 80)
    print("💡 示例对话")
    print("=" * 80 + "\n")
    
    conversations = [
        {
            "user": "我需要为项目添加一个新的数据源。我们的 PostgreSQL 数据库中有一个 'raw' schema，包含 customers、orders 和 payments 三个表。请帮我生成 source 定义。",
            "assistant": "我会使用 generate_source 工具为你生成 source 定义...",
            "result": "生成了 sources.yml 文件，包含完整的表和列定义"
        },
        {
            "user": "现在我想为 customers 表创建一个 staging 模型，请帮我生成代码。",
            "assistant": "我会使用 generate_staging_model 工具...",
            "result": "生成了 stg_customers.sql 文件，符合 dbt 最佳实践"
        },
        {
            "user": "我的 customers 最终模型已经完成了，但是缺少文档。请帮我生成完整的 YAML 文档。",
            "assistant": "我会使用 generate_model_yaml 工具...",
            "result": "生成了包含所有列的 schema.yml，你可以填充具体的描述"
        }
    ]
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n对话 {i}:")
        print("-" * 80)
        print(f"👤 用户: {conv['user']}")
        print()
        print(f"🤖 AI: {conv['assistant']}")
        print()
        print(f"✅ 结果: {conv['result']}")
        print()


def print_benefits():
    """打印使用 codegen 的好处"""
    print("\n" + "=" * 80)
    print("✨ 使用 Codegen 工具的好处")
    print("=" * 80 + "\n")
    
    benefits = [
        "⚡️ 快速启动：几秒钟生成完整的 source 定义，无需手动列出所有表和列",
        "📝 标准化：生成的代码符合 dbt 最佳实践和团队规范",
        "🎯 减少错误：避免手动输入时的拼写错误或遗漏",
        "🔄 易于维护：当数据库 schema 变化时，快速重新生成定义",
        "📚 文档完整：自动包含所有列，确保文档覆盖率",
        "🚀 提高效率：将重复性工作自动化，专注于业务逻辑"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    print()


def main():
    """主函数"""
    print("\n" + "*" * 80)
    print(" " * 20 + "dbt MCP Codegen 工具演示")
    print("*" * 80)
    
    # 打印设置说明
    print_setup_instructions()
    
    # 打印三个场景
    for key in ["scenario_1", "scenario_2", "scenario_3"]:
        print_scenario(key)
    
    # 打印工作流程
    print_workflow()
    
    # 打印示例对话
    create_example_conversation()
    
    # 打印好处
    print_benefits()
    
    print("\n" + "=" * 80)
    print("📚 更多资源")
    print("=" * 80 + "\n")
    print("- dbt-codegen 文档: https://hub.getdbt.com/dbt-labs/codegen/latest/")
    print("- dbt MCP 文档: https://docs.getdbt.com/docs/dbt-ai/about-mcp")
    print("- MCP 协议: https://modelcontextprotocol.io/introduction")
    print()
    
    print("=" * 80)
    print("✅ 演示完成！现在可以在 Cursor 中使用这些工具了。")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

