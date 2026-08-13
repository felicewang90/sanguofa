#!/usr/bin/env python3
"""
增强脚本：
1. 手机端页面导航 - 浮动返回按钮 + 底部Tab导航栏
2. 教师素材上传入口 - 在个人空间新增素材管理面板
"""

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ==========================================
# 1. CSS: 添加移动端导航样式 + 素材上传样式
# ==========================================
new_css = """
/* === 移动端浮动返回按钮 === */
.mobile-back-btn {
  display: none;
  position: fixed;
  top: 70px;
  left: 12px;
  z-index: 1000;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255,255,255,0.95);
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: var(--primary);
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid rgba(26,42,94,0.1);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}
.mobile-back-btn:hover {
  background: var(--primary);
  color: #fff;
}
.mobile-back-btn.visible {
  display: flex;
}
@media (max-width: 768px) {
  .mobile-back-btn {
    top: 62px;
    left: 8px;
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }
}

/* === 移动端底部Tab导航栏 === */
.mobile-tab-bar {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 999;
  background: rgba(255,255,255,0.97);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid rgba(0,0,0,0.06);
  box-shadow: 0 -2px 16px rgba(0,0,0,0.08);
  padding: 4px 0;
  padding-bottom: calc(4px + env(safe-area-inset-bottom, 0px));
}
.mobile-tab-bar.visible {
  display: flex;
}
.mobile-tab-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 6px 2px 4px;
  font-size: 0.62rem;
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 0.2s;
  text-decoration: none;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
  gap: 2px;
}
.mobile-tab-item:active {
  background: rgba(26,42,94,0.05);
}
.mobile-tab-item.active {
  color: var(--primary);
}
.mobile-tab-item .tab-icon {
  font-size: 1.2rem;
  line-height: 1;
}
.mobile-tab-item .tab-label {
  font-size: 0.58rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
@media (max-width: 768px) {
  /* 给底部留出空间，避免内容被Tab遮挡 */
  .main-content {
    padding-bottom: 60px !important;
  }
  .app-footer {
    margin-bottom: 56px !important;
  }
}

/* === 素材上传面板 === */
.material-upload-panel {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  margin-top: 16px;
}
.material-upload-panel h4 {
  margin: 0 0 12px;
  color: var(--primary);
  font-size: 0.95rem;
}
.material-type-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
.material-type-tab {
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  border: 1.5px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  transition: all 0.2s;
}
.material-type-tab.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}
.material-form-group {
  margin-bottom: 12px;
}
.material-form-group label {
  display: block;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.material-form-group input,
.material-form-group select,
.material-form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1.5px solid var(--border);
  border-radius: 8px;
  font-size: 0.82rem;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
  background: #fff;
}
.material-form-group input:focus,
.material-form-group select:focus,
.material-form-group textarea:focus {
  border-color: var(--primary-light);
  box-shadow: 0 0 0 3px rgba(26,42,94,0.08);
}
.material-form-group textarea {
  min-height: 100px;
  resize: vertical;
  line-height: 1.6;
}
.material-submit-btn {
  padding: 10px 28px;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
}
.material-submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(26,42,94,0.25);
}
.material-list-area {
  margin-top: 16px;
}
.material-item-card {
  padding: 12px 16px;
  background: var(--bg-main);
  border-radius: 10px;
  margin-bottom: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid var(--border);
}
.material-item-card .mat-info {
  flex: 1;
  min-width: 0;
}
.material-item-card .mat-title {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.material-item-card .mat-meta {
  font-size: 0.7rem;
  color: var(--text-light);
  margin-top: 2px;
}
.material-item-card .mat-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}
.mat-del-btn {
  padding: 4px 10px;
  font-size: 0.72rem;
  border: 1px solid #e74c3c;
  color: #e74c3c;
  border-radius: 6px;
  cursor: pointer;
  background: transparent;
  transition: all 0.2s;
}
.mat-del-btn:hover {
  background: #e74c3c;
  color: #fff;
}

/* === 教师面板内导航Tab === */
.teacher-sub-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}
.teacher-sub-tab {
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  border: 1.5px solid var(--border);
  background: transparent;
  color: var(--text-secondary);
  transition: all 0.2s;
}
.teacher-sub-tab.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}
"""

