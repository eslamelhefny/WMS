// Run with Node and the Playwright package available on NODE_PATH.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'static/index.html'),'utf8');
for(const [,script] of html.matchAll(/<script>([\s\S]*?)<\/script>/g))new vm.Script(script);
(async()=>{
  const browser=await chromium.launch({channel:'msedge',headless:true});
  const page=await browser.newPage({viewport:{width:1440,height:1000}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  try{
    await page.request.post('http://127.0.0.1:8876/api/store',{data:{user:{name:'Review Manager',position:'Academy Manager',email:'review@andalusia.net',defaultView:'plan'},tasks:[],programs:[],masterData:{}}});
    await page.goto('http://127.0.0.1:8876');
    await page.locator('#plan.active').waitFor();
    await page.evaluate(()=>{
      for(const [id,name] of [['P1','Clinical Leadership'],['P2','Nursing Skills']]){
        const p=createProgramRecord({name,type:'Workshop',route:'B2B',region:'Egypt',startDate:'2026-10-01',endDate:'2026-10-15'});
        p.id=id;
      }
      const first=programs.find(p=>p.id==='P1');
      first.activities[0].status='In Progress';
      first.activities[0].visits.push({id:'OLD1',target:'Existing Partner',date:'2026-08-01',type:'Phone Call',objective:'Legacy visit',outcome:'Agreed',followUp:'',followUpCompleted:true});
      refresh();
    });
    await page.locator('.sidebar [data-view="visits"]').click();
    await page.getByRole('button',{name:'Add contact',exact:true}).click();
    await page.locator('#contact_name').fill('Mona <Partner>');
    await page.locator('#contact_organization').fill('Health Group');
    await page.locator('#contact_email').fill('mona@example.com');
    await page.locator('#contact_phone').fill('+20 100 123 4567');
    await page.getByRole('button',{name:'Save contact',exact:true}).click();
    await page.getByRole('button',{name:'Add visit',exact:true}).click();
    await page.locator('#nv_contactId').selectOption({label:'Mona <Partner> · Health Group'});
    await page.locator('#nv_programId').selectOption('P1');
    await page.locator('#nv_activity').selectOption('Instructors');
    await page.locator('#nv_date').fill('2026-10-02');
    await page.locator('#nv_objective').fill('Discuss training partnership');
    await page.locator('#nv_followUp').fill('2026-10-03');
    await page.getByRole('button',{name:'Save visit',exact:true}).click();
    await page.locator('#networkProgram').selectOption('P1');
    await page.locator('#networkActivity').selectOption('Instructors');
    assert.match(await page.locator('#networkTable').innerText(),/Discuss training partnership/);
    assert.match(await page.locator('#networkTable').innerText(),/Legacy visit/);
    await page.locator('#networkProgram').selectOption('P2');
    assert.match(await page.locator('#networkTable').innerText(),/No visits match/);
    await page.locator('#visits').getByRole('button',{name:'Clear filters'}).click();
    await page.locator('#networkSearch').fill('Health Group');
    assert.match(await page.locator('#networkTable').innerText(),/Discuss training partnership/);
    assert.doesNotMatch(await page.locator('#networkTable').innerText(),/Legacy visit/);
    await page.locator('#networkSearch').fill('');
    await page.locator('#networkContactsTab').click();
    await page.locator('#networkTable').getByRole('button',{name:'History',exact:true}).click();
    assert.match(await page.locator('#networkContactSummary').innerText(),/Mona <Partner>/);
    assert.doesNotMatch(await page.locator('#networkTable').innerText(),/Legacy visit/);
    await page.getByRole('button',{name:'Edit visit',exact:true}).click();
    await page.locator('#nv_status').selectOption('Completed');
    await page.getByRole('button',{name:'Save visit',exact:true}).click();
    assert.equal(await page.locator('#networkVisitModal').evaluate(e=>e.classList.contains('show')),true);
    await page.locator('#nv_outcome').fill('Training proposal requested');
    await page.locator('#nv_followUp').fill('2026-10-01');
    await page.getByRole('button',{name:'Save visit',exact:true}).click();
    assert.equal(await page.locator('#networkVisitModal').evaluate(e=>e.classList.contains('show')),true);
    await page.locator('#nv_followUp').fill('2026-10-03');
    await page.getByRole('button',{name:'Save visit',exact:true}).click();
    await page.locator('.sidebar [data-view="plan"]').click();
    await page.locator('#planProgram').selectOption('P1');
    await page.locator('#planActivity').selectOption('Instructors');
    assert.match(await page.locator('#planInProgress').innerText(),/Instructors/);
    assert.match(await page.locator('#planUpcoming').innerText(),/Follow up with Mona/);
    assert.doesNotMatch(await page.locator('#planUpcoming').innerText(),/Discuss training partnership\nClinical Leadership/);
    await page.waitForFunction(()=>document.getElementById('storageStatus').textContent==='Saved to SQLite');
    await page.reload();
    await page.locator('#plan.active').waitFor();
    await page.locator('.sidebar [data-view="visits"]').click();
    assert.match(await page.locator('#networkTable').innerText(),/Training proposal requested/);
    const backup=await (await page.request.get('http://127.0.0.1:8876/api/export-text')).json();
    assert.equal(backup.masterData.networking.contacts[0].name,'Mona <Partner>');
    assert.equal(backup.masterData.networking.visits[0].status,'Completed');
    await page.locator('#networkContactsTab').click();
    await page.getByRole('button',{name:'Edit',exact:true}).click();
    await page.locator('#contact_phone').fill('+20 111 222 3333');
    await page.getByRole('button',{name:'Save contact',exact:true}).click();
    assert.match(await page.locator('#networkTable').innerText(),/111 222 3333/);
    await page.locator('#networkVisitsTab').click();
    await page.getByRole('button',{name:'Edit visit',exact:true}).click();
    await page.locator('#nv_followUpCompleted').check();
    await page.getByRole('button',{name:'Save visit',exact:true}).click();
    await page.locator('.sidebar [data-view="plan"]').click();
    assert.doesNotMatch(await page.locator('#planUpcoming').innerText(),/Follow up with Mona/);
    for(const width of [1440,390]){
      await page.setViewportSize({width,height:900});
      for(const view of ['plan','visits']){
        await page.evaluate(v=>setView(v),view);
        assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true,`${view} overflow at ${width}`);
        await page.screenshot({path:path.join(root,'tests',`${view}-${width}.png`),fullPage:true});
      }
    }
    await page.locator('#mobileMoreBtn').click();
    await page.locator('#mobileMoreMenu [data-view="plan"]').click();
    await page.locator('#plan.active').waitFor();
    await page.getByRole('button',{name:'Plan a visit',exact:true}).click();
    await page.keyboard.press('Escape');
    assert.equal(await page.locator('#networkVisitModal').evaluate(e=>e.classList.contains('show')),false);
    assert.deepEqual(errors,[]);
    console.log('PASS: syntax, contacts, visits, validation, legacy history, combined filters, follow-ups, SQLite reload, JSON backup, desktop/mobile layout and navigation.');
  }finally{await browser.close()}
})().catch(error=>{console.error(error);process.exitCode=1});
