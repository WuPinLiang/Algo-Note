# 低地距離

## 問題描述
給定一個長度為 `2n` 的序列，其中包含從 1 到 `n` 的每個整數恰好兩次。對於每個整數 `i`（從 1 到 `n`），你需要計算在它的兩個出現位置之間，有多少個數字 `j` 滿足 `j < i`。

## 核心解題思路
這個問題可以高效地通過**離線處理**或**掃描線演算法**結合**數據結構**來解決。核心思想是：當我們處理一個數字 `i` 時，所有比 `i` 小的數字 `j` 都已經被「處理」過了。我們需要做的就是統計這些已經處理過的、比 `i` 小的數字中，有多少個落在 `i` 的兩個出現位置之間。

### 演算法步驟 (適用於 BIT 和 Segment Tree)

1.  **預處理**: 遍歷輸入序列，記錄每個數字的兩個出現位置。可以使用 `map<int, vector<int>> mp`，其中 `mp[value]` 儲存 `[pos1, pos2]`。
2.  **數據結構**: 我們需要一個支持以下操作的數據結構：
    *   **點更新 (Point Update)**: 將某個位置標記為「已出現」（例如，將該位置的值設為 1）。
    *   **區間求和 (Range Sum Query)**: 查詢某個區間內「已出現」位置的總數。
    *   **二元索引樹 (Binary Indexed Tree, BIT)** 和**線段樹 (Segment Tree)** 都能滿足這些要求。
3.  **主循環**: 按照數字的**值**從 1 到 `n` 進行遍歷。
    *   對於當前處理的數字 `i`：
        *   獲取其兩個出現位置：`left_pos = mp[i][0]` 和 `right_pos = mp[i][1]`。
        *   **計算答案**: 查詢數據結構，計算在區間 `(left_pos, right_pos)` 內有多少個位置已經被標記。這個數量就是比 `i` 小且位於 `i` 兩個出現位置之間的數字個數。
            *   具體查詢為 `query(right_pos - 1) - query(left)`。
        *   **標記當前數字的位置**: 將 `left_pos` 和 `right_pos` 在數據結構中標記為「已出現」。這樣，當處理比 `i` 大的數字時，`i` 的位置就可以被計入。

## BIT 實現詳解

### BIT 核心操作
*   `lowbit(x)`: 函式返回 `x` 的最低有效位（例如 `lowbit(4) = 4`, `lowbit(6) = 2`）。
*   `update(pos, val)`: 在 `pos` 位置增加 `val`。它會更新 `pos` 及其所有祖先節點。
*   `query(pos)`: 查詢從 1 到 `pos` 的前綴和。它會累加 `pos` 及其所有父節點的值。

### 程式碼解析 (BIT 版本)
```cpp
#include <iostream>
#include <vector>
#include <map>
#define int long long
#define N 200010 // Max possible position (2*n)
using namespace std;

int bit[N]; // Binary Indexed Tree array

inline int lowbit(int x) {
    return x & (-x);
}

inline int query(int pos) { // Get prefix sum up to pos
    int sum = 0;
    for(int i = pos;i > 0;i -= lowbit(i)) {
        sum += bit[i];
    }
    return sum ;
}

inline void update(int pos, int val) { // Add val to element at pos
    for(int i = pos;i < N;i += lowbit(i)) {
        bit[i] += val;
    }
    return ;
}

inline void solve() {
    int n;
    cin >> n;
    vector<int> v(2 * n + 1); // 1-based indexing for positions
    map<int, vector<int> > mp; // mp[value] = [pos1, pos2]
    for(int i = 1;i <= 2 * n;i++) {
        cin >> v[i];
        mp[v[i]].push_back(i);
    }

    int ans = 0;
    // Iterate through values from 1 to n
    for(int i = 1;i <= n;i++) {
        int left = mp[i][0]; // First occurrence of value i
        int right = mp[i][1]; // Second occurrence of value i

        // Count marked positions in (left, right)
        // query(right - 1) gives sum up to right-1
        // query(left) gives sum up to left
        // Their difference gives sum in (left, right-1]
        ans += query(right - 1) - query(left);

        // Mark the positions of current value i
        update(left, 1);
        update(right, 1);
    }

    cout << ans << '\n';
    return ;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

## Segment Tree 實現詳解

### Segment Tree 核心操作
*   `Node` 結構體：通常儲存區間和 `val`。
*   `query(L, R, qL, qR, idx)`: 查詢在線段樹節點 `idx` 代表的區間 `[L, R]` 中，查詢範圍 `[qL, qR]` 的總和。
*   `update(L, R, pos, val, idx)`: 在線段樹節點 `idx` 代表的區間 `[L, R]` 中，將 `pos` 位置的值更新為 `val`。

### 程式碼解析 (Segment Tree 版本)
```cpp
#include <iostream>
#include <vector>
#include <map>
#define int long long
#define N 200010 // Max possible position (2*n)
using namespace std;

