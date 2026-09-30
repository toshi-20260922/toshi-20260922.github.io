(()=>{
 const stage=document.querySelector('meta[name="preview-stage"]')?.content;
 if(!stage)return;
 const pause=ms=>new Promise(resolve=>setTimeout(resolve,ms));
 async function until(check,ms=15000){const end=Date.now()+ms;while(Date.now()<end){const found=check();if(found)return found;await pause(50);}throw new Error('診断画面の表示を確認できません');}
 const heading=part=>until(()=>document.querySelector('h1')?.textContent?.includes(part));
 const button=label=>[...document.querySelectorAll('button')].find(item=>item.textContent?.trim()===label);
 async function advance(expected,value){
   await heading(expected);
   if(typeof value==='number'){
     const input=await until(()=>document.querySelector('input[type="number"]'));
     Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(input,String(value));
     input.dispatchEvent(new Event('input',{bubbles:true}));
   }else{
     const option=await until(()=>[...document.querySelectorAll('label')].find(item=>item.textContent?.trim()===value));
     option.querySelector('input')?.click();
   }
   await pause(120);
   button('次へ')?.click();
 }
 (async()=>{
   await until(()=>button('無料で診断を始める'));
   await pause(500);
   button('無料で診断を始める').click();
   await heading('年間売上');
   if(stage==='question')return;
   await advance('年間売上',80000000);
   await advance('雇用保険加入従業員',8);
   await advance('製造業ですか','はい');
   await advance('工場がありますか','はい');
   await advance('投資予定額',20000000);
   await advance('従業員は全体',12);
   await advance('今回の投資','人手不足を減らす設備');
   await advance('作業時間の削減効果','作業時間を数値で示せる');
   await advance('投資効果と賃上げ','投資効果と賃上げを数字で説明できる');
   await heading('御社の第一候補');
   if(stage==='result')return;
   button('個別相談へ進む')?.click();
   await heading('診断結果をもとに相談する');
 })().catch(error=>console.error('Static preview route:',error));
})();