# FHE Research Philosophy

## 1. 总体研究哲学：填洞式科研

我们的目标不是从零幻想一个全新的 primitive，而是从已有 FHE 文献、算法、证明和参数空间中系统寻找真实缺口，并尝试用尽可能小但有原则性的技术修改去填补。

核心路径：

```text
已有工作
→ 拆解 claim / assumption / mechanism / bottleneck / parameter regime
→ 检查边界与未覆盖区域
→ 发现 gap
→ 定位 gap 为什么存在
→ 提出最小但非平凡的修补
→ 验证 correctness / security / complexity / concrete gain
→ 判断是否形成可发表 contribution
```

我们的默认原则是：

> 先证明有洞，再想怎么填；先 falsify，再 optimize。

---

## 2. 什么是“填洞式科研”

以下问题都属于我们优先关注的 research gap 来源：

- 检查已有论文是否存在错误、overclaim、遗漏的 parameter region；
- 检查 theorem / proof / complexity 是否真的覆盖作者声称的范围；
- 如果发现问题，判断它只是一个勘误，还是暴露了需要新技术修补的结构性问题；
- 检查不同 FHE optimization 是否可以组合；
- 如果不能组合，找清楚真正的 obstruction；
- 从旧方法中抽象 technique / principle，再迁移到新的 bottleneck；
- 找 special case → general case 的推广空间；
- 找某种优化尚未覆盖的 setting；
- 找现有 trade-off / Pareto frontier 中被忽略的区域。

“没人做过 X”本身不是充分的 research gap。

真正重要的问题是：

```text
为什么没人做？
是没人注意，
还是现有 framework 在这里真的失败？
如果失败，失败在哪里？
这个 obstruction 是否可以被新的 technique 消除？
```

---

## 3. 可发表 FHE Research Gap 的定义

一个值得称为“可发表”的 FHE research gap，应该是：

> 一个真实、重要、此前未被充分解决，而且需要非平凡技术才能填补的缺口。

可以近似写成：

```text
Publishable Gap
=
Novelty
× Technical Nontriviality
× Importance
× Verifiability
```

其中任何一项接近 0，整体价值都会显著下降。

---

## 4. 判断一个 gap 是否可发表的核心标准

### 4.1 Gap 必须真实存在，并且能被精确定位

理想情况下，我们应该能把 gap 写成一句非常具体的话：

```text
Existing works achieve X under condition A,
but do not cover B.
```

或者：

```text
Existing methods incur cost C because of step S,
and no prior work removes this bottleneck in setting R.
```

不接受仅仅：

```text
好像没人研究过这个。
```

必须能指出：

- 哪些 prior works；
- 它们解决了什么；
- 它们没有解决什么；
- 未解决部分的边界在哪里。

---

### 4.2 不能只是 bookkeeping error / trivial erratum

如果发现：

```text
Theorem 少写了一个条件，
补上一句话就修好了。
```

通常只是 erratum，不是完整科研 contribution。

更有价值的情况是：

```text
作者声称 general case 成立
→ proof 在某一步实际依赖额外条件
→ general case 下算法/证明真的失败
→ 需要新的 technique 才能修补
```

重点不是“抓到作者错误”，而是：

> 这个错误是否暴露了一个此前没有被理解的结构、障碍或边界？

---

### 4.3 Gap 必须影响一个有意义的 setting

优先关注：

- 实际重要的 parameter regime；
- 常见 FHE workload；
- bootstrapping / packing / polynomial evaluation 等核心 bottleneck；
- 有意义的 security / secret / algebraic assumption；
- 重要的 memory / key-size / latency / throughput trade-off；
- 理论上自然但此前只解决了特殊情形的问题。

如果 gap 只存在于几乎不会使用的极端参数区域，其发表价值通常较低。

---

### 4.4 修补必须包含非平凡技术，而不是机械拼接

如果有论文 A 和论文 B：

```text
A optimizes component X
B optimizes component Y
```

仅仅发现：

```text
A + B 也能跑
```

通常不足以成为强 contribution。

我们更关心：

```text
A + B directly fails
```

然后定位：

```text
obstruction O
```

