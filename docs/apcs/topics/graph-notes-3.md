# 真假子圖

## 問題描述
給定 `n` 個節點和 `m` 條關係，每條關係表示兩個節點 `a` 和 `b` **必須**屬於不同的集合（或被塗上不同的顏色）。這構成了初始的關係狀態。

接著，有 `p` 個獨立的測試情境。在每個情境中，你需要陸續加入 `k` 條新的「不同集合」關係。你的任務是，對於每個情境，判斷在哪一條新關係加入時，會與之前的關係（包括初始的 `m` 條和這個情境中已經加入的）產生矛盾。

如果產生矛盾，輸出該情境的編號。一個情境結束後，下一個情境開始前的關係狀態會**重置**回最初的 `m` 條關係。

## 核心解題思路
這個問題要求我們維護一組「互斥」關係，並動態地加入新關係和檢查矛盾。這是「擴展域並查集」（或稱「帶權並查集」、「朋友的敵人是朋友」模型）的典型應用。

我們不能只用一個普通的並查集來記錄「屬於相同集合」，因為我們需要表達「必須屬於不同集合」這一核心資訊。

## 擴展域並查集詳解

### 擴展域 (The "Domain")
對於每一個節點 `i`（`1 <= i <= n`），我們在並查集中創建兩個元素：
*   `i`: 代表 `i` 本身。
*   `i + n`: 代表 `i` 的「敵人」或「對立集合」中的元素。

這樣，我們把並查集的大小擴展到了 `2n`。

### 關係的表示
利用這個擴展域，我們可以表達兩種關係：

1.  **`a` 和 `b` 在同一集合**: 如果我們要表示這個關係，我們會合併 `a` 和 `b`，同時合併它們的敵人 `a+n` 和 `b+n`。
    *   `unite(a, b)`
    *   `unite(a+n, b+n)`

2.  **`a` 和 `b` 在不同集合**: 這是本題用到的關係。如果 `a` 和 `b` 不同，就意味著 `a` 和 `b` 的敵人 (`b+n`) 是同類，`b` 和 `a` 的敵人 (`a+n`) 也是同類。
    *   `unite(a, b+n)`
    *   `unite(b, a+n)`

### 檢查矛盾
矛盾發生在什麼時候？當我們要宣告 `a` 和 `b` **必須不同**，卻發現它們已經因為先前的關係而**必須相同**時。

*   在執行 `unite(a, b+n)` 和 `unite(b, a+n)` 之前，我們先檢查 `a` 和 `b` 是否已經在同一個集合中。
*   檢查方法是 `find(a) == find(b)`。如果為真，就表示矛盾發生了。

## 程式碼
**AC 100%**
```cpp
#include <iostream>
#include <vector>
#define int long long
#define N 20005

using namespace std;

int n, m;
int pa[2 * N], sz[2 * N];

vector<int> ori; // Resized in solve

inline int fnd(int x) {
    if(x == pa[x])  return x;
    return pa[x] = fnd(pa[x]);
}

inline void unite(int x, int y) {
    int px = fnd(x), py = fnd(y);
    if(px == py)  return ;
    if(sz[px] > sz[py]) swap(px, py);
    pa[px] = py;
    sz[py] += sz[px];
    return ;
}

// Resets DSU and applies the initial m constraints.
inline void reset_and_apply_initial_constraints() {
     for(int i = 0;i < 2 * N;i++) {
        pa[i] = i;sz[i] = 1;
    }
    for(int i = 0;i < 2 * m;i += 2) {
        int a = ori[i], b = ori[i + 1];
        unite(a, b + n);
        unite(a + n, b);
    }
}

inline void solve() {
    cin >> n >> m;
    ori.resize(2 * m);
    for(int i = 0;i < 2 * m;i++) {
        cin >> ori[i];
    }

    int p, k;
    cin >> p >> k;

    vector<int> ans;

    for(int i = 1;i <= p;i++) { // Loop through p scenarios
        reset_and_apply_initial_constraints(); // Reset for each new scenario
        bool flag = true;
        for(int j = 0;j < k;j++) {
            int a, b;
            cin >> a >> b;
            if(flag) { // If no contradiction found yet in this scenario
                if(fnd(a) == fnd(b)) {
                    flag = false;
                    ans.push_back(i);
                } else {
                    unite(a, b + n);
                    unite(a + n, b);
                }
            }
        }
    }

    for(int i = 0;i < ans.size();i++) {
        cout << ans[i] << '\n';
    }
    return ;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

## 程式碼解析
*   `pa[2 * N]`: 並查集的父指標陣列。大小為 `2*N` 以容納 `n` 個節點和它們各自的 `n` 個「敵人」。
*   `fnd(x)` 和 `unite(x, y)`: 標準的並查集「查找」和「合併」操作（帶路徑壓縮和按大小合併優化）。
*   `reset_and_apply_initial_constraints()`: 這個函式的作用是重置並查集，並將最初的 `m` 條互斥關係應用上去。
*   **主邏輯 `solve()`**:
    *   讀取 `n`, `m` 和初始的 `m` 條關係。
    *   **情境迴圈 `for(int i = 1; i <= p; i++)`**: 處理 `p` 個獨立的測試情境。
    *   **重置狀態**: 在每個情境開始前，呼叫 `reset_and_apply_initial_constraints()` 將 DSU 恢復到只有 `m` 條初始關係的狀態。
    *   **關係迴圈 `for(int j = 0; j < k; j++)`**: 在一個情境中，陸續加入 `k` 條關係。
    *   `if(flag)`: 檢查本情境是否已出現矛盾。如果還沒有，才進行邏輯判斷，這可以避免在一個已經失敗的情境中重複記錄答案。
    *   `if(fnd(a) == fnd(b))`: 這是矛盾檢查點。如果發現 `a` 和 `b` 已經在同一個集合，就將 `flag` 設為 `false` 並記錄情境編號 `i`。
    *   `else { unite(a, b + n); unite(a + n, b); }`: 如果沒有矛盾，就應用這個新的互斥關係。

## 複雜度分析
*   **時間複雜度**: O(M*α(N) + P * (M + K)*α(N))。其中 α(N) 是反阿克曼函數，因為使用了優化後的並查集，其單次操作時間極快，可視為接近常數。每個情境都需要重置(M)和處理(K)條關係。
*   **空間複雜度**: O(N + M)。主要來自並查集的 `pa`, `sz` 陣列（O(N)）和儲存初始關係的 `ori` 向量（O(M)）。
