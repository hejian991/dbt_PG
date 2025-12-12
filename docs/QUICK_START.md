# dbt_pg 项目快速入门指南

## 🚀 快速开始

### 1. 进入项目目录
```bash
cd /Users/hj/code/test_agent2.0/dbt_pg
```

### 2. 激活虚拟环境
```bash
source venv/bin/activate
```

### 3. 运行常用命令

#### 测试数据库连接
```bash
dbt debug
```

#### 加载种子数据（Seeds）
```bash
dbt seed
```

#### 运行所有模型
```bash
dbt run
```

#### 运行特定模型
```bash
# 只运行 customers 模型
dbt run --select customers

# 运行 staging 目录下的所有模型
dbt run --select staging.*

# 运行 customers 及其上游依赖
dbt run --select +customers
```

#### 执行数据质量测试
```bash
dbt test
```

#### 运行特定测试
```bash
# 只测试 customers 模型
dbt test --select customers

# 只测试 staging 模型
dbt test --select staging.*
```

#### 完整构建（推荐）
```bash
# 按依赖顺序执行：seed → run → test
dbt build
```

### 4. 查询数据

#### 使用 psql 连接数据库
```bash
PGPASSWORD="**********" psql \
  -h ep-delicate-cherry-a1japado-pooler.ap-southeast-1.aws.neon.tech \
  -p 5432 \
  -U neondb_owner \
  -d neondb
```

#### 常用查询示例
```sql
-- 查看所有表
\dt public.*

-- 查看所有视图
\dv public.*

-- 查询客户统计
SELECT 
    customer_id,
    first_name,
    last_name,
    number_of_orders,
    customer_lifetime_value
FROM customers
ORDER BY customer_lifetime_value DESC NULLS LAST
LIMIT 10;

-- 查询订单信息
SELECT 
    order_id,
    customer_id,
    order_date,
    status,
    amount,
    credit_card_amount,
    bank_transfer_amount
FROM orders
WHERE status = 'completed'
ORDER BY amount DESC
LIMIT 10;

-- 统计每种支付方式的使用情况
SELECT 
    COUNT(*) FILTER (WHERE credit_card_amount > 0) as credit_card_count,
    COUNT(*) FILTER (WHERE bank_transfer_amount > 0) as bank_transfer_count,
    COUNT(*) FILTER (WHERE coupon_amount > 0) as coupon_count,
    COUNT(*) FILTER (WHERE gift_card_amount > 0) as gift_card_count
FROM orders;
```

## 📊 项目信息

### 数据模型概览

```
Seeds (原始数据)
├── raw_customers (100 条记录)
├── raw_orders (99 条记录)
└── raw_payments (113 条记录)
         │
         ▼
Staging Models (数据清洗 - 视图)
├── stg_customers
├── stg_orders
└── stg_payments
         │
         ▼
Mart Models (业务模型 - 表)
├── customers (客户维度表 - 100 条记录)
└── orders (订单事实表 - 99 条记录)
```

### 数据质量测试
- ✅ 20 个数据质量测试
- ✅ 包括唯一性、非空、值域和关系测试
- ✅ 所有测试通过

## 🛠️ 高级操作

### 刷新特定数据

#### 重新加载特定 seed
```bash
dbt seed --select raw_customers
```

#### 全量刷新增量模型（如果有）
```bash
dbt run --full-refresh
```

### 生成文档

#### 生成并查看项目文档
```bash
# 生成文档
dbt docs generate

# 启动文档服务器（默认端口 8080）
dbt docs serve
```

### 调试和日志

#### 查看详细日志
```bash
dbt run --debug
```

#### 查看日志文件
```bash
cat logs/dbt.log
```

### 清理操作

#### 清理 target 目录
```bash
dbt clean
```

## 🔧 配置文件说明

### `dbt_project.yml`
- 项目名称和版本
- 模型物化策略配置
- 文档颜色配置

### `profiles.yml`
- PostgreSQL 连接信息
- 线程数配置（默认 4）
- SSL 模式配置

### `models/schema.yml`
- 模型描述和文档
- 列级别说明
- 数据质量测试定义

## 📝 开发工作流

### 1. 开发新模型
```bash
# 1. 在 models/ 目录创建新的 .sql 文件
# 2. 运行模型
dbt run --select your_new_model

# 3. 测试模型
dbt test --select your_new_model

# 4. 查看生成的 SQL
dbt compile --select your_new_model
cat target/compiled/dbt_pg/models/your_new_model.sql
```

### 2. 修改现有模型
```bash
# 1. 修改 .sql 文件
# 2. 重新运行模型
dbt run --select modified_model+

# 3. 运行下游依赖的所有模型
dbt run --select modified_model+
```

### 3. 添加测试
```bash
# 1. 在 schema.yml 中添加测试定义
# 2. 运行测试
dbt test --select your_model
```

## 🚨 常见问题

### Q: 连接数据库失败怎么办？
```bash
# 测试连接
dbt debug

# 检查网络连接
ping ep-delicate-cherry-a1japado-pooler.ap-southeast-1.aws.neon.tech
```

### Q: 如何重置所有数据？
```bash
# 删除所有 dbt 创建的表和视图
# 然后重新构建
dbt build
```

### Q: 模型运行很慢怎么办？
```bash
# 1. 检查查询计划
# 在 PostgreSQL 中使用 EXPLAIN ANALYZE

# 2. 考虑添加索引
# 3. 调整物化策略
# 4. 增加 profiles.yml 中的 threads 数量
```

## 📚 相关资源

- [dbt 官方文档](https://docs.getdbt.com/)
- [dbt PostgreSQL 适配器文档](https://docs.getdbt.com/reference/warehouse-setups/postgres-setup)
- [dbt 最佳实践](https://docs.getdbt.com/guides/best-practices)
- [Neon PostgreSQL 文档](https://neon.tech/docs)

## 🎯 下一步

1. ✅ 探索生成的文档：`dbt docs serve`
2. ✅ 尝试创建自己的模型
3. ✅ 添加更多数据质量测试
4. ✅ 优化模型性能
5. ✅ 设置 CI/CD 流水线

---

**快乐数据建模！** 🎉