# Insert CSS before the 智能摘要头 comment
css_insert_marker = '/* === 智能摘要头'
if css_insert_marker in content:
    content = content.replace(css_insert_marker, new_css + '\n' + css_insert_marker)
    print("✅ CSS inserted")
else:
    print("❌ CSS marker not found!")

# ==========================================
# 2. HTML: 添加移动端Tab栏容器 + 返回按钮
# ==========================================
mobile_nav_html = """
    <!-- 移动端浮动返回按钮 -->
    <button class="mobile-back-btn" id="mobileBackBtn" onclick="goBack()">←</button>
    
    <!-- 移动端底部Tab导航栏 -->
    <nav class="mobile-tab-bar" id="mobileTabBar"></nav>
"""

# Insert after </main>, before footer
footer_marker = '<footer class="app-footer" id="appFooter"></footer>'
if footer_marker in content:
    content = content.replace(footer_marker, mobile_nav_html + '\n    ' + footer_marker)
    print("✅ Mobile nav HTML inserted")
else:
    print("❌ Footer marker not found!")

# ==========================================
# 3. JS: 修改 showPage 函数 - 加入导航历史 + Tab栏更新
# ==========================================
old_showpage = """function showPage(page) {
  
  AppState.currentPage = page;
  
  // 切换到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  
  // 更新导航状态
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.page === page);
  });
  
  // 切换页面显示
  document.querySelectorAll('.page-view').forEach(view => {
    view.classList.toggle('active', view.id === `page-${page}`);
  });
  
  
  // Render graph page when switching to it
  if (page === 'graph') {
    renderKnowledgeGraph();
  }

  // Render profile page when switching to it
  if (page === 'profile') {
    renderProfile();
  }
  
}"""

new_showpage = """function showPage(page) {
  // 导航历史管理 - 用于返回按钮
  if (!window._navHistory) window._navHistory = [];
  var prevPage = AppState.currentPage;
  if (prevPage && prevPage !== page) {
    // 避免重复压栈
    if (window._navHistory.length === 0 || window._navHistory[window._navHistory.length - 1] !== prevPage) {
      window._navHistory.push(prevPage);
      // 最多保留20条历史
      if (window._navHistory.length > 20) window._navHistory.shift();
    }
  }
  
  AppState.currentPage = page;
  
  // 切换到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  // 更新导航状态
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.dataset.page === page);
  });
  
  // 切换页面显示
  document.querySelectorAll('.page-view').forEach(view => {
    view.classList.toggle('active', view.id === `page-${page}`);
  });
  
  // 更新移动端导航状态
  updateMobileNav(page);
  
  // Render graph page when switching to it
  if (page === 'graph') {
    renderKnowledgeGraph();
  }

  // Render profile page when switching to it
  if (page === 'profile') {
    renderProfile();
  }
  
  // 教师面板切换时渲染素材管理
  if (page === 'teacher') {
    renderTeacherPanel();
  }
}

// === 返回上一页 ===
function goBack() {
  if (!window._navHistory || window._navHistory.length === 0) {
    showPage('dashboard');
    return;
  }
  var prevPage = window._navHistory.pop();
  // 不再次压栈（showPage会自动压栈当前页）
  var temp = window._navHistory.slice();
  showPage(prevPage);
  window._navHistory = temp;
}

// === 移动端导航栏更新 ===
var MOBILE_TABS = [
  { page: 'dashboard', icon: '🏠', label: '首页' },
  { page: 'qa', icon: '💬', label: '答疑' },
  { page: 'case', icon: '⚖️', label: '实训' },
  { page: 'assess', icon: '📝', label: '测评' },
  { page: 'graph', icon: '🕸️', label: '图谱' }
];

function initMobileTabBar() {
  var bar = document.getElementById('mobileTabBar');
  if (!bar) return;
  bar.innerHTML = MOBILE_TABS.map(function(tab) {
    return '<div class="mobile-tab-item" data-page="' + tab.page + '" onclick="showPage(\\'' + tab.page + '\\')">' +
      '<span class="tab-icon">' + tab.icon + '</span>' +
      '<span class="tab-label">' + tab.label + '</span>' +
    '</div>';
  }).join('');
}

function updateMobileNav(page) {
  // 更新Tab栏高亮
  var bar = document.getElementById('mobileTabBar');
  if (bar) {
    bar.classList.add('visible');
    bar.querySelectorAll('.mobile-tab-item').forEach(function(item) {
      item.classList.toggle('active', item.dataset.page === page);
    });
  }
  // 更新返回按钮
  var backBtn = document.getElementById('mobileBackBtn');
  if (backBtn) {
    if (page === 'dashboard') {
      backBtn.classList.remove('visible');
    } else {
      backBtn.classList.add('visible');
    }
  }
}"""

