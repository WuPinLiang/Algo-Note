# 飛黃騰達

## 問題描述
給定 `n` 個在二維平面上的點 `(x, y)`。我們從原點 `(0,0)` 出發，尋找一條路徑，這條路徑由給定點集中的部分點組成。

移動規則是：從一個點 `(x1, y1)` 只能移動到另一個點 `(x2, y2)`，當且僅當 `x2 >= x1` 且 `y2 >= y1`，並且 `(x2, y2) != (x1, y1)`（即不能移動到完全相同的點，必須有至少一個維度是嚴格增加的）。

我們的目標是找到這條路徑最多可以經過多少個點。

## 核心解題思路
這個問題可以被巧妙地轉化為一個經典的演算法問題：**最長遞增子序列 (Longest Increasing Subsequence, LIS)**。

我們的策略是：
1.  **排序**: 先將所有的點進行排序。排序的主要依據是 `x` 座標，由小到大。如果 `x` 座標相同，則按 `y` 座標由小到大排序。
2.  **對 `y` 座標找 LIS**: 排序後，我們就得到了一個點的序列 `p_1, p_2, ..., p_n`。在這個序列中，`x` 座標是保證非遞減的 (`x(p_i) <= x(p_{i+1})`)。現在，問題轉化為：在這個序列中，找到一個最長的子序列，使得它們的 `y` 座標是**嚴格遞增**的。

為什麼這樣是可行的？
*   排序後，對於任何子序列，`x` 座標已經滿足 `x_new >= x_old` 的條件。
*   如果我們再要求 `y` 座標嚴格遞增 (`y_new > y_old`)，那麼 `(x_new, y_new)` 就不可能等於 `(x_old, y_old)`，完美地滿足了題目要求。
*   這就將一個二維的問題，降維成了一個一維的 LIS 問題。

## LIS 演算法詳解 (耐心排序法)
我們使用一個 O(N log N) 的高效演算法來求解 LIS。這個演算法維護一個輔助陣列 `lis`（或稱 `tails`）。`lis` 陣列的性質是：`lis[i]` 儲存的是所有長度為 `i+1` 的遞增子序列中，結尾元素最小的那一個。這個 `lis` 陣列本身也永遠是遞增的。

演算法步驟如下：
1.  初始化一個空的 `lis` 陣列。
2.  遍歷排序後所有點的 `y` 座標。對於每一個 `y`：
    a.  在 `lis` 陣列中，使用二分搜尋法找到第一個**大於** `y` 的元素的位置。
    b.  如果找不到這樣的元素（即 `y` 比 `lis` 中所有元素都大），這表示 `y` 可以接在目前最長的遞增子序列後面，形成一個更長的子序列。我們將 `y` 加入到 `lis` 的末尾。
    c.  如果找到了，假設位置在 `it`，我們就用 `y` 來取代 `*it`。這一步的意義是：我們找到了一個長度和 `it` 所在位置對應的子序列，但是它的結尾更小 (`y`)。這讓未來有更多機會可以接上更長的序列。
3.  最終，`lis` 陣列的長度，就是最長遞增子序列的長度。

## 程式碼解析

### `lower_bound` vs `upper_bound` (WA vs AC)
這是本題的關鍵細節。
*   `lower_bound(y)`: 尋找第一個**不小於** `y` 的元素。如果序列中有重複元素，它會找到該元素本身。這會導致計算出的是「最長**非遞減**子序列」。
*   `upper_bound(y)`: 尋找第一個**嚴格大於** `y` 的元素。這才能保證我們找到的是「最長**嚴格遞增**子序列」。

根據我們的分析，我們需要 `y` 座標是嚴格遞增的，因此必須使用 `upper_bound`。

**AC 100%**
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#define int long long
using namespace std;

inline bool cmp(pair<int, int> a, pair<int, int> b) {
    if(a.first == b.first)
        return a.second < b.second;
    return a.first < b.first ;
}

inline void solve() {
    int n;cin >> n;
    vector<pair<int, int> > v(n);
    for(int i = 0;i < n;i++)
        cin >> v[i].first >> v[i].second;

    sort(v.begin(), v.end(), cmp);

    vector<int> y(n);
    for(int i = 0;i < n;i++) {
        y[i] = v[i].second;
    }

    vector<int> lis;

    for(int i = 0;i < n;i++) {
        // upper_bound ensures a strictly increasing subsequence.
        auto it = upper_bound(lis.begin(), lis.end(), y[i]);
        if(it == lis.end()) {
            lis.push_back(y[i]);
        }else {
            *it = y[i];
        }
    }
    cout << lis.size() << '\n';
    return ;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

## 複雜度分析
*   **時間複雜度**: O(N log N)。
    *   對 `n` 個點排序的時間是 O(N log N)。
    *   對 `y` 座標序列計算 LIS，需要遍歷 `n` 個元素，每次在 `lis` 陣列中進行一次二分搜尋（O(log N)），所以總時間也是 O(N log N)。
*   **空間複雜度**: O(N)。
    *   需要 O(N) 的空間來儲存點的向量 `v` 和 `y` 座標陣列。
    *   LIS 演算法中的 `lis` 陣列最多也只會儲存 `n` 個元素。