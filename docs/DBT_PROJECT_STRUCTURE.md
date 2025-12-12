# dbt 项目目录结构最佳实践

## 📌 快速答案

**`sources.yml` 放在 `models/staging/` 目录是完全正确的！** ✅

推荐命名为 `_sources.yml`（下划线开头），这样文件会排在目录最前面。

---

## 🏗️ 标准 dbt 项目结构

### 完整结构示例

```
my_dbt_project/
│
├── 📋 项目配置文件
├── dbt_project.yml           # dbt 项目配置
├── profiles.yml              # 数据库连接（本地，不提交）
├── packages.yml              # 依赖包管理
├── .gitignore
└── README.md
│
├── 📁 models/                # ⭐ 核心：所有 dbt 模型
│   │
│   ├── 🔷 staging/           # 第一层：原始数据清洗
│   │   │
│   │   ├── _sources.yml      # ⭐ Source 定义（推荐命名）
│   │   ├── _staging.yml      # Staging 模型文档（可选）
│   │   │
│   │   ├── stg_customers.sql
│   │   ├── stg_orders.sql
│   │   └── stg_payments.sql
│   │
│   ├── 🔶 intermediate/      # 第二层：业务逻辑转换（可选）
│   │   ├── _intermediate.yml
│   │   ├── int_customer_orders.sql
│   │   └── int_order_totals.sql
│   │
│   ├── 🔴 marts/             # 第三层：业务层/最终表
│   │   │
│   │   ├── core/             # 核心业务实体
│   │   │   ├── _core__models.yml
│   │   │   ├── dim_customers.sql      # 维度表
│   │   │   ├── dim_products.sql
│   │   │   └── fct_orders.sql         # 事实表
│   │   │
│   │   ├── finance/          # 财务部门 mart
│   │   │   ├── _finance__models.yml
│   │   │   ├── fct_revenue.sql
│   │   │   └── rpt_monthly_revenue.sql
│   │   │
│   │   └── marketing/        # 营销部门 mart
│   │       ├── _marketing__models.yml
│   │       └── fct_campaigns.sql
│   │
│   └── docs.md               # 全局文档（Markdown）
│
├── 📁 analyses/              # 临时分析查询（不构建模型）
│   └── customer_cohort_analysis.sql
│
├── 📁 tests/                 # 自定义数据测试
│   ├── assert_positive_total.sql
│   └── assert_valid_customer_ids.sql
│
├── 📁 seeds/                 # 静态参考数据（CSV）
│   ├── country_codes.csv
│   └── payment_methods.csv
│
├── 📁 snapshots/             # 慢变维度（SCD Type 2）
│   └── customers_snapshot.sql
│
├── 📁 macros/                # 可重用的 SQL 宏
│   ├── cents_to_dollars.sql
│   └── custom_tests.sql
│
└── 📁 target/                # 编译输出（不提交到 Git）
    ├── compiled/
    ├── run/
    └── manifest.json
```

---

## 📝 文件命名约定

### YAML 配置文件

```yaml
# ✅ 推荐：下划线开头
_sources.yml                    # Source 定义
_<layer>__models.yml            # 模型文档
_staging.yml
_core__models.yml

# ⚠️ 也可以但不推荐
sources.yml
schema.yml                      # 太通用
models.yml
```

**为什么用下划线？**
- 📌 在文件列表中排在最前面
- 🔍 容易识别为配置文件
- 📚 dbt Labs 官方推荐

### SQL 模型文件

```sql
-- Staging 层（1:1 映射 source）
stg_<source>__<table>.sql
stg_stripe__customers.sql
stg_salesforce__accounts.sql

-- Intermediate 层（业务逻辑）
int_<description>.sql
int_customer_orders_joined.sql
int_payments_pivoted.sql

-- Marts 层
-- Fact 表（事实表）
fct_<entity>.sql
fct_orders.sql
fct_revenue.sql

-- Dimension 表（维度表）
dim_<entity>.sql
dim_customers.sql
dim_products.sql

-- Report 层（报表）
rpt_<report_name>.sql
rpt_monthly_revenue.sql
```

---

## 🎯 按项目规模的建议

### 小型项目（< 50 个模型）

```
models/
├── staging/
│   ├── _sources.yml          # 所有 source 在一个文件
│   ├── _staging.yml
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   └── stg_payments.sql
│
└── marts/
    ├── _marts.yml
    ├── customers.sql
    └── orders.sql
```

**特点**：
- ✅ 简单直接
- ✅ 易于导航
- ✅ 适合单一数据源

---

### 中型项目（50-200 个模型）

```
models/
├── staging/
│   ├── stripe/               # 按源系统分组
│   │   ├── _stripe__sources.yml
│   │   ├── _stripe__models.yml
│   │   ├── stg_stripe__customers.sql
│   │   └── stg_stripe__payments.sql
│   │
│   └── salesforce/
│       ├── _salesforce__sources.yml
│       ├── _salesforce__models.yml
│       └── stg_salesforce__accounts.sql
│
├── intermediate/
│   └── int_customer_orders.sql
│
└── marts/
    ├── core/
    │   ├── _core__models.yml
    │   ├── dim_customers.sql
    │   └── fct_orders.sql
    │
    └── finance/
        ├── _finance__models.yml
        └── fct_revenue.sql
```

**特点**：
- ✅ 按源系统组织 staging
- ✅ 按业务领域组织 marts
- ✅ 引入 intermediate 层

