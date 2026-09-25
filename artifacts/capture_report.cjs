const {chromium}=require('playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:960}});
 await page.goto('http://127.0.0.1:8876');
 await page.locator('#plan.active').waitFor();
 await page.evaluate(()=>{
   programs.length=0;tasks.length=0;
   const p=createProgramRecord({name:'Clinical Leadership',type:'Workshop',route:'B2B',region:'Egypt',startDate:'2026-09-20',endDate:'2026-10-15'});p.id='DEMO-P1';
   p.activities[0].status='In Progress';
   masterData.networking={contacts:[{id:'DEMO-C1',name:'Mona Hassan',organization:'Example Healthcare Group',role:'Learning and Development Manager',email:'mona@example.com',phone:'+20 100 000 0000',notes:'Demonstration contact for the networking screen.'},{id:'DEMO-C2',name:'Omar Ali',organization:'Example Training Partner',role:'Partnerships Coordinator',email:'omar@example.com',notes:'Demonstration contact.'}],visits:[
    {id:'DEMO-V1',contactId:'DEMO-C1',programId:p.id,activity:'Instructors',date:'2026-09-20',time:'10:00',type:'Online Meeting',status:'Upcoming',location:'Online',objective:'Discuss clinical training partnership',outcome:'',followUp:'2026-09-22',followUpNotes:'Send proposed instructor profiles',followUpCompleted:false,notes:'Demonstration visit.'},
    {id:'DEMO-V2',contactId:'DEMO-C2',programId:p.id,activity:'Sponsorships',date:'2026-09-10',time:'11:00',type:'Phone Call',status:'Completed',objective:'Review sponsorship opportunities',outcome:'Partner requested a program proposal',followUp:'2026-09-14',followUpNotes:'Share the proposal and agree next steps',followUpCompleted:false} ]};
   refresh();setView('plan');
 });
 await page.waitForTimeout(1600);
 const shot=async name=>{await page.waitForTimeout(500);await page.screenshot({path:path.join(__dirname,'report-assets',name+'.png')});};
 await shot('new-plan');
 await page.evaluate(()=>setView('visits'));await shot('new-visits');
 await page.locator('#networkContactsTab').click();await shot('new-contacts');
 await page.evaluate(()=>openNetworkContact('DEMO-C1'));await shot('new-contact-form');
 await page.evaluate(()=>{networkClose('networkContactModal');openNetworkVisit('DEMO-V1')});await shot('new-visit-form');
 await page.evaluate(()=>networkClose('networkVisitModal'));
 await page.setViewportSize({width:390,height:1000});
 await page.evaluate(()=>setView('plan'));await shot('new-plan-mobile');
 await page.evaluate(()=>{networkState.tab='visits';setView('visits')});await shot('new-visits-mobile');
 await browser.close();
 console.log('Seven screenshots captured using demonstration records in the disposable database.');
})().catch(e=>{console.error(e);process.exit(1)});
