(()=>{'use strict';
if(document.getElementById('cs115-ai')) return;

const STORE=localStorage;
let katexPromise=null;
function ensureKatex(){
  if(typeof window.renderMathInElement==='function')return Promise.resolve();
  if(katexPromise)return katexPromise;
  const addCss=()=>{if(document.querySelector('link[data-cs115-katex]'))return;const l=document.createElement('link');l.rel='stylesheet';l.href='https://cdn.jsdelivr.net/npm/katex@0.18.1/dist/katex.min.css';l.integrity='sha384-1vdNCNel6Tx/NQa8IR1mGOGKsbGreCkOPfbtPPnUURJ5Tu2PRVfQ/7KLZC+Pi1p1';l.crossOrigin='anonymous';l.dataset.cs115Katex='1';document.head.append(l)};
  const script=(src,integrity)=>new Promise((resolve,reject)=>{const found=[...document.scripts].find(x=>x.src===src);if(found){if(found.dataset.loaded==='1')return resolve();found.addEventListener('load',resolve,{once:true});found.addEventListener('error',reject,{once:true});return}const s=document.createElement('script');s.src=src;s.defer=true;s.integrity=integrity;s.crossOrigin='anonymous';s.onload=()=>{s.dataset.loaded='1';resolve()};s.onerror=reject;document.head.append(s)});
  addCss();
  katexPromise=script('https://cdn.jsdelivr.net/npm/katex@0.18.1/dist/katex.min.js','sha384-ycJ6GAwiS15LoUPipwJOrWTvkUHl/YqELValBwI5I4awP1EeEQJYarj+w85ntcz7')
    .then(()=>script('https://cdn.jsdelivr.net/npm/katex@0.18.1/dist/contrib/auto-render.min.js','sha384-bjyGPfbij8/NDKJhSGZNP/khQVgtHUE5exjm4Ydllo42FwIgYsdLO2lXGmRBf5Mz'))
    .catch(error=>{katexPromise=null;console.warn('Không tải được KaTeX',error)});
  return katexPromise;
}
const KEYS={
  api:'cs115_openai_api_key_v2',
  model:'cs115_openai_model_v2',
  chat:'cs115_ai_chat_v2',
  sid:'cs115_ai_session_v2'
};
const get=k=>{try{return STORE.getItem(k)||''}catch{return''}};
const set=(k,v)=>{try{STORE.setItem(k,v)}catch{}};
const del=k=>{try{STORE.removeItem(k)}catch{}};
let sid=get(KEYS.sid);
if(!sid){sid=(crypto.randomUUID?.()||`${Date.now()}${Math.random()}`).replaceAll('-','');set(KEYS.sid,sid)}
let chat=[];
try{chat=JSON.parse(get(KEYS.chat)||'[]').filter(x=>x&&['user','assistant'].includes(x.role)&&typeof x.content==='string').slice(-20)}catch{}

const root=document.createElement('div');
root.id='cs115-ai';
root.innerHTML=`
<button class="ai-open" type="button" aria-label="Mở trợ giảng AI" aria-expanded="false">🧠</button>
<section class="ai-box" hidden aria-label="Trợ giảng AI CS115">
  <header>
    <b aria-hidden="true">∑</b>
    <div><strong>Trợ giảng AI CS115</strong><small>Markdown · công thức LaTeX · ngữ cảnh bài học</small></div>
    <button class="ai-reset" type="button" title="Xóa cuộc trò chuyện" aria-label="Xóa cuộc trò chuyện">↺</button>
    <button class="ai-close" type="button" title="Đóng" aria-label="Đóng chatbot">✕</button>
  </header>
  <details class="ai-settings">
    <summary>Cấu hình OpenAI</summary>
    <label for="cs115-ai-key">OpenAI API key</label>
    <div class="ai-key"><input id="cs115-ai-key" class="ai-key-input" type="password" placeholder="sk-…" autocomplete="off" spellcheck="false"><button class="ai-eye" type="button" aria-label="Hiện hoặc ẩn API key">👁</button></div>
    <div class="ai-row"><button class="ai-models" type="button">Kiểm tra key & tải model</button><button class="ai-forget" type="button">Xóa key</button></div>
    <label for="cs115-ai-model">Model</label>
    <select id="cs115-ai-model" class="ai-select"></select>
    <p class="ai-status" role="status" aria-live="polite"></p>
    <small class="ai-key-note">Key được lưu trong <code>localStorage</code> của trình duyệt này cho đến khi bạn bấm “Xóa key” hoặc xóa dữ liệu website. Không nhập key trên máy dùng chung.</small>
  </details>
  <main class="ai-msgs" aria-live="polite"></main>
  <form><textarea rows="1" placeholder="Hỏi về bài học… Ví dụ: Giải thích vì sao AB ≠ BA" aria-label="Câu hỏi"></textarea><button class="ai-send" type="submit" aria-label="Gửi câu hỏi">➤</button></form>
</section>`;
document.body.append(root);

const $=q=>root.querySelector(q);
const box=$('.ai-box'),openBtn=$('.ai-open'),keyInput=$('.ai-key-input'),modelSelect=$('.ai-select'),msgs=$('.ai-msgs'),text=$('textarea'),status=$('.ai-status'),send=$('.ai-send');
const fallback=[
  {id:'gpt-5.6',label:'GPT-5.6 Sol · mạnh nhất'},
  {id:'gpt-5.6-terra',label:'GPT-5.6 Terra · cân bằng'},
  {id:'gpt-5.6-luna',label:'GPT-5.6 Luna · tiết kiệm'},
  {id:'chat-latest',label:'Chat Latest'}
];

function setModels(list,preferred){
  const old=modelSelect.value||get(KEYS.model);
  modelSelect.replaceChildren();
  for(const item of list){
    const id=typeof item==='string'?item:item.id;
    if(!id) continue;
    const o=document.createElement('option');
    o.value=id;o.textContent=typeof item==='string'?item:(item.label||id);modelSelect.append(o);
  }
  const ids=[...modelSelect.options].map(o=>o.value);
  modelSelect.value=ids.includes(old)?old:ids.includes(preferred)?preferred:ids.includes('gpt-5.6-terra')?'gpt-5.6-terra':ids[0]||'';
  if(modelSelect.value)set(KEYS.model,modelSelect.value);
}
setModels(fallback,'gpt-5.6-terra');
keyInput.value=get(KEYS.api);

function note(message,isBad=false){status.textContent=message||'';status.classList.toggle('bad',isBad)}
function safeUrl(raw){try{const u=new URL(raw,location.href);return ['http:','https:','mailto:'].includes(u.protocol)?u.href:''}catch{return''}}

function appendInline(parent,source){
  const token=/(`[^`\n]+`|\*\*[^*\n]+\*\*|~~[^~\n]+~~|\*[^*\n]+\*|\[[^\]\n]+\]\([^\s)]+\))/g;
  let last=0,m;
  while((m=token.exec(source))){
    if(m.index>last)parent.append(document.createTextNode(source.slice(last,m.index)));
    const t=m[0];
    if(t.startsWith('`')){const e=document.createElement('code');e.textContent=t.slice(1,-1);parent.append(e)}
    else if(t.startsWith('**')){const e=document.createElement('strong');appendInline(e,t.slice(2,-2));parent.append(e)}
    else if(t.startsWith('~~')){const e=document.createElement('del');appendInline(e,t.slice(2,-2));parent.append(e)}
    else if(t.startsWith('*')){const e=document.createElement('em');appendInline(e,t.slice(1,-1));parent.append(e)}
    else{
      const lm=t.match(/^\[([^\]]+)\]\(([^)]+)\)$/);const href=lm?safeUrl(lm[2]):'';
      if(href){const a=document.createElement('a');a.href=href;a.target='_blank';a.rel='noopener noreferrer';a.textContent=lm[1];parent.append(a)}else parent.append(document.createTextNode(t));
    }
    last=token.lastIndex;
  }
  if(last<source.length)parent.append(document.createTextNode(source.slice(last)));
}

