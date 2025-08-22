# 病毒演化

## 問題描述
給定 `n` 個病毒的演化關係，這些關係構成一棵樹。同時，給定每個病毒的一段長度為 `m` 的 DNA 序列。序列中的字元可能是 'A', 'U', 'G', 'C' 四種之一，或是一個代表未知的 '@'。

定義兩個病毒之間的「演化成本」為它們 DNA 序列的**漢明距離**（Hamming distance），即兩個序列在相同位置上字元不同的次數。

你的任務是，為所有序列中的 '@' 指派一個具體的字元（A/U/G/C），使得整棵演化樹的**總演化成本**（所有相鄰病毒對之間的成本總和）最小。你需要輸出這個最小的總成本。

## 核心解題思路
這個問題看似複雜，但有兩個關鍵的簡化思路：

1.  **按位獨立計算**: 總成本是所有相鄰節點間漢明距離的總和。漢明距離又是按位相加的。這意味著 DNA 序列的**每一個位置（每一欄）的最小成本計算是相互獨立的**。我們可以分別計算出第 0 欄、第 1 欄、...、第 `m-1` 欄的最小成本，然後把它們全部加起來，就是最終的總最小成本。

2.  **樹狀動態規劃 (Tree DP)**: 經過簡化後，問題變成了：對於某一欄，樹上的一些節點字元是固定的，一些是未知的('@')，如何為未知節點指派字元，使得樹上所有邊的成本（如果兩端字元不同，成本為 1，相同則為 0）總和最小？這是一個經典的樹狀 DP 問題。

## 樹狀 DP 詳解

對於某一固定的欄位，我們來設計 DP 狀態。

### 狀態定義
`dp[u][c]`：表示在以節點 `u` 為根的子樹中，如果節點 `u` 被指派為字元 `c`（`c` 是 A, U, G, C 之一），那麼該子樹內部的最小總演化成本是多少。

### 狀態轉移
我們使用**後序遍歷 (Post-order Traversal)** 的方式，從葉節點一路向上計算到根節點。

對於一個非葉節點 `u`，假設我們想計算 `dp[u][c_u]`（即 `u` 被指派為字元 `c_u` 的成本）：
這個成本由 `u` 的所有子樹貢獻。對於 `u` 的每一個子節點 `v`，我們需要為 `v` 選擇一個最佳的字元 `c_v`，使得 `v` 的子樹貢獻的成本最小。

`v` 的子樹貢獻的成本 = (`v` 和 `u` 之間的邊的成本) + (`v` 的子樹內部的最小成本)
= `(c_u == c_v ? 0 : 1) + dp[v][c_v]`

為了讓 `v` 的子樹總貢獻最小，我們應該為 `v` 選擇一個 `c_v` 來最小化 `dp[v][c_v] + (c_u == c_v ? 0 : 1)`。

因此，`u` 的狀態轉移方程為：
`dp[u][c_u] = sum( min( dp[v][c_v] + (c_u == c_v ? 0 : 1) ) for all c_v in {A,U,G,C} )`
這個加總需要對 `u` 的所有子節點 `v` 進行。

### 基本情況 (Base Cases)
DP 的基本情況（或說初始化）發生在 `dfs` 訪問到節點 `u`，但在遞迴處理其子節點之前：

*   如果節點 `u` 在當前欄的字元是固定的（例如 'A'），那麼它只能被指派為 'A'。
    *   `dp[u]['A'] = 0`
    *   `dp[u][c] = infinity` （對於 `c != 'A'`）
*   如果節點 `u` 在當前欄的字元是未知的 ('@')，那麼它可以被指派為任何字元，且自身不產生任何成本。
    *   `dp[u][c] = 0` （對於所有 `c`）

