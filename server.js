#!/usr/bin/env node
/**
 * 三国法教学智能体 · 服务端
 *
 * 两个职责：
 *   1. 静态托管 —— 把本目录直接当作站点根目录
 *   2. AI 代理  —— POST /api/ai 转发到火山方舟（豆包）
 *
 * 为什么要这层代理：原来 API Key 由使用者在浏览器里填写、前端直连火山方舟，
 * 学生一多就要人手配一次，而且密钥会暴露在每台设备的浏览器里。
 * 走代理之后，密钥只保存在服务端，浏览器全程不接触；学生打开即用。
 *
 * 密钥来源（二选一，环境变量优先）：
 *   - 环境变量：ARK_API_KEY，模型用 ARK_ENDPOINT（可选）
 *   - 本地文件：ai-proxy.local.json（复制 ai-proxy.local.example.json 改名即可，
 *     该文件已在 .gitignore 中，不会被推到 GitHub）
 */

'use strict';

const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');

const ROOT = __dirname;
const PORT = parseInt(process.env.PORT, 10) || 3000;
const HOST = '0.0.0.0';

const UPSTREAM = 'https://ark.cn-beijing.volces.com/api/v3/chat/completions';
const DEFAULT_MODEL = process.env.ARK_ENDPOINT || 'doubao-seed-2-0-lite-260428';
const MAX_BODY = 512 * 1024;
const UPSTREAM_TIMEOUT = 120000;
const RATE_MAX = parseInt(process.env.AI_RATE_MAX, 10) || 40;
const RATE_WINDOW = 60 * 1000;

// 允许跨域调用本代理的来源（GitHub Pages 入口需要）
const ALLOWED_ORIGINS = (process.env.ALLOWED_ORIGINS ||
  'https://felicewang90.github.io,https://sanguofa-legal-tutor.app.workbuddy.host')
  .split(',').map(s => s.trim()).filter(Boolean);

// ---------------------------------------------------------------- 密钥

function loadKey() {
  if (process.env.ARK_API_KEY) {
    return { apiKey: process.env.ARK_API_KEY, endpoint: process.env.ARK_ENDPOINT || '' };
  }
  try {
    const p = path.join(ROOT, 'ai-proxy.local.json');
    if (fs.existsSync(p)) {
      const j = JSON.parse(fs.readFileSync(p, 'utf8'));
      if (j && j.apiKey) return { apiKey: String(j.apiKey).trim(), endpoint: String(j.endpoint || '').trim() };
    }
  } catch (e) {
    console.error('读取 ai-proxy.local.json 失败:', e.message);
  }
  return null;
}

// ---------------------------------------------------------------- 工具

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.mjs': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.webp': 'image/webp',
  '.ico': 'image/x-icon',
  '.mp4': 'video/mp4',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.txt': 'text/plain; charset=utf-8'
};

function clientIp(req) {
  const xf = req.headers['x-forwarded-for'];
  if (xf) return String(xf).split(',')[0].trim();
  return req.socket.remoteAddress || 'unknown';
}

// 简单滑动窗口限流，防止代理被滥用
const hits = new Map();
function rateOk(ip) {
  const now = Date.now();
  const arr = (hits.get(ip) || []).filter(t => now - t < RATE_WINDOW);
  arr.push(now);
  hits.set(ip, arr);
  if (hits.size > 5000) {
    for (const [k, v] of hits) {
      if (!v.some(t => now - t < RATE_WINDOW)) hits.delete(k);
    }
  }
  return arr.length <= RATE_MAX;
}

function sendJson(res, status, obj, origin) {
  const headers = { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' };
  if (origin) {
    headers['Access-Control-Allow-Origin'] = origin;
    headers['Vary'] = 'Origin';
  }
  res.writeHead(status, headers);
  res.end(JSON.stringify(obj));
}

function corsOrigin(req) {
  const origin = req.headers.origin;
  if (!origin) return null;            // 同域请求，无需 CORS 头
  if (ALLOWED_ORIGINS.indexOf(origin) !== -1) return origin;
  if (/^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origin)) return origin; // 本地调试
  return null;
}

// ---------------------------------------------------------------- AI 代理

