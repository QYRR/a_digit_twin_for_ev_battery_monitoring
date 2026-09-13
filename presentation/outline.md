# Defense Slides Outline — A Digital Twin for EV Battery Monitoring

> 答辩 PPT 大纲 v2（裁剪版）· Chao Song · Politecnico di Torino · MSc Computer Engineering
>
> 约定：**页面内容**（英文，将直接上屏）；**讲稿要点**（英文，排练用）；**备注**（中文，指导用，不上屏）。
> 假设：陈述 **15 分钟**、语言 **英语**（最终以 Prof. Vinco 确认为准）。
> v2 变更：删除原 #3（Why SoH is hard，并入 #2）与原 #16（OTA security，压缩并入 #14），主线 19 → 17 页。
>
> **成品**：`slides.tex` → `slides.pdf`（Beamer，25 页 = 17 主线 + 8 backup；编译：`pdflatex slides.tex` 跑两遍，或 `latexmk -pdf slides.tex`）。逐页讲稿已作为 `\note{}` 内嵌，演讲者可开第二屏显示。字体为 Century Gothic 的 TeX 替代 TeX Gyre Adventor。

---

## 0. 待确认清单（做稿前问导师）

- [ ] 陈述时长（本文按 15 min 排）与问答环节时长
- [ ] 答辩语言（论文为英文，默认英语）
- [ ] 委员会组成（是否另有 co-relatore / 外请委员）
- [ ] 是否要求使用学校官方模板（PoliTo 有 Beamer 模板；PowerPoint 通常可接受）
- [ ] 答辩日期（标题页用）

## 1. 时间预算总览

| # | 标题 | 时间 | 类型 |
|---|---|---|---|
| 1 | Title | 0:10 | 开场 |
| 2 | Motivation & SoH | 0:50 | 动机 |
| 3 | Problem: four barriers | 1:10 | 问题 |
| 4 | Digital Twin vision & the gap | 1:00 | 问题 |
| 5 | Aims & contributions | 0:45 | 定位 |
| 6 | Method overview: five-stage pipeline | 0:45 | 方法 |
| 7 | Multi-length segmentation | 1:15 | 方法 |
| 8 | Feature extraction: the 10-D vector | 1:15 | 方法 |
| 9 | From Python to MCU | 1:00 | 方法 |
| 10 | Experimental setup | 0:45 | 实验 |
| 11 | Accuracy vs BiLSTM | 1:15 | 结果 |
| 12 | Efficiency & memory footprint | 1:10 | 结果 |
| 13 | Generalization to unseen window lengths | 1:15 | 结果 |
| 14 | OTA update architecture | 1:00 | OTA |
| 15 | Conclusions | 0:45 | 收尾 |
| 16 | Future work | 0:30 | 收尾 |
| 17 | Thanks / Q&A | — | 收尾 |

- 总计 ≈ **14:50**（含标题页），留约 10 秒缓冲。
- 排练若超时：先压缩 #3 的口头展开与 #14 的八步叙述；**不动结果页 #11–13**。

---

## 2. 逐页大纲

### Slide 1 — Title（0:10）

- **页面内容**
  - *A Digital Twin for EV Battery Monitoring*
  - 副标题（可选）：*Lightweight SoH Estimation on an Automotive Microcontroller*
  - Candidate: Chao Song
  - Supervisors: Prof. Sara Vinco, Dr. Khaled Sidahmed Sidahmed Alamin
  - Politecnico di Torino — MSc in Computer Engineering
- **素材**：`images/logo/logoPoliTo_symbol_only`（论文同款校徽）
- **讲稿要点**
  - "Good morning. My thesis brings SoH estimation for EV batteries onto the vehicle's own microcontroller. In the next 15 minutes I'll show why that is hard, what I built, and how it performed on real hardware."
- **备注**：开场一句就是电梯演讲的核心——问题、方法、结果一句话全给，不念标题。

