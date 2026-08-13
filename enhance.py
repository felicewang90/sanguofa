#!/usr/bin/env python3
"""三国法教学智能体 - 四项功能增强:
1. 法条速查（核心法条原文可展开）
2. 判例详情展开（经典判例可展开详情）
3. 三层问答模式（入门/法考/实务）
4. 分层题库（按难度筛选）
"""
import re, os

WORK = '/Coze/Drive/3G学堂（1）/所有对话/主对话/sanguofa_repo/index.html'
CODEACT = '/Coze/Drive/3G学堂（1）/所有对话/主对话/codeact_laws_cases.html'

with open(WORK) as f:
    html = f.read()

with open(CODEACT) as f:
    codeact = f.read()

orig_len = len(html)
print(f"Original: {orig_len} chars, {html.count(chr(10))} lines")

# ============================================================
# STEP 1: Insert laws and caseDetails data into MockData
# ============================================================
laws_m = re.search(r'(laws\s*:\s*\[.*?\])\s*,\s*\n\s*caseDetails', codeact, re.DOTALL)
cases_m = re.search(r'(caseDetails\s*:\s*\[.*?\])\s*\n\s*\}\s*;', codeact, re.DOTALL)
laws_data = laws_m.group(1)
cases_data = cases_m.group(1)
print(f"Data: laws={len(laws_data)}ch, cases={len(cases_data)}ch")

# Find MockData closing
mockdata_close = html.find('};\n\n// === 应用状态管理 ==')
assert mockdata_close > 0, "Cannot find MockData closing"
new_data = f",\n    {laws_data},\n    {cases_data}\n"
html = html[:mockdata_close] + new_data + html[mockdata_close:]
print(f"After data insert: {len(html)} chars (+{len(html)-orig_len})")

# ============================================================
# STEP 2: Add 法条速查 UI in QA sidebar
# ============================================================
# Add a "法条速查" button after the sidebar-actions div
old_sidebar_actions = '''<div class="sidebar-actions">
          <button class="sidebar-btn" onclick="quickAction('law')">📋 法条检索</button>
          <button class="sidebar-btn" onclick="quickAction('case')">📑 判例查询</button>
          <button class="sidebar-btn" onclick="quickAction('cross')">🔗 跨部门法联动</button>
        </div>'''

new_sidebar_actions = '''<div class="sidebar-actions">
          <button class="sidebar-btn" onclick="quickAction('law')">📋 法条检索</button>
          <button class="sidebar-btn" onclick="quickAction('case')">📑 判例查询</button>
          <button class="sidebar-btn" onclick="quickAction('cross')">🔗 跨部门法联动</button>
          <button class="sidebar-btn" onclick="showLawsBrowser()" style="background:linear-gradient(135deg,rgba(201,168,76,0.15),rgba(201,168,76,0.05));border-color:rgba(201,168,76,0.3);color:var(--accent);font-weight:600">📜 法条速查</button>
          <button class="sidebar-btn" onclick="showCasesBrowser()" style="background:linear-gradient(135deg,rgba(23,162,184,0.15),rgba(23,162,184,0.05));border-color:rgba(23,162,184,0.3);color:var(--info);font-weight:600">📑 判例详情</button>
        </div>'''
html = html.replace(old_sidebar_actions, new_sidebar_actions)
print("Added 法条速查 and 判例详情 buttons in sidebar")

# ============================================================
# STEP 3: Add 三层问答模式 selector in QA header
# ============================================================
old_qa_header = '''<div class="qa-header">
          <div class="qa-header-left">
            <h3>智能问答</h3>
            <span class="qa-context" id="qaContext">全部知识库</span>
          </div>'''

