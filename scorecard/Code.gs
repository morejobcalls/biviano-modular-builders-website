/**
 * BMB Monthly Scorecard — v3
 * Channel × Service Line matrix, repointed at "Sales (2026)" pipeline, with Needs-Triage breakdown.
 * Trigger: daily via setup(); manual: run refreshScorecard().
 */

// ---------- Config ----------
const LOCATION_ID = 'zPo4vLlEjjXCflgDSXlI';
const GHL_BASE = 'https://services.leadconnectorhq.com';
const GHL_VERSION = '2021-07-28';
const PIPELINE_NAME = 'Sales (2026)';

const FIELD_SOURCE = 'mA9Sd89sgT221rJcziHF';        // bmb_source

// Sales (2026) stage names → which scorecard row they roll up into
const STAGE_MAP = {
  meetingsBooked: ['🟡 Meeting REQUESTED', '🟢 Meeting CONFIRMED'],
  meetingsCompleted: ['✅ Meeting COMPLETED'],
  jobsWon: ['Invoiced', 'Job WON'],
  // Anything in these stages is excluded from "Pipeline $"
  lost: ['Job LOST', '🔴 Meeting CANCELLED', '🥶 Unresponsive', 'Bad Fit Deck', 'Bad Fit Modular'],
};

const CHANNELS = [
  'Meta / Facebook Ads',
  'Google Ads',
  'Google Organic',
  'Email',
  'Direct',
  'Chat widget',
  'Manual entry',
  'Other',
];
const SERVICE_LINES = ['Modular', 'Decking', 'Needs Triage'];

// Triage breakdown buckets — sub-categorize "Needs Triage" so Mike can act
const TRIAGE_BUCKETS = [
  'Custom Design booking (no service question)',
  'Manual entry (no source)',
  'Bare contact (no data)',
];

// ---------- Entry points ----------

