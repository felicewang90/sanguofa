#!/usr/bin/env python3
"""Integrate Supabase Auth into sanguofa index.html"""
import sys

FILE_PATH = '/Coze/Drive/3G学堂（1）/所有对话/主对话/sanguofa/index.html'

# Read the file
with open(FILE_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
print(f"Original file size: {original_len} chars")

changes = 0

# ============================================================
# 1. Add Supabase JS SDK before </head>
# ============================================================
old_head_close = '</style>\n</head>'
new_head_close = '</style>\n<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>\n</head>'

if old_head_close in content:
    content = content.replace(old_head_close, new_head_close, 1)
    changes += 1
    print("[1] Added Supabase JS SDK before </head>")
else:
    print("[1] ERROR: Could not find </style></head> pattern")
    sys.exit(1)

# ============================================================
# 2. Replace login form HTML
# ============================================================
old_login_html = '''  <div id="loginOverlay">
    <div class="login-card">
      <button class="login-modal-close" onclick="closeLoginModal()" title="关闭">&times;</button>
      <div style="margin-bottom:16px">
        <div style="width:56px;height:56px;border-radius:50%;padding:2px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:center;font-size:28px">⚖️</div>
      </div>
      <div class="login-card-title">三国法教学智能体</div>
      <div class="login-card-subtitle">国际公法 · 国际私法 · 国际经济法</div>
      <form id="loginForm" onsubmit="return handleLogin(event)">
        <div class="login-field">
          <label for="loginStudentId">学号</label>
          <input type="text" id="loginStudentId" placeholder="请输入学号" required autocomplete="off">
        </div>
        <div class="login-field">
          <label for="loginName">姓名</label>
          <input type="text" id="loginName" placeholder="请输入姓名" required autocomplete="off">
        </div>
        <div class="login-field">
          <label for="loginRole">角色</label>
          <select id="loginRole">
            <option value="student">学生</option>
            <option value="teacher">教师</option>
          </select>
        </div>
        <div class="login-error" id="loginError"></div>
        <button type="submit" class="login-btn">登 录</button>
      </form>
    </div>
  </div>'''

new_login_html = '''  <div id="loginOverlay">
    <div class="login-card">
      <button class="login-modal-close" onclick="closeLoginModal()" title="关闭">&times;</button>
      <div style="margin-bottom:16px">
        <div style="width:56px;height:56px;border-radius:50%;padding:2px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,0.1);display:flex;align-items:center;justify-content:center;font-size:28px">⚖️</div>
      </div>
      <div class="login-card-title">三国法教学智能体</div>
      <div class="login-card-subtitle">国际公法 · 国际私法 · 国际经济法</div>
      <div id="authTabs" style="display:flex;margin-bottom:16px;border-bottom:2px solid #eee">
        <div id="tabLogin" onclick="switchAuthTab('login')" style="flex:1;text-align:center;padding:10px 0;cursor:pointer;font-weight:bold;border-bottom:2px solid #1a73e8;color:#1a73e8;margin-bottom:-2px;transition:all 0.2s">登录</div>
        <div id="tabRegister" onclick="switchAuthTab('register')" style="flex:1;text-align:center;padding:10px 0;cursor:pointer;color:#666;margin-bottom:-2px;transition:all 0.2s">注册</div>
      </div>
      <form id="loginForm" onsubmit="return handleSupabaseLogin(event)">
        <div class="login-field">
          <label for="loginEmail">邮箱</label>
          <input type="email" id="loginEmail" placeholder="请输入邮箱" required autocomplete="email">
        </div>
        <div class="login-field">
          <label for="loginPassword">密码</label>
          <input type="password" id="loginPassword" placeholder="请输入密码" required autocomplete="current-password">
        </div>
        <div class="login-error" id="loginError"></div>
        <button type="submit" class="login-btn" id="loginBtn">登 录</button>
      </form>
      <form id="registerForm" style="display:none" onsubmit="return handleSupabaseRegister(event)">
        <div class="login-field">
          <label for="regName">姓名</label>
          <input type="text" id="regName" placeholder="请输入姓名" required autocomplete="name">
        </div>
        <div class="login-field">
          <label for="regStudentId">学号</label>
          <input type="text" id="regStudentId" placeholder="请输入学号" required autocomplete="off">
        </div>
        <div class="login-field">
          <label for="regEmail">邮箱</label>
          <input type="email" id="regEmail" placeholder="请输入邮箱" required autocomplete="email">
        </div>
        <div class="login-field">
          <label for="regRole">角色</label>
          <select id="regRole">
            <option value="student">学生</option>
            <option value="teacher">教师</option>
          </select>
        </div>
        <div class="login-field">
          <label for="regPassword">密码</label>
          <input type="password" id="regPassword" placeholder="至少6位密码" required minlength="6" autocomplete="new-password">
        </div>
        <div class="login-error" id="registerError"></div>
        <button type="submit" class="login-btn" id="registerBtn">注 册</button>
      </form>
    </div>
  </div>'''

if old_login_html in content:
    content = content.replace(old_login_html, new_login_html, 1)
    changes += 1
    print("[2] Replaced login form HTML")
else:
    print("[2] ERROR: Could not find login form HTML")
    sys.exit(1)

# ============================================================
# 3. Add Supabase initialization after <script> tag
# ============================================================
old_script_start = '''  <script>

  // Knowledge base: raw JSON, no compression/decompression needed'''

new_script_start = '''  <script>

  // === Supabase 初始化 ===
  var SUPABASE_URL = 'https://buckhpuxcenmnthxumuh.supabase.co';
  var SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ1Y2tocHV4Y2VubW50aHh1bXVoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk1ODU0ODgsImV4cCI6MjEwNTE2MTQ4OH0.HoNx0ZtEEJ5k3lrBJlCOhkv5rT-_C3BpNHJy3cAZXxw';
  var supabase = null;
  (function initSupabase() {
    if (typeof window.supabase !== 'undefined' && window.supabase.createClient) {
      supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
      console.log('[Supabase] Client initialized');
    } else {
      console.warn('[Supabase] SDK not loaded yet, retrying...');
      setTimeout(initSupabase, 500);
    }
  })();

  // Knowledge base: raw JSON, no compression/decompression needed'''

if old_script_start in content:
    content = content.replace(old_script_start, new_script_start, 1)
    changes += 1
    print("[3] Added Supabase initialization code")
else:
    print("[3] ERROR: Could not find <script> start pattern")
    sys.exit(1)

# ============================================================
# 4. Replace initApp function
# ============================================================
old_init_app = '''function initApp() {
  // Check if already logged in
  var savedUser = null;
  try {
    var raw = localStorage.getItem('sanguofa_current_user');
    if (raw) savedUser = JSON.parse(raw);
  } catch(e) {}
  
  if (savedUser && savedUser.studentId && savedUser.name) {
    AppState.currentUser = savedUser;
    AppState.isGuest = false;
    AppState.isTeacherMode = (savedUser.role === 'teacher');
  } else {
    // Guest mode - no login required
    AppState.isGuest = true;
    AppState.currentUser = null;
    AppState.isTeacherMode = false;
  }
  startApp();
}'''

new_init_app = '''async function initApp() {
  // First check Supabase session
  var loggedIn = false;
  if (supabase) {
    try {
      loggedIn = await checkAuthState();
    } catch(e) {
      console.warn('[Supabase] checkAuthState failed:', e);
    }
  }
  
  if (!loggedIn) {
    // Fallback: check localStorage
    var savedUser = null;
    try {
      var raw = localStorage.getItem('sanguofa_current_user');
      if (raw) savedUser = JSON.parse(raw);
    } catch(e) {}
    
    if (savedUser && savedUser.studentId && savedUser.name) {
      AppState.currentUser = savedUser;
      AppState.isGuest = false;
      AppState.isTeacherMode = (savedUser.role === 'teacher');
    } else {
      AppState.isGuest = true;
      AppState.currentUser = null;
      AppState.isTeacherMode = false;
    }
  }
  startApp();
}'''

if old_init_app in content:
    content = content.replace(old_init_app, new_init_app, 1)
    changes += 1
    print("[4] Replaced initApp function")
else:
    print("[4] ERROR: Could not find initApp function")
    sys.exit(1)

# ============================================================
# 5. Replace handleLogin + showLoginModal + closeLoginModal with Supabase auth functions
# ============================================================
old_login_functions = '''// === Login / Logout ===
function handleLogin(e) {
  e.preventDefault();
  var studentId = document.getElementById('loginStudentId').value.trim();
  var name = document.getElementById('loginName').value.trim();
  var role = document.getElementById('loginRole').value;
  var errorEl = document.getElementById('loginError');
  
  if (!studentId || !name) {
    errorEl.textContent = '请填写学号和姓名';
    errorEl.style.display = 'block';
    return false;
  }
  
  var user = { studentId: studentId, name: name, role: role, loginTime: new Date().toISOString() };
  localStorage.setItem('sanguofa_current_user', JSON.stringify(user));
  AppState.currentUser = user;
  AppState.isGuest = false;
  AppState.isTeacherMode = (role === 'teacher');
  
  // Record login in teacher students registry
  var registry = [];
  try {
    var raw = localStorage.getItem('sanguofa_student_registry');
    if (raw) registry = JSON.parse(raw);
  } catch(e) {}
  
  var existing = registry.find(function(r) { return r.studentId === studentId; });
  if (existing) {
    existing.name = name;
    existing.role = role;
    existing.lastActive = new Date().toISOString();
  } else {
    registry.push({ studentId: studentId, name: name, role: role, lastActive: new Date().toISOString() });
  }
  localStorage.setItem('sanguofa_student_registry', JSON.stringify(registry));
  
  // Close login modal
  closeLoginModal();
  startApp();
  return false;
}

function showLoginModal() {
  var overlay = document.getElementById('loginOverlay');
  if (overlay) {
    overlay.classList.add('visible');
    // Reset form and error
    var form = document.getElementById('loginForm');
    if (form) form.reset();
    var errorEl = document.getElementById('loginError');
    if (errorEl) { errorEl.style.display = 'none'; errorEl.textContent = ''; }
    // Focus first input
    setTimeout(function() {
      var firstInput = document.getElementById('loginStudentId');
      if (firstInput) firstInput.focus();
    }, 100);
  }
}

function closeLoginModal() {
  var overlay = document.getElementById('loginOverlay');
  if (overlay) overlay.classList.remove('visible');
}'''

new_login_functions = '''// === Login / Logout (Supabase Auth) ===

// Auth tab 切换
function switchAuthTab(tab) {
  var loginForm = document.getElementById('loginForm');
  var registerForm = document.getElementById('registerForm');
  var tabLoginEl = document.getElementById('tabLogin');
  var tabRegisterEl = document.getElementById('tabRegister');
  if (tab === 'login') {
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
    tabLoginEl.style.borderBottom = '2px solid #1a73e8';
    tabLoginEl.style.color = '#1a73e8';
    tabLoginEl.style.fontWeight = 'bold';
    tabRegisterEl.style.borderBottom = 'none';
    tabRegisterEl.style.color = '#666';
    tabRegisterEl.style.fontWeight = 'normal';
  } else {
    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
    tabRegisterEl.style.borderBottom = '2px solid #1a73e8';
    tabRegisterEl.style.color = '#1a73e8';
    tabRegisterEl.style.fontWeight = 'bold';
    tabLoginEl.style.borderBottom = 'none';
    tabLoginEl.style.color = '#666';
    tabLoginEl.style.fontWeight = 'normal';
  }
}

// Supabase 登录
async function handleSupabaseLogin(e) {
  e.preventDefault();
  if (!supabase) { alert('系统初始化中，请稍后再试'); return false; }
  var email = document.getElementById('loginEmail').value.trim();
  var password = document.getElementById('loginPassword').value;
  var errorEl = document.getElementById('loginError');
  var btn = document.getElementById('loginBtn');
  errorEl.style.display = 'none';
  btn.textContent = '登录中...';
  btn.disabled = true;

  var result = await supabase.auth.signInWithPassword({ email: email, password: password });
  var data = result.data;
  var error = result.error;

  btn.textContent = '登 录';
  btn.disabled = false;

  if (error) {
    var msg = '登录失败';
    if (error.message && error.message.indexOf('Invalid login credentials') >= 0) {
      msg = '邮箱或密码错误';
    } else if (error.message && error.message.indexOf('Email not confirmed') >= 0) {
      msg = '邮箱未验证，请检查邮箱后重试';
    } else {
      msg = error.message || msg;
    }
    errorEl.textContent = msg;
    errorEl.style.display = 'block';
    return false;
  }

  var user = data.user;
  var metadata = user.user_metadata || {};
  var currentUser = {
    id: user.id,
    email: email,
    studentId: metadata.studentId || '',
    name: metadata.name || email,
    role: metadata.role || 'student',
    loginTime: new Date().toISOString()
  };
  localStorage.setItem('sanguofa_current_user', JSON.stringify(currentUser));
  AppState.currentUser = currentUser;
  AppState.isGuest = false;
  AppState.isTeacherMode = (currentUser.role === 'teacher');

  // Record in teacher students registry
  var registry = [];
  try {
    var raw = localStorage.getItem('sanguofa_student_registry');
    if (raw) registry = JSON.parse(raw);
  } catch(ex) {}
  var existing = registry.find(function(r) { return r.studentId === currentUser.studentId; });
  if (existing) {
    existing.name = currentUser.name;
    existing.role = currentUser.role;
    existing.lastActive = new Date().toISOString();
  } else {
    registry.push({
      studentId: currentUser.studentId,
      name: currentUser.name,
      role: currentUser.role,
      loginTime: currentUser.loginTime,
      lastActive: new Date().toISOString()
    });
  }
  localStorage.setItem('sanguofa_student_registry', JSON.stringify(registry));

  closeLoginModal();
  startApp();
  return false;
}

// Supabase 注册
async function handleSupabaseRegister(e) {
  e.preventDefault();
  if (!supabase) { alert('系统初始化中，请稍后再试'); return false; }
  var name = document.getElementById('regName').value.trim();
  var studentId = document.getElementById('regStudentId').value.trim();
  var email = document.getElementById('regEmail').value.trim();
  var role = document.getElementById('regRole').value;
  var password = document.getElementById('regPassword').value;
  var errorEl = document.getElementById('registerError');
  var btn = document.getElementById('registerBtn');
  errorEl.style.display = 'none';
  btn.textContent = '注册中...';
  btn.disabled = true;

  var result = await supabase.auth.signUp({
    email: email,
    password: password,
    options: {
      data: { name: name, studentId: studentId, role: role }
    }
  });
  var data = result.data;
  var error = result.error;

  btn.textContent = '注 册';
  btn.disabled = false;

  if (error) {
    var msg = '注册失败';
    if (error.message && error.message.indexOf('already registered') >= 0) {
      msg = '该邮箱已被注册，请直接登录';
    } else if (error.message && error.message.indexOf('Password') >= 0) {
      msg = error.message;
    } else {
      msg = error.message || msg;
    }
    errorEl.textContent = msg;
    errorEl.style.display = 'block';
    return false;
  }

  // 注册成功
  if (data.session) {
    // 直接获得session（邮箱验证未启用时）
    var user = data.user;
    var currentUser = {
      id: user.id,
      email: email,
      studentId: studentId,
      name: name,
      role: role,
      loginTime: new Date().toISOString()
    };
    localStorage.setItem('sanguofa_current_user', JSON.stringify(currentUser));
    AppState.currentUser = currentUser;
    AppState.isGuest = false;
    AppState.isTeacherMode = (role === 'teacher');
    closeLoginModal();
    startApp();
  } else {
    // 需要邮箱验证
    errorEl.textContent = '注册成功！请检查邮箱验证后登录。';
    errorEl.style.color = '#2e7d32';
    errorEl.style.display = 'block';
    setTimeout(function() { switchAuthTab('login'); }, 3000);
  }
  return false;
}

// 检查 Supabase 登录状态
async function checkAuthState() {
  if (!supabase) return false;
  var result = await supabase.auth.getSession();
  var session = result.data.session;
  if (session && session.user) {
    var user = session.user;
    var metadata = user.user_metadata || {};
    var savedUser = {
      id: user.id,
      email: user.email,
      studentId: metadata.studentId || '',
      name: metadata.name || user.email,
      role: metadata.role || 'student',
      loginTime: new Date().toISOString()
    };
    AppState.currentUser = savedUser;
    AppState.isGuest = false;
    AppState.isTeacherMode = (savedUser.role === 'teacher');
    localStorage.setItem('sanguofa_current_user', JSON.stringify(savedUser));
    return true;
  }
  return false;
}

// 监听 auth 状态变化
if (typeof window.supabase !== 'undefined') {
  (function setupAuthListener() {
    if (supabase) {
      supabase.auth.onAuthStateChange(function(event, session) {
        if (event === 'SIGNED_OUT') {
          AppState.currentUser = null;
          AppState.isGuest = true;
        }
      });
    } else {
      setTimeout(setupAuthListener, 500);
    }
  })();
}

function showLoginModal() {
  var overlay = document.getElementById('loginOverlay');
  if (overlay) {
    overlay.classList.add('visible');
    // Reset to login tab
    switchAuthTab('login');
    // Reset forms and errors
    var loginForm = document.getElementById('loginForm');
    if (loginForm) loginForm.reset();
    var registerForm = document.getElementById('registerForm');
    if (registerForm) registerForm.reset();
    var errorEls = document.querySelectorAll('.login-error');
    errorEls.forEach(function(el) { el.style.display = 'none'; el.textContent = ''; });
    // Focus first input
    setTimeout(function() {
      var firstInput = document.getElementById('loginEmail');
      if (firstInput) firstInput.focus();
    }, 100);
  }
}

function closeLoginModal() {
  var overlay = document.getElementById('loginOverlay');
  if (overlay) overlay.classList.remove('visible');
}'''

if old_login_functions in content:
    content = content.replace(old_login_functions, new_login_functions, 1)
    changes += 1
    print("[5] Replaced login/logout functions with Supabase auth")
else:
    print("[5] ERROR: Could not find login functions")
    sys.exit(1)

# ============================================================
# 6. Replace handleLogout function
# ============================================================
old_logout = '''function handleLogout() {
  localStorage.removeItem('sanguofa_current_user');
  AppState.currentUser = null;
  AppState.isGuest = true;
  AppState.isTeacherMode = false;
  AppState.studentProgress = {};
  AppState.currentPage = 'dashboard';
  
  // Re-render everything for guest mode
  renderNavbar();
  renderDashboard();
  renderQAModule();
  renderCaseModule();
  renderAssessModule();
  renderIdeologyModule();
  showPage('dashboard');
}'''

new_logout = '''async function handleLogout() {
  // Supabase sign out
  if (supabase) {
    try { await supabase.auth.signOut(); } catch(e) { console.warn('[Supabase] signOut error:', e); }
  }
  localStorage.removeItem('sanguofa_current_user');
  AppState.currentUser = null;
  AppState.isGuest = true;
  AppState.isTeacherMode = false;
  AppState.studentProgress = {};
  AppState.currentPage = 'dashboard';
  
  // Re-render everything for guest mode
  renderNavbar();
  renderDashboard();
  renderQAModule();
  renderCaseModule();
  renderAssessModule();
  renderIdeologyModule();
  showPage('dashboard');
  
  // Show login overlay
  showLoginModal();
}'''

if old_logout in content:
    content = content.replace(old_logout, new_logout, 1)
    changes += 1
    print("[6] Replaced handleLogout function")
else:
    print("[6] ERROR: Could not find handleLogout function")
    sys.exit(1)

# ============================================================
# 7. Update DOMContentLoaded to handle async initApp
# ============================================================
old_dom_ready = "document.addEventListener('DOMContentLoaded', initApp);"
new_dom_ready = "document.addEventListener('DOMContentLoaded', function() { initApp(); });"

if old_dom_ready in content:
    content = content.replace(old_dom_ready, new_dom_ready, 1)
    changes += 1
    print("[7] Updated DOMContentLoaded handler")
else:
    print("[7] ERROR: Could not find DOMContentLoaded handler")
    sys.exit(1)

# ============================================================
# Write the file
# ============================================================
with open(FILE_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"\nNew file size: {new_len} chars (delta: {new_len - original_len:+d})")
print(f"Total changes applied: {changes}/7")

if changes == 7:
    print("\n✅ All changes applied successfully!")
else:
    print(f"\n⚠️ Only {changes}/7 changes applied!")
    sys.exit(1)
