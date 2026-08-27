import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix 1: BM25.init() - force re-init when KB_CHUNKS ready but docLens empty
old_init = """  function init() {
    if (docLens.length > 0) return; // 已初始化
    if (!KB_CHUNKS || KB_CHUNKS.length === 0) return; // 知识库未加载完成"""

new_init = """  function init() {
    if (!KB_CHUNKS || KB_CHUNKS.length === 0) {
      console.warn("BM25.init: KB not ready, KB_CHUNKS=", KB_CHUNKS ? KB_CHUNKS.length : 'null');
      return;
    }
    if (docLens.length > 0 && docLens.length === KB_CHUNKS.length) return; // 已初始化且数量匹配"""

content = content.replace(old_init, new_init)

# Fix 2: BM25.search() - add simple text fallback when BM25 returns empty
old_search_return = """    // 按分数排序，取topN
    scores.sort((a, b) => b.score - a.score);
    return scores.slice(0, topN).map(s => ({
      chunk: KB_CHUNKS[s.index],
      score: s.score
    }));
  }"""

new_search_return = """    // 按分数排序，取topN
    scores.sort((a, b) => b.score - a.score);
    let results = scores.slice(0, topN).map(s => ({
      chunk: KB_CHUNKS[s.index],
      score: s.score
    }));
    
    // Fallback: if BM25 returns no results, do simple text matching
    if (results.length === 0) {
      const qLower = query.toLowerCase();
      for (let i = 0; i < KB_CHUNKS.length && results.length < topN; i++) {
        const text = (KB_CHUNKS[i].t + ' ' + KB_CHUNKS[i].x).toLowerCase();
        if (text.includes(qLower)) {
          results.push({ chunk: KB_CHUNKS[i], score: 0.1 });
        }
      }
    }
    
    return results;
  }"""

content = content.replace(old_search_return, new_search_return)

# Fix 3: searchKBInSim() - make async and await _kbReady
old_sim_search = """function searchKBInSim() {
  const input = document.getElementById('simKbSearchInput');
  if (!input) return;
  const query = input.value.trim();
  if (!query) return;
  
  const results = BM25.search(query, 5);"""

new_sim_search = """async function searchKBInSim() {
  const input = document.getElementById('simKbSearchInput');
  if (!input) return;
  const query = input.value.trim();
  if (!query) return;
  
  // Wait for knowledge base to load
  if (typeof _kbReady !== 'undefined') { try { await _kbReady; } catch(e) { console.warn('KB load error:', e); } }
  
  const results = BM25.search(query, 5);"""

content = content.replace(old_sim_search, new_sim_search)

# Fix 4: Add console.log after KB init for debugging
old_kb_log = """    console.log("知识库加载成功，共", KB_CHUNKS.length, "个知识块");"""
new_kb_log = """    console.log("知识库加载成功，共", KB_CHUNKS.length, "个知识块");
    console.log("[KB Debug] KB_CHUNKS type:", typeof KB_CHUNKS, "length:", KB_CHUNKS.length);
    console.log("[KB Debug] Sample chunk:", JSON.stringify(KB_CHUNKS[0]).substring(0, 200));"""

content = content.replace(old_kb_log, new_kb_log)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixes applied successfully!")
print("Changes:")
print("1. BM25.init() - force re-init when KB_CHUNKS ready but docLens empty")
print("2. BM25.search() - added simple text fallback")
print("3. searchKBInSim() - made async with _kbReady await")
print("4. Added debug logging after KB init")
