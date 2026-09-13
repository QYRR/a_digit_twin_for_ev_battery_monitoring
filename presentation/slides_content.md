# 答辩幻灯片内容稿（手动制作 PPT 用）

> 本文档按页拆出 Beamer 版全部 25 页内容（17 主线 + 8 备用）。每页含：**布局说明**、**页面内容**（英文，直接复制进 PPT）、**图片/图表路径**、**讲稿备注**（复制进演讲者备注）。
>
> **PPT 格式建议**：16:9；正文字体 **Century Gothic**（或 Calibri），代码 **Consolas**；
> 配色：标题/强调 PoliTo 蓝 **#005CAB**（RGB 0,92,171）；正文近黑 #0B0B0B；次要文字 #52514E；警示红 **#D03B3B**；浅蓝底框 #ECF2F9。
> 图片路径以仓库根目录为准；插入 PPT 前可先用 [make_charts.py](make_charts.py) 重新生成图表。

---

## 1 标题页

**布局**：居中排版——校徽 → 题目 → 副题 → 姓名 → 单位/导师 → 日期

**页面内容**：

- 校徽：`images/logo/logoPoliTo_symbol_only.pdf`（或转为 PNG）
- 题目（大号加粗）：**A Digital Twin for EV Battery Monitoring**
- 副题：Lightweight SoH Estimation on an Automotive Microcontroller
- 姓名：**Chao Song**
- 单位：Politecnico di Torino — M.Sc. in Computer Engineering
- 导师：Supervisors: Prof. Sara Vinco · Dr. Khaled Sidahmed Sidahmed Alamin
- 日期：**DD Month 2026**（⚠️ 替换为实际答辩日期）

**讲稿**：Good morning. My thesis brings SoH estimation for EV batteries onto the vehicle's own microcontroller. In the next 15 minutes I will show why that is hard, what I built, and how it performed on real hardware.

---

## 2 Motivation & SoH

**布局**：左文右图（图占右 ~45%），底部一条警示框

**页面内容**（左栏）：

- Global EV sales: 3M (2020) → 16.6M (2024), CAGR ≈ 53% (IEA)
- The battery is the most critical — and expensive — component
- The BMS must track two states:
  - **SoC** — minutes to hours
  - **SoH** — months to years
- SoH = C_current / C_initial × 100%; below 70–80% = end of life

**图片**（右栏）：`images/ch1_EV_sales.png`

**底部警示框**（红字标题 "The problem this thesis attacks"）：
SoH has **no sensor** — it must be **inferred**. Aging is nonlinear, multi-factor coupled, and path-dependent.

**讲稿**：Every one of these vehicles carries a battery pack whose health determines safety, range, and cost. The BMS must know that health in real time. SoH, the fraction of original capacity left, has no sensor; it must be inferred, and aging is nonlinear, coupled, and path-dependent.

---

## 3 Problem: four barriers to an on-board estimator

**布局**：全宽编号列表（4 条），底部一句强调框

**页面内容**（编号 1–4）：

1. **Model-based hits a wall** — P2D too heavy for an MCU; ECM + Kalman drifts as the battery ages
2. **Data-driven stops at simulation** — ML is accurate (MAE < 2%) but almost never leaves the Python notebook
3. **Cloud vs. edge: neither is free** — cloud: latency, bandwidth, privacy; edge MCU: ~10⁵× fewer resources than the training server
4. **SoC–SoH coupling** — SoC needs the *current* SoH; a stale SoH ⇒ systematically biased SoC

**底部强调框**：Each layer exposes the next. **SoH is where everything starts.**

**讲稿**：The gap between the literature and a working on-board estimator is four layers deep. Physics models are too heavy or drift. ML models never leave the server. The cloud cannot be trusted with a safety-critical loop, and the edge has almost no resources. And even if you solve all that, SoC estimation needs the current SoH, so SoH is where everything starts.

---

## 4 A Digital Twin vision — and the gap it exposes

