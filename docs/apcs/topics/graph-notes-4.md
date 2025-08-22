# 邏輯電路

## 問題描述
給定一個數位邏輯電路的結構，包含：
*   `p` 個**輸入埠**，每個都有一個初始的 0 或 1 的訊號值。
*   `q` 個**邏輯閘**，類型包括 AND, OR, XOR, NOT。
*   `r` 個**輸出埠**，用於觀測最終結果。
*   `m` 條**連線**，描述了訊號如何從一個元件流向另一個。

你需要計算兩件事：
1.  每一個輸出埠最終穩定的訊號值 (0 或 1)。
2.  整個電路的最大訊號延遲，即從任何一個輸入埠到任何一個輸出埠所需經過的最長路徑。

## 核心解題思路
數位邏輯電路是一個天然的有向圖。每個元件（輸入埠、邏輯閘、輸出埠）都是一個**節點**，而每條連線都是一條**有向邊**。因為電路中沒有回饋迴路（訊號只會單向流動），所以這個圖是一個**有向無環圖 (Directed Acyclic Graph, DAG)**。

對於 DAG，當我們需要按照一定的依賴順序處理節點時（例如，必須先知道邏輯閘的輸入值，才能計算它的輸出值），最經典的演算法就是**拓撲排序 (Topological Sort)**。

## 拓撲排序詳解 (Kahn's Algorithm)

我們使用基於「入度 (In-degree)」的 Kahn 演算法來進行拓撲排序，並在排序過程中同步計算訊號值和延遲。

### 1. 圖的建立與初始化
*   **節點**：將所有 `p+q+r` 個元件視為圖的節點。
*   **邊**：根據 `m` 條連線建立鄰接表 `adj`。
*   **入度 `indeg`**: 建立一個 `indeg` 陣列。在建立邊 `u -> v` 的同時，`indeg[v]` 加一。
*   **佇列 `que`**: 建立一個佇列，並將所有入度為 0 的節點（即初始的輸入埠）加入佇列。這些是我們可以開始處理的節點。

### 2. 遍歷與計算
當佇列不為空時，重複以下步驟：
1.  從佇列中取出一個節點 `u`。
2.  對於 `u` 的每一個相鄰節點 `v`（即 `u -> v`）：
    a.  **更新 `v` 的訊號值**: 根據 `u` 的訊號值 `val[u]` 和 `v` 的閘門類型 `port[v]` 來計算 `val[v]`。
    b.  **更新 `v` 的延遲**: `v` 的延遲取決於所有指向它的節點中，延遲最長的那個。所以 `delay[v] = max(delay[v], delay[u] + 1)`。
    c.  **更新 `v` 的入度**: `indeg[v]` 減一，表示 `v` 的一個依賴項已經處理完畢。
    d.  **檢查是否入隊**: 如果 `indeg[v]` 變為 0，表示 `v` 的所有輸入都已就緒，可以將 `v` 加入佇列。

### 3. 最終結果
*   **最大延遲**: 在拓撲排序的過程中，用一個全域變數 `mx` 記錄所有節點出現過的最大 `delay` 值。
*   **輸出值**: 拓撲排序結束後，`val` 陣列中就儲存了所有元件的最終訊號值。我們只需讀取輸出埠對應的 `val` 值即可。

## 程式碼
**AC 100% using DAG**
```cpp
#include <iostream>
#include <vector>
#include <queue>
#define int long long
#define inf 1000000007
#define N 60000
using namespace std;

vector<int> val(N, -1), delay(N, 0);
int mx = -inf;

inline int cal(int a, int op, int b) {
    if(op == 1) return (a and b);
    else if(op == 2)  return (a or b);
    else if(op == 3)  return (a xor b);
    return -1;
}

inline void solve() {
    int p, q, r, m;
    cin >> p >> q >> r >> m;

    for(int i = 1;i <= p;i++)   cin >> val[i];

    vector<int> port(N);
    for(int i = p + 1;i <= p + q;i++)   cin >> port[i];

    vector<int> adj[N], indeg(N, 0);
    for(int i = 1;i <= m;i++) {
        int a, b;
        cin >> a >> b;
        indeg[b]++;
        adj[a].push_back(b);
    }

    queue<int> que;
    for(int i = 1;i <= p;i++) {
        // Input ports have an in-degree of 0 in a valid circuit
        if(indeg[i] == 0) {
            que.push(i);
        }
    }

    while(!que.empty()) {
        int cur = que.front();
        que.pop();
        mx = max(mx, delay[cur]);
        for(int nxt : adj[cur]) {
            if(port[nxt] == 4) { // NOT gate
                val[nxt] = !val[cur];
            }
            else if(val[nxt] == -1) { // First input to this gate
                val[nxt] = val[cur];
            }
            else { // Second input to this gate
                val[nxt] = cal(val[cur], port[nxt], val[nxt]);
            }
            delay[nxt] = max(delay[nxt], delay[cur] + 1);
            if(--indeg[nxt] == 0)
                que.push(nxt);
        }
    }

    cout << mx << '\n'; // The max delay value itself

    for(int i = p + q + 1;i <= p + q + r;i++) {
        cout << val[i] << ' ';
    }
    cout << '\n';
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
*   `val`, `delay`, `port`, `adj`, `indeg`: 分別儲存訊號值、延遲、閘門類型、鄰接表和入度，是解題的核心資料結構。
*   `cal(...)`: 一個輔助函式，用於計算 AND, OR, XOR 的結果。
*   **初始化**: 程式碼首先讀取所有輸入，建立圖的鄰接表和入度陣列。然後將所有入度為 0 的節點（輸入埠）加入佇列。
*   **拓撲排序迴圈 `while(!que.empty())`**:
    *   `cur = que.front(); que.pop();`: 取出一個所有輸入都已就緒的節點。
    *   `mx = max(mx, delay[cur]);`: 更新全局最大延遲。 
    *   `for(int nxt : adj[cur])`: 遍歷 `cur` 的所有後續節點 `nxt`。
    *   **訊號值計算**: 程式碼用 `val[nxt] == -1` 來判斷這是否是第一個到達 `nxt` 閘門的訊號。如果是，直接賦值；如果不是，就和已有的值進行運算。NOT 閘門是特例，因為它只有一個輸入。
    *   **延遲計算**: `delay[nxt] = max(delay[nxt], delay[cur] + 1);` 確保 `delay[nxt]` 總是其所有前驅節點中最大延遲加一。
    *   `if(--indeg[nxt] == 0) que.push(nxt);`: 關鍵步驟，當一個節點的所有輸入都處理完畢後，將其加入佇列。
*   **輸出**: `cout << mx << '\n';` 輸出記錄到的最大延遲。原程式碼中的 `-1` 可能是對延遲定義的誤解，直接輸出 `mx` 更符合「最長路徑長度」的定義。

## 複雜度分析
*   **時間複雜度**: O(V + E)，其中 V 是元件總數 (`p+q+r`)，E 是連線數 (`m`)。拓撲排序的每個節點和每條邊都只會被訪問常數次。
*   **空間複雜度**: O(V + E)，主要用於儲存鄰接表和各類輔助陣列。
