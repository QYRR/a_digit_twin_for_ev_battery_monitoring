# Ch3 Methodology — 中文大纲

## 整体逻辑链

```
拿到原始电池数据 → 按5种窗口长度分割 → 每窗口提10维特征
    ↓
用特征训练LightGBM → Bayesian搜索最佳超参
    ↓
训练好的模型 → EDEN编译为C数组 → SPC5Studio集成 → UDE烧录调试
    ↓
SPC58上跑推理 → 测MAE/MSE/cycles/RAM/Flash
    ↓
OTA设计：SoH漂移触发 → 云重训SoC → 安全下发 → A/B替换
```

---

## Section 0: Overview（框架总览，约1页）

- 重申本论文在双模型架构中的位置：聚焦SoH基础层
- 展示五阶段流水线图（已有 ch3_ml_workflow.png）
- 展示云边协同架构图（已有 ch3_project_architecture.png）
- 列出五个阶段 + OTA设计的对应小节

**注意**：当前overview内容多处写"SoC"、说OTA"已实现"——需要全部修正为SoH + OTA设计

---

## Section 1: Data Acquisition and Preprocessing（数据获取与预处理）

### 1.1 数据来源
- 两个NASA数据集（NBD + NRD）→ 表格总结
- 数据格式：电压、电流、温度、时间戳、SoH标签
- 说明为什么选这两个：公开、广泛引用、与BiLSTM基线同一数据源

### 1.2 数据预处理
- 按放电周期分组
- 去噪/归一化（如果有的话）
- 划分训练/验证/测试集（交叉验证？还是固定分割？）

---

## Section 2: Multi-Length Segmentation（多长度窗口分割）

- 为什么：电池老化后窗口特性变，固定窗口模型不行
- 怎么做：wlen ∈ {20, 30, 40, 50, 60}，无重叠滑动
- 已有图 ch3_window_segementation.png
- 为什么这5个值：文献常用，覆盖短到长

---

## Section 3: Feature Extraction（特征提取）

- 从每个窗口提取10维特征向量
- 中间计算量：dV, dT, P, Q, dV/dQ
- 最终特征表：
  1. mean discharge voltage rate
  2. mean voltage
  3. mean discharge temperature rate
  4. mean power
  5. mean timestamp
  6–8. mean/max/min of dV/dQ
  9. window duration
  10. mean temperature
- 为什么这样设计：参考文献 feature_eng，捕获电化学退化信号

---

## Section 4: Model Training and Hyperparameter Search（模型训练与超参搜索）

### 4.1 为什么选 LightGBM
- Ch2 已论证，这里一句话回顾 + 引用

### 4.2 超参数搜索
- Optuna Bayesian search
- 搜索空间表（LR, Max Depth, #Leaves, #Estimators, α/β, MCS, CST）
- 目标：最小化验证集 MAE
- 约束：Max Depth ≤ 8, #Leaves ≤ 25（控制模型大小，确保能部署）

### 4.3 训练策略
- 5种窗口长度混合训练（同一个模型）
- Label：对NBD是整周期容量，对NRD是每窗口SoH值
- 训练/验证/测试分割方式

---

## Section 5: Model Compilation（模型编译：EDEN → C）

- EDEN编译器扩展支持LightGBM（由合作者完成）
- 四数组结构：split thresholds / feature indices / right child indices / root indices
- 前序遍历 + 隐式左子节点
- 推理伪代码
- 生成自包含 .c 文件，零外部依赖

---

## Section 6: MCU Deployment（MCU部署）

- 目标硬件：SPC58EC80E5
- 工具链：SPC5Studio（编译+烧录）+ UDE Starterkit（运行+调试）
- 特征提取C语言手写实现
- 模型数组集成到固件工程
- 串口输入测试数据 → 推理 → 串口输出结果
- 与完整BMS套件的关系（SPC58单板 vs 全系统）

---

## Section 7: Performance Verification（性能验证方法）

- 四个维度：
  1. 估计精度：MAE、MSE（FW + Full）
  2. 推理延迟：CPU cycles + 换算 ms
  3. 内存：Flash%（模型参数+代码）、RAM%（运行时缓冲）
  4. 泛化能力：未见窗口长度下的MAE
- 测量工具：SPC5Studio linker map + UDE cycle counter
- BiLSTM基线：相同硬件、相同数据分割、复现测量

---

## Section 8: OTA Update Architecture Design（OTA更新架构设计）

- 定位：设计层面，未在硬件上实现
- 服务对象：SoC模型（不是SoH）
- 触发条件：SoH下降 > 阈值（如1%）或超时
- 流程：数据累积 → 上传 → 云重训SoC → 安全下发 → A/B替换 → 回滚
- 安全：签名验证、版本号、A/B分区
- 容错：Golden Model 出厂固化
- 与整车FOTA的关系

---

## 已确认

1. ~~归一化~~ → MinMaxScaler，可选
2. ~~数据分割~~ → 按放电周期分组后随机分割训练/验证/测试，NBD和NRD相同
3. ~~特征提取C实现~~ → 手写，无定点优化，MCU有FPU直接做浮点
4. ~~NRD label~~ → NBD和NRD一样：同一放电周期的所有窗口共享同一个SoH标签（容量值）
5. ~~性能测量~~ → 单次测量值，未取平均（多次差别不大）