## 程式碼
**AC 100%**
```cpp
#include <iostream>
#include <vector>
#define N 100005
#define inf 1000000007
#define int long long
using namespace std;

vector<int> adj[N];
vector<string> s(N);
vector<char> c(N);

vector<vector<int> > dp(N, vector<int> (4, inf));

int root = 0, n, m, ans = 0;

inline int char2idx(char tmp) {
    if(tmp == 'A')  return 0;
    else if(tmp == 'U') return 1;
    else if(tmp == 'G') return 2;
    else if(tmp == 'C') return 3;
    return -1;
}

inline void dfs(int cur ,int pa) {
    // Base Case / Initialization for node 'cur'
    if(c[cur] == '@') {
        for(int i = 0;i < 4;i++) {
            dp[cur][i] = 0;
        }
    } else if(char2idx(c[cur]) != -1) {
        int idx = char2idx(c[cur]);
        for(int i = 0;i < 4;i++) {
            dp[cur][i] = (i == idx ? 0 : inf);
        }
    }

    // Recursive step (Post-order)
    for(int nxt : adj[cur]) {
        if(nxt == pa)   continue;
        dfs(nxt, cur);
        // State Transition: Aggregate results from child 'nxt'
        for(int i = 0;i < 4;i++) { // For each char choice for parent 'cur'
            if(dp[cur][i] == inf) continue;
            int mi = inf;
            for(int j = 0;j < 4;j++) { // For each char choice for child 'nxt'
                mi = min(mi, dp[nxt][j] + ((i == j) ? 0 : 1));
            }
            dp[cur][i] += mi;
        }
    }
    return ;
}

inline void solve() {
    cin >> n >> m;
    for(int i = 0;i < n;i++) {
        int a, b;
        cin >> a >> b;
        a--, b--;
        if(a == b)  root = a;
        else {
            adj[a].push_back(b);
            adj[b].push_back(a);
        }
        cin >> s[a];
    }
    // Main loop: solve for each column independently
    for(int i = 0;i < m;i++) {
        vector<char> tmp;
        for(int j = 0;j < n;j++) {
            tmp.push_back(s[j][i]);
        }
        c = tmp; // Set the global character column for the DFS

        dfs(root, -1);

        int mn = inf;
        for(int j = 0;j < 4;j++) {
            mn = min(mn, dp[root][j]);
        }
        ans += mn;
    }
    cout << ans << '\n';
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

## 程式碼解析
*   `solve()`: 主函式。外層的 `for` 迴圈遍歷 DNA 序列的每一欄 (`i` from 0 to `m-1`)。
*   `c = tmp`: 在每次迴圈中，將當前欄的所有字元存入全局變數 `c`，供 `dfs` 函式使用。
*   `dfs(root, -1)`: 對當前欄位，從根節點開始執行樹狀 DP。
*   `dfs` 函式內部：
    *   **初始化**: 函式開頭的部分根據 `c[cur]` 的值（'@' 或特定字元）來初始化 `dp[cur]` 陣列，這對應了 DP 的基本情況。
    *   **遞迴**: `for(int nxt : adj[cur]) ... dfs(nxt, cur)` 體現了後序遍歷，先解決子樹問題。
    *   **狀態轉移**: 遞迴返回後，`for(int i=0...){...for(int j=0...){...}}` 的巢狀迴圈，就是在執行狀態轉移方程，將子節點 `nxt` 的最小成本累加到父節點 `cur` 上。
*   `ans += mn`: 在一次 `dfs` 結束後，`dp[root]` 中儲存了根節點分別取 4 種字元時，整棵樹的最小成本。我們取其中的最小值 `mn`，累加到最終答案 `ans` 中。

## 複雜度分析
*   **時間複雜度**: O(M * N * C²)，其中 M 是序列長度，N 是病毒數量，C 是字元集大小（本題為 4）。
    *   我們對 M 欄分別求解。
    *   每一欄的求解是一次 DFS。DFS 訪問每個節點一次。
    *   在每個節點 `u`，我們需要遍歷它的所有子節點 `v`。對於每個 `v`，我們用一個 C*C 的迴圈來計算狀態轉移。所以每個節點的總計算量是 O(degree(u) * C²)。
    *   整棵樹的總計算量是 O(Σ(degree(u) * C²)) = O(E * C²) = O(N * C²)，其中 E 是邊數。
*   **空間複雜度**: O(N*C + N*M)。`dp` 表需要 O(N*C)，儲存輸入的 DNA 序列需要 O(N*M)。
