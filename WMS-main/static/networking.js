/* Network records live in masterData.networking, included in SQLite and JSON backups.
   Existing operational interactions are read from their original program records. */
function networkStore(){
  if(!masterData.networking||typeof masterData.networking!=="object"||Array.isArray(masterData.networking))masterData.networking={};
  for(const key of ["contacts","visits"])if(!Array.isArray(masterData.networking[key]))masterData.networking[key]=[];
  return masterData.networking;
}
const networkState={tab:"visits",contactId:"",editingContact:"",editingVisit:""};
const networkStatuses=["Upcoming","In Progress","Completed","Cancelled"];
function networkId(prefix){return `${prefix}-${crypto.randomUUID()}`}
function networkOption(value,label){return `<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`}
function networkProgramName(id){return programs.find(p=>p.id===id)?.name||(id?"Unavailable program":"General networking")}
function networkActivities(programId=""){
  const selected=programs.filter(p=>!programId||p.id===programId);
  return [...new Set([...defaultActivities().map(a=>a.name),...selected.flatMap(p=>(p.activities||[]).map(a=>a.name)),...networkStore().visits.filter(v=>!programId||v.programId===programId).map(v=>v.activity)].filter(Boolean))].sort();
}
function networkSelect(id,values,placeholder){
  const el=document.getElementById(id),previous=el.value;
  el.innerHTML=networkOption("",placeholder)+values.map(([value,label])=>networkOption(value,label)).join("");
  if([...el.options].some(o=>o.value===previous))el.value=previous;
}
function networkFilters(prefix){
  networkSelect(`${prefix}Program`,programs.map(p=>[p.id,p.name]),"All programs");
  networkSelect(`${prefix}Activity`,networkActivities(document.getElementById(`${prefix}Program`).value).map(a=>[a,a]),"All activities");
  return {program:document.getElementById(`${prefix}Program`).value,activity:document.getElementById(`${prefix}Activity`).value,search:document.getElementById(`${prefix}Search`).value.trim().toLowerCase()};
}
function networkMatches(row,filter){return (!filter.program||row.programId===filter.program)&&(!filter.activity||row.activity===filter.activity)}
function networkContact(visit){return networkStore().contacts.find(c=>c.id===visit.contactId)}
function networkVisitRows(){
  const standalone=networkStore().visits.map(v=>({...v,source:"network",target:networkContact(v)?.name||v.target||"Contact unavailable"}));
  const operational=programs.flatMap(p=>normalizeActivityRecords(p).flatMap(a=>(a.visits||[]).map(v=>({...v,programId:p.id,activity:a.name,status:"Completed",source:"operations"}))));
  return [...standalone,...operational];
}
function networkSearchVisit(v,query){const c=networkContact(v);return !query||[v.target,c?.organization,c?.email,c?.phone,v.objective,v.outcome,v.location,v.notes,v.activity,networkProgramName(v.programId)].join(" ").toLowerCase().includes(query)}
function networkStats(id,items){document.getElementById(id).innerHTML=items.map(([label,value,hint])=>`<div class="card"><span>${escapeHtml(label)}</span><strong>${value}</strong><small>${escapeHtml(hint)}</small></div>`).join("")}
function renderPlan(){
  const filter=networkFilters("plan"),rows=[];
  programs.forEach(p=>normalizeActivityRecords(p).forEach(a=>{
    const status=a.status==="Not Started"?"Upcoming":a.status;
    rows.push({kind:"Activity",title:a.name,programId:p.id,activity:a.name,status,date:p.startDate||"",detail:a.ownerPosition,progress:a.progress,source:"activity"});
  }));
  networkVisitRows().forEach(v=>{
    rows.push({...v,kind:"Visit",title:v.objective||`Visit ${v.target}`,detail:v.target});
    if(v.followUp&&!v.followUpCompleted&&v.status!=="Cancelled")rows.push({...v,kind:"Follow-up",title:`Follow up with ${v.target}`,status:v.followUp<=TODAY?"In Progress":"Upcoming",date:v.followUp,detail:v.followUpNotes||v.objective});
  });
  const filtered=rows.filter(r=>networkMatches(r,filter)&&(!filter.search||[r.title,r.detail,r.activity,networkProgramName(r.programId)].join(" ").toLowerCase().includes(filter.search)));
  const active=filtered.filter(r=>r.status==="In Progress"),upcoming=filtered.filter(r=>r.status==="Upcoming");
  const overdue=filtered.filter(r=>["Upcoming","In Progress"].includes(r.status)&&r.date&&r.date<TODAY);
  networkStats("planKpis",[["In progress",active.length,"Activities, visits & follow-ups"],["Upcoming",upcoming.length,"Work that has not started"],["Overdue",overdue.length,"Open items dated before today"],["Completed",filtered.filter(r=>r.status==="Completed").length,"Finished activities & visits"]]);
  const card=r=>`<article class="plan-item"><span class="badge ${statusClass(r.status)}">${escapeHtml(r.kind)} · ${escapeHtml(r.status)}</span><h4>${escapeHtml(r.title)}</h4><p>${escapeHtml(networkProgramName(r.programId))} · ${escapeHtml(r.activity)}</p><p>${escapeHtml(r.detail||"")}</p><footer><span class="${r.date&&r.date<TODAY?'network-overdue':''}">${escapeHtml(r.date||"Date not set")}${r.date&&r.date<TODAY?' · Overdue':''}</span><button class="action-mini" data-network-action="${r.source==='activity'||r.source==='operations'?'activity':'visit'}" data-id="${escapeHtml(r.id||"")}" data-program="${escapeHtml(r.programId)}" data-activity="${escapeHtml(r.activity)}">${r.source==='activity'||r.source==='operations'?'Open activity':'View visit'}</button></footer></article>`;
  for(const [id,list] of [["planInProgress",active],["planUpcoming",upcoming]])document.getElementById(id).innerHTML=list.sort((a,b)=>(a.date||"9999").localeCompare(b.date||"9999")).map(card).join("")||'<div class="network-empty">No items match these filters.</div>';
  document.getElementById("planResults").textContent=`${active.length+upcoming.length} open items match your filters. Activity dates use the program start date.`;
}
function renderVisits(){
  const filter=networkFilters("network"),all=networkVisitRows(),scoped=all.filter(v=>networkMatches(v,filter));
  const contacts=networkStore().contacts.filter(c=>(!filter.program&&!filter.activity||scoped.some(v=>v.contactId===c.id))&&(!filter.search||[c.name,c.organization,c.role,c.email,c.phone,c.notes].join(" ").toLowerCase().includes(filter.search)));
  const visible=scoped.filter(v=>(!networkState.contactId||v.contactId===networkState.contactId)&&networkSearchVisit(v,filter.search)).sort((a,b)=>String(b.date).localeCompare(String(a.date)));
  networkStats("networkKpis",[["Contacts",contacts.length,"Reusable network contacts"],["Visits",visible.length,"Including operational history"],["Upcoming",visible.filter(v=>v.status==="Upcoming").length,"Planned visits"],["Open follow-ups",visible.filter(v=>v.followUp&&!v.followUpCompleted&&v.status!=="Cancelled").length,"Awaiting follow-up"]]);
  document.getElementById("networkVisitsTab").setAttribute("aria-pressed",networkState.tab==="visits");
  document.getElementById("networkContactsTab").setAttribute("aria-pressed",networkState.tab==="contacts");
  const contact=networkStore().contacts.find(c=>c.id===networkState.contactId),summary=document.getElementById("networkContactSummary");
  summary.hidden=!contact;
  summary.innerHTML=contact?`<strong>${escapeHtml(contact.name)}</strong><p>${escapeHtml([contact.role,contact.organization,contact.email,contact.phone].filter(Boolean).join(" · "))}</p><p>${escapeHtml(contact.notes||"")}</p><button class="btn ghost" data-network-action="clear-contact">Show all contacts’ visits</button>`:"";
  const table=document.getElementById("networkTable");
  if(networkState.tab==="contacts"){
    table.innerHTML=`<caption>${contacts.length} contacts · Program and activity filters use linked visits.</caption><thead><tr><th>Contact person</th><th>Organization / role</th><th>Contact details</th><th>Visits</th><th>Actions</th></tr></thead><tbody>${contacts.map(c=>`<tr><td><strong>${escapeHtml(c.name)}</strong><small>${escapeHtml(c.notes||"")}</small></td><td>${escapeHtml(c.organization||"—")}<small>${escapeHtml(c.role||"")}</small></td><td>${escapeHtml(c.email||"—")}<small>${escapeHtml(c.phone||"")}</small></td><td>${all.filter(v=>v.contactId===c.id).length}</td><td><div class="network-actions"><button class="action-mini" data-network-action="contact-history" data-id="${escapeHtml(c.id)}">History</button><button class="action-mini" data-network-action="contact" data-id="${escapeHtml(c.id)}">Edit</button><button class="action-mini" data-network-action="new-visit" data-id="${escapeHtml(c.id)}">Add visit</button></div></td></tr>`).join("")||'<tr><td colspan="5" class="network-empty">No contacts match. Add a contact to start your network.</td></tr>'}</tbody>`;
  }else{
    table.innerHTML=`<caption>${visible.length} visits · Operational records open in their original activity.</caption><thead><tr><th>Date / status</th><th>Contact person</th><th>Program / activity</th><th>Visit details</th><th>Follow-up</th><th>Actions</th></tr></thead><tbody>${visible.map(v=>`<tr><td>${escapeHtml(v.date||"—")}<small>${escapeHtml(v.time||"")}</small><span class="badge ${statusClass(v.status)}">${escapeHtml(v.status)}</span></td><td><strong>${escapeHtml(v.target)}</strong><small>${escapeHtml(networkContact(v)?.organization||"")}</small>${v.source==='operations'?'<small>Operational interaction</small>':''}</td><td>${escapeHtml(networkProgramName(v.programId))}<small>${escapeHtml(v.activity)}</small></td><td><strong>${escapeHtml(v.objective||"—")}</strong><small>${escapeHtml([v.type,v.location].filter(Boolean).join(" · "))}</small><p>${escapeHtml(v.outcome||"")}</p><small>${escapeHtml(v.notes||"")}</small>${v.evidence?`<small>Evidence: ${escapeHtml(v.evidence)}</small>`:''}</td><td>${v.followUp?`<span class="${!v.followUpCompleted&&v.status!=='Cancelled'&&v.followUp<TODAY?'network-overdue':''}">${escapeHtml(v.followUp)}</span><small>${v.status==='Cancelled'?'Cancelled':v.followUpCompleted?'Completed':'Open'}</small><p>${escapeHtml(v.followUpNotes||"")}</p>`:'—'}</td><td><button class="action-mini" data-network-action="${v.source==='operations'?'activity':'visit'}" data-id="${escapeHtml(v.id)}" data-program="${escapeHtml(v.programId)}" data-activity="${escapeHtml(v.activity)}">${v.source==='operations'?'Open activity':'Edit visit'}</button></td></tr>`).join("")||'<tr><td colspan="6" class="network-empty">No visits match. Add a visit or clear the filters.</td></tr>'}</tbody>`;
  }
}
function networkReset(prefix){for(const suffix of ["Search","Program","Activity"])document.getElementById(prefix+suffix).value="";if(prefix==="network")networkState.contactId="";prefix==="plan"?renderPlan():renderVisits()}
function networkClose(id){document.getElementById(id).classList.remove("show")}
function openNetworkContact(id=""){
  const c=networkStore().contacts.find(c=>c.id===id)||{};networkState.editingContact=c.id||"";
  document.getElementById("networkContactTitle").textContent=c.id?"Edit contact":"Add contact";
  for(const key of ["name","organization","role","email","phone","notes"])document.getElementById("contact_"+key).value=c[key]||"";
  document.getElementById("networkContactModal").classList.add("show");
}
function saveNetworkContact(event){
  event.preventDefault();const data={};for(const key of ["name","organization","role","email","phone","notes"])data[key]=document.getElementById("contact_"+key).value.trim();
  if(!data.name){toast("Enter a contact name");return}
  const existing=networkStore().contacts.find(c=>c.id===networkState.editingContact);
  if(existing)Object.assign(existing,data,{updatedAt:new Date().toISOString()});else networkStore().contacts.push({...data,id:networkId("CON"),createdAt:new Date().toISOString()});
  networkClose("networkContactModal");scheduleSave();renderVisits();renderPlan();toast("Contact saved");
}
function networkVisitActivities(){
  const programId=document.getElementById("nv_programId").value;
  networkSelect("nv_activity",networkActivities(programId).map(a=>[a,a]),"Select activity");
}
function openNetworkVisit(id="",contactId=""){
  if(!networkStore().contacts.length){toast("Add a contact before scheduling a visit");openNetworkContact();return}
  const v=networkStore().visits.find(v=>v.id===id)||{};networkState.editingVisit=v.id||"";
  document.getElementById("networkVisitForm").reset();document.getElementById("networkVisitTitle").textContent=v.id?"Edit visit":"Add visit";
  networkSelect("nv_contactId",networkStore().contacts.map(c=>[c.id,`${c.name}${c.organization?' · '+c.organization:''}`]),"Select contact");
  networkSelect("nv_programId",programs.map(p=>[p.id,p.name]),"General networking");
  const prefix=document.body.dataset.view==="plan"?"plan":"network";
  document.getElementById("nv_programId").value=v.id?(v.programId||""):document.getElementById(prefix+"Program").value;
  networkVisitActivities();
  for(const key of ["contactId","activity","date","time","status","type","location","objective","outcome","followUp","followUpNotes","notes"]){
    const fallback={contactId,activity:document.getElementById(prefix+"Activity").value,date:TODAY,status:"Upcoming",type:"Physical Location"};
    document.getElementById("nv_"+key).value=v[key]??fallback[key]??"";
  }
  document.getElementById("nv_followUpCompleted").checked=Boolean(v.followUpCompleted);
  document.getElementById("networkVisitModal").classList.add("show");
}
function saveNetworkVisit(event){
  event.preventDefault();const data={};
  for(const key of ["contactId","programId","activity","date","time","status","type","location","objective","outcome","followUp","followUpNotes","notes"])data[key]=document.getElementById("nv_"+key).value.trim();
  if(!networkStore().contacts.some(c=>c.id===data.contactId)||!data.activity||!data.date||!data.objective){toast("Choose a contact and activity, and enter a date and purpose");return}
  if(data.programId&&!programs.some(p=>p.id===data.programId)){toast("Choose an available program");return}
  if(!networkStatuses.includes(data.status))return;
  if(data.status==="Completed"&&!data.outcome){toast("Add the visit outcome before marking it completed");return}
  if(data.followUp&&data.followUp<data.date){toast("Follow-up date must be on or after the visit date");return}
  data.followUpCompleted=!data.followUp||document.getElementById("nv_followUpCompleted").checked;
  const existing=networkStore().visits.find(v=>v.id===networkState.editingVisit);
  if(existing)Object.assign(existing,data,{updatedAt:new Date().toISOString()});else networkStore().visits.push({...data,id:networkId("NETVIS"),createdAt:new Date().toISOString(),createdBy:user?.name||""});
  networkClose("networkVisitModal");scheduleSave();renderVisits();renderPlan();toast("Visit saved");
}
document.addEventListener("click",event=>{
  const button=event.target.closest("[data-network-action]");if(!button)return;
  const {networkAction:action,id,program,activity}=button.dataset;
  if(action==="contact")openNetworkContact(id);
  if(action==="visit")openNetworkVisit(id);
  if(action==="new-visit")openNetworkVisit("",id||"");
  if(action==="contact-history"){networkState.contactId=id;networkState.tab="visits";renderVisits()}
  if(action==="clear-contact"){networkState.contactId="";renderVisits()}
  if(action==="activity"){
    selectedProgramId=program;selectedActivityName=activity;selectedProgramStage="Operational Activities";setView("programworkspace");
    const details=document.querySelector("#stageDetailPanel details");if(details)details.open=true;
    document.querySelector("#stageDetailPanel .activity-editor")?.scrollIntoView({block:"start",behavior:"smooth"});
  }
});
