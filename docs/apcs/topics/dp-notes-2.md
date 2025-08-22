# 內積

## 問題描述
給定兩個長度分別為 `n` 和 `m` 的整數陣列 `A` 和 `B`。我們可以選擇將陣列 `A` **翻轉**一次。我們的目標是，從 `A` 和 `B` 中找到一對長度相等、非空的子陣列，使得它們的**內積 (inner product)** 最大。

內積的計算方式為：若子陣列分別為 `[a_1, a_2, ..., a_k]` 和 `[b_1, b_2, ..., b_k]`，其內積為 `a_1*b_1 + a_2*b_2 + ... + a_k*b_k`。

## 核心解題思路
這是一個典型的動態規劃問題。問題的核心是找到以特定位置為結尾的子陣列所能產生的最大內積。

由於陣列 `A` 可以被翻轉，這個問題需要被拆解成兩個子問題：
1.  計算 `A` (不翻轉) 與 `B` 之間的最大子陣列內積。
2.  計算 `A` (翻轉後) 與 `B` 之間的最大子陣列內積。

最終的答案就是這兩個子問題結果中的最大值。

## 動態規劃詳解

### 狀態定義
我們定義 `dp[i][j]` 為：
**A 的子陣列必須以 `A[i]` 結尾，且 B 的子陣列必須以 `B[j]` 結尾時，這兩個等長子陣列所能產生的最大內積。**

### 狀態轉移
對於 `dp[i][j]`，我們在計算時有兩種可能性：

1.  **延續前一個狀態**：如果我們將 `A[i]` 和 `B[j]` 加入到以 `A[i-1]` 和 `B[j-1]` 結尾的最佳子陣列中，那麼新的內積會是 `dp[i-1][j-1] + A[i] * B[j]`。
2.  **重新開始一個新狀態**：如果 `dp[i-1][j-1]` 的值是負的，那麼延續它只會讓我們的總和變小。在這種情況下，不如直接從 `A[i]` 和 `B[j]` 開始一個新的長度為 1 的子陣列，其內積就是 `A[i] * B[j]`。

綜合這兩種情況，我們的狀態轉移方程就是：
`dp[i][j] = max(dp[i-1][j-1] + A[i] * B[j], A[i] * B[j])`

在計算 `dp` 表的過程中，我們需要一個全域變數 `ans` 來隨時記錄出現過的 `dp[i][j]` 的最大值，因為最大內積的子陣列可能在任何位置結束。

### 基本情況 (Base Cases)
`dp` 表的第一行和第一列需要被初始化，因為它們沒有 `dp[i-1][j-1]` 可以參考。
*   `dp[i][0] = A[i] * B[0]` for `i` from 0 to `n-1`.
*   `dp[0][j] = A[0] * B[j]` for `j` from 0 to `m-1`.

## 程式碼
**AC 100%**
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#define int long long
#define inf 1000000007
using namespace std;

int n, m;

inline int solve(vector<int>& a, vector<int>& b) {
    vector<vector<int> > dp(n, vector<int>(m, 0));

    dp[0][0] = max(0ll, a[0] * b[0]);

    int ans = -inf;

    for(int i = 0;i < n;i++) {
        dp[i][0] = a[i] * b[0];
        ans = max(ans, dp[i][0]);
    }

    for(int j = 0;j < m;j++) {
        dp[0][j] = a[0] * b[j];
        ans = max(dp[0][j], ans);
    }

    for(int i = 1;i < n;i++) {
        for(int j = 1;j < m;j++) {
            dp[i][j] = max(dp[i-1][j-1] + a[i] * b[j], a[i] * b[j]);
            ans = max(dp[i][j], ans);
        }
    }
    return ans;
}

signed main() {
    cin >> n >> m;
    vector<int> a(n), b(m);
    for(int i = 0;i < n;i++)
        cin >> a[i];
    for(int i = 0;i < m;i++)
        cin >> b[i];

    int x = solve(a, b);
    reverse(a.begin(), a.end());
    int y = solve(a, b);
    cout << max(x, y) << '\n';
    return 0;
}
```

## 程式碼解析
*   `solve(a, b)` 函式：這個函式接收兩個陣列，並回傳它們之間的最大子陣列內積。它完整地實作了上述的動態規劃邏輯。
*   `dp` 表初始化：程式碼中分別對第一行和第一列進行了初始化，並同時更新了 `ans`。
*   `dp` 狀態轉移：`dp[i][j] = max(dp[i-1][j-1] + a[i] * b[j], a[i] * b[j]);` 這行程式碼完美對應了我們的狀態轉移方程。
*   `main` 函式：
    *   讀取輸入資料。
    *   呼叫 `solve(a, b)` 計算 `A` 不翻轉時的最大內積，存於 `x`。
    *   使用 `reverse(a.begin(), a.end())` 將 `A` 陣列翻轉。
    *   再次呼叫 `solve(a, b)` 計算 `A` 翻轉後的狀況，存於 `y`。
    *   `cout << max(x, y) << '\n';` 輸出兩種情況中的最大值，即為最終答案。

## 複雜度分析
*   **時間複雜度**: O(N * M)。`solve` 函式中的主要運算是填充 `dp` 表，需要兩層 `for` 迴圈，因此時間複雜度為 O(N * M)。我們呼叫 `solve` 兩次，所以總時間是 O(2 * N * M)，簡化為 O(N * M)。
*   **空間複雜度**: O(N * M)。主要的空間開銷來自於 `dp` 表，其大小為 `n * m`。