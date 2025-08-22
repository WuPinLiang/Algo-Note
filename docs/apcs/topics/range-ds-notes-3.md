# 切割費用

## 問題描述
想像有一條長度為 `L` 的線段，其兩端點分別為 0 和 `L`。現在，我們將 `n` 個點依序插入到這條線段上。每插入一個點，它會將其所在的線段區間一分為二。每次插入的「費用」定義為該點所切割的區間的長度。計算總共的切割費用。

例如：線段 `[0, 10]`。
1.  插入點 4。它切割了 `[0, 10]`，費用為 10。線段變為 `[0, 4], [4, 10]`。
2.  插入點 7。它切割了 `[4, 10]`，費用為 6。線段變為 `[0, 4], [4, 7], [7, 10]`。
總費用為 10 + 6 = 16。

## 核心解題思路
這個問題的關鍵在於，每次插入一個新的切割點時，我們需要快速找到它左右兩邊最近的已存在切割點。由於切割點的數量會逐漸增加，並且需要保持有序，`std::set`（或任何平衡二元搜尋樹的實現）是解決這個問題的理想數據結構。

`std::set` 能夠自動維護元素的有序性，並提供高效的查找操作（例如 `upper_bound` 和 `lower_bound`），這使得我們能夠在對數時間內找到新點左右兩側的鄰居。

## 演算法詳解

1.  **初始化**：
    *   創建一個 `std::set<int> st`，用於儲存所有已存在的切割點。
    *   將線段的兩個初始端點 0 和 `L` 插入到 `st` 中。
    *   初始化總切割費用 `ans = 0`。

2.  **依序處理插入點**： 
    *   按照題目給定的順序，遍歷每一個要插入的點 `x_i`。
    *   對於當前的點 `x_i`：
        *   **找到左右鄰居**：使用 `st.upper_bound(x_i)` 找到 `st` 中第一個嚴格大於 `x_i` 的元素。這個元素就是 `x_i` 右邊最近的切割點，我們稱之為 `right`。
        *   `x_i` 左邊最近的切割點 `left`，可以通過找到 `right` 的前一個元素來獲得（例如 `std::prev(it_right)`）。
        *   **計算費用**：當前點 `x_i` 所在的區間就是 `(left, right)`。這個區間的長度是 `right - left`。將這個長度加到 `ans` 中。
        *   **插入新點**：將 `x_i` 插入到 `st` 中，使其成為新的切割點。

3.  **最終答案**：遍歷完所有 `n` 個點後，`ans` 中儲存的就是總切割費用。

## 程式碼
**AC 100%**
```cpp
#include <iostream>
#include <vector>
#include <set> // For std::set
#include <algorithm> // For std::prev (if needed, though not explicitly used in the final code's logic)
#define int long long // Use long long for sums to prevent overflow
using namespace std;

inline void solve() {
    int n, l; // n: number of points, l: total length of segment
    cin >> n >> l;
    vector<int> v(n + 1); // v[num] stores the coordinate of the num-th point
    for(int i = 0;i < n;i++) {
        int x, num; // x: coordinate, num: insertion order
        cin >> x >> num;
        v[num] = x; // Store coordinate by its insertion order
    }

    set<int> st; // Stores existing cut points, automatically sorted
    st.insert(0); // Insert left endpoint
    st.insert(l); // Insert right endpoint

    int ans = 0; // Total cutting cost
    for(int i = 1;i <= n;i++) { // Iterate through points in insertion order
        // Find the first element in set strictly greater than v[i]
        auto it1 = st.upper_bound(v[i]); 
        // it1 now points to 'right' (the first cut point to the right of v[i])

        // Find the element just before it1. This is 'left'.
        // In C++, --it1 is equivalent to std::prev(it1).
        // If v[i] is already in the set, upper_bound(v[i]) points to the element after v[i].
        // Decrementing it then points to v[i] itself. This is correct for finding the segment it divides.
        auto it2 = it1; 
        --it2; 

        int right = *it1;
        int left = *it2;

        ans += (right - left); // Add the length of the segment being cut

        st.insert(v[i]); // Insert the new cut point
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

## 程式碼解析
*   `v[num] = x;`: 題目輸入的點是 `(x, num)` 形式，表示第 `num` 個插入的點的座標是 `x`。我們用 `v` 陣列來按插入順序儲存這些座標。
*   `set<int> st; st.insert(0); st.insert(l);`: 初始化 `set`，包含線段的兩個端點 0 和 `L`。
*   `for(int i = 1; i <= n; i++)`: 按照點的插入順序遍歷。
*   `auto it1 = st.upper_bound(v[i]);`: 找到 `v[i]` 右邊最近的切割點 `right`。
*   `auto it2 = it1; --it2;`: 找到 `v[i]` 左邊最近的切割點 `left`。`it1` 指向 `v[i]` 右邊第一個元素，`--it2` 則指向 `v[i]` 左邊第一個元素（即 `v[i]` 所在的區間的左端點）。
*   `ans += (right - left);`: 將當前被切割的區間長度加到總費用中。
*   `st.insert(v[i]);`: 將新的切割點 `v[i]` 加入 `set`。

## 複雜度分析
*   **時間複雜度**: O(N log N)。
    *   讀取輸入並儲存點：O(N)。
    *   主循環遍歷 `n` 個點。
    *   在 `set` 中進行 `upper_bound` 查找操作：每次 O(log K)，其中 K 是 `set` 中元素的數量（最多 `N+2`）。
    *   在 `set` 中插入操作：每次 O(log K)。
    *   因此，總時間複雜度為 O(N log N)。
*   **空間複雜度**: O(N)。
    *   `v` 陣列：O(N)。
    *   `set`：最多儲存 `N+2` 個元素，所以是 O(N)。