**布局**：左文右图（图占右 ~40%），图下方一个蓝框（research question）

**页面内容**（左栏）：

- Dual-model architecture (Alamin):
  - **SoH model**: deployed once, robust for the long term
  - **SoC model**: refreshed over the air as SoH drifts
- This thesis: **build & deploy the SoH foundation**, design the OTA channel
- Baseline (Sammartino et al.): BiLSTM on SPC58 — but a **fixed 20-sample window**, full-charge start
- Fixed tensor shape ⇒ a new window length = retraining (5 lengths would need 5 models)

**图片**（右栏）：`images/ch3_project_architecture.png`

**蓝框**（标题 "Research question"）：Can one model be trained *once* and stay accurate on *any* input window length?

**讲稿**：In this architecture SoH is the foundation: the SoC model consumes the SoH estimate, so SoH must be right first. The baseline is one of the very few fully deployed works, but it fixes the input window at 20 samples. In the field, trips vary in length and sampling rates change across hardware generations. A fixed-shape LSTM cannot adapt without retraining.

---

## 5 Aims & contributions

**布局**：全宽编号列表（3 条，第 2 条下挂一个子点）

**页面内容**：

1. **Multi-length segmentation + 10-D feature extraction** → one model, any window length
2. **LightGBM compiled to C**, deployed and validated on the SPC58EC80E5 automotive MCU
   - matches BiLSTM accuracy — 11–30× faster
3. **OTA update architecture design** (8-step lifecycle, A/B partitions, security)

**讲稿**：I close the gap with three pieces of work. First, a training strategy that makes window length irrelevant. Second, a tree-based model compiled to C and running on automotive silicon. Third, the OTA design that keeps the companion SoC model current over the battery's life.

---

## 6 Method overview: one pipeline, five stages

**布局**：大图居中（占宽 ~90%），图下一行五阶段文字

**图片**：`images/ch3_ml_workflow.png`

**图下小字**：1. data & multi-length segmentation   2. feature extraction   3. LightGBM + Bayesian HP search   4. EDEN → C   5. MCU deployment & verification

**讲稿**：The whole system is one pipeline of five stages. I will spend time on the two design decisions that carry the thesis — segmentation and feature extraction — then show how the model reaches the MCU.

---

## 7 Multi-length segmentation

**布局**：左图右文（图占左 ~58%），底部一个蓝框

**页面内容**（右栏）：

- wlen ∈ {20, 30, 40, 50, 60}
- non-overlapping, stride = wlen
- label = SoH of the window's last sample
- ≈ 5× more training samples: the same discharge event at five resolutions, always the same label

**图片**（左栏）：`images/ch3_window_segementation.png`

**底部蓝框**（标题 "Training objective"）：Regardless of window length, predict the **same** SoH.

**讲稿**：Instead of one fixed window length, I train on five at once. The same physical discharge event appears at five resolutions, always with the same SoH label. The model learns that length itself must not matter. This is the inductive bias that pays off in the generalization experiment.

---

## 8 Feature extraction: the 10-D vector

**布局**：左右双栏——左栏"原始窗口 + 5 个中间信号"，右栏"10 维特征表 + 两条说明"

**页面内容**（左栏）：

- **Raw window** (wlen × 4: V, I, T, t)
- 5 intermediate signals:
  - V̇ = dV/dt
  - Ṫ = dT/dt
  - P = V · I
  - Q = ∫ I dt
  - **dV/dQ** — the IC-analysis quantity
- **Key property**: the input dimension no longer depends on window length

**右栏特征表**（两列小表格，直接照抄）：

| # | Feature | # | Feature |
|---|---|---|---|
| 1 | mean(dV/dt) | 6 | mean(dV/dQ) |
| 2 | mean(V) | 7 | max(dV/dQ) |
| 3 | mean(dT/dt) | 8 | min(dV/dQ) |
| 4 | mean(V · I) | 9 | window duration |
| 5 | mean(t_rel) | 10 | mean(T) |

**表格下方**：

