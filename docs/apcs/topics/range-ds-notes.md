# 幸運數字

## 問題描述
給定一個包含 `n` 個數字的序列 `v`。我們需要遞迴地定義並找出一個「幸運數字」。

對於一個給定的區間 `[L, R]`：
1.  找出該區間內的最小值 `min_val` 及其索引 `min_idx`。
2.  計算 `min_idx` 左側子區間 `[L, min_idx-1]` 的元素總和 `left_sum`。
3.  計算 `min_idx` 右側子區間 `[min_idx+1, R]` 的元素總和 `right_sum`。
4.  根據 `left_sum` 和 `right_sum` 的比較結果，遞迴地在其中一個子區間中尋找幸運數字：
    *   如果 `left_sum < right_sum`，則在右側子區間 `[min_idx+1, R]` 中尋找。
    *   如果 `left_sum > right_sum`，則在左側子區間 `[L, min_idx-1]` 中尋找。
    *   如果 `left_sum == right_sum`，則在右側子區間 `[min_idx+1, R]` 中尋找。
5.  遞迴的終止條件是當區間只剩下一個元素時 (`L == R`)，此時該元素 `v[L]` 就是幸運數字。

## 核心解題思路
這個問題是一個典型的**分治法 (Divide and Conquer)** 應用，並結合了高效的**區間查詢資料結構**。

1.  **分治法**: 遞迴函式 `f` 體現了分治思想。它將一個大問題（在 `[L, R]` 找幸運數字）分解為一個更小的子問題（在 `[L, min_idx-1]` 或 `[min_idx+1, R]` 找幸運數字）。
2.  **區間最小值查詢 (Range Minimum Query, RMQ)**: 為了在 O(log N) 時間內快速找出區間 `[L, R]` 中的最小值及其索引，我們使用**線段樹 (Segment Tree)**。
3.  **前綴和 (Prefix Sums)**: 為了在 O(1) 時間內快速計算任意區間的元素總和，我們使用**前綴和陣列**。

## 演算法詳解

### 1. 預處理
*   **前綴和陣列**: 建立一個 `prefix` 陣列，其中 `prefix[i]` 儲存 `v[1]` 到 `v[i]` 的所有元素之和。這樣，區間 `[L, R]` 的和就可以通過 `prefix[R] - prefix[L-1]` 快速計算。
*   **線段樹**: 建立一個線段樹來維護原始陣列 `v`。線段樹的每個節點將儲存其所代表區間內的最小值及其索引。

### 2. 遞迴函式 `f(v, prefix, left, right)`
*   **基本情況**: 如果 `left == right`，表示區間只剩一個元素，直接回傳 `v[left]`。
*   **查詢最小值**: 使用線段樹的 `query` 函式，在當前區間 `[left, right]` 中找到最小值 `min_val` 的索引 `m`。
*   **計算子區間和**: 
    *   `left_sum = sum(left, m - 1, prefix)`
    *   `right_sum = sum(m + 1, right, prefix)`
    *   需要注意處理空區間的情況，例如 `m-1 < left` 或 `m+1 > right` 時，對應的區間和為 0。
*   **遞迴呼叫**: 根據 `left_sum` 和 `right_sum` 的比較結果，遞迴呼叫 `f` 函式，傳入新的子區間。