### Slide 2 — Motivation & SoH（0:50）

- **核心信息**：EV 爆发让电池监测成为关键问题；而 SoH 最难——没有传感器，只能推断
- **页面内容**
  - Global EV sales: 3M (2020) → 16.6M (2024), CAGR ≈ 53% (IEA)
  - BMS 追踪两个状态：**SoC**（分钟–小时）vs **SoH**（月–年）
  - SoH = C_current / C_initial × 100%；< 70–80% 即寿命终点
  - No sensor for it — must be **inferred**；aging: nonlinear · coupled · path-dependent
- **素材**：`images/ch1_EV_sales.png`（论文 Fig. 1.1，直接复用）
- **讲稿要点**
  - "Every one of these vehicles carries a battery pack whose health determines safety, range, and cost. The BMS must know that health in real time. SoH — the fraction of original capacity left — has no sensor; it must be inferred, and aging is nonlinear, coupled, and path-dependent. That is the problem this thesis attacks."
- **备注**：本页密度略高——公式与"三词"一行带过，重音放在"必须推断"上。

### Slide 3 — Problem: four barriers（1:10）

- **核心信息**：从学术模型到车上真正运行的 SoH 估计器，中间隔了四道坎
- **页面内容**（建议做成垂直阶梯/漏斗图，见待生成图表 ①）
  1. **Model-based hits a wall** — P2D too heavy for an MCU；ECM+Kalman 随电池老化参数漂移
  2. **Data-driven stops at simulation** — ML 精度高（MAE < 2%）但几乎都停在 Python 离线验证
  3. **Cloud vs edge: neither is free** — 云端延迟/带宽/隐私不可接受；边缘 MCU 资源少约 5 个数量级
  4. **SoC–SoH coupling** — SoC 需要当前 SoH；SoH 过期 → SoC 系统性偏差
- **素材**：待生成图表 ①（问题阶梯图）；无图则用四行文字分层
- **讲稿要点**
  - "The gap between the literature and a working on-board estimator is four layers deep. Physics models are too heavy or drift. ML models never leave the server. The cloud can't be trusted with a safety-critical loop, and the edge has almost no resources. And even if you solve all that — SoC estimation needs the current SoH, so SoH is where everything starts."
- **备注**：全场最重要的"问题页"，每层一句话，讲慢一点。这一页的叙事直接决定后面方法的必要性。

### Slide 4 — Digital Twin vision & the gap（1:00）

- **核心信息**：双模型 Digital Twin 架构中 SoH 是地基；而现有部署工作被"固定窗口"困住
- **页面内容**
  - Dual-model architecture（Alamin）：**SoH model**（部署一次、长期稳健）+ **SoC model**（随 SoH 漂移经 OTA 刷新）
  - This thesis: build & deploy the SoH foundation；design the OTA channel
  - Baseline（Sammartino et al.）：BiLSTM on SPC58 —— 但固定 20 样本窗口 + 满电起步假设
  - Fixed tensor shape ⇒ 换窗口长度 = 重训（5 种长度要 5 个模型）
- **素材**：`images/ch3_project_architecture.png`（论文 Fig. 3.1，本页主图）
- **讲稿要点**
  - "In this architecture SoH is the foundation: the SoC model consumes the SoH estimate, so SoH must be right first. The baseline is one of the very few fully deployed works — but it fixes the input window at 20 samples. In the field, trips vary in length and sampling rates change across hardware generations. A fixed-shape LSTM cannot adapt without retraining."
- **备注**：本页结尾自然抛出 research question："能不能训练一次，就适配任意输入窗口？"——这是全片的悬念，下一页贡献即作答。

### Slide 5 — Aims & contributions（0:45）

- **核心信息**：三件事——多长度训练+特征提取、LightGBM 编译部署、OTA 设计
- **页面内容**
  1. **Multi-length segmentation + 10-D feature extraction** → one model, any window length
  2. **LightGBM compiled to C, deployed & validated on SPC58EC80E5**（matches BiLSTM accuracy, 11–30× faster）
  3. **OTA update architecture design**（8-step lifecycle, A/B, security）
