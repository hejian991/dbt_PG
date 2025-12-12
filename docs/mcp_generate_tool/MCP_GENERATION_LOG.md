# MCP Codegen 工具实际使用记录

## 生成时间
2025-12-12

## 使用的 MCP 工具
- `mcp_dbt-hejian991_generate_source`
- `mcp_dbt-hejian991_generate_staging_model`

---

## 生成记录 1: raw_customers 表的 staging 模型

### 用户请求
> 请通过 dbt-hejian991 mcp 为 raw_customers 表生成 staging 模型

### 执行步骤

#### 步骤 1: 生成 source 定义

**使用工具**: `generate_source`

**参数**:
```json
{
  "schema_name": "public",
  "table_names": ["raw_customers"],
  "generate_columns": true,
  "include_descriptions": true
}
```

**生成结果**:
```yaml
version: 2

sources:
  - name: public
    description: ""
    tables:
      - name: raw_customers
        description: ""
        columns:
          - name: id
            data_type: integer
            description: ""
          - name: first_name
            data_type: text
            description: ""
          - name: last_name
            data_type: text
            description: ""
```

**保存位置**: `models/staging/sources.yml`

---

#### 步骤 2: 生成 staging 模型

**使用工具**: `generate_staging_model`

**参数**:
```json
{
  "source_name": "public",
  "table_name": "raw_customers"
}
```

**生成结果**:
```sql
with source as (

    select * from {{ source('public', 'raw_customers') }}

),

renamed as (

    select
        id,
        first_name,
        last_name

    from source

)

select * from renamed
```

**保存位置**: `models/staging/stg_customers_from_source.sql`

**优化**: 将 `id` 重命名为 `customer_id` 以符合命名规范

---

### 生成的文件

1. ✅ **models/staging/sources.yml**
   - 定义了 public.raw_customers source
   - 包含 3 个列的定义（id, first_name, last_name）
   - 数据类型：integer, text

2. ✅ **models/staging/stg_customers_from_source.sql**
   - 使用 `{{ source('public', 'raw_customers') }}` 引用
   - 包含 source 和 renamed CTEs
   - 符合 dbt 最佳实践

---

### 工具表现评价

| 工具 | 状态 | 说明 |
|------|------|------|
| generate_source | ✅ 优秀 | 成功识别所有列和数据类型 |
| generate_staging_model | ✅ 优秀 | 生成符合最佳实践的 SQL |

---

### 使用体验

#### 优点
- ⚡️ **快速**: 几秒钟完成代码生成
- 🎯 **准确**: 正确识别表结构和数据类型
- 📝 **标准**: 生成的代码符合 dbt 最佳实践
- 🔄 **自动化**: 无需手动编写重复代码

#### 需要改进的地方
- 📝 **描述为空**: 生成的 description 字段需要手动填充
- 🔤 **列名**: 某些列可能需要重命名（如 id → customer_id）

---

### 后续步骤

完成以下任务以使模型投入使用：

- [x] 生成 source 定义
- [x] 生成 staging 模型
- [x] 优化列名（id → customer_id）
- [ ] 填充所有描述字段
- [ ] 运行模型验证: `dbt run --select stg_customers_from_source`
- [ ] 添加数据测试
- [ ] 提交到版本控制

---

### 测试命令

```bash
# 激活虚拟环境
cd /Users/hj/code/test_agent2.0/dbt_pg
source venv/bin/activate

# 测试 source
dbt run --select source:public.raw_customers

# 运行 staging 模型
dbt run --select stg_customers_from_source

# 验证数据
dbt show --select stg_customers_from_source
```

---

### MCP 工具使用总结

#### 成功因素
1. ✅ 数据库连接正常
2. ✅ dbt-codegen 包已安装
3. ✅ 按照正确顺序使用工具（先 source，后 staging）

#### 技巧提示
- 💡 使用 `generate_columns: true` 获取完整的列定义
- 💡 使用 `include_descriptions: true` 生成描述占位符
- 💡 生成后立即填充描述信息
- 💡 检查并优化列名以符合团队规范

---

## 结论

✅ **成功**: 通过 dbt-hejian991 MCP 成功为 raw_customers 表生成了完整的 staging 模型！

**生成文件**:
- `models/staging/sources.yml`
- `models/staging/stg_customers_from_source.sql`

**工具评价**: ⭐⭐⭐⭐⭐ (5/5)

**推荐使用**: 👍 强烈推荐用于自动化生成 dbt 项目文件

---

**记录人**: AI Assistant  
**MCP 服务器**: dbt-hejian991  
**工具版本**: dbt-codegen 0.12.1  
**状态**: ✅ 完成

---

## 生成记录 2: stg_customers_from_source 模型文档

### 用户请求
> 请使用 generate_model_yaml 工具为 stg_customers_from_source 模型生成文档

### 执行步骤

#### 步骤 1: 生成模型文档

**使用工具**: `generate_model_yaml`

**参数**:
```json
{
  "model_names": ["stg_customers_from_source"],
  "include_data_types": true,
  "upstream_descriptions": false
}
```

**生成结果**:
```yaml
version: 2

models:
  - name: stg_customers_from_source
    description: ""
    columns:
      - name: customer_id
        data_type: integer
        description: ""

      - name: first_name
        data_type: text
        description: ""

      - name: last_name
        data_type: text
        description: ""
```

**处理**: 添加到 `models/staging/schema.yml` 并填充描述

---

#### 步骤 2: 优化并添加测试

**优化内容**:
- ✅ 添加模型描述："Staging table for customer data sourced from public.raw_customers"
- ✅ 填充列描述
- ✅ 添加数据质量测试（unique, not_null）

**最终结果**:
```yaml
- name: stg_customers_from_source
  description: "Staging table for customer data sourced from public.raw_customers"
  columns:
    - name: customer_id
      data_type: integer
      description: "Unique identifier for each customer (renamed from id)"
      tests:
        - unique
        - not_null

    - name: first_name
      data_type: text
      description: "Customer's first name"

    - name: last_name
      data_type: text
      description: "Customer's last name"
```

---

### 工具表现评价

| 工具 | 状态 | 说明 |
|------|------|------|
| generate_model_yaml | ✅ 优秀 | 成功识别所有列和数据类型 |

---

### 完整工作流总结

至此，我们已经完成了 MCP codegen 工具的**完整工作流**：

1. ✅ **generate_source** → 生成 source 定义 (_sources.yml)
2. ✅ **generate_staging_model** → 生成 staging 模型 (stg_customers_from_source.sql)
3. ✅ **generate_model_yaml** → 生成模型文档 (schema.yml)

这展示了如何使用 MCP 工具快速搭建一个完整的、符合最佳实践的 dbt staging 层！

---

**更新时间**: 2025-12-12 15:30  
**工作流状态**: ✅ 完整演示完成

