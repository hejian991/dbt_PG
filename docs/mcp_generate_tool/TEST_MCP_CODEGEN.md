# dbt MCP Codegen 工具实际测试

## 测试环境状态

✅ **已完成的设置**:
- dbt-codegen 包已安装 (v0.12.1)
- packages.yml 已配置
- dbt 项目结构完整
- 虚拟环境已配置

⚠️ **需要配置**:
- 设置环境变量 `DISABLE_DBT_CODEGEN=false` 以启用 MCP codegen 工具
- 确保 MCP 服务器配置正确

---

## 测试场景

### 测试 1: 使用 MCP 为 customers 模型生成文档

**目标**: 通过 AI 对话自动生成 customers 模型的完整 YAML 文档

**对话提示**:
```
请使用 generate_model_yaml 工具为 'customers' 模型生成完整的 YAML 文档，
包括所有列的数据类型和描述占位符。
```

**预期结果**:
- AI 调用 MCP 的 `generate_model_yaml` 工具
- 返回包含所有列定义的 YAML
- 包括 customer_id, first_name, last_name 等所有字段

**验证方法**:
```bash
# 检查生成的文件
cat models/schema.yml
```

---

### 测试 2: 使用 MCP 生成新的 staging 模型

**目标**: 为一个假设的新数据源生成 staging 模型

**前提**: 假设我们有一个 'raw' source，包含 'products' 表

**对话提示**:
```
假设我们有一个 'raw' source 包含 'products' 表，
表结构包含 id, name, category, price 列。
请使用 generate_staging_model 工具生成 stg_products.sql 模型。
```

**预期结果**:
- AI 调用 MCP 的 `generate_staging_model` 工具
- 返回符合 dbt 最佳实践的 SQL 代码
- 包含 source CTE 和 renamed CTE

**验证方法**:
```bash
# 检查生成的文件
cat models/staging/stg_products.sql
```

---

### 测试 3: 使用 MCP 生成 source 定义

**目标**: 从数据库 schema 生成 source YAML 定义

**对话提示**:
```
请使用 generate_source 工具为 'public' schema 生成 source 定义，
包括 raw_customers, raw_orders, raw_payments 三个表。
```

**预期结果**:
- AI 调用 MCP 的 `generate_source` 工具
- 返回完整的 sources.yml 内容
- 包含所有表和列的定义

**验证方法**:
```bash
# 检查生成的文件
cat models/staging/sources.yml
```

---

## 实际测试脚本

我已经创建了以下文件来帮助测试：

### 1. `test_codegen.py`
展示三个 codegen 工具的功能和预期输出

运行方法:
```bash
cd /Users/hj/code/test_agent2.0/dbt_pg
python3 test_codegen.py
```

### 2. `codegen_demo.py`
提供详细的场景演示和使用说明

运行方法:
```bash
cd /Users/hj/code/test_agent2.0/dbt_pg
python3 codegen_demo.py
```

### 3. `CODEGEN_GUIDE.md`
完整的使用指南文档

查看方法:
```bash
cat CODEGEN_GUIDE.md
```

---

## 通过 AI 对话测试（推荐方式）

现在你可以在 Cursor 中直接对我说以下内容来测试 MCP codegen 工具：

### 测试命令 1: 生成模型文档
```
请帮我为 customers 模型生成完整的 YAML 文档，使用 generate_model_yaml 工具。
```

### 测试命令 2: 生成 staging 模型
```
请帮我为 stg_orders 模型重新生成 SQL 代码，使用 generate_staging_model 工具。
```

### 测试命令 3: 生成 source 定义
```
请帮我为当前项目的 seed 数据生成 source 定义，使用 generate_source 工具。
```

---

## 验证 MCP 工具可用性

要检查 MCP codegen 工具是否可用，可以通过以下方式：

### 方法 1: 询问 AI
```
当前 dbt MCP 服务器上有哪些 codegen 工具可用？
请列出 generate_source、generate_model_yaml 和 generate_staging_model 的状态。
```

### 方法 2: 检查环境变量
```bash
# 在终端中检查
echo $DISABLE_DBT_CODEGEN
# 应该输出: false（表示工具已启用）
```

### 方法 3: 查看 MCP 配置
检查 Cursor 的 MCP 配置文件中是否包含：
```json
{
  "mcpServers": {
    "dbt-hejian991-remote": {
      "url": "https://...",
      "env": {
        "DISABLE_DBT_CODEGEN": "false"
      }
    }
  }
}
```

---

## 测试结果记录

### 测试 1: generate_model_yaml
- [ ] MCP 工具调用成功
- [ ] 返回了完整的 YAML
- [ ] 包含所有列定义
- [ ] 数据类型正确
- [ ] 格式符合 dbt 规范

**实际输出**:
```
（在此记录实际测试时的输出）
```

---

### 测试 2: generate_staging_model
- [ ] MCP 工具调用成功
- [ ] 生成了 SQL 代码
- [ ] 包含 source CTE
- [ ] 包含 renamed CTE
- [ ] 符合最佳实践

**实际输出**:
```
（在此记录实际测试时的输出）
```

---

### 测试 3: generate_source
- [ ] MCP 工具调用成功
- [ ] 返回了 sources.yml
- [ ] 包含所有表
- [ ] 列定义完整
- [ ] 格式正确

**实际输出**:
```
（在此记录实际测试时的输出）
```

---

## 故障排除

### 问题 1: "Codegen 工具不可用"

如果 AI 提示找不到 codegen 工具，请检查：

1. **环境变量设置**
   ```bash
   export DISABLE_DBT_CODEGEN=false
   ```

2. **MCP 服务器配置**
   确保在 MCP 配置中添加了环境变量

3. **dbt-codegen 包安装**
   ```bash
   cd /Users/hj/code/test_agent2.0/dbt_pg
   source venv/bin/activate
   dbt deps
   ls -la dbt_packages/codegen
   ```

4. **重启 MCP 服务器**
   重启 Cursor 以重新加载 MCP 配置

### 问题 2: "工具调用超时"

可能的原因：
- 网络连接问题
- dbt Cloud API 配额限制
- 数据库连接问题

解决方法：
- 检查网络连接
- 检查 API token 是否有效
- 分批处理，一次只生成一个文件

### 问题 3: "生成的代码格式错误"

解决方法：
- 更新 dbt-codegen 到最新版本 (0.14.0)
- 手动调整生成的代码
- 检查 dbt 版本兼容性

---

## 下一步行动

1. ✅ **安装完成**: dbt-codegen 包已安装
2. ⚠️ **配置环境**: 设置 `DISABLE_DBT_CODEGEN=false`
3. ⏳ **测试工具**: 尝试上述三个测试场景
4. ⏳ **验证结果**: 检查生成的文件是否正确
5. ⏳ **实际应用**: 在真实项目中使用这些工具

---

## 总结

本测试演示了如何：

1. ✅ 安装和配置 dbt-codegen 包
2. ✅ 创建测试脚本和文档
3. ⏳ 通过 MCP 使用 codegen 工具（待测试）
4. ⏳ 验证生成的代码质量（待测试）

**测试状态**: 环境已准备就绪，可以开始实际测试

**建议**: 现在直接在 Cursor 对话中使用上述测试命令，让 AI 调用 MCP codegen 工具来生成实际代码。

---

**文档版本**: 1.0  
**创建日期**: 2025-12-12  
**测试环境**: macOS, dbt 1.10.15, dbt-codegen 0.12.1