function readBody(req) {
  return new Promise((resolve, reject) => {
    let raw = '';
    let aborted = false;
    req.on('data', c => {
      raw += c;
      if (raw.length > MAX_BODY) { aborted = true; req.destroy(); reject(new Error('请求体过大')); }
    });
    req.on('end', () => { if (!aborted) resolve(raw); });
    req.on('error', reject);
  });
}

// 只保留合法字段并收紧取值范围，避免客户端借代理做任何出格的事
function sanitize(payload, cfg) {
  const messages = Array.isArray(payload.messages) ? payload.messages : [];
  const clean = messages
    .filter(m => m && (m.role === 'system' || m.role === 'user' || m.role === 'assistant'))
    .slice(-12)
    .map(m => ({
      role: m.role,
      content: String(m.content == null ? '' : m.content).substring(0, 8000)
    }));

  const out = {
    // 模型由服务端决定，不采信客户端传来的 model
    model: cfg.endpoint || DEFAULT_MODEL,
    messages: clean,
    temperature: 0.3,
    max_tokens: 1300
  };
  if (typeof payload.temperature === 'number' && isFinite(payload.temperature)) {
    out.temperature = Math.min(Math.max(payload.temperature, 0), 1);
  }
  if (payload.max_tokens) {
    out.max_tokens = Math.min(Math.max(parseInt(payload.max_tokens, 10) || 1300, 64), 2000);
  }
  return out;
}

function callUpstream(payload, withThinking, apiKey) {
  const sent = Object.assign({}, payload);
  delete sent.__apiKey;               // 内部字段不外发
  if (withThinking) sent.thinking = { type: 'disabled' };
  const body = JSON.stringify(sent);

  const u = new URL(UPSTREAM);
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: u.hostname,
      path: u.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
        'Authorization': 'Bearer ' + apiKey
      },
      timeout: UPSTREAM_TIMEOUT
    }, resolve);
    req.on('timeout', () => req.destroy(new Error('上游请求超时')));
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function handleAI(req, res) {
  const origin = corsOrigin(req);
  const started = Date.now();
  const done = (code) => console.log('[ai] ' + req.method + ' ' + (req.url || '') + ' -> ' + code + ' (' + (Date.now() - started) + 'ms, ' + clientIp(req) + ')');

  if (req.method === 'OPTIONS') {
    const h = { 'Access-Control-Allow-Methods': 'POST, GET, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' };
    if (origin) { h['Access-Control-Allow-Origin'] = origin; h['Vary'] = 'Origin'; }
    res.writeHead(204, h);
    return res.end();
  }

  const cfg = loadKey();

  // 探活：客户端启动时问一句"服务端 AI 能不能用"
  if (req.method === 'GET') {
    if (!cfg) { done(503); return sendJson(res, 503, { ok: false, error: '服务端未配置 AI 密钥' }, origin); }
    done(200);
    return sendJson(res, 200, { ok: true, model: cfg.endpoint || DEFAULT_MODEL }, origin);
  }

  if (req.method !== 'POST') {
    done(405);
    return sendJson(res, 405, { error: '仅支持 POST / GET' }, origin);
  }

  if (!cfg) {
    done(503);
    return sendJson(res, 503, { error: '服务端 AI 未配置密钥，请在页面右上角「AI增强」中填写自己的 API Key' }, origin);
  }

  if (!rateOk(clientIp(req))) {
    done(429);
    return sendJson(res, 429, { error: '请求过于频繁，请稍后再试' }, origin);
  }

  let payload;
  try {
    payload = JSON.parse(await readBody(req));
  } catch (e) {
    done(400);
    return sendJson(res, 400, { error: '请求体不是合法 JSON' }, origin);
  }

  const body = sanitize(payload, cfg);
  body.__apiKey = cfg.apiKey;
  const wantStream = !!payload.stream;
  if (wantStream) body.stream = true;

  let upstream;
  try {
    upstream = await callUpstream(body, true, cfg.apiKey);
  } catch (e) {
    done(502);
    return sendJson(res, 502, { error: '无法连接 AI 服务: ' + e.message }, origin);
  }

  // 400 多半是模型不认识 thinking 参数 → 去掉重试一次
  if (upstream.statusCode === 400) {
    let errText = '';
    try { errText = await new Promise(r => { let s = ''; upstream.on('data', c => s += c); upstream.on('end', () => r(s)); }); } catch (e) {}
    console.warn('上游返回 400，去掉 thinking 参数重试:', String(errText).substring(0, 120));
    try {
      upstream = await callUpstream(body, false, cfg.apiKey);
    } catch (e) {
      done(502);
      return sendJson(res, 502, { error: '无法连接 AI 服务: ' + e.message }, origin);
    }
  }

  if (upstream.statusCode !== 200) {
    let errText = '';
    try { errText = await new Promise(r => { let s = ''; upstream.on('data', c => s += c); upstream.on('end', () => r(s)); }); } catch (e) {}
    let msg = 'AI 服务返回错误 (' + upstream.statusCode + ')';
    try {
      const j = JSON.parse(errText);
      if (j && j.error && j.error.message) msg = String(j.error.message).substring(0, 200);
      else if (j && j.message) msg = String(j.message).substring(0, 200);
    } catch (e) {}
    // 不回显上游原始报文，避免泄漏账号信息
    const code = upstream.statusCode === 401 ? 401 : 502;
    done(upstream.statusCode);
    return sendJson(res, code, { error: msg }, origin);
  }

  done(200);

  const headers = { 'Cache-Control': 'no-store, no-transform', 'X-Accel-Buffering': 'no' };
  if (origin) { headers['Access-Control-Allow-Origin'] = origin; headers['Vary'] = 'Origin'; }
  if (wantStream) {
    headers['Content-Type'] = 'text/event-stream; charset=utf-8';
    headers['Connection'] = 'keep-alive';
  } else {
    headers['Content-Type'] = 'application/json; charset=utf-8';
  }
  res.writeHead(200, headers);

  req.on('close', () => { try { upstream.destroy(); } catch (e) {} });
  upstream.on('error', () => { try { res.end(); } catch (e) {} });
  upstream.pipe(res);
}