- physically motivated: dV/dQ peak shifts track degradation
- the same logic hand-written in C on the MCU (FPU, float32)

**讲稿**：This is the key design decision. The model never sees the raw time series, it sees ten statistics, chosen the way a battery engineer would look at degradation. Any window length maps to the same ten numbers, so one model serves every length. Feature extraction is the decoupling point between the field and the model.

---

## 9 From Python to MCU: LightGBM → self-contained C

**布局**：左文右代码（代码占右 ~55%，Consolas 小号）

**页面内容**（左栏）：

- **Why LightGBM**: no matrix multiplications, no activations; inference = threshold compares + additions
- **Optuna** Bayesian search, 1000 trials, max_depth ≤ 8 (Flash budget ~O(N_trees × 2^depth))
- **EDEN compiler** → 4 static const arrays, 6 bytes per node
- Firmware = HAL init + feature extraction + inference + main loop
- MCU output matches Python **bit-for-bit**

**右栏代码**（Consolas，等宽）：

```c
float output = 0;
for (int t = 0; t < N_TREES; t++) {
  int idx = roots[t];
  while (features[idx] != LEAF) {
    if (input[features[idx]] <= alphas[idx])
      idx++;                 // left
    else
      idx += children_right[idx];
  }
  output += alphas[idx];
}
return output;
```

**代码下方小字**：No recursion, no malloc, no dependencies.

**讲稿**：A tree ensemble is nothing but thresholds and additions, the cheapest operations an MCU can run. I tuned it with one thousand Bayesian trials under a depth cap that guarantees the Flash budget. EDEN compiles the ensemble into four const arrays; my firmware calls feature extraction, then inference. The MCU output matches Python bit-for-bit.

---

## 10 Experimental setup: two datasets, one fair baseline

**布局**：左表右文（表占左 ~56%）

**左栏表格**（照抄）：

| | NBD | NRD |
|---|---|---|
| Cells | 19 | 28 |
| Discharge cycles | 164 | 258 |
| Sampling rate | 0.09 Hz | 0.33 Hz |
| Label | capacity (Ah) | SoH (%) |
| Load profile | constant current | randomized 0.5–4 A |

**表格下方**：

- cycle-level 64/16/20 split — no leakage across windows
- NRD: cross-cell isolation enforced

**页面内容**（右栏）：

- **BiLSTM baseline** (Sammartino et al.) reproduced: retrained on the *same* split, deployed on the *same* SPC58EC80E5
- Hardware: 180 MHz, 4 MB Flash, 384 KB SRAM
- Metrics: MAE / MSE, inference cycles, Flash & RAM

**讲稿**：Fairness is the point here: same datasets, same split, same silicon. The NBD set is the baseline's own dataset; the NRD set with its randomized loads is the harder, more realistic test.

---

## 11 Accuracy vs BiLSTM

**布局**：大图占宽 ~92% 居中，底部一个蓝框

**图片**：`presentation/figures/fig_mae_vs_wlen.png`（柱状图版，两面板共享同一纵轴刻度，图内无标题）

**图标题（复制到图下方）**：SoH estimation error vs window length — both models deployed on the SPC58EC80E5 (thesis Table 4.4)

**底部蓝框**：**NBD @ wlen 20**: FW MAE **0.0167** vs 0.0202 (−17%) — **NRD**: LightGBM 2.26 → 1.75 (longer windows help) vs BiLSTM 2.91 → 4.37 (longer windows hurt)

**讲稿**：On the baseline's own dataset we are slightly ahead. On the randomized-usage dataset the gap is 2.5 times at the longest window, and look at the directions: our error falls as windows lengthen, the LSTM's grows. That direction matters because real deployments trend toward longer, higher-rate windows.

---

## 12 Efficiency & memory footprint

**布局**：大图占宽 ~92% 居中，底部一个蓝框

**图片**：`presentation/figures/fig_cycles_vs_wlen.png`（单图柱状：两系列合并，纵轴为相对成本 wlen 20 = 1，端点柱标注绝对 cycles，图内无标题）

