# 階梯數字 (Digit DP)

## 問題描述
給定一個非常大的正整數 `n`（可能長達上萬位），計算從 1 到 `n` 的所有整數中，有多少個是「階梯數字」。

一個數字被稱為「階梯數字」，如果它的位數從左到右是**非遞減**的。例如，123, 447, 899 都是階梯數字，而 132, 548 則不是。

## 核心解題思路
由於 `n` 非常大，我們不可能從 1 遍歷到 `n` 來逐一檢查。這種「在一個大數範圍內計數符合特定數位規則的數字」的問題，是**數位 DP (Digit DP)** 的典型應用場景。

數位 DP 的核心思想是，我們不直接計數數字，而是**按位數從高到低（從左到右）構造**這些數字。我們使用一個帶有記憶化的遞迴函式（通常是 DFS）來進行計數，函式的參數會記錄當前構造的狀態。

## 數位 DP 詳解

### 狀態定義 (DFS 函式參數)
我們設計一個遞迴函式 `dfs(depth, last, tight)`，它會回傳在特定限制下，構造完剩餘位數能產生多少個有效的階梯數字。

*   `depth`: `int`，表示我們現在正準備填入第 `depth` 位的數字（從 0 開始）。
*   `last`: `int`，表示前一位（第 `depth-1` 位）填入的數字是什麼。這是為了滿足「非遞減」的規則，即當前位數必須大於等於 `last`。
*   `tight`: `bool`，這是一個關鍵的標記，代表「是否受到 `n` 的位數限制」。
    *   `tight = true`：表示到目前為止，我們填入的前 `depth` 位數字，都和 `n` 的前 `depth` 位完全相同。因此，我們在第 `depth` 位能填的數字，最大不能超過 `n` 的第 `depth` 位數字 `digit[depth]`。
    *   `tight = false`：表示在 `depth` 之前，我們已經填入了一個比 `n` 對應位數小的數字。這意味著我們已經「解開」了 `n` 的限制，接下來的任何位數都可以自由地填 0 到 9 的任何數字（只要滿足階梯數字規則即可）。

### 狀態轉移
在 `dfs(depth, last, tight)` 函式中，我們需要決定第 `depth` 位可以填入哪些數字 `d`。

1.  **確定 `d` 的下界**：根據階梯數字的定義，`d` 必須大於等於前一位數字 `last`。所以 `d` 的迴圈從 `last` 開始。
2.  **確定 `d` 的上界**：
    *   如果 `tight` 是 `true`，表示我們仍受 `n` 的限制，所以 `d` 最大只能到 `digit[depth]`。
    *   如果 `tight` 是 `false`，表示限制已解除，`d` 最大可以到 9。
3.  **遞迴呼叫**：對於每一個合法的 `d`，我們累加遞迴呼叫的結果：`ans += dfs(depth + 1, d, new_tight)`。
    *   `new_tight` 的計算：新的 `tight` 狀態取決於當前的 `tight` 和我們選擇的 `d`。只有當 `tight` 為 `true` **且** `d` 也取到了上界 `digit[depth]` 時，`new_tight` 才會是 `true`。在任何其他情況下，`new_tight` 都會變成 `false`。

### 基本情況 (Base Case)
*   當 `depth == len` 時，表示我們已經成功地構造完一個完整的、符合規則的階梯數字，所以我們回傳 1。

### 記憶化
為了避免重複計算相同的子問題（例如，`dfs(5, 3, false)` 可能會被多次呼叫），我們使用一個 `dp` 陣列來儲存計算過的結果：`dp[depth][last][tight]`。在函式開頭檢查 `dp` 值，如果已經計算過，就直接回傳。

## 程式碼
**AC 100%**
```cpp
#include <iostream>
#include <vector>
#include <cstring>
#define int long long
#define mod 1000000007

using namespace std;

string s;
vector<int> digit;
int dp[100005][10][2];
int len;

inline int dfs(int depth, int last, bool same) {
    if(dp[depth][last][same] != -1) return dp[depth][last][same];
    if(depth == len) {
        return 1;
    }
    int ans = 0;
    for(int i = last; i < 10;i++) {
        if(same and i > digit[depth]) {
            continue;
        }
        bool tmp_same = (same and i == digit[depth]) ? true : false;
        ans = (ans + dfs(depth + 1, i, tmp_same)) % mod;
    }
    return dp[depth][last][same] = ans % mod;
}

inline void solve() {
    for(int i = 0;i < s.size();i++) {
        digit.push_back((int)s.at(i) - '0');
    }
    memset(dp, -1, sizeof(dp));
    len = digit.size();
    cout << (dfs(0, 0, 1) - 1 + mod) % mod<< '
';
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    while(cin >> s) {
        digit.clear();
        solve();
    }
    return 0;
}
```

## 程式碼解析
*   `dp[100005][10][2]`: 記憶化陣列，對應 `dp[depth][last][tight]`。
*   `dfs(depth, last, same)`: 程式碼中的 `same` 參數就是我們所說的 `tight` 標記。
*   `for(int i = last; i < 10;i++)`: 迴圈的下界 `last` 確保了非遞減的特性。
*   `if(same and i > digit[depth])`: 迴圈的上界。如果 `same` (tight) 為真，則當前數字 `i` 不能超過 `n` 對應的數字 `digit[depth]`。
*   `bool tmp_same = (same and i == digit[depth]) ? true : false;`: 計算下一層遞迴的 `tight` 標記。
*   `cout << (dfs(0, 0, 1) - 1 + mod) % mod`:
    *   初始呼叫 `dfs(0, 0, 1)`：從第 0 位開始，前一位數字視為 0，`tight` 標記為 `true` (1)。
    *   `- 1`: 我們的計數方式會把「0」這個數字也算進去（當 `dfs` 找到一個全由 0 組成的數字時）。題目通常要求計算 1 到 `n`，所以需要把 0 的情況減掉。
    *   `+ mod) % mod`: 這是為了防止 `-1` 之後變成負數，是取模運算的標準做法。

## 複雜度分析
*   **時間複雜度**: O(L * 10 * 2 * 10) ≈ O(L)，其中 L 是 `n` 的位數長度。
    *   狀態總數為 `L * 10 * 2`。
    *   每個狀態的計算需要一個最多 10 次的迴圈。
    *   由於記憶化的存在，每個狀態只會被計算一次。
*   **空間複雜度**: O(L * 10 * 2)，主要來自 `dp` 陣列的大小。