// ---------------------------------------------------------------- 静态

function serveStatic(req, res, pathname) {
  let rel;
  try {
    rel = decodeURIComponent(pathname);
  } catch (e) {
    rel = pathname;
  }
  if (rel.charAt(0) === '/') rel = rel.slice(1);
  if (rel === '') rel = 'index.html';

  const filePath = path.join(ROOT, rel);
  // 目录穿越防护
  if (path.relative(ROOT, filePath).indexOf('..') === 0 && filePath !== ROOT) {
    res.writeHead(403, { 'Content-Type': 'text/plain; charset=utf-8' });
    return res.end('403 Forbidden');
  }

  let stat;
  try {
    stat = fs.statSync(filePath);
  } catch (e) {
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    return res.end('404 Not Found');
  }

  if (stat.isDirectory()) {
    const idx = path.join(filePath, 'index.html');
    if (fs.existsSync(idx)) return serveStatic(req, res, path.posix.join(pathname, 'index.html'));
    res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
    return res.end('404 Not Found');
  }

  const ext = path.extname(filePath).toLowerCase();
  const type = MIME[ext] || 'application/octet-stream';
  const cache = ext === '.html' ? 'no-cache' : 'public, max-age=3600';

  res.writeHead(200, {
    'Content-Type': type,
    'Content-Length': stat.size,
    'Cache-Control': cache
  });
  fs.createReadStream(filePath).pipe(res);
}

// ---------------------------------------------------------------- 服务

const server = http.createServer((req, res) => {
  let pathname = '/';
  try {
    pathname = new URL(req.url, 'http://' + (req.headers.host || 'localhost')).pathname;
  } catch (e) {
    pathname = req.url.split('?')[0];
  }

  if (pathname === '/api/ai' || pathname === '/sanguofa/api/ai') {
    return handleAI(req, res).catch(e => sendJson(res, 500, { error: '服务端内部错误' }, corsOrigin(req)));
  }
  return serveStatic(req, res, pathname);
});

server.listen(PORT, HOST, () => {
  const cfg = loadKey();
  console.log('三国法教学智能体服务已启动: http://' + HOST + ':' + PORT);
  console.log('AI 代理状态: ' + (cfg ? '已配置密钥，模型 ' + (cfg.endpoint || DEFAULT_MODEL) : '未配置密钥（学生端将回落到纯知识库检索）'));
});