## 程式碼
**AC 100%**
```cpp
#include <iostream>
#include <vector>
#define int long long
#define inf 1000000007
#define N 300005
using namespace std;

struct Node {
    int mn, mn_idx;

    Node(int _mn = inf, int _mn_idx = 0) {
        mn = _mn, mn_idx = _mn_idx;
    }
}arr[4 * N]; // Segment tree array

int n;

// Build the segment tree
inline void build(vector<int>& v, int left, int right, int idx = 1) {
    if(left == right) {
        arr[idx] = Node(v[left], left);
        return ;
    }

    int mid = (left + right) / 2;
    build(v, left, mid, 2 * idx);
    build(v, mid + 1, right, 2 * idx + 1);

    // Combine results from children
    if(arr[2 * idx].mn < arr[2 * idx + 1].mn) {
        arr[idx].mn = arr[2 * idx].mn;
        arr[idx].mn_idx = arr[2 * idx].mn_idx;
    }else {
        arr[idx].mn = arr[2 * idx + 1].mn;
        arr[idx].mn_idx = arr[2 * idx + 1].mn_idx;
    }
    return ;
}

// Query for minimum index in range [qL, qR]
int query(vector<int>& v, int left, int right, int qL, int qR, int idx = 1) {
    // Current segment [left, right] is outside query range [qL, qR]
    if(right < qL or left > qR) {
        return -1 ; // Indicate no valid minimum found
    }
    // Current segment [left, right] is fully contained within query range [qL, qR]
    else if(qL <= left and qR >= right) {
        return arr[idx].mn_idx;
    }

    int mid = (left + right) / 2;
    int lc = 2 * idx, rc = 2 * idx + 1;
    int l_ans = query(v, left, mid, qL, qR, lc);
    int r_ans = query(v, mid + 1, right, qL, qR, rc);

    // Combine results from left and right children
    if(l_ans == -1) return r_ans; // Only right child found a min
    if(r_ans == -1) return l_ans; // Only left child found a min

    // Both found a min, return the index of the smaller value
    if(v[l_ans] < v[r_ans]) {
        return l_ans;
    }return r_ans;
}

// Calculate sum using prefix sums
inline int sum(int left, int right, vector<int>& prefix) {
    if(left > right) return 0; // Empty range sum is 0
    if(left == 0) return prefix[right]; // Handle 0-based prefix sum if needed, but problem uses 1-based
    return prefix[right] - prefix[left - 1];
}

// Recursive function to find the lucky number
inline int f(vector<int>& v, vector<int>& prefix, int left, int right) {
    if(left == right) // Base case: single element
        return v[left];
    
    // Find minimum in current range
    int m = query(v, 1, n, left, right); // Query on original array range [1, n]

    // Calculate sums of left and right subarrays
    int l_ans = sum(left, m - 1, prefix);
    int r_ans = sum(m + 1, right, prefix);

    // Recursive calls based on sum comparison
    if(l_ans == r_ans) {
        return f(v, prefix, m + 1, right);
    }

    if(l_ans < r_ans) {
        return f(v, prefix, m + 1, right);
    }else // l_ans > r_ans
        return f(v, prefix, left, m - 1);
}

inline void void solve() {
    cin >> n;
    vector<int> v(n + 1), prefix(n+1); // 1-based indexing
    for(int i = 1;i <= n;i++) {
        cin >> v[i];
        prefix[i] = prefix[i - 1] + v[i];
    }
    build(v, 1, n); // Build segment tree on 1-based array
    int ans = f(v, prefix, 1, n); // Initial call for full range [1, n]
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

## 程式碼解析
*   `Node` 結構體：用於線段樹節點，儲存區間最小值 `mn` 及其索引 `mn_idx`。
*   `build` 函式：遞迴地構建線段樹。每個節點儲存其子節點中較小的值及其索引。
*   `query` 函式：實現區間最小值查詢。它會遞迴地在線段樹中查找指定區間 `[qL, qR]` 內的最小值索引。
*   `sum` 函式：利用前綴和陣列 `prefix`，在 O(1) 時間內計算指定區間 `[left, right]` 的總和。特別處理了空區間 (`left > right`) 返回 0 的情況。
*   `f` 函式：這是核心的遞迴分治函式。
    *   基本情況 `if(left == right)`：當區間縮小到一個元素時，直接回傳該元素。
    *   `query(v, 1, n, left, right)`：呼叫線段樹查詢，找到當前處理區間 `[left, right]` 中的最小值索引 `m`。注意這裡的 `1, n` 是原始陣列的範圍，`left, right` 是當前遞迴的範圍。
    *   `l_ans = sum(left, m - 1, prefix)` 和 `r_ans = sum(m + 1, right, prefix)`：計算左右子區間的和。
    *   根據 `l_ans` 和 `r_ans` 的比較結果，遞迴呼叫 `f` 函式，進入左邊或右邊的子區間。
*   `solve` 函式：主邏輯。讀取輸入，建立 `v` 和 `prefix` 陣列（使用 1-based indexing），構建線段樹，然後呼叫 `f` 函式開始尋找幸運數字。

## 複雜度分析
*   **時間複雜度**: O(N log N)。
    *   建立前綴和陣列：O(N)。
    *   建立線段樹：O(N)。
    *   遞迴函式 `f`：每次呼叫 `f` 都會進行一次線段樹查詢（O(log N)）和常數次的前綴和計算。由於每次遞迴都會將問題規模減半（或至少縮小），總的遞迴呼叫次數是 O(N)（類似於快速排序的遞迴樹，但每次只走一邊）。因此，總時間複雜度為 O(N log N)。
*   **空間複雜度**: O(N)。
    *   `v` 和 `prefix` 陣列：O(N)。
    *   線段樹 `arr`：O(4N) ≈ O(N)。