- **素材**：无图，三条编号 + 结果预告
- **讲稿要点**
  - "I close the gap with three pieces of work. First, a training strategy that makes window length irrelevant. Second, a tree-based model compiled to C and running on automotive silicon. Third, the OTA design that keeps the companion SoC model current over the battery's life."
- **备注**：把论文 Contributions 四条压缩成三条（第 1 条吸收多长度+特征两条）；括号里的数字是"预告片"，具体数值后面给。

### Slide 6 — Method overview: five-stage pipeline（0:45）

- **核心信息**：一条流水线：原始放电日志 → 板上固件
- **页面内容**（五阶段一列）
  1. Data acquisition & **multi-length segmentation**
  2. **Feature extraction**（10-D vector）
  3. **LightGBM training** + Bayesian HP search（Optuna）
  4. **EDEN compilation** → self-contained C
  5. **MCU deployment & verification**（SPC58EC80E5）
- **素材**：`images/ch3_ml_workflow.png`（论文 Fig. 3.2）
- **讲稿要点**
  - "The whole system is one pipeline of five stages. I'll spend time on the two design decisions that carry the thesis — segmentation and feature extraction — then show how the model reaches the MCU."
- **备注**：方法部分的"目录页"，30–45 秒带过，不要逐条展开。

### Slide 7 — Multi-length segmentation（1:15）

- **核心信息**：一次训练五个窗口长度 → 模型学到"窗口长度不该影响 SoH 估计"
- **页面内容**
  - wlen ∈ {20, 30, 40, 50, 60}，non-overlapping，stride = wlen
  - Label = 窗口末样本的 SoH（同循环内恒定）
  - 训练样本 ≈ 5× 数据增强：同一放电事件出现在五种时间分辨率，标签相同
  - Objective: **regardless of window length, predict the same SoH**
- **素材**：`images/ch3_window_segementation.png`（论文 Fig. 3.4）；Algorithm 1 放 backup
- **讲稿要点**
  - "Instead of one fixed window length, I train on five at once. The same physical discharge event appears at five resolutions — always with the same SoH label. The model learns that length itself must not matter. This is the inductive bias that pays off in the generalization experiment."
- **备注**：最后一句为 Slide 13 埋伏笔，两页形成呼应。

### Slide 8 — Feature extraction: the 10-D vector（1:15）

- **核心信息**：变长序列 → 固定 10 维统计特征，输入维度与窗口长度解耦（全场最核心的设计）
- **页面内容**
  - Raw window（wlen × 4）→ 5 个中间信号：dV/dt, dT/dt, V·I, Q, **dV/dQ**
  - → 10 维特征：各信号均值 + dV/dQ 的 min/max + 窗口时长
  - Physically motivated：dV/dQ 峰位/峰值随老化漂移（IC 分析思想）
  - 同一套特征逻辑在 MCU 上用 C 手写实现（FPU, float32）
- **素材**：论文 Table 3.1（中间信号）+ 特征列表；待生成图表 ②（"window → 10 numbers"示意图，可选）
- **讲稿要点**
  - "This is the key design decision. The model never sees the raw time series — it sees ten statistics chosen the way a battery engineer would look at degradation. Any window length maps to the same ten numbers, so one model serves every length. Feature extraction is the decoupling point between the field and the model."
- **备注**：全场最重要的一页，可多花 15 秒。讲清楚"解耦"这个词就够了，不必逐条念 10 个特征。

### Slide 9 — From Python to MCU（1:00）

