# 搬家

## 問題描述

在一個 n x m 的網格中，每個格子都有一個特定形狀的水管。我們的目標是計算出，從任意一個水管開始，最多可以連接到多少個水管。這可以想像成，水流從某一點開始，能夠流經的最大範圍。

## 核心解題思路

這個問題可以被模型化為一個圖論問題。網格中的每一個水管都可以被視為圖上的一個**節點 (Node)**。如果兩個相鄰格子的水管可以互相連接，那麼就在這兩個節點之間建立一條**邊 (Edge)**。

如此一來，整個問題就轉換為：**找到這個圖中最大的連通塊 (Connected Component) 的大小**。

## 演算法說明

我們可以使用深度優先搜尋 (DFS) 或廣度優先搜尋 (BFS) 來解決這個問題。這裡我們以 DFS 為例。

### 1. 圖的建立 (Graph Construction)

*   **節點表示**：為了方便在程式中操作，我們需要將 `(i, j)` 這樣的二維座標轉換成一個唯一的整數 ID。一個常見的方法是 `id = i * m + j`，其中 `m` 是網格的寬度。
*   **邊的建立**：我們需要遍歷網格中的每一個格子 `(i, j)`。對於每個格子，我們檢查它的下方和右方（檢查這兩個方向就足夠了，避免重複建立邊）。
    *   **檢查下方**：如果 `(i, j)` 的水管有向下的接口，且它正下方 `(i+1, j)` 的水管有向上的接口，那麼就在 `id(i, j)` 和 `id(i+1, j)` 之間建立一條邊。
    *   **檢查右方**：如果 `(i, j)` 的水管有向右的接口，且它正右方 `(i, j+1)` 的水管有向左的接口，那麼就在 `id(i, j)` 和 `id(i, j+1)` 之間建立一條邊。
*   **資料結構**：我們可以使用**鄰接表 (Adjacency List)**，即 `vector<int> adj[N]`，來儲存這個圖。`adj[u]` 儲存了所有與節點 `u` 相連的節點。

### 2. 搜尋演算法 (DFS)

*   **走訪與計數**：我們遍歷所有 `n * m` 個節點。如果一個節點尚未被訪問過，就表示我們找到了一個新的連通塊。
*   從這個未訪問過的節點開始，執行 DFS。
*   在 DFS 過程中，我們遞迴地訪問所有透過邊相連的鄰居節點，並將它們標記為已訪問。同時，我們用一個計數器 `cnt` 來記錄這個連通塊中總共有多少個節點。
*   **更新答案**：每當一個 DFS 結束後，`cnt` 就代表了當前連通塊的大小。我們用一個全域變數 `ans` 來記錄目前為止發現的最大 `cnt`。

## 程式碼

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#include <map>
#define int long long
#define N 250005
#define inf 1000000007
using namespace std;

//上 右 下 左
map<char, vector<int> > mp = {
  {'X', {1, 1, 1, 1}},
  {'I', {1, 0, 1, 0}},
  {'H', {0, 1, 0, 1}},
  {'L', {1, 1, 0, 0}},
  {'7', {0, 0, 1, 1}},
  {'F', {0, 1, 1, 0}},
  {'J', {1, 0, 0, 1}},
  {'0', {0, 0, 0, 0}}
};

int n, m;

inline int id(int x, int y) {
    return x * m + y;
}

vector<int> vi(N, 0), adj[N];

int cnt = 0;

inline void dfs(int u) {
    cnt++;
    for(int v : adj[u]) {
        if(vi[v]) continue;
        vi[v] = true;
        dfs(v);
    }
}

inline void solve() {
    cin >> n >> m;
    vector<vector<char> > v(n, vector<char> (m));
    for(int i = 0;i < n;i++) {
        for(int j = 0;j < m;j++) {
            cin >> v[i][j];
        }
    }

    for(int i = 0;i < n;i++) {
        for(int j = 0;j < m;j++) {
            // 檢查上、下
            if(i + 1 < n and mp[v[i][j]][2] and mp[v[i + 1][j]][0]) {
                adj[id(i, j)].push_back(id(i + 1, j));
                adj[id(i + 1, j)].push_back(id(i, j));
            }
            //檢查左右
            if(j + 1 < m and mp[v[i][j]][1] and mp[v[i][j + 1]][3]) {
                adj[id(i, j)].push_back(id(i, j + 1));
                adj[id(i, j + 1)].push_back(id(i, j));
            }
        }
    }

    int ans = -inf;
    for(int i = 0;i < n;i++) {
        for(int j = 0;j < m;j++) {
            int idx = id(i, j);
            if(vi[idx]) continue;
            cnt = 0;
            dfs(idx);
            ans = max(ans, cnt);
        }
    }
    cout << ans - 1 << '\n';
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

*   `map<char, vector<int>> mp`: 這是一個很巧妙的設計。它將每種水管字符映射到一個長度為 4 的向量，分別代表該水管是否有「上、右、下、左」四個方向的接口。例如，`'L'` 對應 `{1, 1, 0, 0}`，表示它有向上和向右的接口。
*   `id(x, y)`: 將二維座標 `(x, y)` 轉換為一維的節點 ID，方便用作陣列索引。
*   `adj[N]`: 鄰接表，`adj[u]` 存儲所有與節點 `u` 直接相連的節點。
*   `vi[N]`: `visited` 陣列，用於在 DFS 中記錄一個節點是否已經被訪問過，避免無限循環。
*   `dfs(u)`: 從節點 `u` 開始進行深度優先搜尋。`cnt` 會在每次呼叫時累加，計算當前連通塊的大小。
*   **建圖迴圈**: 程式中的雙層 `for` 迴圈，遍歷所有格子，並根據 `mp` 的定義，檢查下方和右方是否可以連接，如果可以，就將對應的節點 ID 加入彼此的鄰接表。
*   **答案查找迴圈**: 另一個雙層 `for` 迴圈，遍歷所有節點。如果節點 `idx` 未被訪問，就以它為起點開始一次新的 DFS，並用 `ans` 更新最大連通塊的大小。
*   `cout << ans - 1`: 題目要求的輸出可能需要根據具體情境調整，這裡的 `-1` 可能是題目特定要求。

## 複雜度分析

*   **時間複雜度**: O(N * M)。
    *   建立圖的時間複雜度是 O(N * M)，因為我們遍歷了所有格子一次來建立邊。
    *   DFS 的總時間複雜度也是 O(N * M)。雖然看起來有多個 DFS，但每個節點和每條邊在所有 DFS 過程中，總共只會被訪問一次。圖的節點數是 `V = N * M`，邊數 `E` 最多約為 `2 * N * M`。DFS 的複雜度是 O(V + E)，所以是 O(N * M)。
*   **空間複雜度**: O(N * M)。
    *   主要空間開銷來自於鄰接表 `adj` 和訪問陣列 `vi`，它們的大小都與節點總數 `N * M` 成正比。