function makeParagraph(lines){const p=document.createElement('p');lines.forEach((line,i)=>{if(i)p.append(document.createElement('br'));appendInline(p,line)});return p}
function isTableDivider(line){return /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(line)}
function cells(line){return line.trim().replace(/^\||\|$/g,'').split('|').map(x=>x.trim())}
function renderMarkdown(markdown){
  const fragment=document.createDocumentFragment();
  const lines=String(markdown||'').replace(/\r\n?/g,'\n').split('\n');
  let i=0;
  while(i<lines.length){
    const line=lines[i];
    if(!line.trim()){i++;continue}
    const fence=line.match(/^\s*```\s*([\w+-]*)\s*$/);
    if(fence){
      const language=fence[1]||'';const code=[];i++;
      while(i<lines.length&&!/^\s*```\s*$/.test(lines[i]))code.push(lines[i++]);
      if(i<lines.length)i++;
      const wrap=document.createElement('div');wrap.className='ai-code-wrap';
      const copy=document.createElement('button');copy.type='button';copy.className='ai-copy';copy.textContent='Sao chép';
      const pre=document.createElement('pre');const c=document.createElement('code');if(language)c.dataset.language=language;c.textContent=code.join('\n');pre.append(c);
      copy.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(c.textContent);copy.textContent='Đã chép';setTimeout(()=>copy.textContent='Sao chép',1200)}catch{copy.textContent='Không chép được'}});
      wrap.append(copy,pre);fragment.append(wrap);continue;
    }
    const heading=line.match(/^\s*(#{1,4})\s+(.+)$/);
    if(heading){const h=document.createElement('h'+heading[1].length);appendInline(h,heading[2]);fragment.append(h);i++;continue}
    if(/^\s*(---+|___+|\*\*\*+)\s*$/.test(line)){fragment.append(document.createElement('hr'));i++;continue}
    if(i+1<lines.length&&line.includes('|')&&isTableDivider(lines[i+1])){
      const table=document.createElement('table'),thead=document.createElement('thead'),tbody=document.createElement('tbody'),hr=document.createElement('tr');
      cells(line).forEach(v=>{const th=document.createElement('th');appendInline(th,v);hr.append(th)});thead.append(hr);i+=2;
      while(i<lines.length&&lines[i].includes('|')&&lines[i].trim()){const tr=document.createElement('tr');cells(lines[i]).forEach(v=>{const td=document.createElement('td');appendInline(td,v);tr.append(td)});tbody.append(tr);i++}
      const scroll=document.createElement('div');scroll.className='ai-table-scroll';table.append(thead,tbody);scroll.append(table);fragment.append(scroll);continue;
    }
    if(/^\s*>\s?/.test(line)){
      const q=document.createElement('blockquote');const content=[];while(i<lines.length&&/^\s*>\s?/.test(lines[i]))content.push(lines[i++].replace(/^\s*>\s?/,''));q.append(makeParagraph(content));fragment.append(q);continue;
    }
    const list=line.match(/^\s*([-+*]|\d+[.)])\s+(.+)$/);
    if(list){const ordered=/\d/.test(list[1]),ul=document.createElement(ordered?'ol':'ul');
      while(i<lines.length){const m=lines[i].match(/^\s*([-+*]|\d+[.)])\s+(.+)$/);if(!m||(/\d/.test(m[1])!==ordered))break;const li=document.createElement('li');appendInline(li,m[2]);ul.append(li);i++}
      fragment.append(ul);continue;
    }
    const para=[];
    while(i<lines.length&&lines[i].trim()&&!/^\s*```/.test(lines[i])&&!/^\s*(#{1,4})\s+/.test(lines[i])&&!/^\s*>\s?/.test(lines[i])&&!/^\s*([-+*]|\d+[.)])\s+/.test(lines[i])&&!(i+1<lines.length&&lines[i].includes('|')&&isTableDivider(lines[i+1]))){para.push(lines[i++])}
    fragment.append(makeParagraph(para));
  }
  return fragment;
}

function renderMath(container){
  ensureKatex().then(()=>{if(typeof window.renderMathInElement!=='function')return;try{window.renderMathInElement(container,{delimiters:[{left:'$$',right:'$$',display:true},{left:'\\[',right:'\\]',display:true},{left:'\\(',right:'\\)',display:false},{left:'$',right:'$',display:false}],throwOnError:false,strict:'ignore',ignoredTags:['script','noscript','style','textarea','pre','code','option']})}catch(err){console.warn('KaTeX render failed',err)}})
}
function normalizeMathEscapes(value){
  let s=String(value||'').replace(/\r\n?/g,'\n');
  s=s.replaceAll('\\\\[','\\[').replaceAll('\\\\]','\\]').replaceAll('\\\\(','\\(').replaceAll('\\\\)','\\)');
  const body=b=>b.replaceAll('\\\\\\\\','\\\\').replaceAll('\\_','_').replace(/\s*\n\s*/g,' ').trim();
  s=s.replace(/\\\[([\s\S]*?)\\\]/g,(_,b)=>'\\['+body(b)+'\\]');
  s=s.replace(/\$\$([\s\S]*?)\$\$/g,(_,b)=>'\\['+body(b)+'\\]');
  s=s.replace(/\\\(([\s\S]*?)\\\)/g,(_,b)=>'\\('+body(b)+'\\)');
  return s;
}
function bubble(role,content,isBad=false){
  const d=document.createElement('div');d.className='ai-msg '+(isBad?'bad':role);
  if(role==='assistant'&&!isBad){const normalized=normalizeMathEscapes(content);d.classList.add('ai-render');d.append(renderMarkdown(normalized));renderMath(d)}else d.textContent=content;
  msgs.append(d);msgs.scrollTop=msgs.scrollHeight;return d;
}
function renderChat(){msgs.replaceChildren();if(!chat.length)bubble('assistant','Chào bạn! Hãy nhập OpenAI API key trong **Cấu hình OpenAI**. Tôi có thể trình bày Markdown và công thức như $A^T A$, hoặc khối công thức:\n\n$$\\nabla f(x)=0$$');else chat.forEach(x=>bubble(x.role,x.content))}
renderChat();

function show(value){box.hidden=!value;openBtn.setAttribute('aria-expanded',String(value));if(value){if(!keyInput.value)$('.ai-settings').open=true;setTimeout(()=>{(keyInput.value?text:keyInput).focus()},0)}}
openBtn.onclick=()=>show(box.hidden);$('.ai-close').onclick=()=>show(false);document.addEventListener('keydown',e=>{if(e.key==='Escape')show(false)});
$('.ai-eye').onclick=()=>{keyInput.type=keyInput.type==='password'?'text':'password'};
modelSelect.onchange=()=>set(KEYS.model,modelSelect.value);
keyInput.addEventListener('input',()=>{const v=keyInput.value.trim();if(v)set(KEYS.api,v);else del(KEYS.api)});
$('.ai-forget').onclick=()=>{keyInput.value='';del(KEYS.api);note('Đã xóa API key khỏi localStorage.');keyInput.focus()};
$('.ai-reset').onclick=()=>{chat=[];del(KEYS.chat);renderChat();note('Đã xóa cuộc trò chuyện.')};

$('.ai-models').onclick=async function(){
  const key=keyInput.value.trim();if(!key){note('Hãy nhập API key.',true);return keyInput.focus()}
  this.disabled=true;note('Đang kiểm tra key và tải danh sách model…');
  try{
    const r=await fetch('/api/models',{method:'POST',headers:{'x-openai-api-key':key,'Content-Type':'application/json'},body:'{}'});
    const data=await r.json();if(!r.ok)throw Error(data.error||`HTTP ${r.status}`);
    set(KEYS.api,key);setModels(data.models?.length?data.models:fallback,data.preferredModel);note(`Key hợp lệ · tìm thấy ${data.models?.length||0} model văn bản.`)
  }catch(err){note(err.message||'Không tải được model.',true)}finally{this.disabled=false}
};

function pageContext(){
  const clone=document.body.cloneNode(true);clone.querySelector('#cs115-ai')?.remove();clone.querySelectorAll('script,style,noscript,svg').forEach(n=>n.remove());
  const selected=String(getSelection?.()||'').trim();
  return((selected?`Đoạn người học đang chọn:\n${selected.slice(0,3500)}\n\n`:'')+(clone.innerText||clone.textContent||'').replace(/\n{3,}/g,'\n\n')).trim().slice(0,16000)
}
function resize(){text.style.height='auto';text.style.height=Math.min(text.scrollHeight,128)+'px'}
text.oninput=resize;text.onkeydown=e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();root.querySelector('form').requestSubmit()}};
root.querySelector('form').onsubmit=async e=>{
  e.preventDefault();const question=text.value.trim(),key=keyInput.value.trim();if(!question)return;
  if(!key){$('.ai-settings').open=true;note('Hãy nhập API key trước.',true);return keyInput.focus()}
  set(KEYS.api,key);chat.push({role:'user',content:question.slice(0,6000)});chat=chat.slice(-20);set(KEYS.chat,JSON.stringify(chat));bubble('user',question);text.value='';resize();send.disabled=true;
  const wait=bubble('assistant','Đang suy nghĩ…');
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'x-openai-api-key':key,'Content-Type':'application/json'},body:JSON.stringify({model:modelSelect.value,messages:chat,pageTitle:document.title,pageContext:pageContext(),sessionId:sid})});
    const data=await r.json();if(!r.ok)throw Error(data.error||`HTTP ${r.status}`);wait.remove();
    const answer=String(data.reply||'').trim()||'Không nhận được nội dung trả lời.';chat.push({role:'assistant',content:answer});chat=chat.slice(-20);set(KEYS.chat,JSON.stringify(chat));bubble('assistant',answer);note(`Đã trả lời bằng ${data.model||modelSelect.value}.`)
  }catch(err){wait.remove();bubble('assistant',err.message||'Không thể nhận câu trả lời.',true);note(err.message||'Có lỗi xảy ra.',true)}finally{send.disabled=false;text.focus()}
};
})();