**图标题（复制到图下方）**：Inference cost vs window length — relative cost (wlen 20 = 1), absolute cycles at the endpoints (thesis Table 4.4)

**底部蓝框**：**11.6×** faster at wlen 20 (0.403 ms vs 4.656 ms) — **30.7×** at wlen 60 — Flash **< 3%** (91–111 KB) — RAM 0.49% (1.88 KB) — energy 24 μJ vs 279 μJ

**讲稿**：The headline is 11 to 30 times faster. But the trend is the real story: our cost is nearly flat because tree traversal is constant, only the feature loop grows. That flatness is what keeps the BMS real-time budget safe as sampling rates rise.

---

## 13 Generalization to unseen window lengths

**布局**：左图右文（图占左 ~52%），右栏底部一个红框

**图片**（左栏）：`images/ch4_generalization.png`

**页面内容**（右栏）：

- Test lengths {10, 35, 55, 75} — inside and outside the training range
- Avg MAE, NBD: **0.046** vs 0.21–0.38 (BiLSTM variants)
- Avg MAE, NRD: **2.50** vs 9.7–14.9   (4–6×)
- Extreme case: BiLSTM₆₀ jumps 4.2 → **28.2** from length 55 to 75

**红框**（标题 "Why"）：LightGBM consumes *features*, not sequences — truncation and zero-padding are artifacts an LSTM was never trained to see.

**讲稿**：This is the experiment that matters for deployment. A firmware update changes the sampling rate, an unusual trip breaks the window assumption. One LightGBM model, without any modification, stays accurate. Every BiLSTM variant collapses somewhere, by up to 7 times between two lengths 15 samples apart.

---

## 14 OTA update architecture — closing the Digital Twin loop

**布局**：左右双栏——左栏 Role/Triggers/Security，右栏 8 步编号列表；底部一行红字

**页面内容**（左栏）：

- **Role**：The SoC model consumes the SoH estimate ⇒ it must be refreshed as the battery ages.
- **Triggers**：
  - SoH drift > 1 pt since last update
  - or 6-month timeout (safety net)
- **Security & recovery**（小字）：
  - SHA-256 + signature · monotonic version numbers
  - A/B rollback · cloud alerting

**右栏编号列表**（标题 "Update lifecycle (8 steps)"）：

1. on-board data accumulation
2. periodic upload (safe state, TCU)
3. trigger evaluation
4. cloud retraining of the SoC model
5. validation + packaging + signing
6. OTA delivery (hash + signature check)
7. A/B partition installation
8. model switch + confirmation

**底部红字**：Architectural design — not implemented in hardware (future work).

**讲稿**：Because the SoC model consumes the SoH estimate, it must be refreshed as the battery ages; that is what OTA is for. I designed the complete lifecycle, from on-board data accumulation to A/B partition switch, with signatures and rollback. To be clear: this is a design, and its implementation is the first item of future work.

---

## 15 Conclusions

**布局**：全宽编号列表（3 条），底部一个蓝框

**页面内容**：

1. **Accuracy** — matches or beats BiLSTM on both datasets
2. **Efficiency** — 11–30× faster; < 3% Flash, 0.49% RAM
3. **Robustness** — one model, unseen window lengths, no retraining

**底部蓝框**：SoH is the foundation of the dual-model Digital Twin — and the foundation now exists: **trained, compiled, deployed, and measured on real automotive silicon**.

**讲稿**：Back to where I started: SoH is the foundation of the digital twin, and the foundation now exists, trained, compiled, deployed, and measured on real automotive silicon.

---

## 16 Future work

**布局**：全宽项目符号列表（5 条）

**页面内容**：

- Implement the OTA mechanism on hardware (end-to-end validation)
- Integrate the SoC model — handle SoH-to-SoC error propagation (e.g. inject synthetic SoH noise during training)
- Validate on real-world vehicle data
- Model quantization (16/8-bit)
- Federated, privacy-preserving training

