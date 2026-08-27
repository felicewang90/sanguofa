import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire initKBChunks function with a more robust version
old_func = """  async function initKBChunks() {
    if (KB_CHUNKS) return;
    await loadKBData();
    const bin = atob(_KB_B64);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    const ds = new DecompressionStream("gzip");
    const reader = new Blob([bytes]).stream().pipeThrough(ds).getReader();
    const chunks = [];
    while (true) { const {done, value} = await reader.read(); if (done) break; chunks.push(value); }
    const total = chunks.reduce((s, c) => s + c.length, 0);
    const result = new Uint8Array(total);
    let off = 0; for (const c of chunks) { result.set(c, off); off += c.length; }
    KB_CHUNKS = JSON.parse(new TextDecoder().decode(result));
    console.log("知识库加载成功，共", KB_CHUNKS.length, "个知识块");
    console.log("[KB Debug] KB_CHUNKS type:", typeof KB_CHUNKS, "length:", KB_CHUNKS.length);
    console.log("[KB Debug] Sample chunk:", JSON.stringify(KB_CHUNKS[0]).substring(0, 200));
  }"""

new_func = """  // Chunked base64 decode to avoid browser atob() stack overflow on large strings
  function atobChunked(b64) {
    const CHUNK = 0x8000; // 32KB chunks
    let result = '';
    for (let i = 0; i < b64.length; i += CHUNK) {
      result += atob(b64.substring(i, i + CHUNK));
    }
    return result;
  }

  async function initKBChunks() {
    if (KB_CHUNKS) return;
    await loadKBData();
    try {
      // Method 1: Try DecompressionStream with chunked atob
      console.log("[KB] Starting decompression, b64 length:", _KB_B64.length);
      const bin = atobChunked(_KB_B64);
      console.log("[KB] atob done, binary length:", bin.length);
      const bytes = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      const ds = new DecompressionStream("gzip");
      const reader = new Blob([bytes]).stream().pipeThrough(ds).getReader();
      const chunks = [];
      while (true) { const {done, value} = await reader.read(); if (done) break; chunks.push(value); }
      const total = chunks.reduce((s, c) => s + c.length, 0);
      const result = new Uint8Array(total);
      let off = 0; for (const c of chunks) { result.set(c, off); off += c.length; }
      KB_CHUNKS = JSON.parse(new TextDecoder().decode(result));
      console.log("[KB] DecompressionStream SUCCESS, chunks:", KB_CHUNKS.length);
    } catch(e1) {
      console.warn("[KB] DecompressionStream failed:", e1.message, "- trying pako fallback...");
      try {
        // Method 2: Load pako from CDN and use it
        if (typeof pako === 'undefined') {
          await new Promise((resolve, reject) => {
            const s = document.createElement('script');
            s.src = 'https://cdn.jsdelivr.net/npm/pako@2.1.0/dist/pako.min.js';
            s.onload = resolve;
            s.onerror = reject;
            document.head.appendChild(s);
          });
        }
        const bin2 = atobChunked(_KB_B64);
        const bytes2 = new Uint8Array(bin2.length);
        for (let i = 0; i < bin2.length; i++) bytes2[i] = bin2.charCodeAt(i);
        const decompressed = pako.ungzip(bytes2);
        KB_CHUNKS = JSON.parse(new TextDecoder().decode(decompressed));
        console.log("[KB] pako fallback SUCCESS, chunks:", KB_CHUNKS.length);
      } catch(e2) {
        console.error("[KB] Both methods failed. e1:", e1.message, "e2:", e2.message);
        throw new Error("KB decompression failed: " + e2.message);
      }
    }
    console.log("知识库加载成功，共", KB_CHUNKS.length, "个知识块");
    console.log("[KB Debug] KB_CHUNKS type:", typeof KB_CHUNKS, "length:", KB_CHUNKS.length);
    console.log("[KB Debug] Sample chunk:", JSON.stringify(KB_CHUNKS[0]).substring(0, 200));
  }"""

content = content.replace(old_func, new_func)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Decompression fix applied!")
print("Changes:")
print("1. Added atobChunked() to handle large base64 strings")
print("2. Method 1: DecompressionStream with chunked atob")
print("3. Method 2 (fallback): Load pako from CDN for decompression")
