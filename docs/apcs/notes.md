# APCS 觀念、實作要五級分

> 有很多我還沒有 AC 的題目，我下面會一個一個列出來，就當作是要練習的題單，但是我會先以真的考古題練習，模擬的就先等等

---

## 互補 CP

> **觀察題目**
> 從題目測資可以知道暴力解是絕對不可能的。
>
> **Approach**
> 對於題目給的一個整數 `m`（討論前 `m` 個字母），你可以用一個整數來儲存哪些字母出現過，最後再用 **hash map** 維護哪些組合出現過即可。
>
> **要怎麼用一個整數存？**
> 其實就是用二進位表示法來實作。

**WA 75%**

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
            tmp |= 1ll << (int)(c - 'A');
        }
        if(freq.find(tmp xor full) != freq.end()) {
            ans += freq[tmp xor full];
        }
        freq[tmp] ++;
    }
    cout << ans << '\n';
    return ;
}

signed main() {
    fastio
    solve();
    return 0;
}
```

**AC 100%**

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

signed main() {
    fastio
    solve();
    return 0;
}
```

---

## 置物櫃分配

> **直覺**：原以為可貪心，但有反例，應改用 DP。
> **問題重述**：給 `n` 個數字與 `target`，以這些數湊出的和要滿足 `sum >= target`。
> **定義**：`dp(j)` 能否湊出 `j`；**base**：`dp(0) = 1`。
> **轉移**：`dp(j) = dp(j) or dp(j - num)`（倒序 j 以避免重複計算）。

**WA 35%**

```cpp
#include <iostream>
#include <vector>
#define int long long
using namespace std;

inline void solve() {
    int n, m, s;
    cin >> m >> s >> n;

    int sum = 0;
    vector<int> v(n);
    for(int i = 0;i < n;i++) {
        cin >> v[i];
        sum += v[i];
    }

    int target = m - sum + s;
    vector<bool> dp(m, 0);
    dp[0] = 1;
    for(int num : v) {
        for(int j = m;j >= num;j--) {
            if(dp[j]) continue;
            dp[j] = dp[j] or dp[j - num];
        }
    }

    for(int i = target;i <= m;i++) {
        if(dp[i]) {
            cout << i << '\n';
            return ;
        }
    }
    return ;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#define int long long
using namespace std;

inline void solve() {
    int m, s, n;
    cin >> m >> s >> n;

    int sum = 0;
    vector<int> v(n);
    for(int i = 0;i < n;i++) {
        cin >> v[i];
        sum += v[i];
    }

    int need = max(0LL, s - (m - sum));
    vector<bool> dp(sum + 1, false);
    dp[0] = true;

    for (int x : v) {
        for (int j = sum; j >= x; j--) {
            if (dp[j - x]) dp[j] = true;
        }
    }

    for (int i = need; i <= sum; i++) {
        if (dp[i]) {
            cout << i << '\n';
            return;
        }
    }
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0); cout.tie(0);
    solve();
    return 0;
}
```

---

## 飛黃騰達

> **題意**：給 `n` 個二維點 `(x,y)`，從原點出發，只能往 `x,y` 皆不小於當前位置的點移動，最多經過幾點？
> **反例**：僅分別對 `x` 或 `y` 排序會失敗。
> **正解**：先依 `x` 排序，再對 `y` 取嚴格遞增的 LIS。
> **實作細節**：嚴格遞增應使用 `upper_bound`（非 `lower_bound`）。

**WA 30%**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#define int long long
using namespace std;

inline bool cmp(pair<int, int> a, pair<int, int> b) {
    if(a.first == b.first)
        return a.second < b.second;
    return a.first < b.first ;
}