- **核心信息**：LightGBM 编译为零依赖 C——推理 = 阈值比较 + 加法
- **页面内容**
  - Why LightGBM：no matrix multiplications, no activations；固定尺寸输入；leaf-wise + histogram
  - Optuna Bayesian search：1000 trials，**max_depth ≤ 8**（Flash 预算 O(N×2^depth) 的部署约束）
  - EDEN compiler → 4 个 static const 数组，每节点 6 bytes
  - Firmware = HAL init + 手写特征 C + EDEN 推理 C + main loop；输出与 Python **bit-for-bit 一致**
- **素材**：推理伪代码小片段（论文 Listing，放 6–8 行即可）；4 数组内存布局放 backup B6
- **讲稿要点**
  - "A tree ensemble is nothing but thresholds and additions — the cheapest operations an MCU can run. I tuned it with 1,000 Bayesian trials under a depth cap that guarantees the Flash budget. EDEN compiles the ensemble into four const arrays; my firmware calls feature extraction, then inference. The MCU output matches Python bit-for-bit."
- **备注**：如被问"EDEN 由合作者扩展"，口径提前与导师对齐：工具链扩展是合作者工作；训练策略、特征设计、固件集成、部署与全面验证是本人工作。

### Slide 10 — Experimental setup（0:45）

- **核心信息**：两个公开 NASA 数据集、一个公平复现的 baseline、四个评估维度
- **页面内容**
  - **NBD**：19 cells，0.09 Hz，capacity 标签（baseline 所用数据集）｜**NRD**：28 cells，随机负载，0.33 Hz，SoH % 标签
  - Cycle-level 64/16/20 split（防泄漏）；NRD 强制跨电芯隔离
  - BiLSTM 用同一划分重训、部署在同一块 SPC58EC80E5（180 MHz, 4 MB Flash, 384 KB RAM）
  - 指标：MAE/MSE、推理 cycles、Flash/RAM
- **素材**：论文 Table 4.1 压缩版（两数据集一行式）
- **讲稿要点**
  - "Fairness is the point here: same datasets, same split, same silicon. The NBD set is the baseline's own dataset; the NRD set with its randomized loads is the harder, more realistic test."
- **备注**：硬件规格一句话；"同划分、同硬件"是委员会最看重的公平性声明。

### Slide 11 — Accuracy vs BiLSTM（1:15）

- **核心信息**：精度持平或更好——优势恰好出现在部署最难的场景（长窗口、复杂数据）
- **页面内容**
  - NBD @ wlen 20：FW MAE **0.0167** vs 0.0202（−17%）；Full **0.0188** vs 0.0194
  - NRD：LightGBM **2.26 → 1.75**（窗口越长越好——统计收敛）vs BiLSTM **2.91 → 4.37**（越长越差）
  - Why：更长的窗口给特征统计更多样本 → 特征更稳；LSTM 只能硬啃更长序列
- **素材**：`figures/fig_mae_vs_wlen.png`（已生成 ✓）；`tab:sota` 完整表放 backup B3
- **讲稿要点**
  - "On the baseline's own dataset we're slightly ahead. On the randomized-usage dataset the gap is 2.5× at the longest window — and look at the directions: our error falls as windows lengthen, the LSTM's grows. That direction matters because real deployments trend toward longer, higher-rate windows."
- **备注**：页面上只放一张图 + 两个数字结论，不要贴大表。

### Slide 12 — Efficiency & memory footprint（1:10）

- **核心信息**：快 11–30×，开销几乎与窗口长度无关，Flash 占用 < 3%
- **页面内容**
  - @wlen 20：0.403 ms vs 4.656 ms（**11.6×**）；@wlen 60：81.3k vs 2.50M cycles（**30.7×**）
  - LightGBM 随长度仅 +12%（只有特征提取变慢）vs BiLSTM 3×（循环结构线性增长）
  - Flash 2.2–2.7%（91–111 KB），RAM 0.49%（1.88 KB）；energy 24 μJ vs 279 μJ
- **素材**：`figures/fig_cycles_vs_wlen.png`（已生成 ✓）
- **讲稿要点**
  - "The headline is 11 to 30 times faster. But the trend is the real story: our cost is nearly flat because tree traversal is constant — only the feature loop grows. That flatness is what keeps the BMS's real-time budget safe as sampling rates rise."
