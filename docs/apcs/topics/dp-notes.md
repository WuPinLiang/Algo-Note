# 置物櫃分配

## 問題描述

此問題可以被視為一個變形的子集合和問題 (Subset Sum Problem)。給定 `n` 個物品，每個物品有其大小。我們有一個總容量為 `m` 的置物櫃，以及一個最小需求空間 `s`。目標是從這 `n` 個物品中選擇一個子集合，使得所選物品的總大小 `total_size` 滿足 `total_size >= s - (m - sum_of_all_items)`，並在滿足此條件的前提下，最小化 `total_size`。

## 核心解題思路

這是一個典型的動態規劃 (Dynamic Programming) 問題，具體來說是 0/1 背包問題的變體。我們需要判斷是否能湊出特定的總和。

### 動態規劃狀態定義

*   `dp[j]`：一個布林值，表示是否可以從給定的物品中選擇一個子集合，使其總大小恰好為 `j`。

### 基本情況 (Base Case)

*   `dp[0] = true`：總和為 0 總是可行的，即不選擇任何物品。

### 狀態轉移 (Transition)

對於每個物品 `num`：

*   我們從 `j` 等於所有物品總和 `sum` 開始，遞減遍歷到 `num`。
*   `dp[j] = dp[j] or dp[j - num]`：如果總和 `j - num` 是可行的，那麼通過加上當前物品 `num`，總和 `j` 也將變得可行。
*   **重要**：`j` 必須從大到小遍歷。這是 0/1 背包問題的關鍵，確保每個物品 `num` 只被使用一次。如果從小到大遍歷，`num` 可能會被重複使用。

### 最終答案

在填充完 `dp` 表後，我們需要找到滿足條件的最小總和。

1.  計算 `need`：這是我們至少需要湊到的總和。根據問題描述，`need = max(0LL, s - (m - sum_of_all_items))`。`m - sum_of_all_items` 是置物櫃剩餘的空間，`s - (m - sum_of_all_items)` 則是我們需要額外湊出的空間。`max(0LL, ...)` 確保 `need` 不會是負數。
2.  從 `need` 開始，向上遍歷到所有物品的總和 `sum_of_all_items`。第一個遇到的 `j` 使得 `dp[j]` 為 `true` 的，就是我們的答案。

## 程式碼
```cpp
#include <iostream>
#include <vector>
#define int long long
using namespace std;

inline void solve() {
    int m, s, n;
    cin >> m >> s >> n;

    int sum = 0;
    vector<int> v(n);
    for(int i = 0;i < n;i++) {
        cin >> v[i];
        sum += v[i];
    }

    int need = max(0LL, s - (m - sum));
    vector<bool> dp(sum + 1, false);
    dp[0] = true;

    for (int x : v) {
        for (int j = sum; j >= x; j--) {
            if (dp[j - x]) dp[j] = true;
        }
    }

    for (int i = need; i <= sum; i++) {
        if (dp[i]) {
            cout << i << '\n';
            return;
        }
    }
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);
    solve();
    return 0;
}
```

## 程式碼解析

### WA 35% 版本的問題

*   **`target` 計算**：`int target = m - sum + s;` 這個計算方式是錯誤的，它沒有正確反映出需要湊出的最小總和。
*   **`dp` 陣列大小**：`vector<bool> dp(m, 0);` `dp` 陣列的大小應該是所有物品總和 `sum` 加上 1，而不是 `m`。因為我們需要判斷是否能湊出從 0 到 `sum` 之間的任何總和。

### AC 100% 版本

*   **`need` 的正確計算**：`int need = max(0LL, s - (m - sum));` 確保了我們尋找的目標總和是正確的。
*   **`dp` 陣列大小**：`vector<bool> dp(sum + 1, false);` `dp` 陣列的大小被正確設置為 `sum + 1`，能夠覆蓋所有可能的子集合和。
*   **遍歷順序**：`for (int j = sum; j >= x; j--)` 確保了每個物品 `x` 只被考慮一次，符合 0/1 背包的特性。
*   **答案查找**：`for (int i = need; i <= sum; i++)` 從最小需求 `need` 開始查找，保證找到的是滿足條件的最小總和。

## 複雜度分析

*   **時間複雜度**：O(N * S)，其中 N 是物品的數量，S 是所有物品的總和。這是因為我們對每個物品，都需要遍歷一次 `dp` 陣列（從 `sum` 到 `num`）。
*   **空間複雜度**：O(S)，用於儲存 `dp` 陣列。