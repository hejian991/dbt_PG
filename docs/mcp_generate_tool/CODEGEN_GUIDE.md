# dbt MCP Codegen 工具使用指南

本指南详细说明如何使用 dbt-hejian991-remote MCP 的 codegen 工具自动生成 dbt 项目文件。

## 📋 目录

1. [工具概述](#工具概述)
2. [环境设置](#环境设置)
3. [三个核心工具](#三个核心工具)
4. [实际使用示例](#实际使用示例)
5. [最佳实践](#最佳实践)
6. [故障排除](#故障排除)

---

## 工具概述

dbt MCP 提供三个 codegen 工具来自动化生成 dbt 项目文件：

| 工具 | 功能 | 输入 | 输出 |
|------|------|------|------|
| `generate_source` | 从数据库生成 source YAML | Schema 名称、表名 | sources.yml 文件 |
| `generate_model_yaml` | 为模型生成文档 YAML | 模型名称 | schema.yml 文件 |
| `generate_staging_model` | 生成 staging 模型 SQL | Source 名称、表名 | stg_*.sql 文件 |

---

## 环境设置

### 步骤 1: 安装 dbt-codegen 包

已创建 `packages.yml` 文件：

```yaml
packages:
  - package: dbt-labs/codegen
    version: 0.12.1
```

运行安装命令：

```bash
cd /Users/hj/code/test_agent2.0/dbt_pg
dbt deps
```

### 步骤 2: 启用 codegen 工具

**重要**: codegen 工具默认是禁用的，需要设置环境变量启用：

```bash
export DISABLE_DBT_CODEGEN=false
```

或者在 MCP 配置中添加：

```json
{
  "mcpServers": {
    "dbt": {
      "command": "uvx",
      "args": ["dbt-mcp"],
      "env": {
        "DISABLE_DBT_CODEGEN": "false",
        "DBT_ACCOUNT_ID": "your_account_id",
        "DBT_PROJECT_ID": "your_project_id",
        "DBT_TOKEN": "your_token"
      }
    }
  }
}
```

### 步骤 3: 验证 MCP 连接

确保 dbt-hejian991-remote MCP 服务器已正确连接到你的 Cursor。

---

## 三个核心工具

### 1. generate_source - 生成 Source 定义

**用途**: 从数据库 schema 自动生成 source YAML 定义

**使用场景**:
- 添加新的数据源
- 数据库 schema 发生变化需要更新
- 初始化新的 dbt 项目

**对话示例**:

```
用户: 请为 PostgreSQL 数据库中的 'raw' schema 生成 source 定义，
包括 customers、orders 和 payments 表
```

**生成的文件**: `models/staging/sources.yml`

**输出示例**:

```yaml
version: 2

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
            description: ""
            data_type: varchar
          - name: last_name
            description: ""
            data_type: varchar
      
      - name: orders
        description: "Raw order data"
        columns:
          - name: id
            description: ""
            data_type: integer
          - name: user_id
            description: ""
            data_type: integer
          - name: order_date
            description: ""
            data_type: date
          - name: status
            description: ""
            data_type: varchar
      
      - name: payments
        description: "Raw payment data"
        columns:
          - name: id
            description: ""
            data_type: integer
          - name: order_id
            description: ""
            data_type: integer
          - name: payment_method
            description: ""
            data_type: varchar
          - name: amount
            description: ""
            data_type: integer
```

### 2. generate_model_yaml - 生成模型文档

**用途**: 为已存在的 dbt 模型生成完整的 YAML 文档

**使用场景**:
- 为现有模型添加文档
- 更新模型文档（列变化后）
- 确保文档覆盖率

**对话示例**:

```
用户: 请为 'customers' 模型生成完整的 YAML 文档，
包括所有列的数据类型和描述占位符
```

**生成的文件**: `models/schema.yml`

**输出示例**:

```yaml
version: 2

models:
  - name: customers
    description: ""
    columns:
      - name: customer_id
        description: ""
        data_type: integer
        tests:
          - unique
          - not_null
      
      - name: first_name
        description: ""
        data_type: varchar
      
      - name: last_name
        description: ""
        data_type: varchar
      
      - name: first_order_date
        description: ""
        data_type: date
      
      - name: most_recent_order_date
        description: ""
        data_type: date
      
      - name: number_of_orders
        description: ""
        data_type: bigint
      
      - name: total_order_amount
        description: ""
        data_type: numeric
```

**后续步骤**: 填充每个列的具体描述

### 3. generate_staging_model - 生成 Staging 模型

**用途**: 从 source 自动生成 staging 模型的 SQL 代码

**使用场景**:
- 创建新的 staging 层模型
- 快速搭建符合最佳实践的模型结构
- 标准化数据转换模式

**对话示例**:

```
用户: 请从 'raw' source 的 'products' 表生成一个 stg_products staging 模型
```

**生成的文件**: `models/staging/stg_products.sql`

**输出示例**:

```sql
with source as (

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
```

---

## 实际使用示例

### 场景 1: 添加新数据源的完整工作流

**步骤 1**: 生成 source 定义

```
对话: 我需要为 'analytics' schema 生成 source 定义，
包含 user_events 和 session_logs 表
```

AI 会调用 `generate_source` 并创建 `sources.yml`

**步骤 2**: 生成 staging 模型

```
对话: 现在为 user_events 表生成 staging 模型
```

AI 会调用 `generate_staging_model` 并创建 `stg_user_events.sql`

**步骤 3**: 生成文档

```
对话: 为新创建的 stg_user_events 模型生成文档 YAML
```

AI 会调用 `generate_model_yaml` 并更新 `schema.yml`

### 场景 2: 更新现有模型文档

```
对话: 我的 customers 模型增加了几个新列，
请重新生成完整的文档 YAML
```

AI 会重新生成 YAML，包含所有当前列。

### 场景 3: 批量创建 staging 层

```
对话: 我有一个 'raw' source，包含 5 个表：
- users
- orders
- payments
- products
- reviews

请为每个表生成对应的 staging 模型
```

AI 会依次调用 `generate_staging_model` 为每个表生成模型。

---

## 最佳实践

### 1. 按顺序使用工具

推荐工作流程：

```
1. generate_source → 创建 sources.yml
2. generate_staging_model → 创建 stg_*.sql
3. generate_model_yaml → 创建文档
```

### 2. 生成后的必要步骤

生成的代码是模板，需要人工审查和完善：

- ✅ **填充描述**: 为表、列添加有意义的描述
- ✅ **添加测试**: 根据业务规则添加适当的测试
- ✅ **调整类型转换**: 检查数据类型是否需要转换
- ✅ **重命名列**: 确保列名符合命名规范
- ✅ **添加业务逻辑**: 在 staging 层添加必要的数据清洗逻辑

### 3. 命名规范

遵循 dbt 最佳实践：

- Source YAML: `sources.yml` 或 `src_<system>.yml`
- Staging 模型: `stg_<source>_<table>.sql`
- Schema 文件: `schema.yml` 或按层级命名

### 4. 版本控制

生成代码后立即提交到 Git：

```bash
git add models/staging/
git commit -m "feat: add staging models for raw schema"
```

### 5. 文档优先

生成 YAML 后立即填充描述，不要留空：

```yaml
# ❌ 不好
- name: customer_id
  description: ""

# ✅ 好
- name: customer_id
  description: "Unique identifier for customer, sourced from CRM system"
```

---

## 故障排除

### 问题 1: Codegen 工具不可用

**症状**: AI 提示无法找到 codegen 工具

**解决方案**:

1. 检查环境变量:
   ```bash
   echo $DISABLE_DBT_CODEGEN
   # 应该输出: false
   ```

2. 确保已安装 dbt-codegen:
   ```bash
   dbt deps
   ls -la dbt_packages/codegen
   ```

3. 重启 MCP 服务器或 Cursor

### 问题 2: 无法连接到数据库

**症状**: 生成 source 时提示数据库连接失败

**解决方案**:

1. 检查 `profiles.yml` 配置
2. 测试数据库连接:
   ```bash
   dbt debug
   ```

3. 确保有读取 schema 的权限

### 问题 3: 生成的代码格式不正确

**症状**: YAML 格式错误或 SQL 语法问题

**解决方案**:

1. 检查 dbt-codegen 版本:
   ```bash
   cat dbt_packages/codegen/dbt_project.yml
   ```

2. 更新到最新版本:
   ```yaml
   packages:
     - package: dbt-labs/codegen
       version: 0.12.1  # 使用最新版本
   ```

3. 手动调整生成的代码

### 问题 4: MCP 工具调用超时

**症状**: AI 响应很慢或超时

**解决方案**:

1. 检查网络连接
2. 检查 dbt Cloud API 配额
3. 分批处理（一次只生成一个文件）

---

## 直接使用 dbt-codegen（不通过 MCP）

如果不想通过 MCP，可以直接使用 dbt 命令：

### 生成 source

```bash
dbt run-operation generate_source --args '{
  "schema_name": "raw",
  "database_name": "postgres"
}'
```

### 生成 model yaml

```bash
dbt run-operation generate_model_yaml --args '{
  "model_names": ["customers", "orders"]
}'
```

### 生成 base model（staging）

```bash
dbt run-operation generate_base_model --args '{
  "source_name": "raw",
  "table_name": "customers"
}'
```

---

## 总结

dbt MCP codegen 工具可以：

- ⚡️ **提高效率**: 自动化重复性任务
- 📝 **标准化**: 确保代码符合最佳实践
- 🎯 **减少错误**: 避免手动输入错误
- 📚 **完整文档**: 确保所有列都有文档框架

**下一步**:

1. 运行 `dbt deps` 安装 codegen 包
2. 设置 `DISABLE_DBT_CODEGEN=false`
3. 在 Cursor 中尝试上述对话示例
4. 查看生成的代码并完善

---

## 参考资源

- [dbt-codegen 官方文档](https://hub.getdbt.com/dbt-labs/codegen/latest/)
- [dbt MCP 文档](https://docs.getdbt.com/docs/dbt-ai/about-mcp)
- [MCP 协议介绍](https://modelcontextprotocol.io/introduction)
- [dbt 最佳实践](https://docs.getdbt.com/guides/best-practices)

---

**版本**: 1.0  
**最后更新**: 2025-12-12  
**作者**: dbt MCP Team