if old_showpage in content:
    content = content.replace(old_showpage, new_showpage)
    print("✅ showPage function updated")
else:
    print("❌ showPage marker not found! Trying fuzzy match...")
    # Try to find a partial match
    if 'function showPage(page)' in content and 'AppState.currentPage = page;' in content:
        print("  Found partial match, manual inspection needed")
    else:
        print("  Cannot find showPage at all!")

# ==========================================
# 4. JS: 初始化移动端Tab栏（在应用初始化时调用）
# ==========================================
# Find the init/startup code that runs on load
# Look for where renderNavbar is called initially
init_marker = "// === 页面切换 ==="
if init_marker in content:
    # Insert initMobileTabBar call right before the showPage function
    content = content.replace(
        init_marker,
        "// === 初始化移动端Tab栏 ===\nif (typeof initMobileTabBar === 'function') { /* will be called after definition */ }\n\n" + init_marker
    )
    print("✅ Init marker placed (will init after function defined)")

# Actually, let's add the init call after showPage definition, by appending to the updateMobileNav function
# Better approach: add to the end of the file or at the init section
# Let's find where the app initializes
app_init_marker = "// === 首页/仪表盘 ==="
if app_init_marker in content:
    # Insert init call right before renderDashboard
    init_call = """
// === 初始化移动端导航 ===
(function() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { initMobileTabBar(); });
  } else {
    initMobileTabBar();
  }
})();

"""
    content = content.replace(app_init_marker, init_call + app_init_marker)
    print("✅ Mobile tab bar init call added")

# ==========================================
# 5. JS: 增强教师面板 - 添加素材管理Tab和上传功能
# ==========================================
# Replace the renderTeacherPanel function
old_teacher_render_start = "function renderTeacherPanel() {\n  var container = document.getElementById('page-teacher');\n  var students = getAllStudentsData();"

new_teacher_render_start = """function renderTeacherPanel() {
  var container = document.getElementById('page-teacher');
  
  // 如果没有子Tab状态，默认显示学生管理
  if (!window._teacherSubTab) window._teacherSubTab = 'students';
  
  var subTab = window._teacherSubTab;
  
  // 渲染子Tab导航
  var subTabsHtml = '<div class="teacher-sub-tabs">' +
    '<button class="teacher-sub-tab' + (subTab === 'students' ? ' active' : '') + '" onclick="switchTeacherSubTab(\\'students\\')">📊 学生管理</button>' +
    '<button class="teacher-sub-tab' + (subTab === 'materials' ? ' active' : '') + '" onclick="switchTeacherSubTab(\\'materials\\')">📁 素材管理</button>' +
  '</div>';
  
  if (subTab === 'students') {
    renderTeacherStudentsTab(container, subTabsHtml);
  } else if (subTab === 'materials') {
    renderTeacherMaterialsTab(container, subTabsHtml);
  }
}

function switchTeacherSubTab(tab) {
  window._teacherSubTab = tab;
  renderTeacherPanel();
}

function renderTeacherStudentsTab(container, subTabsHtml) {
  var students = getAllStudentsData();"""

if old_teacher_render_start in content:
    content = content.replace(old_teacher_render_start, new_teacher_render_start)
    print("✅ Teacher panel start updated")
else:
    print("❌ Teacher panel start not found!")

# Now we need to close the renderTeacherStudentsTab function properly
# Find the end of the original renderTeacherPanel function
# It ends just before toggleStudentDetail
old_toggle = "function toggleStudentDetail(idx) {"
new_toggle = """function renderTeacherStudentsTab_END() {
  // This function body is inlined in renderTeacherPanel above
}

function toggleStudentDetail(idx) {"""

# Actually this is tricky - let me find the exact end of the teacher panel render
# The original function ends at exportTeacherCSV's closing brace area
# Let me find the end of the teacher panel render by looking for the closing div pattern

# Let me try a different approach: find the line "function toggleStudentDetail"
# and insert the close of renderTeacherStudentsTab + the new material functions before it

