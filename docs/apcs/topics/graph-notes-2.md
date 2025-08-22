# Tree Distance I (CSES 1132)

## 問題描述
給定一棵包含 `n` 個節點的樹。對於樹中的每一個節點，我們需要找出從該節點出發，到樹中其他任意節點的最長路徑長度是多少。

## 核心解題思路
如果我們為每一個節點都做一次 DFS/BFS 來找出最長路徑，那麼總時間複雜度會是 O(N * (N+M)) = O(N^2)，對於 N=200005 的規模來說太慢了。

一個更高效的方法是使用**樹狀動態規劃**，通過**兩次 DFS** 遍歷來解決。

對於任何一個節點 `u`，從它出發的最長路徑，只可能有兩種情況：
1.  路徑完全在 `u` 的**子樹**中（我們稱之為「向下」路徑）。
2.  路徑需要先經過 `u` 的父節點（我們稱之為「向上」路徑），然後可能再走到其他分支。

因此，我們的目標是為每個節點 `u`，分別計算出這兩種路徑的最大長度。

*   **第一次 DFS (`dfs1`)**: **由下而上**的計算。為每個節點 `u` 計算出，從 `u` 出發「向下」能走的最遠距離，記為 `down[u]`。
*   **第二次 DFS (`dfs2`)**: **由上而下**的計算。在 `down` 值已知的基礎上，為每個節點 `u` 計算出，從 `u` 出發「向上」能走的最遠距離，記為 `up[u]`。

最終，對於節點 `u` 的答案就是 `max(down[u], up[u])`。

## 演算法詳解

### 第一次 DFS (`dfs1`) - 計算 `down` 值
這是一個**後序遍歷 (Post-order Traversal)**。我們必須先知道所有子節點的 `down` 值，才能計算父節點的 `down` 值。

*   對於節點 `u`，我們先遞迴呼叫 `dfs1` 處理它的所有子節點 `v`。
*   當遞迴返回後，我們就得到了所有 `down[v]` 的值。
*   `down[u]` 的值，就是 `u` 到其最深的子節點的路徑長度。因此，`down[u] = max(down[v] + 1)`，這裡的 `+1` 代表的是從 `u` 到 `v` 的這條邊。

### 第二次 DFS (`dfs2`) - 計算 `up` 值
這是一個**前序遍歷 (Pre-order Traversal)**。我們需要將父節點的資訊傳遞給子節點。

*   對於節點 `u`，它「向上」的最長路徑 `up[u]` 是已知的。現在我們要計算它的某個子節點 `v` 的 `up[v]`。
*   從 `v` 出發的「向上」路徑有兩種可能：
    1.  先從 `v` 走到 `u`，然後再沿著 `u` 的「向上」路徑走。長度為 `up[u] + 1`。
    2.  先從 `v` 走到 `u`，然後再沿著 `u`「向下」的路徑走到 `u` 的**另一個**子節點 `v'` 的子樹中。長度為 `down[v'] + 2` ( `v -> u -> v'` 是 2 步)。
*   因此，`up[v] = max(up[u] + 1, max(down[v'] + 2))`，其中 `v'` 是 `v` 的所有兄弟節點。
*   **優化**：為了高效計算 `max(down[v'])`，我們可以在 `dfs2` 訪問 `u` 時，預先找出其所有子節點中 `down` 值最大和次大的兩個。
    *   當我們要計算的子節點 `v` 正好是 `down` 值最大的那個分支時，我們就用次大的 `down` 值來計算 `up[v]`。
    *   對於其他子節點，我們都用最大的 `down` 值來計算。

## 程式碼
**AC 100%**
```cpp
#include <iostream>
#include <vector>
#define int long long
#define N 200005
#define inf 1000000007

using namespace std;

vector<int> adj[N], up(N, 0), down(N, 0);

inline void dfs1(int u, int p) {
    for(int v : adj[u]) {
        if(v == p)  continue;
        dfs1(v, u);
        down[u] = max(down[u], down[v] + 1);
    }
}

inline void dfs2(int u, int p) {
    int max1 = -1, max2 = -1;
    for(int v : adj[u]) {
        if(v == p)  continue;
        if(down[v] > max1) {
            max2 = max1;
            max1 = down[v];
        } else if(down[v] > max2) {
            max2 = down[v];
        }
    }

    for(int v : adj[u]) {
        if(v == p)  continue;
        int use = (down[v] == max1) ? max2 : max1;
        up[v] = max(up[u] + 1, use + 2);
        dfs2(v, u);
    }
}

inline void solve() {
    int n;cin >> n;
    int a, b;
    for(int i = 0;i < n - 1;i++) {
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    dfs1(1, 0);
    dfs2(1, 0);

    for(int i = 1;i <= n;i++) {
        cout << max(up[i], down[i]) << ' ';
    }
    cout << '
';
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
*   `dfs1(u, p)`: 實作了第一次 DFS。`p` 是父節點，用於防止遍歷時走回頭路。`down[u] = max(down[u], down[v] + 1);` 這行完美體現了由下而上的 DP 計算。
*   `dfs2(u, p)`: 實作了第二次 DFS。
    *   第一個 `for` 迴圈：遍歷 `u` 的所有子節點，找出 `down` 值的最大 `max1` 和次大 `max2`。
    *   第二個 `for` 迴圈：再次遍歷 `u` 的所有子節點 `v`，準備為它們計算 `up[v]`。
    *   `int use = (down[v] == max1) ? max2 : max1;`: 這是優化的關鍵。如果 `v` 就在最長的分支上，那麼 `u` 向下走的其他最長路徑就是 `max2`；否則，就是 `max1`。
    *   `up[v] = max(up[u] + 1, use + 2);`: 計算 `up[v]`。`up[u] + 1` 對應第一種情況（沿著父節點的 `up` 路徑）。`use + 2` 對應第二種情況（走到兄弟節點的分支），`use` 是兄弟節點的 `down` 值，`+2` 是因為 `v -> u -> v'` 走了兩步。
    *   `dfs2(v, u);`: 遞迴下去，將計算好的 `up` 值傳遞給下一層。
*   `main` 函式：標準的圖輸入處理，然後依序呼叫 `dfs1` 和 `dfs2`，最後輸出每個節點的 `max(up[i], down[i])`。

## 複雜度分析
*   **時間複雜度**: O(N)。兩次 DFS 都只會訪問每個節點和每條邊常數次。
*   **空間複雜度**: O(N)。用於儲存鄰接表 `adj` 以及 `up` 和 `down` 陣列。