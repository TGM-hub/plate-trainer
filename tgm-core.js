// tgm-core.js : cœur commun de l'Atlas et des trainers (pays, tiers, liens, stats).
// Généré par build.py (Atlas) depuis countries.json : ne pas modifier à la main.
// Les copies dans les repos des trainers sont rafraîchies par build.py quand elles existent.
// Script classique (pas de module) : marche en file:// comme sur GitHub Pages.
(function (root) {
  'use strict';
  var VERSION = '2026-10-31';
  var C = {"AD":{"en":"Andorra","fr":"Andorre","continent":"EU","tier":3,"plonkit":"andorra","sv":[42.54,1.58,11]},"AE":{"en":"United Arab Emirates","fr":"Émirats arabes unis","continent":"AS","tier":2,"plonkit":"united-arab-emirates","sv":[24.34,53.98,7]},"AL":{"en":"Albania","fr":"Albanie","continent":"EU","tier":2,"plonkit":"albania","sv":[41.15,20.15,7]},"AR":{"en":"Argentina","fr":"Argentine","continent":"SA","tier":1,"plonkit":"argentina","sv":[-37.08,-63.62,4]},"AS":{"en":"American Samoa","fr":"Samoa américaines","continent":"OC","tier":3,"plonkit":null,"sv":[-14.31,-170.69,11]},"AT":{"en":"Austria","fr":"Autriche","continent":"EU","tier":2,"plonkit":"austria","sv":[47.7,13.34,7]},"AU":{"en":"Australia","fr":"Australie","continent":"OC","tier":1,"plonkit":"australia","sv":[-24.93,133.4,4]},"AX":{"en":"Åland Islands","fr":"Åland","continent":"EU","tier":3,"plonkit":null,"sv":[60.21,20.06,9]},"BA":{"en":"Bosnia & Herzegovina","fr":"Bosnie-Herzégovine","continent":"EU","tier":3,"plonkit":null,"sv":[43.92,17.66,7]},"BD":{"en":"Bangladesh","fr":"Bangladesh","continent":"AS","tier":2,"plonkit":"bangladesh","sv":[23.68,90.33,6]},"BE":{"en":"Belgium","fr":"Belgique","continent":"EU","tier":2,"plonkit":"belgium","sv":[50.5,4.44,8]},"BG":{"en":"Bulgaria","fr":"Bulgarie","continent":"EU","tier":2,"plonkit":"bulgaria","sv":[42.74,25.46,7]},"BM":{"en":"Bermuda","fr":"Bermudes","continent":"NA","tier":3,"plonkit":"bermuda","sv":[32.32,-64.77,12]},"BO":{"en":"Bolivia","fr":"Bolivie","continent":"SA","tier":2,"plonkit":"bolivia","sv":[-16.3,-63.57,5]},"BR":{"en":"Brazil","fr":"Brésil","continent":"SA","tier":1,"plonkit":"brazil","sv":[-14.24,-54.4,4]},"BT":{"en":"Bhutan","fr":"Bhoutan","continent":"AS","tier":3,"plonkit":"bhutan","sv":[27.51,90.41,8]},"BW":{"en":"Botswana","fr":"Botswana","continent":"AF","tier":2,"plonkit":"botswana","sv":[-22.32,24.67,6]},"BY":{"en":"Belarus","fr":"Biélorussie","continent":"EU","tier":4,"plonkit":"belarus","sv":[53.71,27.94,6]},"CA":{"en":"Canada","fr":"Canada","continent":"NA","tier":1,"plonkit":"canada","sv":[56,-96,3]},"CC":{"en":"Cocos (Keeling) Islands","fr":"Îles Cocos","continent":"AS","tier":3,"plonkit":null,"sv":[-12.17,96.84,12]},"CH":{"en":"Switzerland","fr":"Suisse","continent":"EU","tier":2,"plonkit":"switzerland","sv":[46.8,8.21,7]},"CL":{"en":"Chile","fr":"Chili","continent":"SA","tier":1,"plonkit":"chile","sv":[-36.21,-71.36,4]},"CN":{"en":"China","fr":"Chine","continent":"AS","tier":4,"plonkit":"china","sv":[36.91,104.18,4]},"CO":{"en":"Colombia","fr":"Colombie","continent":"SA","tier":1,"plonkit":"colombia","sv":[4.1,-72.95,5]},"CR":{"en":"Costa Rica","fr":"Costa Rica","continent":"NA","tier":4,"plonkit":"costa-rica","sv":[9.63,-84.24,7]},"CW":{"en":"Curaçao","fr":"Curaçao","continent":"NA","tier":3,"plonkit":"curacao","sv":[12.21,-68.96,10]},"CX":{"en":"Christmas Island","fr":"Île Christmas","continent":"OC","tier":3,"plonkit":null,"sv":[-10.49,105.63,12]},"CY":{"en":"Cyprus","fr":"Chypre","continent":"EU","tier":3,"plonkit":"cyprus","sv":[34.88,33.18,9]},"CZ":{"en":"Czechia","fr":"Tchéquie","continent":"EU","tier":2,"plonkit":"czechia","sv":[49.81,15.46,7]},"DE":{"en":"Germany","fr":"Allemagne","continent":"EU","tier":1,"plonkit":"germany","sv":[51.09,10.44,6]},"DK":{"en":"Denmark","fr":"Danemark","continent":"EU","tier":2,"plonkit":"denmark","sv":[56.18,10.36,7]},"DO":{"en":"Dominican Republic","fr":"République dominicaine","continent":"NA","tier":2,"plonkit":"dominican-republic","sv":[18.77,-70.17,8]},"EC":{"en":"Ecuador","fr":"Équateur","continent":"SA","tier":2,"plonkit":"ecuador","sv":[-1.77,-78.11,6]},"EE":{"en":"Estonia","fr":"Estonie","continent":"EU","tier":2,"plonkit":"estonia","sv":[58.58,25,7]},"EG":{"en":"Egypt","fr":"Égypte","continent":"AF","tier":4,"plonkit":"egypt","sv":[26.82,30.79,6]},"ES":{"en":"Spain","fr":"Espagne","continent":"EU","tier":1,"plonkit":"spain","sv":[39.9,-2.96,6]},"FI":{"en":"Finland","fr":"Finlande","continent":"EU","tier":1,"plonkit":"finland","sv":[64.94,26.08,5]},"FK":{"en":"Falkland Islands","fr":"Îles Malouines","continent":"SA","tier":4,"plonkit":"falkland-islands","sv":[-51.79,-59.47,8]},"FO":{"en":"Faroe Islands","fr":"Îles Féroé","continent":"EU","tier":3,"plonkit":"faroe-islands","sv":[61.88,-6.91,9]},"FR":{"en":"France","fr":"France","continent":"EU","tier":1,"plonkit":"france","sv":[46.72,1.69,6]},"GB":{"en":"United Kingdom","fr":"Royaume-Uni","continent":"EU","tier":1,"plonkit":"united-kingdom","sv":[54.34,-3.2,6]},"GE":{"en":"Georgia","fr":"Géorgie","continent":"EU","tier":3,"plonkit":null,"sv":[42.32,43.32,7]},"GH":{"en":"Ghana","fr":"Ghana","continent":"AF","tier":2,"plonkit":"ghana","sv":[7.96,-1.03,6]},"GI":{"en":"Gibraltar","fr":"Gibraltar","continent":"EU","tier":3,"plonkit":"gibraltar","sv":[36.14,-5.35,13]},"GL":{"en":"Greenland","fr":"Groenland","continent":"NA","tier":3,"plonkit":"greenland","sv":[71.71,-42.12,4]},"GR":{"en":"Greece","fr":"Grèce","continent":"EU","tier":2,"plonkit":"greece","sv":[38.34,23.31,6]},"GS":{"en":"South Georgia & South Sandwich Islands","fr":"Géorgie du Sud-et-les Îles Sandwich du Sud","continent":"SA","tier":4,"plonkit":"south-georgia","sv":[-54.43,-36.91,8]},"GT":{"en":"Guatemala","fr":"Guatemala","continent":"NA","tier":2,"plonkit":"guatemala","sv":[15.78,-90.23,7]},"GU":{"en":"Guam","fr":"Guam","continent":"OC","tier":3,"plonkit":null,"sv":[13.44,144.79,10]},"HK":{"en":"Hong Kong SAR China","fr":"R.A.S. chinoise de Hong Kong","continent":"AS","tier":3,"plonkit":"hong-kong","sv":[22.38,114.09,10]},"HR":{"en":"Croatia","fr":"Croatie","continent":"EU","tier":2,"plonkit":"croatia","sv":[44.74,16.46,7]},"HU":{"en":"Hungary","fr":"Hongrie","continent":"EU","tier":2,"plonkit":"hungary","sv":[47.15,19.49,7]},"ID":{"en":"Indonesia","fr":"Indonésie","continent":"AS","tier":1,"plonkit":"indonesia","sv":[-1.74,118.09,4]},"IE":{"en":"Ireland","fr":"Irlande","continent":"EU","tier":2,"plonkit":"ireland","sv":[53.42,-8.21,7]},"IL":{"en":"Israel","fr":"Israël","continent":"AS","tier":2,"plonkit":"israel","sv":[31.46,35.08,7]},"IM":{"en":"Isle of Man","fr":"Île de Man","continent":"EU","tier":3,"plonkit":"isle-of-man","sv":[54.23,-4.56,10]},"IN":{"en":"India","fr":"Inde","continent":"AS","tier":1,"plonkit":"india","sv":[21.79,82.75,4]},"IO":{"en":"British Indian Ocean Territory","fr":"Territoire britannique de l’océan Indien","continent":"AS","tier":4,"plonkit":"british-indian-ocean-territory","sv":[-7.33,72.42,11]},"IQ":{"en":"Iraq","fr":"Irak","continent":"AS","tier":4,"plonkit":"iraq","sv":[33.22,43.66,6]},"IS":{"en":"Iceland","fr":"Islande","continent":"EU","tier":2,"plonkit":"iceland","sv":[64.97,-19.02,6]},"IT":{"en":"Italy","fr":"Italie","continent":"EU","tier":1,"plonkit":"italy","sv":[41.89,12.56,5]},"JE":{"en":"Jersey","fr":"Jersey","continent":"EU","tier":3,"plonkit":"jersey","sv":[49.22,-2.12,12]},"JO":{"en":"Jordan","fr":"Jordanie","continent":"AS","tier":2,"plonkit":"jordan","sv":[31.28,37.12,7]},"JP":{"en":"Japan","fr":"Japon","continent":"AS","tier":1,"plonkit":"japan","sv":[38.26,137.71,5]},"KE":{"en":"Kenya","fr":"Kenya","continent":"AF","tier":2,"plonkit":"kenya","sv":[0.4,37.89,5]},"KG":{"en":"Kyrgyzstan","fr":"Kirghizstan","continent":"AS","tier":2,"plonkit":"kyrgyzstan","sv":[41.22,74.74,6]},"KH":{"en":"Cambodia","fr":"Cambodge","continent":"AS","tier":2,"plonkit":"cambodia","sv":[12.56,104.96,7]},"KR":{"en":"South Korea","fr":"Corée du Sud","continent":"AS","tier":1,"plonkit":"south-korea","sv":[36.47,127.87,7]},"KZ":{"en":"Kazakhstan","fr":"Kazakhstan","continent":"AS","tier":2,"plonkit":"kazakhstan","sv":[48,66.97,4]},"LA":{"en":"Laos","fr":"Laos","continent":"AS","tier":2,"plonkit":"laos","sv":[18.21,103.88,6]},"LB":{"en":"Lebanon","fr":"Liban","continent":"AS","tier":3,"plonkit":"lebanon","sv":[33.88,35.85,8]},"LI":{"en":"Liechtenstein","fr":"Liechtenstein","continent":"EU","tier":3,"plonkit":"liechtenstein","sv":[47.16,9.55,11]},"LK":{"en":"Sri Lanka","fr":"Sri Lanka","continent":"AS","tier":2,"plonkit":"sri-lanka","sv":[7.88,80.79,7]},"LS":{"en":"Lesotho","fr":"Lesotho","continent":"AF","tier":3,"plonkit":"lesotho","sv":[-29.61,28.22,8]},"LT":{"en":"Lithuania","fr":"Lituanie","continent":"EU","tier":2,"plonkit":"lithuania","sv":[55.15,23.91,7]},"LU":{"en":"Luxembourg","fr":"Luxembourg","continent":"EU","tier":3,"plonkit":"luxembourg","sv":[49.81,6.11,9]},"LV":{"en":"Latvia","fr":"Lettonie","continent":"EU","tier":2,"plonkit":"latvia","sv":[56.87,24.61,7]},"MC":{"en":"Monaco","fr":"Monaco","continent":"EU","tier":3,"plonkit":"monaco","sv":[43.75,7.41,13]},"ME":{"en":"Montenegro","fr":"Monténégro","continent":"EU","tier":2,"plonkit":"montenegro","sv":[42.71,19.39,8]},"MG":{"en":"Madagascar","fr":"Madagascar","continent":"AF","tier":3,"plonkit":"madagascar","sv":[-18.83,46.87,5]},"MK":{"en":"North Macedonia","fr":"Macédoine du Nord","continent":"EU","tier":2,"plonkit":"north-macedonia","sv":[41.6,21.73,8]},"ML":{"en":"Mali","fr":"Mali","continent":"AF","tier":4,"plonkit":"mali","sv":[17.57,-4.02,5]},"MN":{"en":"Mongolia","fr":"Mongolie","continent":"AS","tier":2,"plonkit":"mongolia","sv":[46.86,103.82,4]},"MO":{"en":"Macao SAR China","fr":"R.A.S. chinoise de Macao","continent":"AS","tier":3,"plonkit":"macau","sv":[22.22,113.51,13]},"MP":{"en":"Northern Mariana Islands","fr":"Îles Mariannes du Nord","continent":"OC","tier":3,"plonkit":null,"sv":[15.25,145.49,8]},"MQ":{"en":"Martinique","fr":"Martinique","continent":"NA","tier":4,"plonkit":"martinique","sv":[14.64,-61.02,10]},"MT":{"en":"Malta","fr":"Malte","continent":"EU","tier":3,"plonkit":"malta","sv":[35.95,14.37,11]},"MX":{"en":"Mexico","fr":"Mexique","continent":"NA","tier":1,"plonkit":"mexico","sv":[23.63,-101.95,5]},"MY":{"en":"Malaysia","fr":"Malaisie","continent":"AS","tier":1,"plonkit":"malaysia","sv":[3.93,109.69,5]},"NA":{"en":"Namibia","fr":"Namibie","continent":"AF","tier":4,"plonkit":"namibia","sv":[-22.95,18.49,5]},"NG":{"en":"Nigeria","fr":"Nigeria","continent":"AF","tier":2,"plonkit":"nigeria","sv":[9.08,8.66,6]},"NL":{"en":"Netherlands","fr":"Pays-Bas","continent":"EU","tier":2,"plonkit":"netherlands","sv":[52.1,5.32,7]},"NO":{"en":"Norway","fr":"Norvège","continent":"EU","tier":1,"plonkit":"norway","sv":[64.5,13,5]},"NP":{"en":"Nepal","fr":"Népal","continent":"AS","tier":4,"plonkit":"nepal","sv":[28.37,84.11,6]},"NZ":{"en":"New Zealand","fr":"Nouvelle-Zélande","continent":"OC","tier":1,"plonkit":"new-zealand","sv":[-40.53,172.51,5]},"OM":{"en":"Oman","fr":"Oman","continent":"AS","tier":4,"plonkit":"oman","sv":[20.81,55.91,6]},"PA":{"en":"Panama","fr":"Panama","continent":"NA","tier":2,"plonkit":"panama","sv":[8.41,-80.11,7]},"PE":{"en":"Peru","fr":"Pérou","continent":"SA","tier":1,"plonkit":"peru","sv":[-9.19,-75.01,5]},"PH":{"en":"Philippines","fr":"Philippines","continent":"AS","tier":1,"plonkit":"philippines","sv":[12.11,121.91,5]},"PK":{"en":"Pakistan","fr":"Pakistan","continent":"AS","tier":4,"plonkit":"pakistan","sv":[30.39,68.95,5]},"PL":{"en":"Poland","fr":"Pologne","continent":"EU","tier":1,"plonkit":"poland","sv":[51.93,19.12,6]},"PM":{"en":"St. Pierre & Miquelon","fr":"Saint-Pierre-et-Miquelon","continent":"NA","tier":4,"plonkit":"saint-pierre-and-miquelon","sv":[46.93,-56.26,10]},"PN":{"en":"Pitcairn Islands","fr":"Îles Pitcairn","continent":"OC","tier":4,"plonkit":"pitcairn-islands","sv":[-24.37,-128.32,12]},"PR":{"en":"Puerto Rico","fr":"Porto Rico","continent":"NA","tier":2,"plonkit":"puerto-rico","sv":[18.23,-66.44,9]},"PS":{"en":"Palestinian Territories","fr":"Territoires palestiniens","continent":"AS","tier":3,"plonkit":null,"sv":[31.87,34.89,8]},"PT":{"en":"Portugal","fr":"Portugal","continent":"EU","tier":2,"plonkit":"portugal","sv":[39.57,-7.85,6]},"PY":{"en":"Paraguay","fr":"Paraguay","continent":"SA","tier":4,"plonkit":null,"sv":[-23.42,-58.45,6]},"QA":{"en":"Qatar","fr":"Qatar","continent":"AS","tier":3,"plonkit":"qatar","sv":[25.36,51.18,8]},"RE":{"en":"Réunion","fr":"La Réunion","continent":"AF","tier":3,"plonkit":"reunion","sv":[-21.13,55.53,10]},"RO":{"en":"Romania","fr":"Roumanie","continent":"EU","tier":1,"plonkit":"romania","sv":[45.97,24.97,6]},"RS":{"en":"Serbia","fr":"Serbie","continent":"EU","tier":2,"plonkit":"serbia","sv":[44.21,20.91,7]},"RU":{"en":"Russia","fr":"Russie","continent":"EU","tier":1,"plonkit":"russia","sv":[61,96,3]},"RW":{"en":"Rwanda","fr":"Rwanda","continent":"AF","tier":3,"plonkit":"rwanda","sv":[-1.94,29.87,8]},"SE":{"en":"Sweden","fr":"Suède","continent":"EU","tier":1,"plonkit":"sweden","sv":[62.19,17.65,5]},"SG":{"en":"Singapore","fr":"Singapour","continent":"AS","tier":3,"plonkit":"singapore","sv":[1.36,103.82,11]},"SI":{"en":"Slovenia","fr":"Slovénie","continent":"EU","tier":2,"plonkit":"slovenia","sv":[46.15,14.95,8]},"SJ":{"en":"Svalbard & Jan Mayen","fr":"Svalbard et Jan Mayen","continent":"EU","tier":4,"plonkit":"svalbard","sv":[78.4,16,8]},"SK":{"en":"Slovakia","fr":"Slovaquie","continent":"EU","tier":2,"plonkit":"slovakia","sv":[48.68,19.7,7]},"SM":{"en":"San Marino","fr":"Saint-Marin","continent":"EU","tier":3,"plonkit":"san-marino","sv":[43.94,12.46,12]},"SN":{"en":"Senegal","fr":"Sénégal","continent":"AF","tier":2,"plonkit":"senegal","sv":[14.5,-14.46,7]},"ST":{"en":"São Tomé & Príncipe","fr":"Sao Tomé-et-Principe","continent":"AF","tier":4,"plonkit":"sao-tome-and-principe","sv":[0.87,6.96,8]},"SZ":{"en":"Eswatini","fr":"Eswatini","continent":"AF","tier":3,"plonkit":"eswatini","sv":[-26.53,31.45,8]},"TH":{"en":"Thailand","fr":"Thaïlande","continent":"AS","tier":1,"plonkit":"thailand","sv":[13.03,101.51,5]},"TN":{"en":"Tunisia","fr":"Tunisie","continent":"AF","tier":2,"plonkit":"tunisia","sv":[33.78,9.52,6]},"TR":{"en":"Türkiye","fr":"Turquie","continent":"AS","tier":1,"plonkit":"turkey","sv":[38.96,35.43,5]},"TW":{"en":"Taiwan","fr":"Taïwan","continent":"AS","tier":2,"plonkit":"taiwan","sv":[23.6,121,7]},"TZ":{"en":"Tanzania","fr":"Tanzanie","continent":"AF","tier":4,"plonkit":"tanzania","sv":[-6.35,34.89,5]},"UA":{"en":"Ukraine","fr":"Ukraine","continent":"EU","tier":1,"plonkit":"ukraine","sv":[48.79,31.13,5]},"UG":{"en":"Uganda","fr":"Ouganda","continent":"AF","tier":2,"plonkit":"uganda","sv":[1.38,32.27,6]},"UM":{"en":"U.S. Outlying Islands","fr":"Îles mineures éloignées des États-Unis","continent":"OC","tier":4,"plonkit":"us-minor-outlying-islands","sv":null},"US":{"en":"United States","fr":"États-Unis","continent":"NA","tier":1,"plonkit":"united-states","sv":[39.5,-98.5,4]},"UY":{"en":"Uruguay","fr":"Uruguay","continent":"SA","tier":2,"plonkit":"uruguay","sv":[-32.52,-55.78,7]},"VI":{"en":"U.S. Virgin Islands","fr":"Îles Vierges des États-Unis","continent":"NA","tier":3,"plonkit":"us-virgin-islands","sv":[18.04,-64.8,9]},"VN":{"en":"Vietnam","fr":"Viêt Nam","continent":"AS","tier":2,"plonkit":"vietnam","sv":[15.96,105.79,5]},"VU":{"en":"Vanuatu","fr":"Vanuatu","continent":"OC","tier":4,"plonkit":"vanuatu","sv":[-16.98,168.21,6]},"ZA":{"en":"South Africa","fr":"Afrique du Sud","continent":"AF","tier":1,"plonkit":"south-africa","sv":[-28.47,24.67,5]}};
  var CONTINENTS = { EU: { fr: 'Europe', en: 'Europe' }, AS: { fr: 'Asie', en: 'Asia' }, AF: { fr: 'Afrique', en: 'Africa' },
    NA: { fr: 'Amérique du Nord', en: 'North America' }, SA: { fr: 'Amérique du Sud', en: 'South America' }, OC: { fr: 'Océanie', en: 'Oceania' } };
  var TIER_NAMES = { 1: { fr: 'Courant', en: 'Common' }, 2: { fr: 'Régulier', en: 'Regular' }, 3: { fr: 'Rare', en: 'Rare' }, 4: { fr: 'Très rare', en: 'Very rare' } };

  function lsGet(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function up(iso) { return String(iso || '').toUpperCase(); }
  function num(v) { return typeof v === 'number' && isFinite(v) ? v : null; }

  var intl = {};
  function intlName(iso, lang) {
    try { intl[lang] = intl[lang] || new Intl.DisplayNames([lang], { type: 'region' }); return intl[lang].of(iso); } catch (e) { return iso; }
  }

  // ---------------------------------------------------------------- pays
  function country(iso) { return C[up(iso)] || null; }
  function tierDefault(iso) { var c = country(iso); return c ? c.tier : 4; }
  // Les réglages de tier faits dans City Placer (cp.prefs.tierOv) s'appliquent partout
  function tier(iso) {
    var ov = (lsGet('cp.prefs', {}) || {}).tierOv || {};
    var t = +ov[up(iso)];
    return t >= 1 && t <= 4 ? t : tierDefault(iso);
  }
  function name(iso, lang) {
    lang = lang || 'fr';
    var c = country(iso);
    return (c && (c[lang] || c.en)) || intlName(up(iso), lang);
  }
  function flag(iso) {
    iso = up(iso);
    return /^[A-Z]{2}$/.test(iso) ? String.fromCodePoint(0x1F1A5 + iso.charCodeAt(0), 0x1F1A5 + iso.charCodeAt(1)) : '';
  }
  function plonkitUrl(iso) { var c = country(iso); return c && c.plonkit ? 'https://www.plonkit.net/' + c.plonkit : null; }
  // Google Maps avec le calque de couverture Street View
  function svUrl(iso) { var c = country(iso), s = c && c.sv; return s ? 'https://www.google.com/maps/@' + s[0] + ',' + s[1] + ',' + s[2] + 'z/data=!5m1!1e5' : null; }
  function topoUrl(iso) { var c = country(iso), s = c && c.sv; return s ? 'https://opentopomap.org/#map=' + s[2] + '/' + s[0] + '/' + s[1] : null; }
  function isos(filter) {
    var all = Object.keys(C);
    return typeof filter === 'function' ? all.filter(function (k) { return filter(C[k], k); }) : all;
  }

  // ---------------------------------------------------------------- stats communes
  // localStorage tgm.stats.<app> = { app, v, updatedAt, seen, correct, total, practiced, mastered, weak, due, byCountry }
  //   seen / correct : réponses données / justes (toutes sessions)
  //   total : éléments à apprendre ; practiced : déjà vus ; mastered : acquis ; weak : dernière réponse fausse ;
  //   due : à revoir (null si le trainer n'a pas de répétition espacée)
  //   byCountry : { ISO: { seen, correct, total?, practiced?, mastered?, weak? } }
  // Chaque trainer garde ses propres clés : ce résumé est un instantané qu'il réécrit après chaque réponse.
  var FIELDS = ['seen', 'correct', 'total', 'practiced', 'mastered', 'weak', 'due'];
  var PREFIX = 'tgm.stats.';
  function clean(o) {
    var r = {};
    FIELDS.forEach(function (f) { r[f] = num(o && o[f]); });
    return r;
  }
  var stats = {
    key: function (app) { return PREFIX + app; },
    read: function (app) { return lsGet(PREFIX + app, null); },
    write: function (app, s) {
      var out = clean(s);
      out.app = app; out.v = 1; out.updatedAt = new Date().toISOString();
      out.byCountry = {};
      var bc = (s && s.byCountry) || {};
      Object.keys(bc).forEach(function (k) {
        var iso = up(k), x = clean(bc[k]), y = {};
        if (!/^[A-Z]{2}$/.test(iso)) return;
        FIELDS.forEach(function (f) { if (x[f] != null) y[f] = x[f]; });
        out.byCountry[iso] = y;
      });
      return lsSet(PREFIX + app, out) ? out : null;
    },
    all: function () {
      var r = {};
      try {
        for (var i = 0; i < localStorage.length; i++) {
          var k = localStorage.key(i);
          if (k && k.indexOf(PREFIX) === 0) { var v = lsGet(k, null); if (v) r[k.slice(PREFIX.length)] = v; }
        }
      } catch (e) {}
      return r;
    },
    // Résume un historique Leitner {clé: [vus, justes, boîte, ...]} ; isoOf(clé) donne le pays (ou null)
    fromLeitner: function (hist, isoOf, opts) {
      opts = opts || {};
      var mastBox = opts.masteredBox || 4, s = { seen: 0, correct: 0, practiced: 0, mastered: 0, weak: 0, byCountry: {} };
      Object.keys(hist || {}).forEach(function (k) {
        var h = hist[k];
        if (!Array.isArray(h) || !h[0]) return;
        var iso = isoOf ? isoOf(k) : null, c = null;
        if (iso) c = s.byCountry[iso] = s.byCountry[iso] || { seen: 0, correct: 0, practiced: 0, mastered: 0, weak: 0 };
        var m = (h[2] || 0) >= mastBox ? 1 : 0, w = (h[2] || 0) === 0 ? 1 : 0;
        [s, c].forEach(function (o) { if (!o) return; o.seen += h[0]; o.correct += h[1] || 0; o.practiced++; o.mastered += m; o.weak += w; });
      });
      return s;
    },
  };

  root.TGM = {
    version: VERSION, countries: C, continents: CONTINENTS, tierNames: TIER_NAMES,
    country: country, has: function (iso) { return !!country(iso); }, isos: isos,
    tier: tier, tierDefault: tierDefault, name: name, flag: flag, continent: function (iso) { var c = country(iso); return c ? c.continent : null; },
    plonkitUrl: plonkitUrl, svUrl: svUrl, topoUrl: topoUrl,
    stats: stats,
  };
})(typeof window !== 'undefined' ? window : this);