**讲稿**：Each of these is a direction I can discuss in the questions.

---

## 17 Thank you — Questions?

**布局**：居中大字 + GitHub 链接

**页面内容**：

- **Thank you — Questions?**（大号加粗居中）
- Code & pipeline: https://github.com/QYRR/batteryML

---

# 备用页（Backup，Q&A 时翻出）

## B1 Backup: why LightGBM? — method comparison

**表格**（照抄）：

| Method | Accuracy | Cost | MCU-deployable | Input flexibility |
|---|---|---|---|---|
| Electrochemical | Very high | Very high | No | — |
| ECM + Filter | Moderate | Low | Yes | — |
| Classical ML | Moderate–High | Moderate | Limited | Yes |
| Deep Learning | High | High | Limited | No |
| LightGBM | High | Very low | Yes | Yes |

**下方要点**：LightGBM is the only row combining high accuracy with freedom from fixed-length inputs (through feature extraction)

## B2 Backup: raw data structure

**图片**（居中 ~82% 宽）：`images/ch3_inputdata_sample.png`

**图下小字**：Rows are sampling instants within a discharge cycle; every row of a cycle shares the same SoH label.

## B3 Backup: full deployment results (Table 4.4)

**布局**：左右两张小表并排

**NBD**（L = LightGBM, B = BiLSTM）：

| WL | M | MAE% | MSE%² | kcyc | RAM% | Flash% |
|---|---|---|---|---|---|---|
| 20 | L | 1.013 | 2.321 | 72.6 | 0.49 | 2.71 |
| 20 | B | 1.045 | 2.031 | 838 | 0.13 | 0.21 |
| 30 | L | 0.840 | 1.741 | 74.7 | 0.49 | 2.71 |
| 30 | B | 0.873 | 1.451 | 1250 | 0.13 | 0.21 |
| 40 | L | 0.738 | 1.161 | 77.1 | 0.49 | 2.71 |
| 40 | B | 2.160 | 7.544 | 1670 | 0.13 | 0.21 |
| 50 | L | 0.921 | 2.321 | 79.0 | 0.49 | 2.71 |
| 50 | B | 1.551 | 4.062 | 2080 | 0.13 | 0.21 |
| 60 | L | 0.932 | 1.741 | 81.3 | 0.49 | 2.71 |
| 60 | B | 1.514 | 3.772 | 2500 | 0.13 | 0.21 |

**NRD**：

| WL | M | MAE% | MSE%² | kcyc | RAM% | Flash% |
|---|---|---|---|---|---|---|
| 20 | L | 2.256 | 12.622 | 73.3 | 0.49 | 2.23 |
| 20 | B | 2.908 | 14.897 | 838 | 0.13 | 0.21 |
| 30 | L | 2.208 | 11.788 | 75.4 | 0.49 | 2.23 |
| 30 | B | 4.127 | 27.588 | 1250 | 0.13 | 0.21 |
| 40 | L | 2.183 | 10.498 | 77.8 | 0.49 | 2.23 |
| 40 | B | 4.002 | 28.180 | 1670 | 0.13 | 0.21 |
| 50 | L | 1.881 | 7.137 | 79.6 | 0.49 | 2.23 |
| 50 | B | 4.751 | 40.870 | 2080 | 0.13 | 0.21 |
| 60 | L | 1.751 | 7.357 | 82.0 | 0.49 | 2.23 |
| 60 | B | 4.368 | 30.323 | 2500 | 0.13 | 0.21 |

**表下小字**：L = LightGBM (this work), B = BiLSTM. MAE/MSE on the SoH scale.

## B4 Backup: generalization detail

**布局**：左右两张表并排

**NBD — MAE**：

