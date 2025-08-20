# 進階圖論

## BCC (Biconnected Component)

**定義**：最大的不含割點的連通子圖。
**特性**：任何一個 $BCC$ 內部，刪掉任意一個點後，圖仍然連通。

## 割點 (Articulation Point)

**定義**：對於一個連通分量，如果刪掉某個點後使得圖分裂成兩個或多個連通分量，那這個點就是**割點**。

### 怎麼找割點？

建立陣列 `dfn` 紀錄每一個被探訪的時間，以及 `low` 紀錄一步之內最多可以回溯到的節點：

* 若一個點能回溯到比父節點更早的節點，表示它不需要經過父節點就能回到祖先 → 它不是割點。

注意：

* `low(i)` 表示能回到的最上層節點，數字越小越「高」。
* 若某個點最上能回到的節點 = 父節點，代表刪掉父節點會斷開 → 父節點是割點。

### 邏輯

* `dfn[i]`：節點 `i` 被 DFS 探訪的時間。
* `low[i]`：節點 `i` 或子樹能回溯到的最早祖先的 `dfn` 值。
* 若 `low[nxt] >= dfn[i]`，代表子節點 `nxt` 無法繞過 `i` 回到更高的祖先 → `i` 是割點。
* 根節點要特別處理：若只有一個子節點，則不是割點。

```cpp
inline void dfs(int cur, int pa = -1) {
    int child_cnt = 0;
    dfn[cur] = low[cur] = ord++;
    for(int nxt : adj[cur]) {
        if(!dfn[nxt]) {
            child_cnt ++;
            dfs(nxt, cur);
            low[cur] = min(low[cur], low[nxt]);
            if(low[nxt] >= dfn[cur])
                cut[cur] = 1;
        } else if(nxt != pa) {
            low[cur] = min(low[cur], dfn[nxt]);
        }
    }
    if(child_cnt == 1 && dfn[cur] == 1)
        cut[cur] = 0;
}
```

> 上述程式主要是找割點。

---

## 找橋 (Bridge)

邏輯與割點類似：

* 維護 `dfn`（進入時間）與 `low`（能回溯到的最早節點）。
* 對於一條邊 `(u,v)`，若 `low[v] > dfn[u]`，則這條邊是橋。

```cpp
vector<pii> bridge;
vector<int> adj[N];
vector<int> dfn(N, 0), low(N, inf);
int ord = 1;

inline void dfs(int cur, int pa = -1) {
    dfn[cur] = low[cur] = ord++;
    for(int nxt : adj[cur]) {
        if(!dfn[nxt]) {
            dfs(nxt, cur);
            low[cur] = min(low[cur], low[nxt]);
            if(low[nxt] > dfn[cur]) {
                bridge.push_back({cur, nxt});
            }
        } else if(nxt != pa) {
            low[cur] = min(low[cur], dfn[nxt]);
        }
    }
}

inline void solve() {
    cin >> n >> m;
    for(int i = 0;i < m;i++) {
        int a, b;cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    for(int i = 1;i <= n;i++) {
        if(!dfn[i]) dfs(i);
    }
    cout << bridge.size() << '\n';
    for(auto [a, b] : bridge) {
        cout << a << ' ' << b << '\n';
    }
}
```

---

## 強連通分量 (Strongly Connected Component, SCC)

**定義**：在有向圖中，如果 `u` 可以到 `v`，且 `v` 也能到 `u`，則 `u,v` 屬於同一個 SCC。

### Kosaraju 演算法

時間複雜度：$O(N+M)$

1. 在反向圖上 $DFS$，記錄完成順序。
2. 在正向圖上，依照完成順序反向進行 $DFS$，劃分 $SCC$。