- **备注**：**主动**点出 BiLSTM 内存更小（0.21% Flash / 0.13% RAM）——以 <3% Flash 换 10–30× 速度完全值得；且 SPC5Studio AI 仅支持特定网络结构，EDEN 生成的 C 完全可移植。这是可预期的 Q&A，先说为强。

### Slide 13 — Generalization to unseen window lengths（1:15）

- **核心信息**：训练时没见过的窗口长度上，一个模型保持稳定；BiLSTM 全线崩坏（全场最强结果）
- **页面内容**
  - Test lengths {10, 35, 55, 75}：跨出训练区间两侧
  - NBD：avg MAE **0.046** vs BiLSTM 各变体 0.21–0.38；NRD：**2.50** vs 9.7–14.9（4–6×）
  - 极端案例：BiLSTM₆₀ 在 55→75 之间从 4.2 跳到 **28.2**
  - Why：模型吃特征不吃序列——截断/补零制造了 LSTM 从未见过的伪影
- **素材**：`images/ch4_generalization.png`（论文 Fig. 4.1 热力图，本页主图）
- **讲稿要点**
  - "This is the experiment that matters for deployment. A firmware update changes the sampling rate, an unusual trip breaks the window assumption — one LightGBM model, without any modification, stays accurate. Every BiLSTM variant collapses somewhere, by up to 7× between two lengths 15 samples apart."
- **备注**：⚠️ 论文 NBD 泛化表中 BiLSTM₆₀ 行与 LightGBM 行数值完全相同（疑似笔误），**先修论文数字再同步本页**。热力图 + 两个平均值就是全部，详细数值表放 backup B4。

### Slide 14 — OTA update architecture（1:00）

- **核心信息**：SoH 漂移触发云端重训 SoC 模型、OTA 下发——八步生命周期完整设计，闭环 Digital Twin
- **页面内容**
  - Role：SoC 依赖 SoH ⇒ 电池老化后 SoC 模型必须刷新
  - Triggers：SoH 漂移 > 1 pt **或** 6 个月超时兜底
  - 8 steps：accumulate → upload → trigger check → retrain → validate & sign → deliver → A/B install → switch & confirm
  - Security: SHA-256 + digital signature, monotonic version numbers · Recovery: A/B rollback + cloud alerting
  - 明确标注：**architectural design — not implemented in hardware**
- **素材**：待生成图表 ⑤（OTA 八步流程图）；无图则两列编号列表
- **讲稿要点**
  - "Because the SoC model consumes the SoH estimate, it must be refreshed as the battery ages — that's what OTA is for. I designed the complete lifecycle, from on-board data accumulation to A/B partition switch, with signatures and rollback. To be clear: this is a design, and its implementation is the first item of future work."
- **备注**：主动、清晰地承认 scope 边界，委员会欣赏诚实的边界划分；本页底部一行吸收原安全页要点，model-vs-firmware OTA 风险对比放 backup B7。这页同时是"Digital Twin"题目点题的闭环页。

### Slide 15 — Conclusions（0:45）

- **核心信息**：三条已验证结论——精度、效率、稳健性
- **页面内容**
  1. **Accuracy** — matches or beats BiLSTM on both datasets
  2. **Efficiency** — 11–30× faster；< 3% Flash, 0.49% RAM
  3. **Robustness** — one model, unseen window lengths, no retraining
  - SoH 是双模型 Digital Twin 的地基 → **地基现已存在，并在真实车规硅片上被测量验证**
- **素材**：无
- **讲稿要点**
  - "Back to where I started: SoH is the foundation of the digital twin, and the foundation now exists — trained, compiled, deployed, and measured on real automotive silicon."
- **备注**：与 Slide 4 首尾呼应；结论页数字和 #5 的"预告"完全一致。

