
# 雙 BIT（Fenwick Tree）：區間修改 ＋ 區間查詢

> 目標：支援兩種操作，皆為 **O(log n)**
>
> 1. 區間加值：`[l, r] += x`
> 2. 區間查詢：`sum(l, r)`
>
> 全程 **1‑based index**；陣列建議開到 `n+2` 以容納 `r+1`。

---

## 1. 差分觀念（把「區間加」變兩次單點加）

對 `[l, r] += x` 等價於：

```
diff[l]   += x
diff[r+1] -= x
```

單點值：$a[i] = \sum_{j=1}^{i} diff[j]$

---

## 2. 推導前綴和

$\displaystyle \text{prefix}(i) = \sum_{k=1}^{i} a[k] = \sum_{k=1}^{i} \sum_{j=1}^{k} diff[j] = \sum_{j=1}^{i} (i-j+1)\,diff[j] $

係數分解 $(i-j+1)=(i+1)-j$ 得：
$\boxed{\;\text{prefix}(i)=(i+1)\sum_{j\le i} diff[j] \; -\; \sum_{j\le i} j\,diff[j]\;}$

> 結論：需要同時維護 `Σ diff[j]` 與 `Σ (j·diff[j])` ⇒ 用 **兩棵 BIT**。

---

## 3. 兩棵 BIT 的分工與查詢公式

* **BIT1**：$S_1(i)=\sum_{j\le i} diff[j]$
* **BIT2**：$S_2(i)=\sum_{j\le i} j\,diff[j]$

查詢公式（固定版本）：
$\boxed{\;\text{prefix}(i)=(i+1)\,Q_1(i) - Q_2(i)\;}$
其中 `Q1(i)=query(BIT1,i)`、`Q2(i)=query(BIT2,i)`。

區間和：$\text{sum}(l,r)=\text{prefix}(r)-\text{prefix}(l-1)$。

---

## 4. 區間加值時怎麼更新兩棵 BIT？

對 `[l, r] += x`：

* **BIT1**（存 `diff`） ： `+x@l`, `-x@(r+1)`
* **BIT2**（存 `j·diff[j]`）： `+l·x@l`, `-(r+1)·x@(r+1)`

> 心訣：同一個索引 `j`，**BIT2 多乘一個 `j`**。左端乘 `l`，右端乘 `r+1`。

---

## 5. C++ 模板（1-based；`N ≥ n+2`；使用 `long long`）

```cpp
#define lowbit(x) ((x) & (-(x)))
const int N = 200005; // 依題目調整（建議 n+2）
long long bit1[N], bit2[N];

inline void add(long long *bit, int idx, long long val){
    for(; idx < N; idx += lowbit(idx)) bit[idx] += val;
}

inline long long sum(long long *bit, int idx){
    long long s = 0;
    for(; idx > 0; idx -= lowbit(idx)) s += bit[idx];
    return s;
}

// 區間加值 [l, r] += x
inline void range_add(int l, int r, long long x){
    add(bit1, l, x);            // diff[l]   += x
    add(bit1, r+1, -x);         // diff[r+1] -= x
    add(bit2, l, 1LL*l*x);      // j·diff[j] at j=l
    add(bit2, r+1, -1LL*(r+1)*x); // j·diff[j] at j=r+1
}

// prefix(i) = a[1] + ... + a[i]
inline long long prefix_sum(int i){
    return (i + 1) * sum(bit1, i) - sum(bit2, i);
}

// sum(l, r)
inline long long range_sum(int l, int r){
    return prefix_sum(r) - prefix_sum(l - 1);
}
```

---

## 6. 複雜度、邊界與 Debug 心法

* **時間**：每次更新 / 查詢皆 **O(log n)**；**空間**：兩棵 `O(n)`。
* **邊界**：

  * 開到 `n+2` 以防 `r+1`；
  * 使用 `long long` 防溢位；
  * 1‑based：若輸入是 0‑based 要轉。
* **快速自檢**：

  * 做完一次 `[l,r]+=x` 後，`prefix(l-1)` 不變、`prefix(r)` 應增加 `x*(r-l+1)`。
  * 多次更新交換順序，查詢結果不變（可測線性疊加）。

---

## 7. 等價的另一套寫法（勿混搭）

也有人用：

* 更新：BIT2 用 `+(l-1)*x` 與 `-r*x`
* 查詢：`prefix(i) = i * Q1(i) - Q2(i)`

兩套是**等價**重排；**更新與查詢必須成對**使用同一套，本筆記全篇使用「`(i+1)` 與 `l, r+1`」版本。
