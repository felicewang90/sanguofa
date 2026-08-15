#!/usr/bin/env python3
"""修复教师面板：素材管理 + 移动端布局 + 底部导航栏"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# ===== 1. CSS ADDITIONS =====
css_new = """

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

# Insert CSS after @media 768px block
m = re.search(r'@media\s*\(max-width:\s*768px\)', content)
s = m.start()
depth = 0
css_pos = s
for i in range(s, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            css_pos = i + 1
            break

content = content[:css_pos] + css_new + content[css_pos:]

# Recalculate positions after CSS insertion
css_added_len = len(css_new)
html_insert = content.index('</main>')

# ===== 2. HTML ADDITIONS (mobile back button + tab bar) =====
html_new = """
    <!-- 移动端浮动返回按钮 -->
    <button class="mobile-back-btn" id="mobileBackBtn" onclick="goBack()">←</button>
    
    <!-- 移动端底部Tab导航栏 -->
    <nav class="mobile-tab-bar" id="mobileTabBar"></nav>
"""

content = content[:html_insert] + html_new + content[html_insert:]

html_added_len = len(html_new)

# ===== 3. REPLACE showPage function =====
showpage_new = """
// === 页面切换 ===
function showPage(page) {
  // 导航历史管理 - 用于返回按钮
  if (!window._navHistory) window._navHistory = [];
  var prevPage = AppState.currentPage;
  if (prevPage && prevPage !== page) {
    if (window._navHistory.length === 0 || window._navHistory[window._navHistory.length - 1] !== prevPage) {
      window._navHistory.push(prevPage);
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
  
  // 切换 page-view
  document.querySelectorAll('.page-view').forEach(view => {
    view.classList.toggle('active', view.id === `page-${page}`);
  });
  
  // 更新移动端导航状态
  updateMobileNav(page);
  
  // Render graph page when switching to it
  if (page === 'graph') {
    setTimeout(renderGraph, 100);
  }
  
  if (page === 'profile') {
    renderProfile();
  }
  
  // 教师面板切换时渲染素材管理
  if (page === 'teacher') {
    renderTeacherPanel();
  }
}
"""

# Find showPage function
m = re.search(r'\n// === 页面切换 ===\nfunction showPage\(page\)\s*\{', content)
sp_start = m.start() + 1
depth = 0
sp_end = sp_start
for i in range(sp_start, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            sp_end = i + 1
            break

content = content[:sp_start] + showpage_new.strip() + content[sp_end:]

sp_change = len(showpage_new.strip()) - (sp_end - sp_start)

# ===== 4. REPLACE renderTeacherPanel function =====
rtp_new = """
// === 教师管理面板（含子Tab） ===
function renderTeacherPanel() {
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
  var students = getAllStudentsData();
  students = students.filter(function(s) { return s.role !== 'teacher'; });
  
  var totalStudents = students.length;
  var avgScore = totalStudents > 0 ? Math.round(students.reduce(function(s, st) { return s + st.avgScore; }, 0) / totalStudents) : 0;
  var completedRate = totalStudents > 0 ? Math.round(students.filter(function(s) { return s.completedCases >= 3; }).length / totalStudents * 100) : 0;
  var totalCases = FIXED_CASES.length;
  
  var lastActive = '-';
  if (students.length > 0) {
    var latest = students.reduce(function(a, b) { return (a.lastActive > b.lastActive) ? a : b; });
    try { lastActive = new Date(latest.lastActive).toLocaleDateString('zh-CN'); } catch(e) {}
  }
  
  var rows = students.map(function(st, idx) {
    var lastActiveStr = '-';
    try { lastActiveStr = new Date(st.lastActive).toLocaleDateString('zh-CN'); } catch(e) {}
    return '<tr onclick="toggleStudentDetail(' + idx + ')" style="cursor:pointer">' +
      '<td><strong>' + st.studentId + '</strong></td>' +
      '<td>' + st.name + '</td>' +
      '<td>' + st.completedCases + ' / ' + (st.totalCases || totalCases) + '</td>' +
      '<td>' + st.avgScore + '分</td>' +
      '<td>' +
        '<div class="teacher-bar"><div class="teacher-bar-fill" style="width:' + st.progress + '%"></div></div>' +
      '</td>' +
      '<td>' + lastActiveStr + '</td>' +
    '</tr>' +
    '<tr id="studentDetail_' + idx + '" style="display:none">' +
      '<td colspan="6" style="background:#f8f9fc;padding:16px">' +
        '<div style="font-size:0.82rem;color:var(--text-secondary)">案例成绩详情：</div>' +
        '<div style="margin-top:8px;display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px">' +
          (function() {
            var caseNames = FIXED_CASES.map(function(c) { return c.name; });
            var html = '';
            caseNames.forEach(function(cName) {
              var sc = st.caseScores && st.caseScores[cName];
              var scoreText = sc ? sc.score + '分' : '未完成';
              var color = sc ? (sc.score >= 80 ? 'var(--success)' : sc.score >= 60 ? 'var(--accent)' : '#e74c3c') : 'var(--text-light)';
              html += '<div style="padding:8px 12px;background:#fff;border-radius:8px;border:1px solid var(--border);font-size:0.78rem">' +
                '<div style="color:var(--text-secondary);margin-bottom:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis" title="' + cName + '">' + cName.substring(0, 12) + '</div>' +
                '<div style="font-weight:700;color:' + color + '">' + scoreText + '</div></div>';
            });
            return html;
          })() +
        '</div>' +
      '</td>' +
    '</tr>';
  }).join('');
  
  container.innerHTML = '<div class="teacher-panel">' +
    '<div class="teacher-panel-header">' +
      '<h2>📊 教师管理面板</h2>' +
      subTabsHtml +
      '<div style="display:flex;gap:10px">' +
        '<button class="teacher-export-btn" style="background:var(--primary)" onclick="generateDemoStudentData()">🎲 模拟数据</button>' +
        '<button class="teacher-export-btn" onclick="exportTeacherCSV()">📥 导出CSV报告</button>' +
      '</div>' +
    '</div>' +
    '<div class="teacher-stats-grid">' +
      '<div class="teacher-stat-card"><div class="ts-num">' + totalStudents + '</div><div class="ts-label">学生总数</div></div>' +
      '<div class="teacher-stat-card"><div class="ts-num">' + avgScore + '</div><div class="ts-label">平均分</div></div>' +
      '<div class="teacher-stat-card"><div class="ts-num">' + completedRate + '%</div><div class="ts-label">完成率(>=3案例)</div></div>' +
      '<div class="teacher-stat-card"><div class="ts-num">' + lastActive + '</div><div class="ts-label">最近活跃</div></div>' +
    '</div>' +
    '<div class="teacher-table-wrap">' +
      '<table class="teacher-table">' +
        '<thead><tr><th>学号</th><th>姓名</th><th>完成案例</th><th>平均分</th><th>学习进度</th><th>最近活跃</th></tr></thead>' +
        '<tbody>' + rows + '</tbody>' +
      '</table>' +
    '</div>' +
    '<div style="background:var(--bg-card);border-radius:var(--radius-md);padding:20px;box-shadow:var(--shadow-sm)">' +
      '<h4 style="margin-bottom:12px;color:var(--primary)">📈 班级案例完成率</h4>' +
      '<div class="case-stats-grid">' +
        FIXED_CASES.map(function(c, i) {
          var count = students.filter(function(s) { return s.completedCases > i; }).length;
          var pct = totalStudents > 0 ? Math.round(count / totalStudents * 100) : 0;
          return '<div class="case-stat-item">' +
            '<div class="case-stat-name" title="' + c.name + '">' + c.name.substring(0, 10) + '</div>' +
            '<div class="case-stat-pct">' + pct + '%</div>' +
            '<div class="teacher-bar" style="margin-top:6px"><div class="teacher-bar-fill" style="width:' + pct + '%"></div></div>' +
          '</div>';
        }).join('') +
      '</div>' +
    '</div>' +
  '</div>';
}

// === 素材管理面板 ===
function renderTeacherMaterialsTab(container, subTabsHtml) {
  var materials = loadTeacherMaterials();
  
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
    listHtml = currentList.map(function(m) {
      var typeLabel = m.type === 'case' ? '📋 案例' : m.type === 'law' ? ' 法条' : '📄 政策文件';
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
        '<button class="material-type-tab' + (window._materialType === 'case' ? ' active' : '') + '" onclick="switchMaterialType(\\'case\\')"> 三国法案例</button>' +
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
  var content_el = document.getElementById('matContent');
  var keywords = document.getElementById('matKeywords');
  
  if (!title || !title.value.trim()) {
    showToast('请填写标题/名称');
    return;
  }
  if (!content_el || !content_el.value.trim()) {
    showToast('请填写内容');
    return;
  }
  
  var material = {
    id: 'mat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 6),
    type: window._materialType,
    title: title.value.trim(),
    subject: subject ? subject.value : '',
    content: content_el.value.trim(),
    keywords: keywords ? keywords.value.trim() : '',
    createdAt: new Date().toISOString(),
    source: 'teacher_upload'
  };
  
  var materials = loadTeacherMaterials();
  materials.push(material);
  try {
    localStorage.setItem('sanguofa_teacher_materials', JSON.stringify(materials));
  } catch(e) {
    console.warn('localStorage save failed:', e);
  }
  
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

function syncTeacherMaterialToRuntime(material) {
  if (MockData && MockData.qaResponses) {
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
  
  if (material.type === 'law' && MockData && MockData.laws) {
    var lawExists = MockData.laws.some(function(l) { return l.id === material.id; });
    if (!lawExists) {
      MockData.laws.push({
        id: material.id,
        name: material.title,
        subject: material.subject,
        articles: [{ number: '自定义', text: material.content }],
        source: 'teacher_upload'
      });
    }
  }
  
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

function restoreTeacherMaterials() {
  var materials = loadTeacherMaterials();
  if (materials.length === 0) return;
  materials.forEach(function(m) { syncTeacherMaterialToRuntime(m); });
  console.log('[素材恢复] 已恢复', materials.length, '条教师上传素材');
}
"""

# Find renderTeacherPanel
m = re.search(r'\nfunction renderTeacherPanel\(\)\s*\{', content)
rtp_start = m.start() + 1
depth = 0
rtp_end = rtp_start
for i in range(rtp_start, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            rtp_end = i + 1
            break

content = content[:rtp_start] + rtp_new.strip() + content[rtp_end:]

rtp_change = len(rtp_new.strip()) - (rtp_end - rtp_start)

# ===== 5. ADD mobile nav functions + goBack before toggleStudentDetail =====
mobile_nav_js = """

// === 返回上一页 ===
function goBack() {
  if (!window._navHistory || window._navHistory.length === 0) {
    showPage('dashboard');
    return;
  }
  var prevPage = window._navHistory.pop();
  var temp = window._navHistory.slice();
  showPage(prevPage);
  window._navHistory = temp;
}

// === 移动端导航栏更新 ===
var MOBILE_TABS = [
  { page: 'dashboard', icon: '', label: '首页' },
  { page: 'qa', icon: '💬', label: '答疑' },
  { page: 'case', icon: '⚖️', label: '实训' },
  { page: 'assess', icon: '📝', label: '测评' },
  { page: 'graph', icon: '️', label: '图谱' }
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
  var bar = document.getElementById('mobileTabBar');
  if (bar) {
    bar.classList.add('visible');
    bar.querySelectorAll('.mobile-tab-item').forEach(function(item) {
      item.classList.toggle('active', item.dataset.page === page);
    });
  }
  var backBtn = document.getElementById('mobileBackBtn');
  if (backBtn) {
    if (page === 'dashboard') {
      backBtn.classList.remove('visible');
    } else {
      backBtn.classList.add('visible');
    }
  }
}

// === 初始化移动端导航 ===
(function() {
  function doInit() {
    initMobileTabBar();
    if (AppState && AppState.currentPage) {
      updateMobileNav(AppState.currentPage);
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', doInit);
  } else {
    doInit();
  }
})();

// === 应用启动时恢复教师素材 ===
if (typeof restoreTeacherMaterials === 'function') { setTimeout(restoreTeacherMaterials, 500); }

"""

# Find toggleStudentDetail
toggle_pos = content.index('\nfunction toggleStudentDetail')

content = content[:toggle_pos] + mobile_nav_js + content[toggle_pos:]

# ===== 6. Add mobile responsive CSS for teacher panel =====
# Add to the existing @media 768px block
mobile_teacher_css = """
  
  /* 教师面板移动端适配 */
  .teacher-stats-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  .teacher-table-wrap {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  .teacher-table {
    min-width: 600px;
  }
  .case-stats-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
  .case-stat-item {
    padding: 10px !important;
  }
  .teacher-sub-tabs {
    flex-wrap: wrap;
  }
  .teacher-sub-tab {
    font-size: 0.75rem;
    padding: 6px 14px;
  }
  .material-type-tabs {
    flex-wrap: wrap;
  }
  .material-type-tab {
    font-size: 0.72rem;
    padding: 5px 12px;
  }
  .mobile-back-btn {
    top: 62px;
    left: 8px;
    width: 36px;
    height: 36px;
    font-size: 1rem;
  }
  .main-content {
    padding-bottom: 60px !important;
  }
  .app-footer {
    margin-bottom: 56px !important;
  }
"""

# Find the @media 768px block again (positions shifted)
m = re.search(r'@media\s*\(max-width:\s*768px\)', content)
s = m.start()
depth = 0
media_end = s
for i in range(s, len(content)):
    if content[i] == '{': depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            media_end = i
            break

# Insert before the closing }
content = content[:media_end] + mobile_teacher_css + content[media_end:]

# ===== SAVE =====
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Done! New file size: {len(content)} bytes")
print("Modifications:")
print("  1. CSS: +material/tabs/mobile-back styles")
print("  2. HTML: +mobile back button + tab bar")
print("  3. JS: showPage enhanced with nav history + mobile nav")
print("  4. JS: renderTeacherPanel → sub-tabs (students/materials)")
print("  5. JS: +material management functions (8 new functions)")
print("  6. JS: +mobile nav functions (goBack, initMobileTabBar, updateMobileNav)")
print("  7. CSS: +mobile responsive for teacher panel")