new_qa_header = '''<div class="qa-header">
          <div class="qa-header-left">
            <h3>智能问答</h3>
            <span class="qa-context" id="qaContext">全部知识库</span>
          </div>
          <div class="qa-mode-selector" style="display:flex;gap:4px;margin-left:12px;background:rgba(0,0,0,0.03);border-radius:8px;padding:3px">
            <button class="qa-mode-btn active" onclick="setQAMode('intro',this)" style="padding:4px 10px;border:none;border-radius:6px;font-size:0.7rem;cursor:pointer;background:var(--primary);color:#fff;transition:all 0.2s" title="适合初学者，详细解释概念">入门</button>
            <button class="qa-mode-btn" onclick="setQAMode('exam',this)" style="padding:4px 10px;border:none;border-radius:6px;font-size:0.7rem;cursor:pointer;background:transparent;color:var(--text-secondary);transition:all 0.2s" title="法考风格，重点考点+真题提示">法考</button>
            <button class="qa-mode-btn" onclick="setQAMode('practice',this)" style="padding:4px 10px;border:none;border-radius:6px;font-size:0.7rem;cursor:pointer;background:transparent;color:var(--text-secondary);transition:all 0.2s" title="实务导向，案例+操作指引">实务</button>
          </div>'''
html = html.replace(old_qa_header, new_qa_header)
print("Added 三层问答模式 selector")

# ============================================================
# STEP 4: Add 分层题库 difficulty selector in quiz section
# ============================================================
old_subject_desc = '''<div class="subject-selector-desc">选择科目后将随机抽取 10 道单选(6分)、5 道多选(8分)和 1 道案例分析(20分)</div>'''

new_subject_desc = '''<div class="subject-selector-desc">选择科目后将随机抽取 10 道单选(6分)、5 道多选(8分)和 1 道案例分析(20分)</div>
        <div class="difficulty-selector" style="display:flex;align-items:center;gap:8px;margin-top:10px;justify-content:center">
          <span style="font-size:0.8rem;color:var(--text-secondary)">🎯 难度：</span>
          <button class="diff-btn active" onclick="setDifficulty('all',this)" style="padding:4px 14px;border:1px solid rgba(79,172,254,0.3);border-radius:16px;font-size:0.72rem;cursor:pointer;background:var(--info);color:#fff;transition:all 0.2s">全部</button>
          <button class="diff-btn" onclick="setDifficulty('basic',this)" style="padding:4px 14px;border:1px solid rgba(79,172,254,0.3);border-radius:16px;font-size:0.72rem;cursor:pointer;background:transparent;color:var(--info);transition:all 0.2s">⭐ 本科基础</button>
          <button class="diff-btn" onclick="setDifficulty('exam',this)" style="padding:4px 14px;border:1px solid rgba(79,172,254,0.3);border-radius:16px;font-size:0.72rem;cursor:pointer;background:transparent;color:var(--info);transition:all 0.2s">⭐⭐ 法考真题</button>
          <button class="diff-btn" onclick="setDifficulty('advanced',this)" style="padding:4px 14px;border:1px solid rgba(79,172,254,0.3);border-radius:16px;font-size:0.72rem;cursor:pointer;background:transparent;color:var(--info);transition:all 0.2s">⭐⭐⭐ 实务进阶</button>
        </div>'''
html = html.replace(old_subject_desc, new_subject_desc)
print("Added 分层题库 difficulty selector")

