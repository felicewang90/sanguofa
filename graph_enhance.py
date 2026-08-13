#!/usr/bin/env python3
"""三国法教学智能体 - 知识图谱可视化功能
在导航栏新增"知识图谱"页面，用 Canvas 力导向图展示三国法知识体系关系
"""

WORK = '/Coze/Drive/3G学堂（1）/所有对话/主对话/sanguofa_repo/index.html'

with open(WORK) as f:
    html = f.read()

orig_len = len(html)
print(f"Original: {orig_len} chars, {html.count(chr(10))} lines")

# ============================================================
# STEP 1: Add new page-view div for graph
# ============================================================
old_page_views = '''      <div class="page-view" id="page-profile"></div>'''
new_page_views = '''      <div class="page-view" id="page-graph"></div>


      <div class="page-view" id="page-profile"></div>'''
html = html.replace(old_page_views, new_page_views)
print("Added page-graph div")

# ============================================================
# STEP 2: Add nav-item for graph (after 涉外法治资鉴)
# ============================================================
old_nav = '''<a class="nav-item" data-page="ideology" onclick="showPage('ideology')">涉外法治资鉴</a>'''
new_nav = '''<a class="nav-item" data-page="ideology" onclick="showPage('ideology')">涉外法治资鉴</a>
      <a class="nav-item" data-page="graph" onclick="showPage('graph')">🕸️ 知识图谱</a>'''
html = html.replace(old_nav, new_nav)
print("Added nav-item for graph")

# ============================================================
# STEP 3: Add renderGraph trigger in showPage
# ============================================================
old_showpage = """  // Render profile page when switching to it
  if (page === 'profile') {
    renderProfile();
  }"""
new_showpage = """  // Render graph page when switching to it
  if (page === 'graph') {
    renderKnowledgeGraph();
  }

  // Render profile page when switching to it
  if (page === 'profile') {
    renderProfile();
  }"""
html = html.replace(old_showpage, new_showpage)
print("Added renderGraph trigger in showPage")