| Model | 10 | 35 | 55 | 75 | Avg |
|---|---|---|---|---|---|
| LightGBM | 0.041 | 0.023 | 0.025 | 0.095 | 0.046 |
| BiLSTM₂₀ | 0.106 | 0.491 | 0.492 | 0.274 | 0.341 |
| BiLSTM₃₀ | 0.059 | 0.042 | 0.504 | 0.497 | 0.276 |
| BiLSTM₄₀ | 0.102 | 0.073 | 0.668 | 0.660 | 0.376 |
| BiLSTM₅₀ | 0.097 | 0.068 | 0.033 | 0.643 | 0.210 |
| BiLSTM₆₀ | 0.041 | 0.023 | 0.025 | 0.095 | 0.046 |

**NRD — MAE**：

| Model | 10 | 35 | 55 | 75 | Avg |
|---|---|---|---|---|---|
| LightGBM | 3.7 | 2.3 | 1.7 | 2.3 | 2.50 |
| BiLSTM₂₀ | 5.3 | 15.3 | 7.5 | 10.8 | 9.73 |
| BiLSTM₃₀ | 5.5 | 19.8 | 19.9 | 12.6 | 14.45 |
| BiLSTM₄₀ | 6.8 | 4.2 | 24.0 | 24.5 | 14.88 |
| BiLSTM₅₀ | 7.5 | 4.8 | 21.7 | 22.2 | 14.05 |
| BiLSTM₆₀ | 8.9 | 4.8 | 4.2 | 28.2 | 11.53 |

**⚠️ 重要提醒**：NBD 表中 **BiLSTM₆₀ 行与 LightGBM 行数值完全相同**（论文 Table 4.5 疑似笔误）。做 PPT 前先去查训练日志核实，修正后再把正确数字放上这页。

## B5 Backup: hyperparameter search

**布局**：左右两张表并排

**Search space**：

| Parameter | Range |
|---|---|
| Learning rate | [10⁻⁵, 0.7] |
| Max depth | [3, 8] |
| Num leaves | [2, 25] |
| Num estimators | [50, 450] |
| α (L1) | [10⁻⁶, 1] |
| β (L2) | [10⁻⁶, 1] |
| Min child samples | [2, 25] |
| Column samples/tree | [0.1, 1] |

**Best configurations**：

| | NBD | NRD |
|---|---|---|
| LR | 0.147 | 0.085 |
| Depth | 8 | 8 |
| Leaves | 25 | 18 |
| Trees | 384 | 443 |
| α | 6.5×10⁻² | 1.9×10⁻⁶ |
| β | 6.7×10⁻⁵ | 3.6×10⁻⁴ |
| MCS | 6 | 17 |
| CST | 0.46 | 0.61 |

## B6 Backup: EDEN in-memory representation

**页面内容**：

- 4 static arrays per ensemble:
  - **ROOTS** (uint16) — start of each tree
  - **FEATURES** (uint8) — feature index, or leaf sentinel
  - **ALPHAS** (float) — split threshold, or leaf contribution
  - **CHILDREN_RIGHT** (uint8) — pre-order layout: left child is implicit
- 6 bytes per node — model: 111 KB (NBD) / 91.34 KB (NRD) of 4 MB Flash

## B7 Backup: OTA details

**页面内容**：

- **Update triggers**: SoH drift > 1 pt *or* 6-month timeout — update frequency on the order of months
- **Delivery**: parked + sufficient battery + good signal — integrity (SHA-256) and authenticity (signature) checked before install
- **Recovery**: anomalous outputs (SoC outside [0,100]%, physics violations, deviation from Coulomb counting) ⇒ atomic switch back to the previous model + cloud alert
- **Model OTA vs firmware OTA**: payload ~100–300 KB; low risk — degradation is gradual and reversible; rollback is a pointer swap

## B8 Backup: preliminary SoC experiments

**页面内容**：

- An SoC model with the SoH estimate as an input feature was trained and evaluated
- Finding: SoH estimation errors **propagate** into SoC predictions, amplifying the overall error
- Consequence: SoH accuracy must be established *first* — the dual-model cascade cannot function without a solid foundation
- This is why the thesis concentrates on the SoH layer