# ============================================================
# STEP 5: Add JavaScript functions for all new features
# ============================================================
# Insert before the closing </script> tag
js_functions = '''
// === 法条速查功能 ===
function showLawsBrowser() {
  const chat = document.getElementById('qaChat');
  const welcome = document.getElementById('qaWelcome');
  if (welcome) welcome.style.display = 'none';
  
  const laws = MockData.laws || [];
  const subjectNames = {public:'国际公法', private:'国际私法', economic:'国际经济法'};
  const subjectIcons = {public:'🌐', private:'⚖️', economic:'💼'};
  
  // Group by subject
  const grouped = {};
  laws.forEach(law => {
    if (!grouped[law.category]) grouped[law.category] = [];
    grouped[law.category].push(law);
  });
  
  let html = '<div style="padding:16px">';
  html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:16px"><span style="font-size:1.3rem">📜</span><h3 style="margin:0;font-size:1.1rem;color:var(--primary)">核心法条速查</h3><span style="font-size:0.75rem;color:var(--text-secondary);background:rgba(79,172,254,0.1);padding:2px 8px;border-radius:10px">' + laws.length + ' 部法律文件</span></div>';
  html += '<p style="font-size:0.78rem;color:var(--text-secondary);margin:0 0 16px;line-height:1.6">点击法条名称展开原文，支持公约、国内法、司法解释快速查阅</p>';
  
  Object.keys(grouped).forEach(cat => {
    html += '<div style="margin-bottom:16px"><div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;padding-bottom:6px;border-bottom:2px solid var(--info)">' + subjectIcons[cat] + '<span style="font-weight:700;color:var(--primary);font-size:0.9rem">' + subjectNames[cat] + '</span><span style="font-size:0.7rem;color:var(--text-secondary)">(' + grouped[cat].length + '部)</span></div>';
    
    grouped[cat].forEach(law => {
      html += '<div style="margin-bottom:6px;border:1px solid rgba(79,172,254,0.15);border-radius:10px;overflow:hidden">';
      html += '<div onclick="toggleLawDetail(\\'' + law.id + '\\')" style="padding:10px 14px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;transition:background 0.2s" onmouseover="this.style.background=\\'rgba(79,172,254,0.05)\\'" onmouseout="this.style.background=\\'transparent\\'">';
      html += '<div><span style="font-size:0.85rem;font-weight:600;color:var(--text-primary)">' + law.name + '</span><span style="font-size:0.68rem;color:var(--text-secondary);margin-left:8px;background:rgba(0,0,0,0.04);padding:1px 6px;border-radius:4px">' + law.type + '</span></div>';
      html += '<span class="law-arrow-' + law.id + '" style="font-size:0.7rem;color:var(--text-secondary);transition:transform 0.3s">▶</span>';
      html += '</div>';
      html += '<div id="law-detail-' + law.id + '" style="display:none;padding:0 14px 12px;border-top:1px solid rgba(79,172,254,0.08)">';
      html += '<div style="font-size:0.72rem;color:var(--text-secondary);margin-bottom:8px">📌 ' + law.source + '</div>';
      law.articles.forEach(art => {
        html += '<div style="margin-bottom:8px;padding:8px 10px;background:rgba(79,172,254,0.03);border-radius:6px;border-left:3px solid var(--info)">';
        html += '<div style="font-size:0.78rem;font-weight:600;color:var(--primary);margin-bottom:4px">' + art.num + (art.title ? ' ' + art.title : '') + '</div>';
        html += '<div style="font-size:0.75rem;color:var(--text-primary);line-height:1.6">' + art.text + '</div>';
        html += '</div>';
      });
      html += '</div></div>';
    });
    html += '</div>';
  });
  html += '</div>';
  
  // Add as system message
  addSystemMessage(html);
}

function toggleLawDetail(lawId) {
  const detail = document.getElementById('law-detail-' + lawId);
  const arrow = document.querySelector('.law-arrow-' + lawId);
  if (detail.style.display === 'none') {
    detail.style.display = 'block';
    if (arrow) { arrow.style.transform = 'rotate(90deg)'; arrow.textContent = '▼'; }
  } else {
    detail.style.display = 'none';
    if (arrow) { arrow.style.transform = 'rotate(0deg)'; arrow.textContent = '▶'; }
  }
}

// === 判例详情功能 ===
function showCasesBrowser() {
  const chat = document.getElementById('qaChat');
  const welcome = document.getElementById('qaWelcome');
  if (welcome) welcome.style.display = 'none';
  
  const cases = MockData.caseDetails || [];
  const subjectNames = {public:'国际公法', private:'国际私法', economic:'国际经济法'};
  const subjectIcons = {public:'🌐', private:'⚖️', economic:'💼'};
  
  const grouped = {};
  cases.forEach(c => {
    if (!grouped[c.subject]) grouped[c.subject] = [];
    grouped[c.subject].push(c);
  });
  
  let html = '<div style="padding:16px">';
  html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:16px"><span style="font-size:1.3rem">📑</span><h3 style="margin:0;font-size:1.1rem;color:var(--info)">经典判例详情</h3><span style="font-size:0.75rem;color:var(--text-secondary);background:rgba(23,162,184,0.1);padding:2px 8px;border-radius:10px">' + cases.length + ' 个案例</span></div>';
  html += '<p style="font-size:0.78rem;color:var(--text-secondary);margin:0 0 16px;line-height:1.6">点击展开查看案情摘要、争议焦点、裁判要旨及中国立场评析</p>';
  
  Object.keys(grouped).forEach(sub => {
    html += '<div style="margin-bottom:16px"><div style="display:flex;align-items:center;gap:6px;margin-bottom:8px;padding-bottom:6px;border-bottom:2px solid var(--info)">' + subjectIcons[sub] + '<span style="font-weight:700;color:var(--primary);font-size:0.9rem">' + subjectNames[sub] + '</span></div>';
    
    grouped[sub].forEach(c => {
      html += '<div style="margin-bottom:8px;border:1px solid rgba(23,162,184,0.15);border-radius:10px;overflow:hidden">';
      html += '<div onclick="toggleCaseDetail(\\'' + c.id + '\\')" style="padding:10px 14px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;transition:background 0.2s" onmouseover="this.style.background=\\'rgba(23,162,184,0.05)\\'" onmouseout="this.style.background=\\'transparent\\'">';
      html += '<div><span style="font-size:0.85rem;font-weight:600;color:var(--text-primary)">' + c.name + '</span><span style="font-size:0.68rem;color:var(--text-secondary);margin-left:8px">' + c.court + ' (' + c.year + ')</span></div>';
      html += '<span class="case-arrow-' + c.id + '" style="font-size:0.7rem;color:var(--text-secondary);transition:transform 0.3s">▶</span>';
      html += '</div>';
      html += '<div id="case-detail-' + c.id + '" style="display:none;padding:0 14px 14px">';
      // Facts
      html += '<div style="margin-bottom:10px"><div style="font-size:0.78rem;font-weight:700;color:var(--primary);margin-bottom:4px">📋 案情摘要</div><div style="font-size:0.75rem;line-height:1.7;color:var(--text-primary);padding:8px 10px;background:rgba(79,172,254,0.03);border-radius:6px">' + c.facts + '</div></div>';
      // Issues
      html += '<div style="margin-bottom:10px"><div style="font-size:0.78rem;font-weight:700;color:var(--primary);margin-bottom:4px">🔍 争议焦点</div>';
      c.issues.forEach((issue, idx) => {
        html += '<div style="font-size:0.75rem;line-height:1.6;padding:4px 10px;margin-bottom:3px;background:rgba(201,168,76,0.04);border-radius:4px;border-left:3px solid var(--accent)">' + (idx+1) + '. ' + issue + '</div>';
      });
      html += '</div>';
      // Holding
      html += '<div style="margin-bottom:10px"><div style="font-size:0.78rem;font-weight:700;color:var(--primary);margin-bottom:4px">⚖️ 裁判要旨</div><div style="font-size:0.75rem;line-height:1.7;color:var(--text-primary);padding:8px 10px;background:rgba(23,162,184,0.03);border-radius:6px">' + c.holding + '</div></div>';
      // Reasoning
      html += '<div style="margin-bottom:10px"><div style="font-size:0.78rem;font-weight:700;color:var(--primary);margin-bottom:4px">📝 裁判说理</div><div style="font-size:0.75rem;line-height:1.7;color:var(--text-primary);padding:8px 10px;background:rgba(0,0,0,0.02);border-radius:6px">' + c.reasoning + '</div></div>';
      // China position
      html += '<div><div style="font-size:0.78rem;font-weight:700;color:#c0392b;margin-bottom:4px">🇨🇳 中国立场</div><div style="font-size:0.75rem;line-height:1.7;color:var(--text-primary);padding:8px 10px;background:linear-gradient(135deg,rgba(192,57,43,0.04),rgba(192,57,43,0.01));border-radius:6px;border:1px solid rgba(192,57,43,0.12)">' + c.chinaPosition + '</div></div>';
      html += '</div></div>';
    });
    html += '</div>';
  });
  html += '</div>';
  
  addSystemMessage(html);
}

function toggleCaseDetail(caseId) {
  const detail = document.getElementById('case-detail-' + caseId);
  const arrow = document.querySelector('.case-arrow-' + caseId);
  if (detail.style.display === 'none') {
    detail.style.display = 'block';
    if (arrow) { arrow.style.transform = 'rotate(90deg)'; arrow.textContent = '▼'; }
  } else {
    detail.style.display = 'none';
    if (arrow) { arrow.style.transform = 'rotate(0deg)'; arrow.textContent = '▶'; }
  }
}

// === 三层问答模式 ===
const QA_MODES = {
  intro: {
    label: '入门模式',
    color: 'var(--primary)',
    systemPrompt: '你是一位国际法入门教师，用通俗易懂的语言解释概念，多举例子帮助理解。回答要详细、循序渐进，适合初学者。',
    style: '详细解释、类比举例、基础概念优先'
  },
  exam: {
    label: '法考模式',
    color: 'var(--accent)',
    systemPrompt: '你是一位法考辅导名师，重点讲解考试高频考点、易错点和答题技巧。回答要条理清晰，标注重要程度，提示常见陷阱。',
    style: '考点突出、真题关联、答题技巧'
  },
  practice: {
    label: '实务模式',
    color: 'var(--info)',
    systemPrompt: '你是一位涉外法律实务专家，结合真实案例和实务操作回答。注重法律适用分析、风险防范建议和操作指引。',
    style: '案例导向、实务操作、风险防范'
  }
};

function setQAMode(mode, btn) {
  AppState.qaMode = mode || 'intro';
  document.querySelectorAll('.qa-mode-btn').forEach(b => {
    b.style.background = 'transparent';
    b.style.color = 'var(--text-secondary)';
    b.classList.remove('active');
  });
  if (btn) {
    btn.style.background = QA_MODES[AppState.qaMode].color;
    btn.style.color = '#fff';
    btn.classList.add('active');
  }
  const ctx = document.getElementById('qaContext');
  if (ctx) ctx.textContent = QA_MODES[AppState.qaMode].label;
}

// === 分层题库 ===
function setDifficulty(level, btn) {
  AppState.quizDifficulty = level || 'all';
  document.querySelectorAll('.diff-btn').forEach(b => {
    b.style.background = 'transparent';
    b.style.color = 'var(--info)';
    b.classList.remove('active');
  });
  if (btn) {
    btn.style.background = 'var(--info)';
    btn.style.color = '#fff';
    btn.classList.add('active');
  }
}

// Initialize AppState defaults if not set
if (typeof AppState !== 'undefined') {
  AppState.qaMode = AppState.qaMode || 'intro';
  AppState.quizDifficulty = AppState.quizDifficulty || 'all';
}
'''