struct Node {
    int val; // Sum of values in this segment
    Node(int _val = 0) {
        val = _val;
    }
}arr[4 * N]; // Segment tree array

// Query for sum in range [qL, qR]
int query(int L, int R, int qL, int qR, int idx = 1) {
    // Current segment [L, R] is fully contained within query range [qL, qR]
    if(qL <= L and qR >= R) {
        return arr[idx].val;
    }
    // Current segment [L, R] is outside query range [qL, qR]
    if(qL > R or qR < L)  return 0;

    int M = (L + R) / 2; // Midpoint

    // Recursively query left and right children
    int Lans = query(L, M, qL, qR, 2 * idx);
    int Rans = query(M + 1, R, qL, qR, 2 * idx + 1);

    return Lans + Rans; // Sum results
}

// Update value at position 'pos' to 'val'
void update(int L, int R, int pos, int val, int idx = 1) {
    // Current segment [L, R] does not contain 'pos'
    if(L > pos or R < pos)  return ;

    // Leaf node: update its value
    if(L == R and L == pos) {
        arr[idx].val = val;
        return ;
    }

    int M = (L + R) / 2; // Midpoint

    // Recursively update in left or right child
    update(L, M, pos, val, 2 * idx);
    update(M + 1, R, pos, val, 2 * idx + 1);

    // Update parent node's sum
    arr[idx].val = arr[2 * idx].val + arr[2 * idx + 1].val;
    return ;
}

inline void solve() {
    int n;
    cin >> n;
    vector<int> v(2 * n + 1); // 1-based indexing for positions
    map<int, vector<int> > mp; // mp[value] = [pos1, pos2]
    for(int i = 1;i <= 2 * n;i++) {
        cin >> v[i];
        mp[v[i]].push_back(i);
    }

    int ans = 0;
    // Iterate through values from 1 to n
    for(int i = 1;i <= n;i++) {
        int left = mp[i][0]; // First occurrence of value i
        int right = mp[i][1]; // Second occurrence of value i

        // Count marked positions in [left, right]
        // The problem asks for numbers *between* the two occurrences,
        // so we query range (left, right) which is [left+1, right-1]
        ans += query(1, 2 * n, left + 1, right - 1); // Query range [left+1, right-1]

        // Mark the positions of current value i
        update(1, 2 * n, left, 1);
        update(1, 2 * n, right, 1);
    }

    cout << ans << '\n';
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
    *   預處理（記錄位置）：O(N)。
    *   主循環：`n` 次迭代。每次迭代包含兩次數據結構查詢和兩次更新。
    *   BIT 的查詢和更新操作都是 O(log M)，其中 M 是最大位置（`2N`）。
    *   Segment Tree 的查詢和更新操作也是 O(log M)。
    *   因此，總時間複雜度為 O(N log N)。
*   **空間複雜度**: O(N)。
    *   `mp` 映射：O(N)。
    *   BIT 陣列或 Segment Tree 陣列：O(N)。