# ============================================================
# STEP 4: Add the full knowledge graph implementation
# ============================================================
graph_js = r'''
// === 知识图谱可视化模块 ===
function renderKnowledgeGraph() {
  const container = document.getElementById('page-graph');
  container.innerHTML = `
    <div class="graph-container" style="position:relative;width:100%;height:calc(100vh - 60px);background:linear-gradient(180deg,#0a0e27 0%,#1a1f3a 40%,#0d1225 100%);overflow:hidden">
      <canvas id="graphCanvas" style="width:100%;height:100%;cursor:grab"></canvas>
      
      <!-- Top overlay title -->
      <div style="position:absolute;top:16px;left:50%;transform:translateX(-50%);text-align:center;pointer-events:none;z-index:10">
        <h2 style="margin:0;font-size:1.3rem;color:#c9a84c;text-shadow:0 0 20px rgba(201,168,76,0.3);letter-spacing:3px">三 国 法 知 识 图 谱</h2>
        <p style="margin:4px 0 0;font-size:0.72rem;color:rgba(255,255,255,0.5)">拖拽节点 · 滚轮缩放 · 点击查看详情</p>
      </div>
      
      <!-- Legend -->
      <div style="position:absolute;bottom:20px;left:20px;background:rgba(10,14,39,0.85);border:1px solid rgba(201,168,76,0.2);border-radius:12px;padding:12px 16px;z-index:10;backdrop-filter:blur(8px)">
        <div style="font-size:0.72rem;color:rgba(255,255,255,0.6);margin-bottom:8px;font-weight:600">图 例</div>
        <div style="display:flex;flex-direction:column;gap:5px">
          <div style="display:flex;align-items:center;gap:8px"><span style="width:10px;height:10px;border-radius:50%;background:#4facfe;display:inline-block;box-shadow:0 0 6px rgba(79,172,254,0.5)"></span><span style="font-size:0.68rem;color:rgba(255,255,255,0.7)">国际公法</span></div>
          <div style="display:flex;align-items:center;gap:8px"><span style="width:10px;height:10px;border-radius:50%;background:#43e97b;display:inline-block;box-shadow:0 0 6px rgba(67,233,123,0.5)"></span><span style="font-size:0.68rem;color:rgba(255,255,255,0.7)">国际私法</span></div>
          <div style="display:flex;align-items:center;gap:8px"><span style="width:10px;height:10px;border-radius:50%;background:#fa709a;display:inline-block;box-shadow:0 0 6px rgba(250,112,154,0.5)"></span><span style="font-size:0.68rem;color:rgba(255,255,255,0.7)">国际经济法</span></div>
          <div style="display:flex;align-items:center;gap:8px"><span style="width:10px;height:10px;border-radius:50%;background:#c9a84c;display:inline-block;box-shadow:0 0 6px rgba(201,168,76,0.5)"></span><span style="font-size:0.68rem;color:rgba(255,255,255,0.7)">核心枢纽</span></div>
        </div>
        <div style="margin-top:8px;padding-top:8px;border-top:1px solid rgba(255,255,255,0.08)">
          <div style="display:flex;flex-direction:column;gap:4px">
            <div style="display:flex;align-items:center;gap:8px"><span style="width:20px;height:2px;background:rgba(255,255,255,0.3);display:inline-block"></span><span style="font-size:0.65rem;color:rgba(255,255,255,0.5)">关联</span></div>
            <div style="display:flex;align-items:center;gap:8px"><span style="width:20px;height:2px;background:rgba(201,168,76,0.5);display:inline-block;border-top:1px dashed rgba(201,168,76,0.5)"></span><span style="font-size:0.65rem;color:rgba(255,255,255,0.5)">跨学科</span></div>
          </div>
        </div>
      </div>
      
      <!-- Node detail panel -->
      <div id="graphDetail" style="display:none;position:absolute;top:60px;right:20px;width:300px;max-height:calc(100vh - 140px);overflow-y:auto;background:rgba(10,14,39,0.92);border:1px solid rgba(201,168,76,0.25);border-radius:14px;padding:20px;z-index:10;backdrop-filter:blur(12px);box-shadow:0 8px 32px rgba(0,0,0,0.4)">
      </div>
      
      <!-- Controls -->
      <div style="position:absolute;bottom:20px;right:20px;display:flex;flex-direction:column;gap:8px;z-index:10">
        <button onclick="graphZoom(1.2)" style="width:36px;height:36px;border-radius:8px;border:1px solid rgba(201,168,76,0.3);background:rgba(10,14,39,0.8);color:#c9a84c;font-size:1.1rem;cursor:pointer;backdrop-filter:blur(4px)">+</button>
        <button onclick="graphZoom(0.8)" style="width:36px;height:36px;border-radius:8px;border:1px solid rgba(201,168,76,0.3);background:rgba(10,14,39,0.8);color:#c9a84c;font-size:1.1rem;cursor:pointer;backdrop-filter:blur(4px)">−</button>
        <button onclick="graphReset()" style="width:36px;height:36px;border-radius:8px;border:1px solid rgba(201,168,76,0.3);background:rgba(10,14,39,0.8);color:#c9a84c;font-size:0.75rem;cursor:pointer;backdrop-filter:blur(4px)">⟲</button>
      </div>
    </div>
  `;
  
  initGraphCanvas();
}

// === Graph Data ===
const GRAPH_DATA = {
  nodes: [
    // === 核心枢纽节点 ===
    {id:'hub-sovereignty', label:'国家主权', group:'hub', x:0, y:0, r:28, desc:'国际法基本原则，贯穿三国法全部领域的核心概念', keywords:['主权平等','不干涉内政','领土完整']},
    {id:'hub-treaty', label:'条约机制', group:'hub', x:0, y:0, r:24, desc:'国际条约是三国法共同的法律渊源和规则载体', keywords:['VCLT','条约必须遵守','保留制度']},
    {id:'hub-dispute', label:'争端解决', group:'hub', x:0, y:0, r:22, desc:'ICJ/WTO-DSB/ICSID/仲裁等多元争端解决机制', keywords:['ICJ','仲裁','调解','DSU']},
    
    // === 国际公法 ===
    {id:'pub-unclos', label:'UNCLOS\n海洋法公约', group:'public', x:0, y:0, r:22, desc:'《联合国海洋法公约》，海洋宪章。规定领海、专属经济区、大陆架、公海、国际海底区域等制度', keywords:['领海','EEZ','大陆架','公海','区域制度']},
    {id:'pub-territory', label:'领土制度', group:'public', x:0, y:0, r:16, desc:'国家领土的取得方式（先占、时效、添附、割让、征服）、边界制度、南极北极制度', keywords:['先占','时效','添附','边界']},
    {id:'pub-diplomatic', label:'外交关系法', group:'public', x:0, y:0, r:15, desc:'《维也纳外交关系公约》，使馆制度、外交特权与豁免', keywords:['使馆','外交特权','豁免','维也纳外交公约']},
    {id:'pub-immunity', label:'国家豁免', group:'public', x:0, y:0, r:17, desc:'国家及其财产豁免，2004年联合国公约，中国《外国国家豁免法》(2024)采限制豁免主义', keywords:['限制豁免','绝对豁免','执行豁免','2024立法']},
    {id:'pub-useofforce', label:'武力使用', group:'public', x:0, y:0, r:16, desc:'《联合国宪章》第2(4)条禁止武力威胁，第51条自卫权，安理会授权', keywords:['宪章第2条','自卫权','安理会','R2P']},
    {id:'pub-humanrights', label:'国际人权法', group:'public', x:0, y:0, r:15, desc:'国际人权宪章（UDHR+ICCPR+ICESCR），人权条约体系', keywords:['UDHR','ICCPR','ICESCR','人权理事会']},
    {id:'pub-statehood', label:'国家承认', group:'public', x:0, y:0, r:14, desc:'国家构成要素、政府承认、国际组织法律人格', keywords:['蒙特维的亚公约','构成说','宣告说']},
    {id:'pub-vclt', label:'VCLT\n条约法公约', group:'public', x:0, y:0, r:19, desc:'《维也纳条约法公约》(1969)，条约的缔结、生效、保留、解释、终止', keywords:['保留','解释','情势变更','强行法']},
    
    // === 国际私法 ===
    {id:'pri-applicable', label:'法律适用法', group:'private', x:0, y:0, r:22, desc:'《涉外民事关系法律适用法》(2010)，中国国际私法核心立法。规定合同、侵权、物权、婚姻家庭等法律选择规则', keywords:['合同','侵权','物权','婚姻','最密切联系']},
    {id:'pri-jurisdiction', label:'涉外管辖权', group:'private', x:0, y:0, r:17, desc:'涉外民事诉讼管辖权规则：被告住所地、合同履行地、侵权行为地、协议管辖', keywords:['一般管辖','特别管辖','协议管辖','不方便法院']},
    {id:'pri-recognition', label:'判决承认执行', group:'private', x:0, y:0, r:16, desc:'外国法院判决的承认与执行，《海牙判决公约》(2019)', keywords:['海牙判决公约','互惠','公共秩序保留']},
    {id:'pri-arbitration', label:'国际商事仲裁', group:'private', x:0, y:0, r:18, desc:'纽约公约框架下的国际商事仲裁制度，仲裁协议效力、仲裁程序、裁决承认与执行', keywords:['纽约公约','仲裁协议','裁决执行','CIETAC']},
    {id:'pri-conflict', label:'冲突法理论', group:'private', x:0, y:0, r:15, desc:'萨维尼法律关系本座说、美国冲突法革命、最密切联系原则、政府利益分析', keywords:['本座说','冲突革命','最密切联系','意思自治']},
    {id:'pri-characterization', label:'识别与反致', group:'private', x:0, y:0, r:13, desc:'国际私法基本问题：识别（定性）、反致（转致）、先决问题、公共秩序保留、法律规避', keywords:['定性','反致','公共秩序','规避']},
    {id:'pri-immunity2', label:'领事关系法', group:'private', x:0, y:0, r:13, desc:'《维也纳领事关系公约》，领事特权与豁免，与外交豁免的区别', keywords:['领事','保护','维也纳领事公约']},
    
    // === 国际经济法 ===
    {id:'eco-wto', label:'WTO体制', group:'economic', x:0, y:0, r:22, desc:'世界贸易组织，多边贸易体制核心。GATT/GATS/TRIPS三大支柱', keywords:['GATT','GATS','TRIPS','最惠国','国民待遇']},
    {id:'eco-cisg', label:'CISG\n国际货物买卖', group:'economic', x:0, y:0, r:19, desc:'《联合国国际货物销售合同公约》，统一国际货物买卖规则。根本违约、风险转移、预期违反', keywords:['根本违约','风险转移','要约承诺','CISG']},
    {id:'eco-investment', label:'国际投资法', group:'economic', x:0, y:0, r:17, desc:'BITs、ICSID公约、征收与补偿、投资者-国家争端解决(ISDS)', keywords:['BIT','ICSID','征收','ISDS','公平待遇']},
    {id:'eco-trade', label:'国际贸易支付', group:'economic', x:0, y:0, r:15, desc:'信用证(UCP600)、托收、汇付，国际贸易支付方式与风险分配', keywords:['UCP600','信用证','独立抽象','严格相符']},
    {id:'eco-ip', label:'知识产权国际保护', group:'economic', x:0, y:0, r:16, desc:'巴黎公约、伯尔尼公约、TRIPS协定，知识产权国际保护最低标准', keywords:['TRIPS','巴黎公约','伯尔尼','国民待遇','最低保护']},
    {id:'eco-dsb', label:'WTO争端解决', group:'economic', x:0, y:0, r:17, desc:'DSU机制：磋商→专家组→上诉→执行。反向一致原则，报复机制', keywords:['DSU','专家组','上诉机构','反向一致','报复']},
    {id:'eco-monetary', label:'国际货币金融法', group:'economic', x:0, y:0, r:14, desc:'IMF协定、SDR、国际货币基金组织职能与贷款条件性', keywords:['IMF','SDR','贷款条件','牙买加体系']},
    {id:'eco-tax', label:'国际税法', group:'economic', x:0, y:0, r:13, desc:'避免双重征税协定、转让定价、BEPS行动计划、税收情报交换', keywords:['OECD','BEPS','转让定价','税收协定']},
  ],
  
  edges: [
    // 核心枢纽连接
    {from:'hub-sovereignty', to:'pub-immunity', label:'主权派生', cross:false},
    {from:'hub-sovereignty', to:'pub-territory', label:'领土主权', cross:false},
    {from:'hub-sovereignty', to:'pub-useofforce', label:'主权保护', cross:false},
    {from:'hub-sovereignty', to:'pri-jurisdiction', label:'管辖主权', cross:true},
    {from:'hub-treaty', to:'pub-vclt', label:'条约法', cross:false},
    {from:'hub-treaty', to:'eco-cisg', label:'条约统一', cross:true},
    {from:'hub-dispute', to:'eco-dsb', label:'WTO争端', cross:false},
    {from:'hub-dispute', to:'pri-arbitration', label:'仲裁机制', cross:true},
    {from:'hub-dispute', to:'pub-immunity', label:'管辖豁免', cross:false},
    
    // 公法内部连接
    {from:'pub-unclos', to:'pub-territory', label:'海洋领土', cross:false},
    {from:'pub-unclos', to:'pub-diplomatic', label:'海上外交', cross:false},
    {from:'pub-vclt', to:'pub-useofforce', label:'条约终止', cross:false},
    {from:'pub-vclt', to:'pub-statehood', label:'缔约能力', cross:false},
    {from:'pub-diplomatic', to:'pub-immunity', label:'豁免关联', cross:false},
    {from:'pub-humanrights', to:'pub-useofforce', label:'R2P', cross:false},
    {from:'pub-statehood', to:'pub-diplomatic', label:'国家→外交', cross:false},
    {from:'pub-unclos', to:'hub-sovereignty', label:'海洋主权', cross:false},
    
    // 私法内部连接
    {from:'pri-applicable', to:'pri-conflict', label:'理论基础', cross:false},
    {from:'pri-applicable', to:'pri-characterization', label:'适用前提', cross:false},
    {from:'pri-jurisdiction', to:'pri-recognition', label:'管辖→执行', cross:false},
    {from:'pri-arbitration', to:'pri-recognition', label:'裁决执行', cross:false},
    {from:'pri-conflict', to:'pri-characterization', label:'识别先决', cross:false},
    {from:'pri-immunity2', to:'pub-diplomatic', label:'领外交关联', cross:true},
    
    // 经济法内部连接
    {from:'eco-wto', to:'eco-dsb', label:'WTO机制', cross:false},
    {from:'eco-wto', to:'eco-ip', label:'TRIPS', cross:false},
    {from:'eco-wto', to:'eco-trade', label:'贸易规则', cross:false},
    {from:'eco-cisg', to:'eco-trade', label:'买卖支付', cross:false},
    {from:'eco-investment', to:'eco-monetary', label:'投资金融', cross:false},
    {from:'eco-monetary', to:'eco-tax', label:'金融税收', cross:false},
    {from:'eco-ip', to:'eco-trade', label:'知识贸易', cross:false},
    
    // 跨学科连接（重要！）
    {from:'pub-immunity', to:'pri-arbitration', label:'执行豁免vs仲裁', cross:true},
    {from:'pub-unclos', to:'eco-trade', label:'海运贸易', cross:true},
    {from:'pri-applicable', to:'eco-cisg', label:'合同法律适用', cross:true},
    {from:'eco-investment', to:'pub-immunity', label:'投资vs主权', cross:true},
    {from:'pri-arbitration', to:'eco-investment', label:'ISDS仲裁', cross:true},
    {from:'pub-humanrights', to:'eco-investment', label:'人权vs投资', cross:true},
    {from:'eco-dsb', to:'hub-sovereignty', label:'主权让渡', cross:true},
  ]
};

// === Graph Canvas Implementation ===
let graphState = {
  canvas: null,
  ctx: null,
  nodes: [],
  edges: [],
  scale: 1,
  offsetX: 0,
  offsetY: 0,
  dragging: null,
  hoveredNode: null,
  selectedNode: null,
  isDraggingCanvas: false,
  lastMouse: {x:0, y:0},
  animFrame: null,
  particles: [],
  initialized: false
};

function initGraphCanvas() {
  const canvas = document.getElementById('graphCanvas');
  if (!canvas) return;
  
  const container = canvas.parentElement;
  canvas.width = container.clientWidth * 2;
  canvas.height = container.clientHeight * 2;
  canvas.style.width = container.clientWidth + 'px';
  canvas.style.height = container.clientHeight + 'px';
  
  const ctx = canvas.getContext('2d');
  ctx.scale(2, 2); // Retina
  
  graphState.canvas = canvas;
  graphState.ctx = ctx;
  graphState.scale = 1;
  graphState.offsetX = container.clientWidth / 2;
  graphState.offsetY = container.clientHeight / 2;
  
  // Initialize nodes with positions (arranged in clusters)
  const nodes = GRAPH_DATA.nodes.map((n, i) => {
    let angle, radius;
    if (n.group === 'hub') {
      angle = (i / 3) * Math.PI * 2;
      radius = 30 + Math.random() * 20;
    } else if (n.group === 'public') {
      angle = (i / 10) * Math.PI * 2 + 0.3;
      radius = 120 + Math.random() * 60;
    } else if (n.group === 'private') {
      angle = (i / 7) * Math.PI * 2 + 2.1;
      radius = 120 + Math.random() * 60;
    } else {
      angle = (i / 8) * Math.PI * 2 + 4.2;
      radius = 120 + Math.random() * 60;
    }
    return {
      ...n,
      x: Math.cos(angle) * radius + (Math.random() - 0.5) * 30,
      y: Math.sin(angle) * radius + (Math.random() - 0.5) * 30,
      vx: 0,
      vy: 0,
      targetX: 0,
      targetY: 0
    };
  });
  
  // Build edges with references
  const edges = GRAPH_DATA.edges.map(e => ({
    ...e,
    source: nodes.find(n => n.id === e.from),
    target: nodes.find(n => n.id === e.to)
  })).filter(e => e.source && e.target);
  
  graphState.nodes = nodes;
  graphState.edges = edges;
  
  // Initialize background particles
  graphState.particles = [];
  for (let i = 0; i < 50; i++) {
    graphState.particles.push({
      x: Math.random() * container.clientWidth,
      y: Math.random() * container.clientHeight,
      r: Math.random() * 1.5 + 0.3,
      speed: Math.random() * 0.2 + 0.05,
      alpha: Math.random() * 0.3 + 0.1
    });
  }
  
  // Event listeners
  canvas.addEventListener('mousedown', graphMouseDown);
  canvas.addEventListener('mousemove', graphMouseMove);
  canvas.addEventListener('mouseup', graphMouseUp);
  canvas.addEventListener('wheel', graphWheel);
  canvas.addEventListener('click', graphClick);
  
  // Touch support
  canvas.addEventListener('touchstart', graphTouchStart, {passive: false});
  canvas.addEventListener('touchmove', graphTouchMove, {passive: false});
  canvas.addEventListener('touchend', graphTouchEnd);
  
  graphState.initialized = true;
  graphAnimate();
}

function graphAnimate() {
  if (!graphState.initialized) return;
  
  const ctx = graphState.ctx;
  const canvas = graphState.canvas;
  if (!ctx || !canvas) return;
  
  const w = canvas.width / 2;
  const h = canvas.height / 2;
  
  // Clear
  ctx.clearRect(0, 0, w, h);
  
  // Draw background particles
  graphState.particles.forEach(p => {
    p.y -= p.speed;
    if (p.y < 0) { p.y = h; p.x = Math.random() * w; }
    ctx.beginPath();
    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(201,168,76,${p.alpha})`;
    ctx.fill();
  });
  
  // Apply force simulation (simplified)
  applyForces();
  
  // Save state for transform
  ctx.save();
  ctx.translate(graphState.offsetX, graphState.offsetY);
  ctx.scale(graphState.scale, graphState.scale);
  
  // Draw edges
  graphState.edges.forEach(edge => {
    const s = edge.source;
    const t = edge.target;
    const isHighlighted = graphState.hoveredNode && 
      (s.id === graphState.hoveredNode.id || t.id === graphState.hoveredNode.id);
    const isSelected = graphState.selectedNode &&
      (s.id === graphState.selectedNode.id || t.id === graphState.selectedNode.id);
    
    ctx.beginPath();
    const dx = t.x - s.x;
    const dy = t.y - s.y;
    const cx = (s.x + t.x) / 2 - dy * 0.1;
    const cy = (s.y + t.y) / 2 + dx * 0.1;
    ctx.moveTo(s.x, s.y);
    ctx.quadraticCurveTo(cx, cy, t.x, t.y);
    
    if (edge.cross) {
      ctx.strokeStyle = isHighlighted || isSelected 
        ? 'rgba(201,168,76,0.6)' 
        : 'rgba(201,168,76,0.15)';
      ctx.setLineDash([4, 4]);
    } else {
      ctx.strokeStyle = isHighlighted || isSelected 
        ? 'rgba(255,255,255,0.5)' 
        : 'rgba(255,255,255,0.1)';
      ctx.setLineDash([]);
    }
    ctx.lineWidth = isHighlighted || isSelected ? 1.5 : 0.8;
    ctx.stroke();
    ctx.setLineDash([]);
    
    // Edge label (only when highlighted)
    if ((isHighlighted || isSelected) && edge.label) {
      ctx.font = '9px sans-serif';
      ctx.fillStyle = 'rgba(255,255,255,0.6)';
      ctx.textAlign = 'center';
      ctx.fillText(edge.label, cx, cy - 4);
    }
  });
  
  // Draw nodes
  graphState.nodes.forEach(node => {
    const isHovered = graphState.hoveredNode && graphState.hoveredNode.id === node.id;
    const isSelected = graphState.selectedNode && graphState.selectedNode.id === node.id;
    const isConnected = graphState.hoveredNode && graphState.edges.some(e => 
      (e.source.id === graphState.hoveredNode.id && e.target.id === node.id) ||
      (e.target.id === graphState.hoveredNode.id && e.source.id === node.id)
    );
    
    const colors = {
      hub: {fill: '#c9a84c', glow: 'rgba(201,168,76,0.4)'},
      public: {fill: '#4facfe', glow: 'rgba(79,172,254,0.3)'},
      private: {fill: '#43e97b', glow: 'rgba(67,233,123,0.3)'},
      economic: {fill: '#fa709a', glow: 'rgba(250,112,154,0.3)'}
    };
    const color = colors[node.group] || colors.public;
    const r = node.r * (isHovered ? 1.2 : isSelected ? 1.15 : 1);
    const alpha = (isHovered || isSelected || isConnected || !graphState.hoveredNode) ? 1 : 0.3;
    
    // Glow
    if (isHovered || isSelected) {
      ctx.beginPath();
      ctx.arc(node.x, node.y, r + 8, 0, Math.PI * 2);
      const grad = ctx.createRadialGradient(node.x, node.y, r, node.x, node.y, r + 8);
      grad.addColorStop(0, color.glow);
      grad.addColorStop(1, 'transparent');
      ctx.fillStyle = grad;
      ctx.fill();
    }
    
    // Node circle
    ctx.beginPath();
    ctx.arc(node.x, node.y, r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(${hexToRgb(color.fill)},${alpha * 0.15})`;
    ctx.fill();
    ctx.strokeStyle = `rgba(${hexToRgb(color.fill)},${alpha})`;
    ctx.lineWidth = isHovered ? 2.5 : isSelected ? 2 : 1.2;
    ctx.stroke();
    
    // Label
    ctx.font = `${isHovered || isSelected ? 'bold ' : ''}${r > 20 ? 10 : r > 15 ? 9 : 8}px sans-serif`;
    ctx.fillStyle = `rgba(255,255,255,${alpha})`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    const lines = node.label.split('\n');
    if (lines.length > 1) {
      lines.forEach((line, i) => {
        ctx.fillText(line, node.x, node.y + (i - (lines.length-1)/2) * 11);
      });
    } else {
      ctx.fillText(node.label, node.x, node.y);
    }
  });
  
  ctx.restore();
  
  graphState.animFrame = requestAnimationFrame(graphAnimate);
}

function applyForces() {
  const nodes = graphState.nodes;
  const edges = graphState.edges;
  
  // Repulsion between nodes
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const dx = nodes[j].x - nodes[i].x;
      const dy = nodes[j].y - nodes[i].y;
      const dist = Math.sqrt(dx*dx + dy*dy) || 1;
      const force = 800 / (dist * dist);
      const fx = dx / dist * force;
      const fy = dy / dist * force;
      nodes[i].vx -= fx;
      nodes[i].vy -= fy;
      nodes[j].vx += fx;
      nodes[j].vy += fy;
    }
  }
  
  // Attraction along edges
  edges.forEach(e => {
    const dx = e.target.x - e.source.x;
    const dy = e.target.y - e.source.y;
    const dist = Math.sqrt(dx*dx + dy*dy) || 1;
    const idealDist = e.cross ? 180 : 100;
    const force = (dist - idealDist) * 0.005;
    const fx = dx / dist * force;
    const fy = dy / dist * force;
    e.source.vx += fx;
    e.source.vy += fy;
    e.target.vx -= fx;
    e.target.vy -= fy;
  });
  
  // Center gravity
  nodes.forEach(n => {
    if (n === graphState.dragging) return;
    n.vx -= n.x * 0.001;
    n.vy -= n.y * 0.001;
    // Apply velocity with damping
    n.x += n.vx * 0.3;
    n.y += n.vy * 0.3;
    n.vx *= 0.85;
    n.vy *= 0.85;
  });
}

// === Mouse/Touch handlers ===
function screenToGraph(sx, sy) {
  return {
    x: (sx - graphState.offsetX) / graphState.scale,
    y: (sy - graphState.offsetY) / graphState.scale
  };
}

function findNodeAt(gx, gy) {
  for (let i = graphState.nodes.length - 1; i >= 0; i--) {
    const n = graphState.nodes[i];
    const dx = gx - n.x;
    const dy = gy - n.y;
    if (dx*dx + dy*dy < (n.r + 5) * (n.r + 5)) return n;
  }
  return null;
}

function graphMouseDown(e) {
  const rect = graphState.canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const g = screenToGraph(sx, sy);
  const node = findNodeAt(g.x, g.y);
  
  if (node) {
    graphState.dragging = node;
    graphState.canvas.style.cursor = 'grabbing';
  } else {
    graphState.isDraggingCanvas = true;
    graphState.lastMouse = {x: e.clientX, y: e.clientY};
    graphState.canvas.style.cursor = 'grabbing';
  }
}

function graphMouseMove(e) {
  const rect = graphState.canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const g = screenToGraph(sx, sy);
  
  if (graphState.dragging) {
    graphState.dragging.x = g.x;
    graphState.dragging.y = g.y;
    graphState.dragging.vx = 0;
    graphState.dragging.vy = 0;
  } else if (graphState.isDraggingCanvas) {
    graphState.offsetX += e.clientX - graphState.lastMouse.x;
    graphState.offsetY += e.clientY - graphState.lastMouse.y;
    graphState.lastMouse = {x: e.clientX, y: e.clientY};
  } else {
    const node = findNodeAt(g.x, g.y);
    graphState.hoveredNode = node;
    graphState.canvas.style.cursor = node ? 'pointer' : 'grab';
  }
}

function graphMouseUp(e) {
  graphState.dragging = null;
  graphState.isDraggingCanvas = false;
  graphState.canvas.style.cursor = 'grab';
}

function graphClick(e) {
  const rect = graphState.canvas.getBoundingClientRect();
  const sx = e.clientX - rect.left;
  const sy = e.clientY - rect.top;
  const g = screenToGraph(sx, sy);
  const node = findNodeAt(g.x, g.y);
  
  if (node) {
    graphState.selectedNode = node;
    showGraphDetail(node);
  } else {
    graphState.selectedNode = null;
    document.getElementById('graphDetail').style.display = 'none';
  }
}

function graphWheel(e) {
  e.preventDefault();
  const factor = e.deltaY > 0 ? 0.9 : 1.1;
  graphState.scale *= factor;
  graphState.scale = Math.max(0.3, Math.min(3, graphState.scale));
}

// Touch support
let touchState = {startDist: 0, startScale: 1};

function graphTouchStart(e) {
  e.preventDefault();
  if (e.touches.length === 1) {
    const t = e.touches[0];
    const rect = graphState.canvas.getBoundingClientRect();
    const sx = t.clientX - rect.left;
    const sy = t.clientY - rect.top;
    const g = screenToGraph(sx, sy);
    const node = findNodeAt(g.x, g.y);
    if (node) {
      graphState.dragging = node;
    } else {
      graphState.isDraggingCanvas = true;
      graphState.lastMouse = {x: t.clientX, y: t.clientY};
    }
  } else if (e.touches.length === 2) {
    const dx = e.touches[0].clientX - e.touches[1].clientX;
    const dy = e.touches[0].clientY - e.touches[1].clientY;
    touchState.startDist = Math.sqrt(dx*dx + dy*dy);
    touchState.startScale = graphState.scale;
  }
}

function graphTouchMove(e) {
  e.preventDefault();
  if (e.touches.length === 1) {
    const t = e.touches[0];
    const rect = graphState.canvas.getBoundingClientRect();
    const sx = t.clientX - rect.left;
    const sy = t.clientY - rect.top;
    const g = screenToGraph(sx, sy);
    
    if (graphState.dragging) {
      graphState.dragging.x = g.x;
      graphState.dragging.y = g.y;
      graphState.dragging.vx = 0;
      graphState.dragging.vy = 0;
    } else if (graphState.isDraggingCanvas) {
      graphState.offsetX += t.clientX - graphState.lastMouse.x;
      graphState.offsetY += t.clientY - graphState.lastMouse.y;
      graphState.lastMouse = {x: t.clientX, y: t.clientY};
    }
  } else if (e.touches.length === 2) {
    const dx = e.touches[0].clientX - e.touches[1].clientX;
    const dy = e.touches[0].clientY - e.touches[1].clientY;
    const dist = Math.sqrt(dx*dx + dy*dy);
    graphState.scale = touchState.startScale * (dist / touchState.startDist);
    graphState.scale = Math.max(0.3, Math.min(3, graphState.scale));
  }
}

function graphTouchEnd(e) {
  graphState.dragging = null;
  graphState.isDraggingCanvas = false;
}

// === Graph Controls ===
function graphZoom(factor) {
  graphState.scale *= factor;
  graphState.scale = Math.max(0.3, Math.min(3, graphState.scale));
}

function graphReset() {
  graphState.scale = 1;
  const canvas = graphState.canvas;
  if (canvas) {
    graphState.offsetX = canvas.width / 4;
    graphState.offsetY = canvas.height / 4;
  }
  graphState.selectedNode = null;
  document.getElementById('graphDetail').style.display = 'none';
}

// === Graph Detail Panel ===
function showGraphDetail(node) {
  const panel = document.getElementById('graphDetail');
  if (!panel) return;
  
  const colors = {hub:'#c9a84c', public:'#4facfe', private:'#43e97b', economic:'#fa709a'};
  const groupNames = {hub:'核心枢纽', public:'国际公法', private:'国际私法', economic:'国际经济法'};
  const color = colors[node.group] || '#4facfe';
  
  // Find connected nodes
  const connected = graphState.edges
    .filter(e => e.source.id === node.id || e.target.id === node.id)
    .map(e => {
      const other = e.source.id === node.id ? e.target : e.source;
      return {node: other, label: e.label, cross: e.cross};
    });
  
  let html = `
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px">
      <div style="width:36px;height:36px;border-radius:50%;background:${color}20;border:2px solid ${color};display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0">
        ${node.group === 'hub' ? '🔗' : node.group === 'public' ? '🌐' : node.group === 'private' ? '⚖️' : '💼'}
      </div>
      <div>
        <div style="font-size:0.95rem;font-weight:700;color:${color}">${node.label.replace('\n',' ')}</div>
        <div style="font-size:0.68rem;color:rgba(255,255,255,0.5)">${groupNames[node.group]}</div>
      </div>
    </div>
    <div style="font-size:0.78rem;color:rgba(255,255,255,0.8);line-height:1.7;margin-bottom:14px;padding:10px 12px;background:rgba(255,255,255,0.03);border-radius:8px;border-left:3px solid ${color}">
      ${node.desc}
    </div>
  `;
  
  // Keywords
  if (node.keywords && node.keywords.length) {
    html += '<div style="margin-bottom:14px"><div style="font-size:0.72rem;color:rgba(255,255,255,0.4);margin-bottom:6px">🏷️ 关键词</div><div style="display:flex;flex-wrap:wrap;gap:4px">';
    node.keywords.forEach(kw => {
      html += `<span style="font-size:0.65rem;padding:2px 8px;background:${color}15;color:${color};border:1px solid ${color}30;border-radius:10px">${kw}</span>`;
    });
    html += '</div></div>';
  }
  
  // Connected nodes
  if (connected.length) {
    html += '<div><div style="font-size:0.72rem;color:rgba(255,255,255,0.4);margin-bottom:6px">🔗 关联知识点 (' + connected.length + ')</div>';
    connected.forEach(c => {
      const cColor = colors[c.node.group] || '#4facfe';
      html += `<div onclick="graphSelectNode('${c.node.id}')" style="padding:6px 10px;margin-bottom:4px;background:rgba(255,255,255,0.03);border-radius:6px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;transition:background 0.2s;border-left:2px solid ${c.cross ? '#c9a84c' : cColor}" onmouseover="this.style.background='rgba(255,255,255,0.06)'" onmouseout="this.style.background='rgba(255,255,255,0.03)'">
        <span style="font-size:0.75rem;color:${cColor}">${c.node.label.replace('\n',' ')}</span>
        <span style="font-size:0.62rem;color:rgba(255,255,255,0.4)">${c.label || ''}${c.cross ? ' 🔄跨学科' : ''}</span>
      </div>`;
    });
    html += '</div>';
  }
  
  panel.innerHTML = html;
  panel.style.display = 'block';
}

function graphSelectNode(nodeId) {
  const node = graphState.nodes.find(n => n.id === nodeId);
  if (node) {
    graphState.selectedNode = node;
    // Center on node
    const canvas = graphState.canvas;
    graphState.offsetX = canvas.width / 4 - node.x * graphState.scale;
    graphState.offsetY = canvas.height / 4 - node.y * graphState.scale;
    showGraphDetail(node);
  }
}

// === Utility ===
function hexToRgb(hex) {
  const r = parseInt(hex.slice(1,3), 16);
  const g = parseInt(hex.slice(3,5), 16);
  const b = parseInt(hex.slice(5,7), 16);
  return `${r},${g},${b}`;
}
'''

# Insert before the last </script>
last_script_close = html.rfind('</script>')
html = html[:last_script_close] + graph_js + '\n' + html[last_script_close:]
print(f"Added knowledge graph JS ({len(graph_js)} chars)")

# ============================================================
# STEP 5: Write result
# ============================================================
with open(WORK, 'w') as f:
    f.write(html)

print(f"\nFinal: {len(html)} chars ({len(html)/1024:.0f} KB)")
print(f"Total added: +{len(html)-orig_len} chars ({(len(html)-orig_len)/1024:.1f} KB)")
print("DONE!")