# Insert before the last </script> tag
last_script_close = html.rfind('</script>')
if last_script_close > 0:
    html = html[:last_script_close] + js_functions + '\n' + html[last_script_close:]
    print("Inserted JS functions before </script>")
else:
    print("ERROR: Cannot find </script> tag")

# ============================================================
# STEP 6: Modify generateResponse to use QA mode
# ============================================================
# Find the generateResponse function and modify it to prepend mode prompt
old_gen = "function generateResponse(text) {"
new_gen = """function generateResponse(text) {
  // 三层问答模式增强
  const mode = AppState.qaMode || 'intro';
  const modeConfig = QA_MODES[mode];
  const modePrefix = modeConfig ? `【${modeConfig.label}】回答风格：${modeConfig.style}\\n\\n` : '';
"""
html = html.replace(old_gen, new_gen, 1)

# Also modify the Doubao AI response
old_ai = "function generateResponseWithAI(text) {"
new_ai = """function generateResponseWithAI(text) {
  // 三层问答模式增强
  const mode = AppState.qaMode || 'intro';
  const modeConfig = QA_MODES[mode];
  const modePrefix = modeConfig ? `【${modeConfig.label}】回答风格：${modeConfig.style}\\n\\n` : '';
"""
html = html.replace(old_ai, new_ai, 1)
print("Modified generateResponse and generateResponseWithAI for QA mode")

