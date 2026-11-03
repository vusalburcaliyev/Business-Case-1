const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname,'../dashboard/Bank_Campaign_Dashboard.html'),'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function dashboard() {
  const elements = {};
  const mock = () => ({
    value:'', hidden:false, innerHTML:'', textContent:'', dataset:{}, handlers:{}, attributes:{},
    add(){}, addEventListener(name,fn){this.handlers[name]=fn;},
    setAttribute(name,value){this.attributes[name]=value;}
  });
  const nav = ['overview','followup'].map(page => ({...mock(),dataset:{page}}));
  const document = {
    getElementById(id){return elements[id] ??= mock();},
    querySelectorAll(){return nav;}
  };
  vm.runInNewContext(script,{document,Option:function(){}});
  return {elements,nav};
}

test('dashboard shows SQL-verified headline values and recalculates for a channel',()=>{
  const {elements:e} = dashboard();
  assert.match(e['overview-cards'].innerHTML, /45,211/);
  assert.match(e['overview-cards'].innerHTML, /5,289/);
  assert.match(e['overview-cards'].innerHTML, /11\.70%/);
  assert.match(e['overview-cards'].innerHTML, /71\.20%/);
  e.channel.value = 'Cellular';
  e.channel.handlers.change();
  assert.match(e['overview-cards'].innerHTML, /29,285/);
  assert.match(e['overview-cards'].innerHTML, /4,369/);
  assert.match(e['overview-cards'].innerHTML, /14\.92%/);
});

test('prior history filters and the page controls work',()=>{
  const {elements:e,nav} = dashboard();
  assert.match(e['followup-cards'].innerHTML, /3,064/);
  e.history.value = 'No prior contact';
  e.history.handlers.change();
  assert.match(e['history-chart'].innerHTML, /No records/);
  nav[1].handlers.click();
  assert.equal(e.overview.hidden,true);
  assert.equal(e.followup.hidden,false);
  assert.equal(nav[1].attributes['aria-pressed'],'true');
  e.reset.handlers.click();
  assert.equal(e.history.value,'');
  assert.match(e['history-chart'].innerHTML, /Outcome not recorded/);
});

test('multiple slicers use their intersection; empty rates display blank',()=>{
  const {elements:e} = dashboard();
  e.channel.value = 'Not recorded';
  e.channel.handlers.change();
  assert.match(e['overview-cards'].innerHTML, /13,020/);
  assert.match(e['overview-cards'].innerHTML, /0\.00%/);
  e.month.value = '5';
  e.history.value = 'Prior contact';
  e.history.handlers.change();
  assert.match(e['month-chart'].innerHTML, /May/);
  assert.doesNotMatch(e['month-chart'].innerHTML, /March|Aug/);
  e.month.value = '99'; // force an empty intersection
  e.month.handlers.change();
  assert.match(e['overview-cards'].innerHTML, /—/);
  assert.match(e['channel-chart'].innerHTML, /No records/);
});
