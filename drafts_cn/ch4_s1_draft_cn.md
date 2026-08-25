# Ch4 Section 4.1 — 实验设置（完整中文版）

---

## 正文

### 4.1.1 硬件与软件环境

实验在两个不同的计算环境中进行：

**训练环境**：模型训练和超参数搜索在一台配备 [TODO: CPU/GPU型号和内存] 的工作站上完成。软件栈基于 Python，核心依赖为 lightgbm==4.5.0 和 optuna==4.2.0。完整依赖清单见附录 [ref:appendix]。

**部署与性能测量环境**：目标硬件为 STMicroelectronics SPC58EC80E5 汽车微控制器（双核 Power Architecture e200z420n3 @ 120 MHz，4 MB Flash，608 KB SRAM）。代码编译使用 SPC5Studio IDE 集成的 GCC Power Architecture 交叉编译器，优化级别 -O2。程序的运行、调试和周期计数通过 UDE Starterkit 进行。Flash 和 RAM 占用数据从 SPC5Studio 链接器生成的 map 文件中提取。

MCU 上的推理性能测量使用随机生成的窗口数据——周期数仅取决于窗口长度和模型结构，与数据具体数值无关。模型精度（MAE/MSE）在 Python 训练环境中使用测试集评估——MCU 推理输出已在一对一比对中验证与 Python 输出完全一致，无需逐窗口在硬件上复测精度。

### 4.1.2 数据集

本实验使用两个公开的 NASA 锂离子电池数据集，基本信息如 Ch3 表 3.1 所述。以下补充统计细节。

**NASA Battery Dataset (NBD)**：包含 [TODO: N颗电池] 18650 锂离子电池在室温下的充放电循环数据。采样率约 0.09 Hz（约每 11 秒一个采样点）。[TODO: 总共X个放电周期，每周期Y±Z行]。SoH 标签为每周期实测放电容量，范围约为 [TODO: min-max] Ah。按 64/16/20 比例分割后，训练集约 [TODO] 个窗口，验证集约 [TODO] 个，测试集约 [TODO] 个（5种窗口长度合计）。

**NASA Randomized Battery Usage Dataset (NRD)**：包含 28 颗 18650 LCO 电池在随机化充放电条件下的数据。随机化意味着放电不一定从满电开始、电流曲线不规则、更接近真实驾驶场景。采样率约 0.33 Hz（约每 3 秒一个采样点）。[TODO: 总共X个放电周期，每周期Y±Z行]。SoH 标签为每周期 SoH 值，范围约为 [TODO: min-max]%。分割时确保测试集中的电池（[TODO: N颗]）不出现在训练或验证集中。分割后训练集约 [TODO] 个窗口，验证集约 [TODO] 个，测试集约 [TODO] 个。

**两个数据集的标签单位说明**：NBD 的 SoH 标签单位为 Ah（容量），NRD 为百分比。这导致两个数据集上的 MAE 数值量级不同（NBD 约 0.01–0.04，NRD 约 1.7–4.8）——这不是模型在 NRD 上表现差了 100 倍，而是标签尺度不同。为便于跨数据集比较，可在归一化尺度上额外报告 MAE。

### 4.1.3 评估指标

以下指标在 Ch3 Section 3.7 中已被定义，此处简要回顾：

- **MAE（Mean Absolute Error）**：预测值与真值之间绝对差的均值。主指标。
- **MSE（Mean Squared Error）**：预测值与真值之间平方差的均值。惩罚大偏差，辅助指标。
- **FW（First Window）**：仅取每个放电周期的第一个窗口计算 MAE。对标 Sammartino 等人 [Sammartino2021] 的评估协议。与 BiLSTM 对比时使用 wlen=20（基线固定长度）。
- **Full**：测试集全部窗口。
- **Inference cycles**：从特征提取开始到模型推理结束的 CPU 时钟周期数，通过 UDE 周期计数器测量。
- **Flash / RAM**：链接器 map 文件报告的静态存储占用。

### 4.1.4 BiLSTM 基线

为公平评估 LightGBM 方案的性能，本实验复现了 Sammartino 等人的 BiLSTM 基线 [Sammartino2021]。该基线是目前少数完整覆盖"训练→MCU 部署"全流程的 SoH 估计工作，且部署于同系列 SPC58 MCU 上。

BiLSTM 的 [TODO: 具体配置——从项目文件中查找]：
- 层数：[TODO]
- 隐藏单元数：[TODO]
- 训练配置：epochs=[TODO], learning rate=[TODO], batch size=[TODO]
- 输入窗口长度：wlen=20（固定，原始论文设定）
- MCU 推理：通过 SPC5Studio AI 组件将 Keras 模型转换为 C 代码

本实验使用与 LightGBM 完全相同的数据分割和评估协议训练 BiLSTM，在与 LightGBM 相同的 SPC58 硬件上测量其推理性能，确保对比的公平性。

对于多窗口长度部署实验（Section 4.4），为每个窗口长度 wlen ∈ {20, 30, 40, 50, 60} 分别训练一个 BiLSTM 模型（因为 BiLSTM 输入维度固定）。对于未见窗口长度泛化实验（Section 4.5），对每个 BiLSTM 模型使用 [TODO: 截断策略——待确认代码] 来适配与训练长度不同的测试窗口。