function setup() {
  const ui = SpreadsheetApp.getUi();
  let apiKey = PropertiesService.getScriptProperties().getProperty('GHL_API_KEY');
  if (!apiKey) {
    const resp = ui.prompt('BMB Scorecard Setup', 'Paste the GHL API key:', ui.ButtonSet.OK_CANCEL);
    if (resp.getSelectedButton() !== ui.Button.OK) return;
    apiKey = (resp.getResponseText() || '').trim();
    if (!apiKey) { ui.alert('No key entered. Aborting.'); return; }
    PropertiesService.getScriptProperties().setProperty('GHL_API_KEY', apiKey);
  }
  ScriptApp.getProjectTriggers().forEach(function(t) {
    if (t.getHandlerFunction() === 'refreshScorecard') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('refreshScorecard').timeBased().everyDays(1).atHour(6).create();
  refreshScorecard();
  ui.alert('Setup complete. Daily refresh scheduled for ~6am. Dashboard populated.');
}

function refreshScorecard() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const log = getOrCreateSheet_(ss, 'Log');
  try {
    const apiKey = PropertiesService.getScriptProperties().getProperty('GHL_API_KEY');
    if (!apiKey) throw new Error('GHL_API_KEY not set in Script Properties.');

    const now = new Date();
    const curWindow = monthWindow_(now, 0);
    const prevWindow = monthWindow_(now, -1);

    const contacts = fetchContactsSince_(apiKey, prevWindow.start);
    const pipeline = findPipeline_(apiKey, PIPELINE_NAME);
    let opps = [];
    if (pipeline) opps = fetchOpportunities_(apiKey, pipeline.id);

    const curData = buildMonthData_(contacts, opps, pipeline, curWindow);
    const prevData = buildMonthData_(contacts, opps, pipeline, prevWindow);

    writeDashboard_(ss, curWindow, curData, prevWindow, prevData, !!pipeline);
    appendLog_(log, 'OK', 'Refreshed. Contacts: ' + contacts.length + ', Opps: ' + opps.length + ', Pipeline: ' + (pipeline ? 'found' : 'MISSING'));
  } catch (err) {
    appendLog_(log, 'ERROR', err && err.stack ? err.stack : String(err));
    throw err;
  }
}

// ---------- Classifiers ----------

function classifyChannel_(contact) {
  const u = getUtm_(contact);
  const src = (u.source || '').toLowerCase();
  const med = (u.medium || '').toLowerCase();
  const sourceField = (contact.source || '').toLowerCase();
  const tags = (contact.tags || []).map(function(t){ return (t || '').toLowerCase(); });

  if (['fb','facebook','ig','instagram','meta'].indexOf(src) !== -1) return 'Meta / Facebook Ads';
  if (med === 'paidsocial' || med === 'paid social' || med === 'paid_social') return 'Meta / Facebook Ads';
  if (src === 'google' && ['cpc','ppc','paid','paidsearch','paid_search'].indexOf(med) !== -1) return 'Google Ads';
  if (src === 'google') return 'Google Organic';
  if (med === 'organic') return 'Google Organic';
  if (med === 'email' || src === 'email' || sourceField.indexOf('email') !== -1) return 'Email';
  if (sourceField.indexOf('chat') !== -1) return 'Chat widget';
  if (sourceField.indexOf('manual') !== -1) return 'Manual entry';
  if (tags.indexOf('source:manual-entry') !== -1) return 'Manual entry';
  if (tags.indexOf('source:direct-booking') !== -1) return 'Direct';
  if (!src && !med && !sourceField) return 'Direct';
  // Custom Design Meeting bookings are direct calendar — count as Direct
  if (sourceField.indexOf('custom design') !== -1) return 'Direct';
  return 'Other';
}

function classifyServiceLine_(contact) {
  // 1. bmb_source set — definite modular signal
  const bmbSource = readCustomField_(contact, FIELD_SOURCE);
  if (bmbSource) return 'Modular';

  // 2. ANY bmb_* custom field set (calculator submission, survey answer, town, sqft, etc.)
  const cfs = contact.customFields || [];
  for (var i = 0; i < cfs.length; i++) {
    const cf = cfs[i];
    const k = (cf.key || cf.name || '').toLowerCase();
    // Field keys we know are modular-only
    if (k.indexOf('bmb_') === 0 && cf.value && String(cf.value).trim()) return 'Modular';
  }

  // 3. UTM/campaign/landing-page mentions
  const u = getUtm_(contact);
  const haystack = ((u.campaign || '') + ' ' + (u.term || '') + ' ' + (u.content || '') + ' ' + (u.url || '')).toLowerCase();
  if (haystack.indexOf('modular') !== -1) return 'Modular';
  if (haystack.indexOf('dream-home') !== -1) return 'Modular';
  if (haystack.indexOf('bivianomodularbuilders') !== -1) return 'Modular';
  if (haystack.indexOf('adu') !== -1) return 'Modular';
  if (haystack.indexOf('deck') !== -1) return 'Decking';

  // 4. GHL source field
  const sourceField = (contact.source || '').toLowerCase();
  if (sourceField.indexOf('modular') !== -1) return 'Modular';
  if (sourceField.indexOf('deck') !== -1) return 'Decking';

  // 5. Tags
  const tags = (contact.tags || []).map(function(t){ return (t || '').toLowerCase(); });
  for (var j = 0; j < tags.length; j++) {
    const t = tags[j];
    if (t.indexOf('lead:modular') !== -1 || t === 'modular') return 'Modular';
    if (t.indexOf('lead:decking') !== -1 || t === 'decking' || t === 'deck') return 'Decking';
  }

  return 'Needs Triage';
}

/**
 * For contacts that land in Needs Triage, sub-categorize WHY so Mike can act on each one.
 */
function classifyTriageReason_(contact) {
  const sourceField = (contact.source || '').toLowerCase();
  const tags = (contact.tags || []).map(function(t){ return (t || '').toLowerCase(); });
  if (sourceField.indexOf('custom design') !== -1) return 'Custom Design booking (no service question)';
  if (sourceField.indexOf('manual') !== -1) return 'Manual entry (no source)';
  if (tags.indexOf('source:manual-entry') !== -1) return 'Manual entry (no source)';
  if (!sourceField) return 'Bare contact (no data)';
  return 'Bare contact (no data)';
}

function getUtm_(contact) {
  var u = { source: '', medium: '', campaign: '', term: '', content: '', url: '' };
  const a = contact.attributionSource;
  if (a && typeof a === 'object') {
    u.source = u.source || a.utmSource || a.utm_source || '';
    u.medium = u.medium || a.utmMedium || a.utm_medium || '';
    u.campaign = u.campaign || a.utmCampaign || a.utm_campaign || '';
    u.term = u.term || a.utmTerm || a.utm_term || '';
    u.content = u.content || a.utmContent || a.utm_content || '';
    u.url = u.url || a.url || a.referrer || '';
  }
  const arr = contact.attributions || [];
  for (var i = 0; i < arr.length; i++) {
    const x = arr[i] || {};
    u.source = u.source || x.utmSource || x.utm_source || '';
    u.medium = u.medium || x.utmMedium || x.utm_medium || '';
    u.campaign = u.campaign || x.utmCampaign || x.utm_campaign || '';
    u.term = u.term || x.utmTerm || x.utm_term || '';
    u.content = u.content || x.utmContent || x.utm_content || '';
    u.url = u.url || x.url || x.landingPage || x.referrer || '';
  }
  return u;
}

// ---------- Data assembly ----------

function buildMonthData_(allContacts, allOpps, pipeline, win) {
  const contacts = allContacts.filter(function(c) {
    const d = parseDate_(c.dateAdded || c.createdAt || c.dateCreated);
    return d && d >= win.start && d < win.end;
  });

  // Channel × Service Line matrix
  const matrix = {};
  CHANNELS.forEach(function(ch) {
    matrix[ch] = {};
    SERVICE_LINES.forEach(function(sl) { matrix[ch][sl] = 0; });
  });

  // Triage breakdown
  const triage = {};
  TRIAGE_BUCKETS.forEach(function(b) { triage[b] = 0; });

  contacts.forEach(function(c) {
    const ch = classifyChannel_(c);
    const sl = classifyServiceLine_(c);
    if (!matrix[ch]) {
      matrix[ch] = {};
      SERVICE_LINES.forEach(function(s) { matrix[ch][s] = 0; });
    }
    matrix[ch][sl] = (matrix[ch][sl] || 0) + 1;
    if (sl === 'Needs Triage') {
      const reason = classifyTriageReason_(c);
      triage[reason] = (triage[reason] || 0) + 1;
    }
  });

  // Funnel + revenue from Sales (2026) pipeline
  let meetingsBooked = null, meetingsCompleted = null, jobsWon = null;
  let pipelineDollars = null, closedDollars = null;

  if (pipeline) {
    const stageIdByName = {};
    (pipeline.stages || []).forEach(function(st) {
      stageIdByName[(st.name || '').trim()] = st.id;
    });

    function stageIdsForGroup(groupKey) {
      const names = STAGE_MAP[groupKey] || [];
      const ids = [];
      names.forEach(function(n) {
        for (var key in stageIdByName) {
          if (key.toLowerCase().trim() === n.toLowerCase().trim()) ids.push(stageIdByName[key]);
        }
      });
      return ids;
    }

    const bookedIds = stageIdsForGroup('meetingsBooked');
    const completedIds = stageIdsForGroup('meetingsCompleted');
    const wonIds = stageIdsForGroup('jobsWon');
    const lostIds = stageIdsForGroup('lost');

    // Filter opps to those whose contact was created in this month
    const contactIds = {};
    contacts.forEach(function(c) { contactIds[c.id] = true; });

    const monthOpps = allOpps.filter(function(o) {
      const cid = o.contactId || (o.contact && o.contact.id);
      return cid && contactIds[cid];
    });

    function inGroup(o, ids) { return ids.indexOf(o.pipelineStageId || o.stageId) !== -1; }
    meetingsBooked = monthOpps.filter(function(o) { return inGroup(o, bookedIds); }).length;
    meetingsCompleted = monthOpps.filter(function(o) { return inGroup(o, completedIds); }).length;
    jobsWon = monthOpps.filter(function(o) { return inGroup(o, wonIds); }).length;

    let pipelineSum = 0, closedSum = 0;
    monthOpps.forEach(function(o) {
      const val = Number(o.monetaryValue || o.opportunityValue || 0);
      if (!val) return;
      const sid = o.pipelineStageId || o.stageId;
      if (lostIds.indexOf(sid) !== -1) return;
      pipelineSum += val;
      if (wonIds.indexOf(sid) !== -1) closedSum += val;
    });
    pipelineDollars = pipelineSum;
    closedDollars = closedSum;
  }

  return {
    matrix: matrix,
    triage: triage,
    totalLeads: contacts.length,
    meetingsBooked: meetingsBooked,
    meetingsCompleted: meetingsCompleted,
    jobsWon: jobsWon,
    pipelineDollars: pipelineDollars,
    closedDollars: closedDollars,
  };
}

// ---------- GHL API ----------

function ghlFetch_(apiKey, path, opts) {
  const url = path.indexOf('http') === 0 ? path : (GHL_BASE + path);
  const params = Object.assign({
    method: 'get',
    muteHttpExceptions: true,
    headers: {
      Authorization: 'Bearer ' + apiKey,
      Version: GHL_VERSION,
      Accept: 'application/json',
    },
  }, opts || {});
  if (params.payload && typeof params.payload !== 'string') {
    params.contentType = 'application/json';
    params.payload = JSON.stringify(params.payload);
  }
  const resp = UrlFetchApp.fetch(url, params);
  const code = resp.getResponseCode();
  const text = resp.getContentText();
  if (code >= 300) throw new Error('GHL ' + code + ' on ' + path + ': ' + text.slice(0, 500));
  return JSON.parse(text);
}

function findPipeline_(apiKey, name) {
  const res = ghlFetch_(apiKey, '/opportunities/pipelines?locationId=' + LOCATION_ID);
  const list = res.pipelines || res.data || [];
  return list.find(function(p) { return (p.name || '').toLowerCase() === name.toLowerCase(); }) || null;
}

function fetchOpportunities_(apiKey, pipelineId) {
  const all = [];
  let url = '/opportunities/search?location_id=' + LOCATION_ID + '&pipeline_id=' + pipelineId + '&limit=100';
  let safety = 0;
  while (url && safety++ < 50) {
    const res = ghlFetch_(apiKey, url);
    const batch = res.opportunities || res.data || [];
    all.push.apply(all, batch);
    const meta = res.meta || {};
    if (meta.nextPageUrl) {
      url = meta.nextPageUrl.indexOf('http') === 0 ? meta.nextPageUrl : (GHL_BASE + meta.nextPageUrl);
    } else if (meta.startAfterId && meta.startAfter) {
      url = '/opportunities/search?location_id=' + LOCATION_ID + '&pipeline_id=' + pipelineId + '&limit=100&startAfterId=' + meta.startAfterId + '&startAfter=' + meta.startAfter;
    } else {
      url = null;
    }
  }
  return all;
}

function fetchContactsSince_(apiKey, sinceDate) {
  const all = [];
  const iso = sinceDate.toISOString();
  let page = 1;
  let safety = 0;
  while (safety++ < 100) {
    const body = {
      locationId: LOCATION_ID,
      pageLimit: 100,
      page: page,
      filters: [{ field: 'dateAdded', operator: 'gte', value: iso }],
    };
    let res;
    try {
      res = ghlFetch_(apiKey, '/contacts/search', { method: 'post', payload: body });
    } catch (e) {
      return fetchContactsLegacy_(apiKey, sinceDate);
    }
    const batch = res.contacts || res.data || [];
    if (!batch.length) break;
    all.push.apply(all, batch);
    const total = res.total || (res.meta && res.meta.total);
    if (total && all.length >= total) break;
    if (batch.length < 100) break;
    page++;
  }
  // Hydrate each contact — list endpoint truncates attribution
  return all.map(function(c) {
    try {
      const full = ghlFetch_(apiKey, '/contacts/' + c.id);
      return full.contact || c;
    } catch (e) { return c; }
  });
}

function fetchContactsLegacy_(apiKey, sinceDate) {
  const all = [];
  let startAfter = null, startAfterId = null, safety = 0;
  while (safety++ < 100) {
    let url = '/contacts/?locationId=' + LOCATION_ID + '&limit=100';
    if (startAfter) url += '&startAfter=' + startAfter;
    if (startAfterId) url += '&startAfterId=' + startAfterId;
    const res = ghlFetch_(apiKey, url);
    const batch = res.contacts || res.data || [];
    if (!batch.length) break;
    all.push.apply(all, batch);
    const oldest = batch[batch.length - 1];
    const oldestDate = parseDate_(oldest.dateAdded || oldest.createdAt);
    if (oldestDate && oldestDate < sinceDate) break;
    const meta = res.meta || {};
    if (!meta.startAfter || !meta.startAfterId) break;
    startAfter = meta.startAfter;
    startAfterId = meta.startAfterId;
  }
  return all.filter(function(c) {
    const d = parseDate_(c.dateAdded || c.createdAt);
    return d && d >= sinceDate;
  });
}

function readCustomField_(contact, fieldId) {
  const arr = contact.customFields || contact.customField || [];
  const hit = arr.find(function(f) { return f.id === fieldId; });
  if (!hit) return null;
  return hit.value != null ? hit.value : (hit.fieldValue != null ? hit.fieldValue : null);
}

// ---------- Sheet writing ----------

function writeDashboard_(ss, curWin, cur, prevWin, prev, hasPipeline) {
  const sh = getOrCreateSheet_(ss, 'Dashboard');
  sh.clear();

  const curLabel = 'MONTHLY SCORECARD — ' + monthLabel_(curWin.start);
  const prevLabel = 'MONTHLY SCORECARD — ' + monthLabel_(prevWin.start);

  // Layout: cols A-E (current month), F (spacer), G-K (prev month). 11 cols total.

  const rows = [];
  rows.push([curLabel, '', '', '', '', '', prevLabel, '', '', '', '']);
  rows.push(['─'.repeat(40), '', '', '', '', '', '─'.repeat(40), '', '', '', '']);

  // Section 1 — Leads matrix
  rows.push(['Leads by Channel × Service Line', '', '', '', '', '', 'Leads by Channel × Service Line', '', '', '', '']);
  rows.push(['', 'Modular', 'Decking', 'Needs Triage', 'Total', '', '', 'Modular', 'Decking', 'Needs Triage', 'Total']);

  const totalRowCur = { Modular: 0, Decking: 0, 'Needs Triage': 0, Total: 0 };
  const totalRowPrev = { Modular: 0, Decking: 0, 'Needs Triage': 0, Total: 0 };

  CHANNELS.forEach(function(ch) {
    const cCells = SERVICE_LINES.map(function(sl) { return (cur.matrix[ch] && cur.matrix[ch][sl]) || 0; });
    const pCells = SERVICE_LINES.map(function(sl) { return (prev.matrix[ch] && prev.matrix[ch][sl]) || 0; });
    const cTot = cCells.reduce(function(a,b){ return a+b; }, 0);
    const pTot = pCells.reduce(function(a,b){ return a+b; }, 0);
    cCells.forEach(function(v,i) { totalRowCur[SERVICE_LINES[i]] += v; });
    totalRowCur.Total += cTot;
    pCells.forEach(function(v,i) { totalRowPrev[SERVICE_LINES[i]] += v; });
    totalRowPrev.Total += pTot;
    rows.push([
      '  ' + ch, cCells[0], cCells[1], cCells[2], cTot,
      '',
      '  ' + ch, pCells[0], pCells[1], pCells[2], pTot,
    ]);
  });
  rows.push([
    '  TOTAL',
    totalRowCur.Modular, totalRowCur.Decking, totalRowCur['Needs Triage'], totalRowCur.Total,
    '',
    '  TOTAL',
    totalRowPrev.Modular, totalRowPrev.Decking, totalRowPrev['Needs Triage'], totalRowPrev.Total,
  ]);

  rows.push(['', '', '', '', '', '', '', '', '', '', '']);

  // Section 2 — Triage queue breakdown
  rows.push(['Triage Queue — why these leads need follow-up', '', '', '', '', '', 'Triage Queue — why these leads need follow-up', '', '', '', '']);
  TRIAGE_BUCKETS.forEach(function(b) {
    const cN = cur.triage[b] || 0;
    const pN = prev.triage[b] || 0;
    rows.push(['  ' + b, cN, '', '', '', '', '  ' + b, pN, '', '', '']);
  });
  rows.push(['', '', '', '', '', '', '', '', '', '', '']);

  // Section 3 — Funnel (Sales 2026)
  rows.push(['Funnel — Sales (2026) pipeline', '', '', '', '', '', 'Funnel — Sales (2026) pipeline', '', '', '', '']);
  if (hasPipeline) {
    rows.push(['  Meetings Booked',    cur.meetingsBooked,    '', '', '', '', '  Meetings Booked',    prev.meetingsBooked,    '', '', '']);
    rows.push(['  Meetings Completed', cur.meetingsCompleted, '', '', '', '', '  Meetings Completed', prev.meetingsCompleted, '', '', '']);
    rows.push(['  Jobs Won',           cur.jobsWon,           '', '', '', '', '  Jobs Won',           prev.jobsWon,           '', '', '']);
  } else {
    rows.push(['  Meetings Booked',    'Sales (2026) pipeline not found', '', '', '', '', '  Meetings Booked',    'Sales (2026) pipeline not found', '', '', '']);
    rows.push(['  Meetings Completed', 'Sales (2026) pipeline not found', '', '', '', '', '  Meetings Completed', 'Sales (2026) pipeline not found', '', '', '']);
    rows.push(['  Jobs Won',           'Sales (2026) pipeline not found', '', '', '', '', '  Jobs Won',           'Sales (2026) pipeline not found', '', '', '']);
  }
  rows.push(['', '', '', '', '', '', '', '', '', '', '']);

  // Section 4 — Revenue
  rows.push(['Revenue — Sales (2026) opportunity value', '', '', '', '', '', 'Revenue — Sales (2026) opportunity value', '', '', '', '']);
  if (hasPipeline) {
    rows.push(['  Pipeline $ (active opps)', formatCurrency_(cur.pipelineDollars), '', '', '', '', '  Pipeline $ (active opps)', formatCurrency_(prev.pipelineDollars), '', '', '']);
    rows.push(['  Closed $ (Invoiced + Won)', formatCurrency_(cur.closedDollars),  '', '', '', '', '  Closed $ (Invoiced + Won)', formatCurrency_(prev.closedDollars),  '', '', '']);
  } else {
    rows.push(['  Pipeline $ (active opps)', 'Sales (2026) pipeline not found', '', '', '', '', '  Pipeline $ (active opps)', 'Sales (2026) pipeline not found', '', '', '']);
    rows.push(['  Closed $ (Invoiced + Won)', 'Sales (2026) pipeline not found', '', '', '', '', '  Closed $ (Invoiced + Won)', 'Sales (2026) pipeline not found', '', '', '']);
  }
  rows.push(['', '', '', '', '', '', '', '', '', '', '']);

  rows.push(['Last updated', new Date(), '', '', '', '', '', '', '', '', '']);

  sh.getRange(1, 1, rows.length, 11).setValues(rows);

  // Formatting — titles
  sh.getRange(1, 1, 1, 11).setFontWeight('bold').setFontSize(14);
  sh.getRange(3, 1).setFontWeight('bold');
  sh.getRange(3, 7).setFontWeight('bold');
  sh.getRange(4, 1, 1, 11).setFontWeight('bold').setBackground('#F1F3F4');

  // TOTAL row (after header rows + CHANNELS rows)
  const totalRowIdx = 4 + CHANNELS.length + 1;
  sh.getRange(totalRowIdx, 1, 1, 11).setFontWeight('bold').setBackground('#E8F0FE');

  // Sub-section header bolding
  const triageHeaderIdx = totalRowIdx + 2;
  sh.getRange(triageHeaderIdx, 1).setFontWeight('bold');
  sh.getRange(triageHeaderIdx, 7).setFontWeight('bold');

  const funnelHeaderIdx = triageHeaderIdx + TRIAGE_BUCKETS.length + 2;
  sh.getRange(funnelHeaderIdx, 1).setFontWeight('bold');
  sh.getRange(funnelHeaderIdx, 7).setFontWeight('bold');

  const revenueHeaderIdx = funnelHeaderIdx + 4;
  sh.getRange(revenueHeaderIdx, 1).setFontWeight('bold');
  sh.getRange(revenueHeaderIdx, 7).setFontWeight('bold');

  // Column widths
  sh.setColumnWidth(1, 320);
  sh.setColumnWidth(2, 95);
  sh.setColumnWidth(3, 95);
  sh.setColumnWidth(4, 110);
  sh.setColumnWidth(5, 80);
  sh.setColumnWidth(6, 30);
  sh.setColumnWidth(7, 320);
  sh.setColumnWidth(8, 95);
  sh.setColumnWidth(9, 95);
  sh.setColumnWidth(10, 110);
  sh.setColumnWidth(11, 80);

  // Right-align numeric matrix cells
  sh.getRange(5, 2, CHANNELS.length + 1, 4).setHorizontalAlignment('right');
  sh.getRange(5, 8, CHANNELS.length + 1, 4).setHorizontalAlignment('right');

  // Last updated date format
  sh.getRange(rows.length, 2).setNumberFormat('yyyy-mm-dd hh:mm:ss');
}

// ---------- Helpers ----------

function monthWindow_(ref, offset) {
  const start = new Date(ref.getFullYear(), ref.getMonth() + offset, 1, 0, 0, 0, 0);
  const end = new Date(ref.getFullYear(), ref.getMonth() + offset + 1, 1, 0, 0, 0, 0);
  return { start: start, end: end };
}
function monthLabel_(d) {
  return Utilities.formatDate(d, Session.getScriptTimeZone() || 'America/New_York', 'MMMM yyyy').toUpperCase();
}
function parseDate_(v) {
  if (!v) return null;
  if (v instanceof Date) return v;
  const d = new Date(v);
  return isNaN(d.getTime()) ? null : d;
}
function formatCurrency_(n) {
  if (n == null) return '$0';
  const abs = Math.abs(n);
  if (abs >= 1000000) return '$' + (n / 1000000).toFixed(1) + 'M';
  if (abs >= 10000) return '$' + Math.round(n / 1000) + 'K';
  return '$' + Math.round(n).toLocaleString('en-US');
}
function getOrCreateSheet_(ss, name) {
  let sh = ss.getSheetByName(name);
  if (!sh) sh = ss.insertSheet(name);
  return sh;
}
function appendLog_(sh, level, msg) {
  if (sh.getLastRow() === 0) sh.appendRow(['Timestamp', 'Level', 'Message']);
  sh.appendRow([new Date(), level, msg]);
}
