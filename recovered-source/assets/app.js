(function(){
  const progress=document.querySelector('.progress');
  function updateReading(){if(!progress)return;const d=document.documentElement;const max=d.scrollHeight-d.clientHeight;progress.style.width=(max?d.scrollTop/max*100:0)+'%'}
  window.addEventListener('scroll',updateReading,{passive:true});updateReading();

  const tocLinks=[...document.querySelectorAll('.toc a')];
  const sections=tocLinks.map(a=>document.querySelector(a.getAttribute('href'))).filter(Boolean);
  if(sections.length&&'IntersectionObserver'in window){
    const obs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting)tocLinks.forEach(a=>a.classList.toggle('active',a.getAttribute('href')==='#'+e.target.id))}),{rootMargin:'-18% 0px -70% 0px'});
    sections.forEach(s=>obs.observe(s));
  }

  const root=document.body;
  const lessonId=root.dataset.lesson;
  const exercises=[...document.querySelectorAll('details.exercise')];
  const storeKey=lessonId?'cs115-progress:'+lessonId:null;
  let state={};
  if(storeKey){try{state=JSON.parse(localStorage.getItem(storeKey)||'{}')}catch(e){state={}}}
  const strip=s=>String(s??'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[−–—]/g,'-').replace(/[×·]/g,'*').replace(/[\[\]{}(),]/g,' ').replace(/\s+/g,' ').trim();
  function acceptable(ex,val){
    const answers=String(ex.dataset.answer||'').split('||').map(strip).filter(Boolean);
    const v=strip(val);
    if(!v)return false;
    const vn=Number(v.replace(',','.'));
    for(const a of answers){
      if(v===a)return true;
      const an=Number(a.replace(',','.'));
      if(Number.isFinite(vn)&&Number.isFinite(an)&&Math.abs(vn-an)<=1e-4)return true;
      if(ex.dataset.mode==='contains'&&a.split(' ').every(t=>v.includes(t)))return true;
    }
    return false;
  }
  function persist(){if(storeKey)localStorage.setItem(storeKey,JSON.stringify(state))}
  function updateExerciseStats(){
    const total=exercises.length;const checked=Object.values(state).filter(x=>x&&x.checked).length;const correct=Object.values(state).filter(x=>x&&x.correct).length;
    document.querySelectorAll('[data-stat="correct"]').forEach(e=>e.textContent=correct);
    document.querySelectorAll('[data-stat="checked"]').forEach(e=>e.textContent=checked);
    document.querySelectorAll('[data-stat="total"]').forEach(e=>e.textContent=total);
    document.querySelectorAll('[data-progress-bar]').forEach(e=>e.style.width=(total?correct/total*100:0)+'%');
    if(lessonId)localStorage.setItem('cs115-summary:'+lessonId,JSON.stringify({correct,total,updated:Date.now()}));
  }
  function closeOthers(active){exercises.forEach(e=>{if(e!==active){e.open=false;e.dataset.view='question'}})}
  exercises.forEach((ex,i)=>{
    ex.dataset.view='question';
    const id=ex.dataset.id||String(i+1);ex.dataset.id=id;
    ex.addEventListener('toggle',()=>{if(ex.open)closeOthers(ex)});
    const input=ex.querySelector('[data-answer-input]');
    const feedback=ex.querySelector('.feedback');
    const hint=ex.querySelector('.hint');
    const saved=state[id];
    if(saved&&input){input.value=saved.value||'';if(saved.checked){feedback.textContent=saved.correct?'✓ Đúng':'Chưa đúng';feedback.className='feedback '+(saved.correct?'ok':'bad')}}
    ex.querySelectorAll('[data-check]').forEach(btn=>btn.addEventListener('click',()=>{
      const value=input?input.value:'';const ok=acceptable(ex,value);const prev=state[id]||{tries:0};state[id]={value,checked:true,correct:ok,tries:(prev.tries||0)+1};
      feedback.textContent=ok?'✓ Chính xác':'✗ Chưa đúng, hãy kiểm tra lại';feedback.className='feedback '+(ok?'ok':'bad');
      if(!ok&&state[id].tries>=2&&hint)hint.style.display='block';persist();updateExerciseStats();
    }));
    ex.querySelectorAll('[data-toggle-solution]').forEach(btn=>btn.addEventListener('click',()=>{closeOthers(ex);ex.open=true;ex.dataset.view=ex.dataset.view==='solution'?'question':'solution';btn.textContent=ex.dataset.view==='solution'?'Quay lại đề bài':'Xem lời giải'}));
  });
  document.querySelectorAll('[data-reset-progress]').forEach(btn=>btn.addEventListener('click',()=>{if(!confirm('Xóa toàn bộ đáp án và tiến độ của bài học này?'))return;state={};persist();exercises.forEach(ex=>{const input=ex.querySelector('[data-answer-input]');if(input)input.value='';const fb=ex.querySelector('.feedback');if(fb){fb.textContent='';fb.className='feedback'}const h=ex.querySelector('.hint');if(h)h.style.display='none';ex.open=false;ex.dataset.view='question'});updateExerciseStats()}));
  updateExerciseStats();

  const cards=[...document.querySelectorAll('.lesson-card')];
  const search=document.querySelector('[data-library-search]');
  const filters=[...document.querySelectorAll('[data-filter]')];
  let active='all';
  function refreshCards(){const q=strip(search?search.value:'');cards.forEach(c=>{const cat=c.dataset.category||'';const text=strip(c.innerText);c.classList.toggle('hidden',!(active==='all'||cat===active)||!(q===''||text.includes(q)))})}
  if(search)search.addEventListener('input',refreshCards);
  filters.forEach(b=>b.addEventListener('click',()=>{filters.forEach(x=>x.classList.remove('active'));b.classList.add('active');active=b.dataset.filter;refreshCards()}));
  cards.forEach(c=>{const id=c.dataset.lesson;let s={correct:0,total:Number(c.dataset.total||0)};try{s=JSON.parse(localStorage.getItem('cs115-summary:'+id)||JSON.stringify(s))}catch(e){};c.querySelectorAll('[data-card-correct]').forEach(e=>e.textContent=s.correct||0);c.querySelectorAll('[data-card-total]').forEach(e=>e.textContent=s.total||c.dataset.total||0);c.querySelectorAll('[data-card-bar]').forEach(e=>e.style.width=((s.total||0)?(s.correct||0)/s.total*100:0)+'%')});
})();
