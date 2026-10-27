// Front plate rules for the "Front plates" map in Study. Edit by hand.
// k: "both" = front and rear required · "rear" = rear plate only · "mostly" = front and rear for most vehicles,
//    but a missing front plate is common or legal in some cases.
// since: year of the last change. Street View in that unit may predate it, so older coverage can show the old rule.
// Sources: Wikipedia "Vehicle license plates of the United States" and "Vehicle registration plates of Canada"
// / "of Mexico" (read 2026-10-27); RCI (2019) for New Brunswick.
window.FRONT_RULES = {
  "US": { // ---------- United States ----------
    both:   ["CA","CO","CT","DC","HI","IL","IA","ME","MD","MN","NH","NJ","NY","ND","OR","TX","VT","VA","WA","WI","VI"],
    rear:   ["AL","AK","AZ","AR","DE","FL","GA","IN","KS","KY","LA","MI","MS","NM","NC","OH","OK","PA","PR","SC","TN","UT","WV"],
    mostly: ["ID","MA","MO","MT","NE","NV","RI","SD","WY"]
  },
  "CA": { // ---------- Canada ----------
    both:   ["BC","MB","ON"],
    rear:   ["AB","SK","QC","NB","NS","PE","NL","YT","NT","NU"]
  },
  "MX": { // ---------- Mexico: every state issues a front and a rear plate ----------
    both:   ["AGU","BCN","BCS","CAM","CHP","CHH","COA","COL","DIF","DUR","GUA","GRO","HID","JAL","MEX","MIC","MOR","NAY","NLE","OAX","PUE","QUE","ROO","SLP","SIN","SON","TAB","TAM","TLA","VER","YUC","ZAC"]
  }
};
// Per-unit notes, keyed "US-OH" etc.
window.FRONT_NOTES = {
  "US-OH": { since: 2020, note: "Rear plate only since July 2020; older coverage still shows front plates." },
  "US-AK": { since: 2022, note: "One plate per vehicle since a 2022 law." },
  "US-UT": { since: 2025, note: "No front plate issued or required since 1 January 2025; most coverage predates this." },
  "US-ID": { since: 2025, note: "Since July 2025, a front plate is only required if the car has a front bracket." },
  "US-RI": { since: 2026, note: "Since June 2026, a single rear plate is allowed on cars without a front bracket." },
  "US-NE": { note: "Front plate no longer required from 1 January 2029. Also optional on cars built without a front bracket." },
  "US-NV": { note: "Two plates issued, but the front one is optional on cars without a bracket and rarely enforced." },
  "US-WY": { note: "Front plate optional on cars built without a front bracket (since 2015)." },
  "US-MT": { note: "Front plate can be skipped on cars without a bracket, with Highway Patrol approval (since 2017)." },
  "US-MA": { note: "Older green-on-white plates were issued as a single rear plate; the current base comes in pairs." },
  "US-SD": { note: "A single rear plate is available for cars driven under 7,500 miles a year." },
  "US-MO": { note: "Front and rear for cars; some trucks carry a single front plate." },
  "US-TX": { note: "Front plate required, but the fine was missing in 2012-2013, so some cars skip it." },
  "US-PR": { note: "Rear plate only." },
  "CA-NB": { since: 2019, note: "Front plate dropped in 2019; recent coverage shows a mix of cars with and without one." },
  "CA-AB": { note: "Rear plate only since 1992." },
  "CA-SK": { note: "Rear plate only since 2004." },
  "CA-QC": { note: "Rear plate only since 1979." },
  "CA-NL": { note: "Rear plate only on cars, but pickups, trucks, buses, emergency and government vehicles carry a front plate." }
};