material_functions = """
// === 素材管理面板 ===
function renderTeacherMaterialsTab(container, subTabsHtml) {
  // 加载已保存的素材
  var materials = loadTeacherMaterials();
  
  // 当前选中的素材类型
  if (!window._materialType) window._materialType = 'case';
  
  var caseMatList = materials.filter(function(m) { return m.type === 'case'; });
  var lawMatList = materials.filter(function(m) { return m.type === 'law'; });
  var docMatList = materials.filter(function(m) { return m.type === 'document'; });
  
  var currentList = window._materialType === 'case' ? caseMatList : 
                    window._materialType === 'law' ? lawMatList : docMatList;
  
  var listHtml = '';
  if (currentList.length === 0) {
    listHtml = '<div style="text-align:center;padding:30px;color:var(--text-light);font-size:0.85rem">暂无素材，请在下方添加</div>';
  } else {
    listHtml = currentList.map(function(m, idx) {
      var typeLabel = m.type === 'case' ? '📋 案例' : m.type === 'law' ? '📜 法条' : '📄 政策文件';
      var dateStr = '';
      try { dateStr = new Date(m.createdAt).toLocaleDateString('zh-CN'); } catch(e) {}
      return '<div class="material-item-card">' +
        '<div class="mat-info">' +
          '<div class="mat-title">' + (m.title || '无标题') + '</div>' +
          '<div class="mat-meta">' + typeLabel + ' · ' + (m.subject || '通用') + ' · ' + dateStr + '</div>' +
        '</div>' +
        '<div class="mat-actions">' +
          '<button class="mat-del-btn" onclick="deleteTeacherMaterial(\\'' + m.id + '\\')">删除</button>' +
        '</div>' +
      '</div>';
    }).join('');
  }
  
  container.innerHTML = '<div class="teacher-panel">' +
    '<div class="teacher-panel-header"><h2>📊 教师管理中心</h2></div>' +
    subTabsHtml +
    '<div class="material-upload-panel">' +
      '<h4>📁 素材自主上传</h4>' +
      '<p style="font-size:0.78rem;color:var(--text-secondary);margin-bottom:14px">教师可自主新增三国法案例、核心法条、涉外政策文件，扩充平台知识库。新增素材将即时纳入知识库搜索和智能问答范围。</p>' +
      
      '<div class="material-type-tabs">' +
        '<button class="material-type-tab' + (window._materialType === 'case' ? ' active' : '') + '" onclick="switchMaterialType(\\'case\\')">📋 三国法案例</button>' +
        '<button class="material-type-tab' + (window._materialType === 'law' ? ' active' : '') + '" onclick="switchMaterialType(\\'law\\')">📜 核心法条</button>' +
        '<button class="material-type-tab' + (window._materialType === 'document' ? ' active' : '') + '" onclick="switchMaterialType(\\'document\\')">📄 涉外政策文件</button>' +
      '</div>' +
      
      '<div id="materialForm">' + getMaterialFormHtml(window._materialType) + '</div>' +
    '</div>' +
    
    '<div class="material-list-area" style="margin-top:20px">' +
      '<h4 style="margin-bottom:12px;color:var(--primary)">📚 已上传素材 (' + currentList.length + ')</h4>' +
      listHtml +
    '</div>' +
  '</div>';
}

function getMaterialFormHtml(type) {
  if (type === 'case') {
    return '<div class="material-form-group"><label>案例名称</label><input id="matTitle" placeholder="如：南海仲裁案管辖权争议" /></div>' +
      '<div class="material-form-group"><label>所属学科</label><select id="matSubject">' +
        '<option value="public">国际公法</option><option value="private">国际私法</option><option value="economic">国际经济法</option>' +
      '</select></div>' +
      '<div class="material-form-group"><label>案情摘要</label><textarea id="matContent" placeholder="请描述案件基本情况、争议焦点、裁判结果等..."></textarea></div>' +
      '<div class="material-form-group"><label>关键词（逗号分隔）</label><input id="matKeywords" placeholder="如：管辖权,UNCLOS,南海,仲裁" /></div>' +
      '<button class="material-submit-btn" onclick="submitTeacherMaterial()">✅ 提交案例</button>';
  } else if (type === 'law') {
    return '<div class="material-form-group"><label>法条名称</label><input id="matTitle" placeholder="如：《联合国海洋法公约》第121条" /></div>' +
      '<div class="material-form-group"><label>所属学科</label><select id="matSubject">' +
        '<option value="public">国际公法</option><option value="private">国际私法</option><option value="economic">国际经济法</option>' +
      '</select></div>' +
      '<div class="material-form-group"><label>法条原文</label><textarea id="matContent" placeholder="请输入法条原文内容..."></textarea></div>' +
      '<div class="material-form-group"><label>关键词（逗号分隔）</label><input id="matKeywords" placeholder="如：岛屿,领海,专属经济区" /></div>' +
      '<button class="material-submit-btn" onclick="submitTeacherMaterial()">✅ 提交法条</button>';
  } else {
    return '<div class="material-form-group"><label>文件标题</label><input id="matTitle" placeholder="如：教育部关于加强涉外法治人才培养的意见" /></div>' +
      '<div class="material-form-group"><label>文件类别</label><select id="matSubject">' +
        '<option value="policy">政策法规</option><option value="frontier">前沿动态</option><option value="document">实务文书</option>' +
      '</select></div>' +
      '<div class="material-form-group"><label>文件内容/摘要</label><textarea id="matContent" placeholder="请输入政策文件的核心内容或全文摘要..."></textarea></div>' +
      '<div class="material-form-group"><label>关键词（逗号分隔）</label><input id="matKeywords" placeholder="如：涉外法治,人才培养,教育部" /></div>' +
      '<button class="material-submit-btn" onclick="submitTeacherMaterial()">✅ 提交文件</button>';
  }
}

function switchMaterialType(type) {
  window._materialType = type;
  renderTeacherPanel();
}

function submitTeacherMaterial() {
  var title = document.getElementById('matTitle');
  var subject = document.getElementById('matSubject');
  var content = document.getElementById('matContent');
  var keywords = document.getElementById('matKeywords');
  
  if (!title || !title.value.trim()) {
    showToast('请填写标题/名称');
    return;
  }
  if (!content || !content.value.trim()) {
    showToast('请填写内容');
    return;
  }
  
  var material = {
    id: 'mat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
    type: window._materialType,
    title: title.value.trim(),
    subject: subject ? subject.value : '',
    content: content.value.trim(),
    keywords: keywords ? keywords.value.trim() : '',
    createdAt: new Date().toISOString(),
    source: 'teacher_upload'
  };
  
  // 保存到localStorage
  var materials = loadTeacherMaterials();
  materials.push(material);
  try {
    localStorage.setItem('sanguofa_teacher_materials', JSON.stringify(materials));
  } catch(e) {
    console.warn('localStorage save failed:', e);
  }
  
  // 同步到运行时数据 - 让知识库搜索和问答能用到新素材
  syncTeacherMaterialToRuntime(material);
  
  showToast((material.type === 'case' ? '案例' : material.type === 'law' ? '法条' : '政策文件') + '已添加成功！');
  renderTeacherPanel();
}

function loadTeacherMaterials() {
  try {
    var data = localStorage.getItem('sanguofa_teacher_materials');
    return data ? JSON.parse(data) : [];
  } catch(e) {
    return [];
  }
}

function deleteTeacherMaterial(matId) {
  if (!confirm('确定删除该素材？')) return;
  var materials = loadTeacherMaterials();
  materials = materials.filter(function(m) { return m.id !== matId; });
  try {
    localStorage.setItem('sanguofa_teacher_materials', JSON.stringify(materials));
  } catch(e) {}
  showToast('已删除');
  renderTeacherPanel();
}

// === 将教师上传素材同步到运行时数据 ===
function syncTeacherMaterialToRuntime(material) {
  // 1. 同步到知识库搜索索引（MockData.qaResponses追加）
  if (MockData && MockData.qaResponses) {
    // 查找是否已存在（避免重复）
    var exists = MockData.qaResponses.some(function(q) { return q.id === material.id; });
    if (!exists) {
      MockData.qaResponses.push({
        id: material.id,
        question: material.title,
        answer: material.content,
        keywords: material.keywords ? material.keywords.split(/[,，]/).map(function(k) { return k.trim(); }) : [],
        category: material.subject || 'general',
        type: material.type === 'law' ? 'law' : material.type === 'case' ? 'case' : 'policy',
        source: 'teacher_upload'
      });
    }
  }
  
  // 2. 如果是案例类型，同步到案例实训
  if (material.type === 'case' && typeof FIXED_CASES !== 'undefined') {
    var caseExists = FIXED_CASES.some(function(c) { return c.id === material.id; });
    if (!caseExists) {
      FIXED_CASES.push({
        id: material.id,
        name: material.title,
        subject: material.subject,
        brief: material.content.substring(0, 150) + (material.content.length > 150 ? '...' : ''),
        detail: material.content,
        keywords: material.keywords ? material.keywords.split(/[,，]/).map(function(k) { return k.trim(); }) : [],
        source: 'teacher_upload'
      });
    }
  }
  
  // 3. 如果是法条类型，同步到法条速查
  if (material.type === 'law' && MockData && MockData.laws) {
    var lawExists = MockData.laws.some(function(l) { return l.id === material.id; });
    if (!lawExists) {
      MockData.laws.push({
        id: material.id,
        name: material.title,
        subject: material.subject,
        articles: [{
          number: '自定义',
          text: material.content
        }],
        source: 'teacher_upload'
      });
    }
  }
  
  // 4. 如果是政策文件，同步到涉外法治资鉴
  if (material.type === 'document' && MockData && MockData.ideologyDocs) {
    var docExists = MockData.ideologyDocs.some(function(d) { return d.id === material.id; });
    if (!docExists) {
      MockData.ideologyDocs.push({
        id: material.id,
        title: material.title,
        category: material.subject || 'policy',
        summary: material.content.substring(0, 200),
        content: material.content,
        date: new Date().toLocaleDateString('zh-CN'),
        source: 'teacher_upload'
      });
    }
  }
  
  console.log('[素材同步] 已同步到运行时:', material.type, material.title);
}

// === 应用启动时恢复教师素材 ===
function restoreTeacherMaterials() {
  var materials = loadTeacherMaterials();
  if (materials.length === 0) return;
  
  materials.forEach(function(m) {
    syncTeacherMaterialToRuntime(m);
  });
  console.log('[素材恢复] 已恢复', materials.length, '条教师上传素材');
}

"""