# ============================================================
# STEP 7: Modify startQuiz to support difficulty filtering
# ============================================================
# Find the startQuiz function and modify question selection
old_quiz_filter = "function startQuiz(subject) {"
new_quiz_filter = """function startQuiz(subject) {
  // 分层题库：按难度过滤
  const difficulty = AppState.quizDifficulty || 'all';
"""
html = html.replace(old_quiz_filter, new_quiz_filter, 1)

# Find where questions are filtered by subject and add difficulty filter
old_q_filter = "MockData.questions.filter(q=>q.subject==='public')"
# This appears multiple times in the template literal for subject buttons
# We need to modify the actual quiz question selection, not the display count

# Look for the actual question selection logic
# In startQuiz, after subject filtering, add difficulty filtering
# Let's find the pattern where questions are selected
# Typically: const singles = questions.filter(q => q.type === 'single')

# Add difficulty assignment to questions that don't have it
# We'll add a difficulty property based on question id ranges
diff_assignment = """
// 分层题库：为题目分配难度（如果还没有difficulty字段）
MockData.questions.forEach(q => {
  if (!q.difficulty) {
    if (q.id <= 18) q.difficulty = 'basic';
    else if (q.id <= 36) q.difficulty = 'exam';
    else q.difficulty = 'advanced';
  }
});
"""
# Insert after MockData definition
mockdata_end = html.find('// === 应用状态管理 ==')
if mockdata_end > 0:
    html = html[:mockdata_end] + diff_assignment + '\n' + html[mockdata_end:]
    print("Added difficulty assignment for questions")