### Slide 16 — Future work（0:30）

- **页面内容**
  - Implement OTA on hardware (end-to-end validation)
  - SoC model integration（误差传播：训练时注入合成 SoH 噪声）
  - Real-world vehicle data；model quantization（16/8-bit）；federated learning
- **素材**：无
- **备注**：只列不展开；每一项都对应一个潜在 Q&A，提前准备好一句话答案。

### Slide 17 — Thanks / Q&A

- **页面内容**
  - "Thank you — Questions?"
  - Code & pipeline: **github.com/QYRR/batteryML**
- **备注**：代码仓库放出来是加分项（可复现性）；答辩前确认仓库 README 是完整的。

---

## 3. Backup Slides（问答弹药库，不放主线）

| B# | 内容 | 来源 | 应对问题 |
|---|---|---|---|
| B1 | 五类方法对比矩阵（Accuracy/Cost/MCU/Input flexibility） | 论文 Table 2.1 | "Why LightGBM?"（必被问） |
| B2 | 原始数据结构图 + 数据集完整统计表 | Fig. 3.3 / Table 4.1 | 数据细节追问 |
| B3 | 完整 deployment 大表（20 行）+ tab:sota | Table 4.4 / 4.3 | 任何具体数字 |
| B4 | 泛化详细数值表 ×2 | Table 4.5 / 4.6 | 热力图细节 |
| B5 | 超参搜索空间 + 最优超参 | Table 3.2 / 4.2 | "怎么调的参？" |
| B6 | EDEN 四数组内存布局 + 推理 C 代码 | Ch3 §3.5 | "编译器做了什么？" |
| B7 | OTA 触发条件细节 + 八步全文 + model-vs-firmware OTA 风险对比 | Ch3 §3.8 | OTA 设计细节 |
| B8 | SoC 初步实验（SoH 误差传播） | Ch1 §1.2 Layer 4 | "为什么不做 SoC？" |

## 4. 30 秒电梯演讲（开场 & 被要求压缩时用）

> Batteries age, and the BMS must know how much. My thesis builds the SoH estimation layer of a digital-twin BMS: a LightGBM model trained on windows of five lengths and fed by ten statistical features — compiled to C and deployed on an automotive-grade microcontroller. It matches a BiLSTM baseline in accuracy, runs 11 to 30 times faster, occupies under 3% of Flash, and keeps its accuracy on window lengths never seen in training. I also designed the OTA mechanism that will keep the companion SoC model current as the battery ages.

## 5. 图表清单（Session 第 ② 步）

| # | 图表 | 用于 | 状态 |
|---|---|---|---|
| ① | 问题四层阶梯图 | Slide 3 | 待生成 |
| ② | "window → 10 features" 示意图 | Slide 8 | 可选 |
| ③ | MAE vs wlen 折线（两数据集） | Slide 11 | ✅ `figures/fig_mae_vs_wlen.png` |
| ④ | inference cycles vs wlen 折线 | Slide 12 | ✅ `figures/fig_cycles_vs_wlen.png` |
| ⑤ | OTA 八步流程图 | Slide 14 | 待生成 |

数据来源：论文 [experiment.tex](../content/chapters/experiment.tex) Table 4.4（③④）、[methodology.tex](../content/chapters/methodology.tex) §3.8（⑤）、[introduction.tex](../content/chapters/introduction.tex) §1.2（①）。

## 6. 答辩前待办（与 PPT 并行）

- [ ] **修复论文 NBD 泛化表疑似笔误**：BiLSTM₆₀ 行与 LightGBM 行数值完全相同（[experiment.tex](../content/chapters/experiment.tex) Table 4.5），需查训练日志核实
- [ ] 与导师对齐 EDEN 编译器贡献边界的口径
- [ ] 排练 ≥ 3 次并计时；录音自听一遍
- [ ] 确认 github.com/QYRR/batteryML 仓库 README 完整（Slide 17 会展示）
