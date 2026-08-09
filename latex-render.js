(()=>{'use strict';
if(window.__cs115LatexRender)return;window.__cs115LatexRender=true;

const KATEX='https://cdn.jsdelivr.net/npm/katex@0.18.1/dist/';
const css=()=>{if(document.querySelector('link[data-cs115-katex-main]'))return;const l=document.createElement('link');l.rel='stylesheet';l.href=KATEX+'katex.min.css';l.dataset.cs115KatexMain='1';document.head.appendChild(l)};
const loadScript=(src)=>new Promise((resolve,reject)=>{const found=[...document.scripts].find(s=>s.src===src);if(found){if(window.katex)return resolve();found.addEventListener('load',resolve,{once:true});found.addEventListener('error',reject,{once:true});return}const s=document.createElement('script');s.src=src;s.defer=true;s.onload=resolve;s.onerror=reject;document.head.appendChild(s)});

const exact=new Map([
['v = (v₁, v₂, …, vₙ) ∈ Rⁿ','\\mathbf v=(v_1,v_2,\\ldots,v_n)\\in\\mathbb R^n'],
['AB = B − A = (4−1, 1−(−2), 5−3) = (3,3,2)','\\overrightarrow{AB}=B-A=(4-1,\\,1-(-2),\\,5-3)=(3,3,2)'],
['x = [x₁ x₂ … xₙ]ᵀ ∈ Rⁿˣ¹','\\mathbf x=[x_1\\;x_2\\;\\cdots\\;x_n]^T\\in\\mathbb R^{n\\times1}'],
['xᵀ = [x₁ x₂ … xₙ] ∈ R¹ˣⁿ','\\mathbf x^T=[x_1\\;x_2\\;\\cdots\\;x_n]\\in\\mathbb R^{1\\times n}'],
['α ∈ R','\\alpha\\in\\mathbb R'],
['u+v=(u₁+v₁,…,uₙ+vₙ) · u−v=(u₁−v₁,…,uₙ−vₙ) · αu=(αu₁,…,αuₙ)','\\mathbf u+\\mathbf v=(u_1+v_1,\\ldots,u_n+v_n)\\qquad \\mathbf u-\\mathbf v=(u_1-v_1,\\ldots,u_n-v_n)\\qquad \\alpha\\mathbf u=(\\alpha u_1,\\ldots,\\alpha u_n)'],
['||x||₁ = Σ |xᵢ|','\\lVert\\mathbf x\\rVert_1=\\sum_i|x_i|'],
['||x||₂ = √(Σ xᵢ²) = √(xᵀx)','\\lVert\\mathbf x\\rVert_2=\\sqrt{\\sum_i x_i^2}=\\sqrt{\\mathbf x^T\\mathbf x}'],
['||x||∞ = max |xᵢ|','\\lVert\\mathbf x\\rVert_\\infty=\\max_i|x_i|'],
['x̂ = x / ||x||₂ = (3/5, 4/5)','\\hat{\\mathbf x}=\\frac{\\mathbf x}{\\lVert\\mathbf x\\rVert_2}=\\left(\\frac35,\\frac45\\right)'],
['d(x,y)=||x−y||','d(\\mathbf x,\\mathbf y)=\\lVert\\mathbf x-\\mathbf y\\rVert'],
['u·v = uᵀv = Σ uᵢvᵢ = ||u||·||v||·cosθ','\\mathbf u\\cdot\\mathbf v=\\mathbf u^T\\mathbf v=\\sum_i u_i v_i=\\lVert\\mathbf u\\rVert\\,\\lVert\\mathbf v\\rVert\\cos\\theta'],
['u·v = 2(−1)+(−1)4+3·2 = 0','\\mathbf u\\cdot\\mathbf v=2(-1)+(-1)4+3\\cdot2=0'],
['projᵥ(u) = (u·v / ||v||²) v, với v≠0','\\operatorname{proj}_{\\mathbf v}(\\mathbf u)=\\frac{\\mathbf u\\cdot\\mathbf v}{\\lVert\\mathbf v\\rVert^2}\\mathbf v,\\qquad \\mathbf v\\ne\\mathbf0'],
['w = c₁v₁ + c₂v₂ + … + cₖvₖ','\\mathbf w=c_1\\mathbf v_1+c_2\\mathbf v_2+\\cdots+c_k\\mathbf v_k'],
['q₁=a₁/||a₁||','\\mathbf q_1=\\frac{\\mathbf a_1}{\\lVert\\mathbf a_1\\rVert}'],
['ũ₂=a₂−(q₁·a₂)q₁,   q₂=ũ₂/||ũ₂||','\\tilde{\\mathbf u}_2=\\mathbf a_2-(\\mathbf q_1\\cdot\\mathbf a_2)\\mathbf q_1,\\qquad \\mathbf q_2=\\frac{\\tilde{\\mathbf u}_2}{\\lVert\\tilde{\\mathbf u}_2\\rVert}'],
['ŷ = b + wᵀx','\\hat y=b+\\mathbf w^T\\mathbf x']
]);

const sub={'₀':'_0','₁':'_1','₂':'_2','₃':'_3','₄':'_4','₅':'_5','₆':'_6','₇':'_7','₈':'_8','₉':'_9','ᵢ':'_i','ⱼ':'_j','ₖ':'_k','ₙ':'_n','ₘ':'_m'};
const sup={'²':'^2','³':'^3','ⁿ':'^n','ᵀ':'^T'};
function generic(s){
  let t=s.trim();
  if(exact.has(t))return exact.get(t);
  t=t.replace(/R([⁰¹²³⁴⁵⁶⁷⁸⁹ⁿᵐ]+)ˣ([⁰¹²³⁴⁵⁶⁷⁸⁹ⁿᵐ]+)/g,(_,a,b)=>`\\mathbb R^{${decodeSup(a)}\\times${decodeSup(b)}}`);
  t=t.replace(/R([⁰¹²³⁴⁵⁶⁷⁸⁹ⁿᵐ]+)/g,(_,a)=>`\\mathbb R^{${decodeSup(a)}}`);
  t=[...t].map(ch=>sub[ch]||sup[ch]||ch).join('');
  t=t.replaceAll('−','-').replaceAll('·','\\cdot ').replaceAll('×','\\times ').replaceAll('≠','\\ne ').replaceAll('≤','\\le ').replaceAll('≥','\\ge ').replaceAll('∈','\\in ').replaceAll('∞','\\infty ').replaceAll('Σ','\\sum ').replaceAll('θ','\\theta ').replaceAll('α','\\alpha ').replaceAll('β','\\beta ').replaceAll('λ','\\lambda ').replaceAll('∇','\\nabla ').replaceAll('…','\\ldots ');
  t=t.replace(/\|\|([^|]+)\|\|/g,'\\lVert $1\\rVert');
  t=t.replace(/√\(([^()]*)\)/g,'\\sqrt{$1}');
  t=t.replace(/√([^\s,+-]+)/g,'\\sqrt{$1}');
  t=t.replace(/\bcos(?=\\theta|\s*\\theta)/g,'\\cos ');
  t=t.replace(/\bsin(?=\\theta|\s*\\theta)/g,'\\sin ');
  return t;
}
function decodeSup(s){return [...s].map(ch=>({'⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','ⁿ':'n','ᵐ':'m'}[ch]||ch)).join('')}
function renderAll(){
  if(!window.katex)return;
  document.querySelectorAll('.formula').forEach(el=>{
    if(el.dataset.latexDone==='1'||el.querySelector('.katex'))return;
    const raw=(el.textContent||'').replace(/\s+/g,' ').trim();
    if(!raw)return;
    try{window.katex.render(generic(raw),el,{displayMode:true,throwOnError:true,strict:'ignore',trust:false});el.dataset.latexDone='1';el.style.overflowX='auto';el.style.overflowY='hidden'}catch(err){console.debug('CS115 LaTeX skipped:',raw,err?.message||err)}
  });
}
css();
loadScript(KATEX+'katex.min.js').then(()=>{renderAll();const mo=new MutationObserver(()=>renderAll());mo.observe(document.body,{childList:true,subtree:true})}).catch(err=>console.warn('Không tải được KaTeX cho công thức CS115',err));
})();