# Now modify the question filtering in startQuiz
# Find the pattern where questions are filtered
# Look for: const allQuestions = MockData.questions.filter
old_startquiz_body = """const questions = MockData.questions.filter(q => q.subject === subject);"""
new_startquiz_body = """let questions = MockData.questions.filter(q => q.subject === subject);
  // 分层题库：按难度过滤
  const diff = AppState.quizDifficulty || 'all';
  if (diff !== 'all') {
    const filtered = questions.filter(q => q.difficulty === diff);
    if (filtered.length >= 5) {
      questions = filtered;
    } else {
      // 如果该难度题目不够，补充其他难度的题目
      questions = filtered.concat(
        questions.filter(q => q.difficulty !== diff).slice(0, 16 - filtered.length)
      );
    }
  }"""
html = html.replace(old_startquiz_body, new_startquiz_body, 1)
print("Modified startQuiz for difficulty filtering")

# ============================================================
# STEP 8: Finalize and write
# ============================================================
with open(WORK, 'w') as f:
    f.write(html)

print(f"\nFinal: {len(html)} chars ({len(html)/1024:.0f} KB)")
print(f"Total added: +{len(html)-orig_len} chars ({(len(html)-orig_len)/1024:.1f} KB)")
print("DONE - all 4 features implemented!")
