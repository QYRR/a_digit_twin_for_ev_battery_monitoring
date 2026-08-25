# Ch4 Experiments — 中文大纲

## 整体逻辑

```
实验环境交代 → 数据集展开 → 指标回顾 → 基线配置
    ↓
RQ1: 超参搜出来是什么？（超参表）
    ↓
RQ2: 跟BiLSTM比谁准？（SoTA对比表，wlen=20单点）
    ↓
RQ3: 各种窗口长度下全面对比？（部署性能大表 → 本章核心）
    ↓
RQ4: 没见过窗口长度还能不能行？（泛化实验）
    ↓
讨论：数字说明了什么 + 有什么局限
```

---

## Section 4.1: Experimental Setup

### 4.1.1 硬件与软件环境
- 训练环境：PC/服务器，Python + lightgbm==4.5.0 + optuna==4.2.0
- 部署环境：SPC58EC80E5，120 MHz，4 MB Flash，608 KB SRAM
- 编译器：SPC5Studio（GCC Power Architecture, -O2）
- 调试/测量：UDE Starterkit

### 4.1.2 数据集详情
展开 Ch3 的简表，给出两个数据集的统计信息：
- NBD：几颗电池？总共几个放电周期？每周期大约多少行？SoH标签范围（如 2.0 → 1.6 Ah）？
- NRD：28颗18650 LCO，随机充放电，每周期SoH标签范围？
- 训练/验证/测试分割后的样本量（窗口总数）

### 4.1.3 评估指标
简要回顾 Ch3 定义的指标：MAE（FW + Full）、MSE、cycles、Flash%、RAM%

### 4.1.4 BiLSTM 基线配置
- 架构：几层？隐藏单元数？
- 训练：epochs、learning rate、batch size
- 输入：wlen=20（原始论文设定）
- 部署：SPC5Studio AI 转换 → SPC58 上同条件测量
- 说明：用相同数据分割复现，保证公平对比

---

## Section 4.2: Hyperparameter Optimization Results

- 展示 NBD 和 NRD 各自的最优超参数表（paper Table II 的内容）
- 简要分析：NRD 需要更多树/更强正则化 → 数据集更复杂
- 指出部署约束生效：max_depth ≤ 8, num_leaves ≤ 25

---

## Section 4.3: Accuracy Comparison with BiLSTM

- 展示 SoTA 对比表（paper Table III）：wlen=20 下的 MAE(FW) + MAE(Full) + latency + energy
- 分析每一项差异的原因

---

## Section 4.4: Deployment Performance（核心）

- 展示部署性能大表（paper Table IV）：5种窗口长度 × 2个数据集 × 2个模型
- 分维度分析：
  - 精度：LightGBM 在 NRD 上全面领先，NBD 上长窗口领先
  - 延迟：LightGBM cycle count 几乎不变（~75k），BiLSTM 线性增长（838k→2.5M）
  - 内存：LightGBM Flash 2.2-2.7%, RAM 0.49%；BiLSTM Flash 0.21%, RAM 0.13%

---

## Section 4.5: Generalization to Unseen Window Lengths

- 展示泛化结果表（paper Figure 3 的数据，用表格呈现）
- 训练窗口 {20,30,40,50,60} → 测试 {10,35,55,75}
- LightGBM 稳定，BiLSTM 剧烈波动 → 解释原因

---

## Section 4.6: Discussion and Limitations

- 总结发现
- 诚实说明局限

---

## 需确认

1. NBD 和 NRD 的具体统计数字（电池数、周期数、SoH范围、总窗口数）——你有这些数吗？
2. BiLSTM 的具体配置（层数、隐藏单元、epoch、lr、batch size）
3. paper Figure 2（不同窗口长度下的MAE曲线）和 Figure 3（泛化热力图）——你有这些图吗？还是用表格呈现就够了？
4. NRD 的 MAE 数值比 NBD 大两个数量级（~0.02 vs ~2.2），因为标签单位不同（Ah vs 百分比）。这个在写作时需要特别解释一下，避免读者困惑