再引入新的 representation / decomposition / transformation / proof idea：

```text
A + R + B works
```

此时真正的 contribution 通常是：

```text
R
```

或者：

```text
对 obstruction O 的新理解
```

---

### 4.5 最好改变某个 frontier，而不是只做微小常数优化

FHE 的评价不能只看 runtime，而应考虑多维指标：

```text
latency
throughput
key size
memory
ciphertext size
precision
noise
multiplicative depth
number of NTTs
number of external products
number of key switchings
security assumption
```

理想的 gap 是：

- 在某个 regime 内严格优于已有方法；
- 或填补 Pareto frontier 中此前无人覆盖的区域；
- 或打破一个长期存在的 trade-off。

例如：

```text
现有低-latency 方法需要巨大 bootstrapping key
→ 新方法允许略微增加 latency
→ 大幅降低 key size
```

即使不是所有维度都 SOTA，也可能形成有意义 contribution。

---

### 4.6 最好产生“新理解”，而不只是“新实现”

强 contribution 通常不仅回答：

```text
How can we make it faster?
```

还回答：

```text
Why was this bottleneck there in the first place?
```

例如：

```text
过去大家认为某成本来自 algebraic necessity
```

但我们发现：

```text
它其实只是某种 representation artifact
```

这种 conceptual correction / structural explanation 本身具有很高科研价值。

---

### 4.7 Gap 必须可验证

一个 research gap 至少应该能通过以下一种方式验证：

- formal proof；
- correctness analysis；
- security analysis；
- asymptotic complexity；
- concrete operation count；
- implementation benchmark；
- parameter sweep；
- counterexample / failure case。

最好同时有理论与 concrete evaluation。

仅仅依靠叙事：

```text
“这个 setting 看起来很重要”
```

是不够的。

---

### 4.8 必须存在明确 baseline

所有 candidate contribution 都必须回答：

> Compared with exactly which prior work?

并尽量能写出：

```text
old cost → new cost
```

例如：

```text
K external products → K/r external products
```

```text
O(n log q) decomposition work → O(h log q)
```

```text
K NTTs → K - Δ NTTs
```

```text
large key size → smaller key size under regime R
```

没有明确 baseline，就很难定义 contribution。

---

## 5. 我们重点寻找的七类 FHE research gap

### 5.1 Correctness Hole

作者声称的结论范围大于实际证明范围：

```text
Claimed domain
-
Actually proved domain
```

重点检查：

- theorem statement；
- hidden assumptions；
- proof 中实际使用但 statement 未说明的条件；
- correctness / noise / security 是否真的覆盖所有参数。

如果修补 general case 需要新技术，就可能形成 contribution。

---

### 5.2 Parameter Hole

不同方法只覆盖 parameter space 的不同区域。

我们应主动检查：

```text
N
q
decomposition base
precision
degree
batch size
secret sparsity
number of slots
circuit depth
GPU / CPU regime
memory budget
```

寻找：

```text
现有方法都没有占优的 parameter region
```

特别关注 crossover region，而不是只看作者报告的默认参数。

---

### 5.3 Assumption Hole

已有优化可能要求：

```text
N = 2^k
sparse secret
binary secret
large batch
special modulus
special cyclotomic ring
special packing structure
```

需要追问：

```text
这个 assumption 真的是数学上必要的吗？
还是 proof / implementation / representation 造成的？
```

如果实际只需要更弱的 assumption：

```text
A → A'
```

则可能产生 generalization。

---

### 5.4 Composition Hole

两个已有 optimization 是否能组合？

不能只问：

```text
A + B 能不能做？
```

而要问：

```text
如果不能做，真正的 obstruction 在哪里？
```

有价值的路径通常是：

```text
A + B fails
→ identify obstruction O
→ introduce technique R
→ A + R + B works
```

---

### 5.5 Technique-Transfer Hole

不要只迁移算法 syntax，而要抽象底层 principle。

路径：

```text
Technique
→ underlying principle
→ identify same structural bottleneck elsewhere
→ transfer principle
```

例如某方法表面上利用 sparse secret，真正 principle 可能是：

```text
利用结构化 secret 消除 repeated computation
```

