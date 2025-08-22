# 美食博覽會

## 問題描述
給定一個由 `n` 個數字組成的序列，每個數字代表一種食物。我們的目標是找到一個最長的連續子序列（子陣列），使得這個子序列中的所有食物種類都是**獨一無二**的（即沒有重複的食物）。

## 核心解題思路
這是一個經典的**滑動窗口 (Sliding Window)** 或**雙指針 (Two Pointers)** 問題。我們維護一個動態的窗口 `[left, right]`，並確保窗口內的元素滿足「所有食物種類獨一無二」的條件。

演算法步驟如下：
1.  初始化左指針 `left = 0`，最大長度 `max_length = 0`。
2.  使用一個哈希表（`map` 或 `unordered_map`）`mp` 來記錄當前窗口內每個食物種類的出現頻率。
3.  右指針 `right` 從 0 開始向右遍歷整個序列。
    *   當 `right` 指針向右移動時，將 `v[right]` 加入到當前窗口中，並更新 `mp` 中 `v[right]` 的頻率。
    *   **檢查窗口有效性**：如果 `v[right]` 的頻率在加入後變為大於 1（表示出現了重複），或者在加入 `v[right]` 之前 `v[right]` 就已經存在於 `mp` 中（這表示 `v[right]` 是重複的），那麼當前窗口就是無效的。
    *   **收縮窗口**：當窗口無效時，我們需要移動 `left` 指針向右收縮窗口，直到窗口再次變為有效。每次移動 `left`，就將 `v[left]` 從窗口中移除（更新 `mp` 中 `v[left]` 的頻率，如果頻率歸零則從 `mp` 中刪除）。
    *   **更新最大長度**：在每次 `right` 指針移動後，窗口 `[left, right]` 都是有效的。此時，更新 `max_length = max(max_length, right - left + 1)`。

## 程式碼
**WA 50%** (此程式碼解決的是「最長不重複子陣列」問題)
```cpp
#include <iostream>
#include <vector>
#include <map>
#define int long long
#define inf 1000000007
using namespace std;

inline void solve() {
    int n, k; // Note: k is read but not used in this specific solution
    cin >> n >> k;
    vector<int> v(n);
    for(int i = 0;i < n;i++)
        cin >> v[i];

    int left = 0, mx = 0; // Initialize mx to 0 for empty array case

    map<int, int> mp; // Stores frequency of elements in the current window

    for(int right = 0;right < n;right++) {
        // While the current element v[right] is already in the map (meaning it's a duplicate in the current window)
        while(mp.count(v[right]) && left <= right) {
            mp[v[left]]--; // Decrease count of element at left pointer
            if(mp[v[left]] == 0) {
                mp.erase(v[left]);
            }
            left++; // Shrink window from left
        }

        mp[v[right]]++; // Add current element v[right] to the window

        mx = max(mx, right - left + 1); // Update max length of valid window
    }

    cout << mx << '\n';

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
*   `left`, `right`: 滑動窗口的左右指針。
*   `mp`: `map<int, int>` 用於儲存窗口內每個數字的頻率。
*   `for(int right = 0; right < n; right++)`: 右指針 `right` 遍歷整個陣列，擴展窗口。
*   `while(mp.count(v[right]) && left <= right)`: 這是收縮窗口的條件。如果 `v[right]` 在當前窗口中已經存在（即 `mp` 中有它的記錄），則表示引入了重複元素，窗口無效。此時，`left` 指針向右移動，並從 `mp` 中移除 `v[left]`，直到窗口再次有效。
*   `mp[v[right]]++;`: 將 `v[right]` 加入窗口。
*   `mx = max(mx, right - left + 1);`: 更新找到的最長有效子陣列長度。

## 複雜度分析
*   **時間複雜度**: O(N)。`left` 和 `right` 指針都只會向右移動，每個元素最多被訪問和處理兩次（一次被 `right` 訪問，一次被 `left` 訪問）。`map` 的操作（插入、刪除、查找）在平均情況下是 O(log D)，其中 D 是窗口中不同元素的數量。如果使用 `unordered_map`，平均情況下是 O(1)。
*   **空間複雜度**: O(D)。`map` 的空間開銷取決於窗口中不同元素的數量。在最壞情況下，所有元素都不同，D 等於 N。

## 關於 `k` 和「分段 DP」的說明
原題的提示中提到了 `k` 和「分段 DP」。這暗示了這個問題可能有一個更通用的版本，例如：
*   找到最長子陣列，其中包含**至多 `k` 種不同**的元素。
*   找到最長子陣列，其中允許**至多 `k` 個重複**的元素。

對於這些更通用的問題，滑動窗口的條件和收縮邏輯會有所不同。而「分段 DP」則可能用於解決更複雜的變體，例如允許在子陣列中跳過某些部分，或者在多個不連續的子陣列中尋找最佳解。由於這裡沒有提供更通用的 AC 程式碼，我們無法對其進行詳細分析。