# Insert material functions before toggleStudentDetail
toggle_marker = "function toggleStudentDetail(idx) {"
if toggle_marker in content:
    content = content.replace(toggle_marker, material_functions + toggle_marker)
    print("✅ Material management functions inserted")
else:
    print("❌ toggleStudentDetail marker not found!")

# Now we need to fix the renderTeacherPanel function - the original body needs to be in renderTeacherStudentsTab
# The original renderTeacherPanel body runs from after the new opening to just before toggleStudentDetail
# We need to find the end of the original function body and wrap it properly

# Actually, the issue is that the original function body is now inside renderTeacherPanel 
# but we split it - the students tab should call the original code, and materials tab calls new code
# Let me check if the structure is correct by looking at what we have now

# The new renderTeacherPanel function:
# 1. Checks subTab
# 2. Renders subTabs HTML
# 3. If students -> calls renderTeacherStudentsTab(container, subTabsHtml)
# 4. If materials -> calls renderTeacherMaterialsTab(container, subTabsHtml)
# 
# But the original body code is still there after the new header, not inside renderTeacherStudentsTab
# We need to wrap the original body into renderTeacherStudentsTab

# Let me find the original function body and the students tab function
old_body_start = "function renderTeacherStudentsTab(container, subTabsHtml) {\n  var students = getAllStudentsData();"
# The original body continues until the material_functions we just inserted
# We need to make sure the original body properly closes