inline void solve() {
    int n;cin >> n;
    vector<pair<int, int> > v(n);
    for(int i = 0;i < n;i++)
        cin >> v[i].first >> v[i].second;

    sort(v.begin(), v.end(), cmp);

    vector<int> y(n);
    for(int i = 0;i < n;i++) {
        y[i] = v[i].second;
    }

    vector<int> lis;

    for(int i = 0;i < n;i++) {
        auto it = lower_bound(lis.begin(), lis.end(), y[i]);
        if(it == lis.end()) {
            lis.push_back(y[i]);
        }else {
            *it = y[i];
        }
    }
    cout << lis.size() << '\n';
    return ;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#define int long long
using namespace std;

inline bool cmp(pair<int, int> a, pair<int, int> b) {
    if(a.first == b.first)
        return a.second < b.second;
    return a.first < b.first ;
}

inline void solve() {
    int n;cin >> n;
    vector<pair<int, int> > v(n);
    for(int i = 0;i < n;i++)
        cin >> v[i].first >> v[i].second;

    sort(v.begin(), v.end(), cmp);

    vector<int> y(n);
    for(int i = 0;i < n;i++) {
        y[i] = v[i].second;
    }

    vector<int> lis;

    for(int i = 0;i < n;i++) {
        auto it = upper_bound(lis.begin(), lis.end(), y[i]);
        if(it == lis.end()) {
            lis.push_back(y[i]);
        }else {
            *it = y[i];
        }
    }
    cout << lis.size() << '\n';
    return ;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

---

## 幸運數字

> **想法**：以線段樹維護多個區間的最小值 **位置**（而非值），依題意流程進行。

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
}arr[4 * N];

int n;

inline void build(vector<int>& v, int left, int right, int idx = 1) {
    if(left == right) {
        arr[idx] = Node(v[left], left);
        return ;
    }

    int mid = (left + right) / 2;
    build(v, left, mid, 2 * idx);
    build(v, mid + 1, right, 2 * idx + 1);

    if(arr[2 * idx].mn < arr[2 * idx + 1].mn) {
        arr[idx].mn = arr[2 * idx].mn;
        arr[idx].mn_idx = arr[2 * idx].mn_idx;
    }else {
        arr[idx].mn = arr[2 * idx + 1].mn;
        arr[idx].mn_idx = arr[2 * idx + 1].mn_idx;
    }
    return ;
}

int query(vector<int>& v, int left, int right, int qL, int qR, int idx = 1) {
    if(right < qL or left > qR) {
        return -1 ;
    }
    else if(qL <= left and qR >= right) {
        return arr[idx].mn_idx;
    }

    int mid = (left + right) / 2;
    int lc = 2 * idx, rc = 2 * idx + 1;
    int l_ans = query(v, left, mid, qL, qR, lc);
    int r_ans = query(v, mid + 1, right, qL, qR, rc);

    if(l_ans == -1) return r_ans;
    if(r_ans == -1) return l_ans;

    if(v[l_ans] < v[r_ans]) {
        return l_ans;
    }return r_ans;
}

inline int sum(int left, int right, vector<int>& prefix) {
    if(left == 1) return prefix[right];
    return prefix[right] - prefix[left - 1];
}

inline int f(vector<int>& v, vector<int>& prefix, int left, int right) {
    if(left == right)
        return v[left];
    int m = query(v, 1, n, left, right);

    int l_ans = sum(left, m - 1, prefix);
    int r_ans = sum(m + 1, right, prefix);

    if(l_ans == r_ans) {
        return f(v, prefix, m + 1, right);
    }

    if(l_ans < r_ans) {
        return f(v, prefix, m + 1, right);
    }else
        return f(v, prefix, left, m - 1);
}

inline void solve() {
    cin >> n;
    vector<int> v(n + 1), prefix(n+1);
    for(int i = 1;i <= n;i++) {
        cin >> v[i];
        prefix[i] = prefix[i - 1] + v[i];
    }
    build(v, 1, n);
    int ans = f(v, prefix, 1, n);
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

## 搬家

> **目標**：最大連通塊大小。
> **作法**：可用 DSU，或將輸入轉邊後以 DFS/BFS。
> **易錯點**：掃相鄰格時，常見只需檢查「下、右」，不必同時處理「上、左」，避免邊重複。

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

---

## 美食博覽會

> **k = 1 的情況**：two pointers 可解。
> **進階**：後 50% 需要「分段 DP」。

**WA 50%**

```cpp
#include <iostream>
#include <vector>
#include <map>
#define int long long
#define inf 1000000007
using namespace std;

inline void solve() {
    int n, k;
    cin >> n >> k;
    vector<int> v(n);
    for(int i = 0;i < n;i++)
        cin >> v[i];

    int left = 0, mx = -inf;

    map<int, int> mp;

    for(int right = 0;right < n;right++) {

        while(mp.count(v[right]) and left <= right) {
            mp[v[left]]--;
            if(mp[v[left]] == 0)  mp.erase(v[left]);
            left ++;
        }

        mp[v[right]]++;

        mx = max(mx, right - left + 1);
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

---

## 內積

> **題意**：兩陣列 `A, B`，允許翻轉其中之一，找長度相同子陣列的最大內積。
> **策略**：20% 可列舉 `(i, j, len)`；100% 用 `dp(i,j)` 表示 `A` 以 `i`、`B` 以 `j` 結尾的最佳值，並比較是否延續或重開。

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#define int long long
#define inf 1000000007
using namespace std;

int n, m;

inline int solve(vector<int>& a, vector<int>& b) {
    vector<vector<int> > dp(n, vector<int>(m, 0));

    dp[0][0] = max(0ll, a[0] * b[0]);

    int ans = -inf;

    for(int i = 0;i < n;i++) {
        dp[i][0] = a[i] * b[0];
        ans = max(ans, dp[i][0]);
    }

    for(int j = 0;j < m;j++) {
        dp[0][j] = a[0] * b[j];
        ans = max(dp[0][j], ans);
    }

    for(int i = 1;i < n;i++) {
        for(int j = 1;j < m;j++) {
            dp[i][j] = max(dp[i-1][j-1] + a[i] * b[j], a[i] * b[j]);
            ans = max(dp[i][j], ans);
        }
    }
    return ans;
}

signed main() {
    cin >> n >> m;
    vector<int> a(n), b(m);
    for(int i = 0;i < n;i++)
        cin >> a[i];
    for(int i = 0;i < m;i++)
        cin >> b[i];

    int x = solve(a, b);
    reverse(a.begin(), a.end());
    int y = solve(a, b);
    cout << max(x, y) << '\n';
    return 0;
}
```

---

## 低地距離

> **題意**：長度 `2n` 序列（1..n 各出現兩次），對每個數字，計算其兩次出現之間比它小的數字個數。
> **兩種寫法**：
>
> 1. **BIT**：由左至右維護出現位置，查詢區間內已標記的數量差。
> 2. **Segment Tree**：等價以點更新、區間和查詢。

**AC 100% using BIT**

```cpp
#include <iostream>
#include <vector>
#include <map>
#define int long long
#define N 200010
using namespace std;

int bit[N];

inline int lowbit(int x) {
    return x & (-x);
}

inline int query(int pos) {
    int sum = 0;
    for(int i = pos;i > 0;i -= lowbit(i)) {
        sum += bit[i];
    }
    return sum ;
}

inline void update(int pos, int val) {
    for(int i = pos;i < N;i += lowbit(i)) {
        bit[i] += val;
    }
    return ;
}

inline void solve() {
    int n;cin >> n;
    vector<int> v(2 * n + 1);
    map<int, vector<int> > mp;
    for(int i = 1;i <= 2 * n;i++) {
        cin >> v[i];
        mp[v[i]].push_back(i);
    }

    int ans = 0;
    for(int i = 1;i <= n;i++) {
        int left = mp[i][0];
        int right = mp[i][1];

        ans += query(right) - query(left);

        update(left, 1);update(right, 1);
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

**AC 100% using segment tree**

```cpp
#include <iostream>
#include <vector>
#include <map>
#define int long long
#define N 200010
using namespace std;

struct Node {
    int val;
    Node(int _val = 0) {
        val = _val;
    }
}arr[4 * N];

int query(int L, int R, int qL, int qR, int idx = 1) {
    if(qL <= L and qR >= R) {
        return arr[idx].val;
    }
    if(qL > R or qR < L)  return 0;

    int M = (L + R) / 2;

    int Lans = query(L, M, qL, qR, 2 * idx);
    int Rans = query(M + 1, R, qL, qR, 2 * idx + 1);

    return Lans + Rans;
}

void update(int L, int R, int pos, int val, int idx = 1) {
    if(L > pos or R < pos)  return ;

    if(L == R and L == pos) {
        arr[idx].val = val;
        return ;
    }

    int M = (L + R) / 2;

    update(L, M, pos, val, 2 * idx);
    update(M + 1, R, pos, val, 2 * idx + 1);

    arr[idx].val = arr[2 * idx].val + arr[2 * idx + 1].val;
    return ;
}

inline void solve() {
    int n;cin >> n;
    vector<int> v(2 * n + 1);
    map<int, vector<int> > mp;
    for(int i = 1;i <= 2 * n;i++) {
        cin >> v[i];
        mp[v[i]].push_back(i);
    }

    int ans = 0;
    for(int i = 1;i <= n;i++) {
        int left = mp[i][0];
        int right = mp[i][1];

        ans += query(1, 2 * n, left, right);
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

## 投資遊戲

> **題意**：最大子陣列和，但可跳過 `k` 個元素。
> **DP 定義**：`dp[i][j]` 為到 `i`、使用 `j` 次「跳過」的最大獲益。
> **轉移**：從「延續 + v\[i]」、「消耗一次跳過」、「直接從 v\[i] 開始」三者取最大；最後枚舉 `j` 取全局最佳。

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#define int long long
#define inf 1000000007

using namespace std;

inline void solve() {
    int n, k;
    cin >> n >> k;
    vector<int> v(n);
    for(int i = 0;i < n;i++) {
        cin >> v[i];
    }

    vector<vector<int> > dp(n, vector<int> (k + 1, 0));

    for(int i = 0;i < n;i++) {
        for(int j = 0;j <= k;j++) {
            if(i - 1 >= 0)  dp[i][j] = max(dp[i][j], dp[i-1][j] + v[i]);
            if(i - 1 >= 0 and j - 1 >= 0) dp[i][j] = max(dp[i][j], dp[i-1][j-1]);
            dp[i][j] = max(dp[i][j], v[i]);
        }
    }

    int ans = -inf;

    for(int i = 0;i < n;i++) {
        for(int j = 0;j <= k;j++) {
            ans = max(ans, dp[i][j]);
        }
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

---

## 切割費用

> **想法**：二分搜；每次插入時用集合找左右切割點，累加區段長度。

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#include <set>
#define int long long
using namespace std;

inline void solve() {
    int n, l;
    cin >> n >> l;
    vector<int> v(n + 1);
    for(int i = 0;i < n;i++) {
        int x, num;cin >> x >> num;
        v[num] = x;
    }

    set<int> st;
    st.insert(0);st.insert(l);

    int ans = 0;
    for(int i = 1;i <= n;i++) {
        auto it1 = st.upper_bound(v[i]);
        auto it2 = --st.upper_bound(v[i]);

        int right = *it1, left = *it2;

        ans += (right - left);

        st.insert(v[i]);
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

---

## 階梯數字 (Digit DP)

> **題意**：計數 `0..n` 中相鄰位不遞減（或題目限定）的數字數量，`n` 可能極大（上萬位）。
> **核心模板**：`dfs(depth, last, tight)` + 記憶化。`tight` 表示是否仍受上界限制。
> **收尾**：注意是否要扣掉 `0`，以及取模處理。

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#include <cstring>
#define int long long
#define mod 1000000007

using namespace std;

string s;
vector<int> digit;
int dp[100005][10][2];
int len;

inline int dfs(int depth, int last, bool same) {
    if(dp[depth][last][same] != -1) return dp[depth][last][same];
    if(depth == len) {
        return 1;
    }
    int ans = 0;
    for(int i = last; i < 10;i++) {
        if(same and i > digit[depth]) {
            continue;
        }
        bool tmp_same = (same and i == digit[depth]) ? true : false;
        ans = (ans + dfs(depth + 1, i, tmp_same)) % mod;
    }
    return dp[depth][last][same] = ans % mod;
}

inline void solve() {
    for(int i = 0;i < s.size();i++) {
        digit.push_back((int)s.at(i) - '0');
    }
    memset(dp, -1, sizeof(dp));
    len = digit.size();
    cout << (dfs(0, 0, 1) - 1 + mod) % mod<< '\n';
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    while(cin >> s) {
        digit.clear();
        solve();
    }
    return 0;
}
```

---

## Tree Distance I (CSES 1132)

> **思路**：兩次 DFS。
>
> 1. `dfs1`：自底向上算每點「往下」最遠距離 `down[u]`。
> 2. `dfs2`：自頂向下算「往上」距離 `up[u]`，用最大、次大 `down` 分配到子節點。
>    **輸出**：各點 `max(up[u], down[u])`。

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

## 真假子圖

> **技巧**：擴展域並查集。
> 對於「a 與 b 必不同色」：合併 `a` 與 `b'`，以及 `a'` 與 `b`。檢查矛盾時判斷 `find(a) == find(b)`。

**AC 100%**

```cpp
#include <iostream>
#include <vector>
#define int long long
#define N 20005

using namespace std;

int n, m;
int pa[2 * N], sz[2 * N];

vector<int> ori(2 * N);

inline int fnd(int x) {
    if(x == pa[x])  return x;
    return pa[x] = fnd(pa[x]);
}

inline void unite(int x, int y) {
    int px = fnd(x), py = fnd(y);
    if(px == py)  return ;
    if(sz[px] > sz[py]) swap(px, py);
    pa[px] = py;
    sz[py] += sz[px];
    return ;
}

inline void init() {
     for(int i = 0;i < 2 * N;i++) {
        pa[i] = i;sz[i] = 1;
    }
    for(int i = 0;i < 2 * m;i += 2) {
        int a = ori[i], b = ori[i + 1];
        unite(a, b + n);
        unite(a + n, b);
    }
}

inline void solve() {
    cin >> n >> m;
    for(int i = 0;i < 2 * m;i++) {
        cin >> ori[i];
    }

    init();

    int p, k;
    cin >> p >> k;

    vector<int> ans ;

    for(int i = 1;i <= p;i++) {
        bool flag = true;
        for(int j = 0;j < k;j++) {
            int a, b;
            cin >> a >> b;
            if(fnd(a) == fnd(b))  flag = false;
            unite(a, b + n);
            unite(a + n, b);
        }
        if(!flag) {
            ans.push_back(i);
            init();
        }
    }

    for(int i = 0;i < ans.size();i++) {
        cout << ans[i] << '\n';
    }
    return ;
}

signed main() {
    ios_base::sync_with_stdio(false);
    cin.tie(0);cout.tie(0);
    solve();
    return 0;
}
```

---

## 邏輯電路

> **題意**：給定輸入埠、邏輯閘、輸出埠與連線，計算輸出值及最大延遲層數。
> **方法**：DAG 拓樸排序，自前而後逐點計算；閘類型含 AND/OR/XOR/NOT；同步維護每點 delay。

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
            else if(val[nxt] == -1) {
                val[nxt] = val[cur];
            }
            else {
                val[nxt] = cal(val[cur], port[nxt], val[nxt]);
            }
            delay[nxt] = max(delay[nxt], delay[cur] + 1);
            if(--indeg[nxt] == 0)
                que.push(nxt);
        }
    }

    cout << mx - 1 << '\n';

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

---

## 病毒演化

> **模型**：樹 DP。`dp[i][j]` 為以 `i` 為根且 `i` 取字母 `j`（A/U/G/C）的最小漢明距離；若字元為 `@`，此位可任意不加成本。
> **合併**：父節點選擇 `i`，子節點枚舉 `j`，若 `i!=j` 則加 1，累加所有子樹成本；每欄位獨立計算後疊加。

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

    for(int nxt : adj[cur]) {
        if(nxt == pa)   continue;
        dfs(nxt, cur);
        for(int i = 0;i < 4;i++) {
            if(dp[cur][i] == inf) continue;
            int mi = inf;
            for(int j = 0;j < 4;j++) {
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
    for(int i = 0;i < m;i++) {
        vector<char> tmp;
        for(int j = 0;j < n;j++) {
            tmp.push_back(s[j][i]);
        }
        c = tmp;

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