那么应寻找其他同样存在：

```text
structured secret + repeated computation
```

的场景。

---

### 5.6 Generalization Hole

从 special case 推广到 general case，例如：

```text
binary secret → small secret → general secret
2-power cyclotomic → general cyclotomic
single ciphertext → batched ciphertexts
special matrix shape → general matrix shape
special degree range → general degree range
```

真正有价值的 generalization 需要出现：

```text
general case introduces obstruction O
```

并通过新的 technique 解决 O。

仅仅把符号写得更一般不算 substantive contribution。

---

### 5.7 Trade-off Hole

FHE optimization 的真正空间通常是 Pareto frontier，而不是单一 runtime。

需要检查：

```text
latency ↔ throughput
latency ↔ key size
memory ↔ recomputation
precision ↔ runtime
noise ↔ depth
packing density ↔ rotation/key-switch cost
precomputation ↔ online cost
```

问题不是：

```text
谁绝对最快？
```

而是：

```text
是否存在一个此前没人占据的 trade-off point？
```

---

## 6. 弱、中、强 gap 的区分

### Weak Gap

```text
Existing work did not benchmark N = 4096.
We benchmark N = 4096.
```

通常不足以形成论文。

### Medium Gap

```text
Existing method performs poorly at N = 4096
because decomposition overhead dominates.

We modify the decomposition strategy
and improve this regime.
```

已经具有论文雏形。

### Strong Gap

```text
Existing approaches implicitly assume that
the decomposition cost can only be reduced
by increasing the decomposition base.

We show that the dominant cost actually comes
from repeated structure across components.

We introduce a shared representation that removes
this redundancy, prove correctness/noise bounds,
and improve both asymptotic and concrete costs
in the previously uncovered regime.
```

这类 gap 同时包含：

```text
new observation
+ obstruction
+ new technique
+ theory
+ concrete gain
```

是我们优先追求的形态。

---

## 7. Candidate Gap 的统一记录模板

以后每一个 FHE research idea 都尽量按以下模板归档：

```text
Known:
现在已有工作知道什么？

Claim:
已有工作明确声称什么？

Baseline:
最直接的 baseline 是哪篇论文 / 哪个算法？

Boundary:
现有结论真正覆盖到哪里？

Hole:
具体哪里没有被覆盖、证明或优化？

Importance:
为什么这个 setting / region / bottleneck 值得研究？

Reason:
为什么这个洞长期存在？

Obstruction:
真正阻止已有方法继续推进的技术障碍是什么？

Hypothesis:
我们认为可以通过什么结构或技术解决？

Fast Falsification Test:
最快怎样证明这个 hypothesis 是错的？

Correctness:
如果方案成立，正确性如何证明？

Security:
是否改变安全假设或 security reduction？

Complexity:
old cost → new cost 是什么？

Concrete Evaluation:
哪些参数、benchmark、operation counts 能验证 gain？

Prior-Art Risk:
有没有已有论文已经做过相同或等价的事情？

Contribution:
如果成功，人们会因此知道什么以前不知道的东西？
```

---

## 8. 最终筛选问题

任何候选 idea，在投入大量时间之前，都先回答：

> **What exactly is the gap?**

> **Why do existing methods fail there?**

> **What nontrivial new idea is required to fix it?**

> **What measurable or provable frontier changes if we succeed?**

> **What new understanding will the community gain?**

如果前三个问题说不清楚，这个题目暂时不应该进入高投入阶段。

---

## 9. 我们的核心原则

```text
不是为了“新”而新，
而是寻找 existing knowledge 与 actual capability 之间的缝隙。
```

```text
不是先发明 solution 再寻找 problem，
而是先确认 problem / gap / obstruction，
再设计最小而有原则性的 solution。
```

```text
不是问“能不能发 paper”，
而是问：
如果成功，
人们对这个问题会多知道什么以前不知道的东西？
```

最终，一个成熟的 FHE contribution 应尽量形成完整证据链：

```text
Gap
→ Why existing methods miss it
→ Technical obstruction
→ New technique
→ Correctness
→ Security
→ Complexity
→ Concrete gain
→ New understanding
```