# Let me check - after our new material functions, what comes next?
# It should be the toggleStudentDetail function
# And before toggleStudentDetail, we have the restoreTeacherMaterials function
# So the original teacher panel body is between renderTeacherStudentsTab start and the material functions

# Actually, the problem is: the original renderTeacherPanel body code 
# (from "var students = getAllStudentsData()" all the way to the closing "})();" pattern)
# is now floating between our new renderTeacherStudentsTab header and the material functions.
# We need to:
# 1. Close the renderTeacherStudentsTab function properly at the end of the original body
# 2. Make sure the original container.innerHTML = ... structure is preserved

# Let me verify the structure is intact. The original function had:
# var students = getAllStudentsData();
# ... calculations ...
# container.innerHTML = '<div class="teacher-panel">...</div>';
# 
# This should now be inside renderTeacherStudentsTab(container, subTabsHtml)
# The function takes container and subTabsHtml as parameters
# It starts with: var students = getAllStudentsData();
# And the container.innerHTML should include subTabsHtml

# Let me find and modify the container.innerHTML to include subTabsHtml
old_teacher_panel_header = "'<div class=\"teacher-panel-header\">' +"
# We need to add subTabsHtml after the panel header
# Find the original pattern

# Actually, the structure might work already because:
# 1. renderTeacherPanel renders subTabsHtml
# 2. Calls renderTeacherStudentsTab(container, subTabsHtml)  
# 3. renderTeacherStudentsTab starts with: var students = getAllStudentsData();
# 4. The original container.innerHTML starts with '<div class="teacher-panel">'
# 5. We need to inject subTabsHtml inside the teacher-panel div