---

### 大型项目（> 200 个模型）

```
models/
├── staging/
│   ├── stripe/
│   │   ├── base/             # 更细粒度分层
│   │   │   └── base_stripe__customers.sql
│   │   ├── _stripe__sources.yml
│   │   └── stg_stripe__customers.sql
│   │
│   └── salesforce/
│       ├── core_objects/
│       ├── custom_objects/
│       └── _salesforce__sources.yml
│
├── intermediate/
│   ├── customer/             # 按实体分组
│   │   ├── int_customer_orders.sql
│   │   └── int_customer_lifetime_value.sql
│   │
│   └── finance/
│       └── int_revenue_calculations.sql
│
└── marts/
    ├── core/
    │   ├── dimensions/
    │   │   ├── dim_customers.sql
    │   │   └── dim_products.sql
    │   │
    │   └── facts/
    │       ├── fct_orders.sql
    │       └── fct_order_items.sql
    │
    ├── finance/
    │   ├── metrics/
    │   └── reports/
    │
    └── marketing/
```

**特点**：
- ✅ 更深的目录层次
- ✅ 按实体和领域细分
- ✅ 分离 dimensions 和 facts

---

## 🎓 sources.yml 位置详解

### ✅ 推荐位置 1：与 staging 模型在同一目录

```
models/staging/
├── _sources.yml              ⭐ 最推荐
├── stg_customers.sql
└── stg_orders.sql
```

**优点**：
- 就近原则
- staging 层负责处理 source
- 易于查找和维护

---

### ✅ 推荐位置 2：按源系统分组

```
models/staging/
├── stripe/
│   ├── _stripe__sources.yml  ⭐ 多数据源推荐
│   ├── stg_stripe__customers.sql
│   └── stg_stripe__payments.sql
│
└── salesforce/
    ├── _salesforce__sources.yml
    └── stg_salesforce__accounts.sql
```

**优点**：
- 清晰的源系统边界
- 适合多数据源项目
- 每个团队可以独立维护自己的源

---

### ❌ 不推荐：单独的 sources 目录

```
models/
├── sources/                  # ❌ 不推荐
│   └── sources.yml
│
└── staging/
    ├── stg_customers.sql
    └── stg_orders.sql
```

**缺点**：
- 与使用 source 的模型分离
- 不符合 dbt 社区最佳实践
- 维护时需要跨目录查找

---

## 💡 实际案例：你的项目

### 当前结构
```
models/
├── staging/
│   ├── sources.yml           # 已重命名为 _sources.yml ✅
│   ├── schema.yml
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   └── stg_payments.sql
│
├── customers.sql
├── orders.sql
└── schema.yml
```

### 推荐优化后的结构

```
models/
│
├── staging/
│   ├── _sources.yml          # ✅ 已完成
│   ├── _staging.yml          # 重命名 schema.yml
│   ├── stg_customers.sql
│   ├── stg_orders.sql
│   ├── stg_payments.sql
│   └── stg_customers_from_source.sql  # 新生成的
│
├── marts/                    # 创建 marts 目录
│   ├── core/
│   │   ├── _core__models.yml # 移动原来的 schema.yml
│   │   ├── dim_customers.sql # 重命名 customers.sql
│   │   └── fct_orders.sql    # 重命名 orders.sql
│   │
│   └── _marts.yml
│
└── docs.md
```

---

## 🔄 三层架构详解

### Layer 1: Staging（原始层）
**目的**：1:1 映射 source 表，轻度清洗

```sql
-- stg_customers.sql
select
    id as customer_id,
    lower(email) as email,
    created_at
from {{ source('public', 'raw_customers') }}
```

**特点**：
- 列重命名
- 类型转换
- 基本清洗
- 不做业务逻辑

---

### Layer 2: Intermediate（中间层，可选）
**目的**：复杂的业务逻辑转换

```sql
-- int_customer_orders.sql
select
    c.customer_id,
    c.email,
    count(o.order_id) as order_count,
    sum(o.amount) as total_spent
from {{ ref('stg_customers') }} c
left join {{ ref('stg_orders') }} o
    on c.customer_id = o.customer_id
group by 1, 2
```

**特点**：
- 复杂 join
- 聚合计算
- 业务规则
- 不对外暴露

---

### Layer 3: Marts（业务层）
**目的**：最终的、对业务友好的表

```sql
-- dim_customers.sql
select
    customer_id,
    email,
    first_order_date,
    order_count,
    total_lifetime_value,
    customer_segment
from {{ ref('int_customer_orders') }}
```

**特点**：
- 对业务用户友好
- 完整的文档
- 数据测试
- BI 工具直接使用

---

## ✅ 检查清单

使用这个清单检查你的项目结构：

- [x] sources.yml 在 staging 目录 ✅
- [ ] YAML 文件使用下划线开头
- [ ] staging 模型命名为 `stg_<source>__<table>`
- [ ] marts 按业务领域组织
- [ ] 每个目录有自己的 schema.yml
- [ ] 使用 docs.md 添加文档
- [ ] .gitignore 包含 target/ 和 logs/

---

## 📚 参考资源

- [dbt 官方最佳实践](https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview)
- [dbt 风格指南](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md)
- [Discourse 社区讨论](https://discourse.getdbt.com/)

---

**总结**：你的 `sources.yml` 位置完全正确！建议重命名为 `_sources.yml` 以符合最佳实践。✅

