# 互補 CP

## 問題描述

此問題旨在尋找給定字串集合中，有多少對字串是「互補」的。互補的定義是，在考慮前 `m` 個字母的情況下，兩個字串的字元集合合併後恰好包含這 `m` 個字母的所有種類。例如，若 `m=3` (A, B, C)，字串 "AB" 和 "C" 互補，因為它們的字元集合 {A, B} 和 {C} 合併後是 {A, B, C}。

## 核心解題思路

本題的核心在於利用 **位元遮罩 (bitmask)** 來高效地表示每個字串所包含的字元集合，並結合 **雜湊表 (hash map)** 來快速查找互補的字元集合。由於題目測資規模較大，暴力枚舉所有字串對會導致超時，因此需要更優化的方法。

1.  **位元遮罩表示字元集合**：對於前 `m` 個字母，我們可以使用一個整數的 `m` 個最低位來表示它們是否存在。例如，如果 `m=3`，`001` (二進位) 可以表示只包含 'C'，`011` 表示包含 'B' 和 'C'。這樣，每個字串的字元集合都可以被壓縮成一個唯一的整數。
2.  **尋找互補集合**：如果一個字串的位元遮罩是 `mask`，那麼它的互補集合的位元遮罩就是 `mask` 與一個包含所有 `m` 個字母的「完整遮罩」(`full_mask`) 進行 **XOR 運算** 的結果 (`mask XOR full_mask`)。這是因為 XOR 運算會將 `mask` 中為 1 的位元變為 0，將為 0 的位元變為 1，正好得到其補集。
3.  **雜湊表計數**：使用一個 `unordered_map` 來儲存每個位元遮罩出現的頻率。當處理一個字串時，計算其位元遮罩 `tmp` 和互補遮罩 `complement_mask`。如果 `complement_mask` 已經在雜湊表中，就將其頻率加到總答案中。然後，將 `tmp` 的頻率加一。

## 逐步解題邏輯

1.  **初始化 `full_mask`**：計算一個 `full_mask`，它是一個所有 `m` 個最低位都為 1 的整數。這可以通過 `(1LL << m) - 1` 來實現。
2.  **遍歷輸入字串**：對於每個輸入字串：
    a.  **生成字串的位元遮罩 `tmp`**：遍歷字串中的每個字元。將字元轉換為 0 到 `m-1` 之間的索引（例如 'A' -> 0, 'B' -> 1, ...）。然後，將 `1LL` 左移該索引位，並與 `tmp` 進行位元 OR 運算 (`|=`)，以標記該字元的存在。**注意：只有當字元索引小於 `m` 時才進行位元操作，這是 WA 75% 和 AC 100% 版本的關鍵區別。**
    b.  **計算互補遮罩 `complement_mask`**：`complement_mask = tmp XOR full_mask`。
    c.  **查找互補對**：在 `freq` 雜湊表中查找 `complement_mask`。如果找到，表示之前已經處理過一個與當前字串互補的字串，將 `freq[complement_mask]` 的值加到總答案 `ans` 中。
    d.  **更新頻率**：將當前字串的位元遮罩 `tmp` 的頻率在 `freq` 雜湊表中加一 (`freq[tmp]++`)。
3.  **輸出結果**：最終的 `ans` 即為互補字串對的數量。

## 程式碼

```cpp
#include <iostream>
#include <vector>
#include <unordered_map>
#define int long long
#define fastio ios_base::sync_with_stdio(false);
using namespace std;

inline int ctoi(char c) {
    if(c >= 'A' and c <= 'Z') return c - 'A';
    return c - 'a' + 26;
}

inline void solve() {
    int n, m;
    cin >> m >> n;

    int full = (1ll << m) - 1;

    unordered_map<int, int> freq;
    int ans = 0;

    for(int i = 0;i < n;i++) {
        string s;cin >> s;
        int tmp = 0;
        for(int c : s) {
            int idx = ctoi(c);
            if(idx < m)
               tmp |= 1ll << (int)(idx);
        }
        if(freq.find(tmp xor full) != freq.end()) {
            ans += freq[tmp xor full];
        }
        freq[tmp] ++;
    }
    cout << ans << '\n';
    return ;
}

inline void test() {
    cout << " a " <<  (int)'a' << " A " <<  (int)'A' << '\n';
    return ;
}

signed main() {
    fastio
    //test();
    solve();
    return 0;
}
// (int)'A' < (int) 'a'
```

## 程式碼解析

### `ctoi` 函數

*   將字元轉換為整數索引。例如，'A' 轉換為 0，'B' 轉換為 1。這個函數在處理字元時非常有用，確保它們能正確地映射到位元遮罩的位元位置。

### `solve` 函數

*   **`full = (1ll << m) - 1;`**: 創建一個位元遮罩，其中前 `m` 位都設置為 1。這代表了所有 `m` 個字母的集合。
*   **`unordered_map<int, int> freq;`**: 雜湊表，用於儲存每個位元遮罩出現的頻率。
*   **`tmp |= 1ll << (int)(c - 'A');` (WA 75% 版本)**: 這個版本沒有檢查字元索引是否在 `m` 的範圍內。如果輸入字串包含的字元超出了前 `m` 個字母的範圍（例如 `m=3` 但字串包含 'D'），那麼 `(c - 'A')` 會產生一個大於等於 `m` 的索引，導致 `tmp` 包含不應考慮的位元，從而計算出錯誤的互補對。
*   **`if(idx < m) tmp |= 1ll << (int)(idx);` (AC 100% 版本)**: 這是修正後的關鍵部分。它確保只有在前 `m` 個字母範圍內的字元才被納入位元遮罩的計算。這保證了 `tmp` 僅反映了與 `m` 相關的字元集合，從而正確地找到互補對。
*   **`if(freq.find(tmp xor full) != freq.end()) { ans += freq[tmp xor full]; }`**: 這是查找互補對並累加答案的邏輯。`tmp xor full` 計算出當前字串的互補遮罩，然後在 `freq` 中查找其頻率。
*   **`freq[tmp] ++;`**: 將當前字串的位元遮罩的頻率加一，為後續的查找做準備。

## 複雜度分析

*   **時間複雜度**：O(N * L + U)，其中 N 是輸入字串的數量，L 是字串的最大長度，U 是唯一位元遮罩的數量。在最壞情況下，U 可以達到 2^m，但通常會遠小於此。由於 `m` 通常較小（例如 26），所以位元遮罩的生成和雜湊表操作都非常高效。
*   **空間複雜度**：O(U)，用於儲存雜湊表。在最壞情況下，U 可以達到 2^m。