# Let me find the exact innerHTML construction in the original
orig_innerhtml = "container.innerHTML = '<div class=\"teacher-panel\">' +\n    '<div class=\"teacher-panel-header\">' +"
if orig_innerhtml in content:
    # Replace to include subTabsHtml
    new_innerhtml = "container.innerHTML = '<div class=\"teacher-panel\">' +\n    '<div class=\"teacher-panel-header\">' +"
    # Actually we need to add subTabsHtml after the header
    # Find the full header block
    orig_header_block = "'<div class=\"teacher-panel-header\">' +\n      '<h2>📊 教师管理面板</h2>' +"
    new_header_block = "'<div class=\"teacher-panel-header\">' +\n      '<h2>📊 教师管理面板</h2>' +\n      subTabsHtml +"
    
    if orig_header_block in content:
        content = content.replace(orig_header_block, new_header_block)
        print("✅ Added subTabsHtml to students tab header")
    else:
        print("⚠️ Could not find exact header block, trying alternative...")
        # Try another pattern
        alt_header = "'<h2>📊 教师管理面板</h2>' +"
        if alt_header in content:
            content = content.replace(alt_header, "'<h2>📊 教师管理面板</h2>' +\n      subTabsHtml +", 1)
            print("✅ Added subTabsHtml via alternative match")
        else:
            print("❌ Cannot find header to inject subTabsHtml")
else:
    print("⚠️ innerHTML pattern not found, checking alternative...")
    # The format might be different, let's try a simpler approach
    if "'<h2>📊 教师管理面板</h2>'" in content:
        content = content.replace(
            "'<h2>📊 教师管理面板</h2>' +",
            "'<h2>📊 教师管理面板</h2>' +\n      subTabsHtml +",
            1
        )
        print("✅ Added subTabsHtml via simpler match")

# ==========================================
# 6. JS: 在应用初始化时恢复教师素材
# ==========================================
# Find the app startup/init code
# Look for the init call or DOMContentLoaded
init_section = "// === 初始化移动端Tab栏 ==="
if init_section in content:
    content = content.replace(
        init_section,
        "// === 恢复教师上传素材 ===\nif (typeof restoreTeacherMaterials === 'function') { setTimeout(restoreTeacherMaterials, 500); }\n\n" + init_section
    )
    print("✅ Teacher materials restore call added")

# ==========================================
# 7. Fix: 确保移动端Tab栏在初始化时被调用
# ==========================================
# The initMobileTabBar function is defined after showPage, but the IIFE that calls it
# is placed before the function definition. Let's fix this by moving the call
# to right after the function definition.

# Actually, the IIFE checks document.readyState, so if the DOM is already loaded,
# it calls initMobileTabBar() directly. Since the function is defined by then, it should work.
# But let's verify the order is correct.

# Let's also add a call to updateMobileNav after init
init_iife = """(function() {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() { initMobileTabBar(); });
  } else {
    initMobileTabBar();
  }
})();"""

new_init_iife = """(function() {
  function doInit() {
    initMobileTabBar();
    // 初始化当前页面的移动端导航状态
    if (AppState && AppState.currentPage) {
      updateMobileNav(AppState.currentPage);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', doInit);
  } else {
    doInit();
  }
})();"""

if init_iife in content:
    content = content.replace(init_iife, new_init_iife)
    print("✅ Enhanced init IIFE")

# ==========================================
# Write output
# ==========================================
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ All enhancements applied! File size: {len(content)} chars")