```cpp
int n, m;
vector<int> adj[N], revadj[N], scc_id(N, 0), pos, vis(N, 0);

inline void revdfs(int cur) {
    vis[cur] = 1;
    for(int nxt : revadj[cur]) if(!vis[nxt]) revdfs(nxt);
    pos.push_back(cur);
}

inline void dfs(int cur, int val) {
    scc_id[cur] = val;
    for(int nxt : adj[cur]) if(!scc_id[nxt]) dfs(nxt, val);
}

inline void kosaraju() {
    for(int i = 1;i <= n;i++) if(!vis[i]) revdfs(i);
    int cnt = 0;
    for(int i = n-1;i >= 0;i--) {
        int tmp = pos[i];
        if(!scc_id[tmp]) dfs(tmp , ++cnt);
    }
    cout << cnt << '\n';
    for(int i = 1;i <= n;i++) cout << scc_id[i] << ' ';
    cout << '\n';
}
```

---

## 賽局理論 (Game Theory)

### Nim's Game

有 $n$ 堆石頭，兩人輪流拿石頭（至少 $1$ 個），誰最後無法操作誰輸。

結論：

* 若 `xor sum == 0` → 後手勝
* 否則 → 先手勝

```cpp
int t;cin >> t;
while(t--) {
    int n;cin >> n;
    int sum = 0;
    for(int i = 0;i < n;i++) {
        int num;cin >> num;
        sum ^= num;
    }
    cout << (sum==0 ? "second\n" : "first\n");
}
```

### DP + Game Theory

給定 $n$, $k$ 種可拿石子數，dp\[i] 表示當前局面是否必勝。

```cpp
int x, n;cin >> x >> n;
vector<int> v(n), dp(x+1);
for(int i=0;i<n;i++) cin>>v[i];
for(int i=0;i<=x;i++) {
    for(int j=0;j<n;j++) {
        if(i-v[j]>=0 && !dp[i-v[j]]) dp[i]=1;
    }
}
for(int i=1;i<=x;i++) cout << "LW"[dp[i]];
```

---

## Bitmask DP

例題：電梯問題（$CSES 1653$）。
狀態 `dp[s] = {rides, last_weight}`。

```cpp
#include <iostream>
#include <vector>
#define int long long 
#define inf 1000000007
 
using namespace std ;
using pii = pair<int, int> ;
 
inline void solve() {
    int n, w;cin >> n >> w;
    vector<int> v(n);
    for(int i = 0;i < n;i++)
        cin >> v[i];
    vector<pii> dp(1 << n, {inf, inf});
    dp[0] = {1, 0};
    for(int s = 0;s < (1 << n);s++) {
        for(int i = 0;i < n;i++) {
            if((s & (1 << i)) == 0) {
                pii tmp = dp[s];
                if(tmp.second + v[i] <= w) {
                    tmp.second += v[i];
                }else {
                    tmp.first ++;
                    tmp.second = v[i];
                }
                
                if(tmp < dp[(s | (1 << i))]) {
                    dp[(s | (1 << i))] = tmp;
                }
            }
        }
    }
 
    //for(int s = 0;s < (1 << n);s++)
    //    cout << dp[s].first << ' ' << dp[s].second << '\n';
    cout << dp[(1 << n) - 1].first << '\n';
    return ;
}
 
signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
 
// bit-mask dp 

```

---

## 區間 DP

### 例題 1：取石子遊戲（最大差值）

```cpp
vector<vector<int>> dp(N, vector<int>(N,0));
int f(int l,int r){
    if(l>r) return 0;
    if(l==r) return v[l];
    if(dp[l][r]) return dp[l][r];
    return dp[l][r]=max(v[r]-f(l,r-1), v[l]-f(l+1,r));
}
```

### 例題 2：取石子遊戲（第一人最大值）

```cpp
vector<vector<int>> dp(N, vector<int>(N,0)), psum(N,0);
int f(int l,int r){
    if(l>r) return 0;
    if(l==r) return v[l];
    if(dp[l][r]) return dp[l][r];
    return dp[l][r] = psum[r]-psum[l-1]-min(f(l+1,r), f(l,r-1));
}
```
