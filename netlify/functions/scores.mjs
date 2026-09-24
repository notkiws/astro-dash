// Shared leaderboard for DILI ORBIT.
//
//   GET  /api/scores                       -> { board: [ {n,s,k}, ... ] }   top 10
//   POST /api/scores { name, score, level } -> { board, rank }
//
// One row per pilot name, highest score kept, same rule the game uses locally.
// Storage is Netlify Blobs (part of this site, no third party). The only data kept
// is a display name, a score and a sector number: no accounts, no wallet, no
// personal data. The name is forced to A-Z0-9 and capped, and the score is range
// checked, so a bad client cannot poison the board with junk or huge numbers.
import { getStore } from "@netlify/blobs";

// Strong consistency on purpose: the default (eventual) read cache can serve a board
// that is a few seconds old, which loses scores when two players finish close together.
const STORE = () => getStore({ name: "dili-orbit-scores", consistency: "strong" });

const NAME_MAX = 8, TOP = 10, KEEP = 50, MAX_SCORE = 300000;

const cleanName = (v) => String(v == null ? "" : v).toUpperCase().replace(/[^A-Z0-9]/g, "").slice(0, NAME_MAX);

function tidy(list){
  const best = new Map();
  for(const e of list){
    if(!e || typeof e.n !== "string" || typeof e.s !== "number") continue;
    const n = cleanName(e.n);
    const s = Math.floor(e.s);
    if(!n || !Number.isFinite(s) || s <= 0) continue;
    const cur = best.get(n);
    if(!cur || s > cur.s) best.set(n, { n: n, s: s, k: Math.min(3, Math.max(1, Math.floor(e.k) || 1)) });
  }
  return Array.from(best.values()).sort((a, b) => b.s - a.s).slice(0, KEEP);
}

export default async (req) => {
  const headers = { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" };
  const store = STORE();

  if(req.method === "GET"){
    const board = tidy((await store.get("board", { type: "json" })) || []);
    return new Response(JSON.stringify({ board: board.slice(0, TOP) }), { headers });
  }

  if(req.method === "POST"){
    let body;
    try{ body = await req.json(); }
    catch(err){ return new Response(JSON.stringify({ error: "bad json" }), { status: 400, headers }); }
    const name = cleanName(body && body.name);
    const score = Math.floor(Number(body && body.score));
    const level = Math.min(3, Math.max(1, Math.floor(Number(body && body.level)) || 1));
    if(!name || !Number.isFinite(score) || score <= 0 || score > MAX_SCORE){
      return new Response(JSON.stringify({ error: "score out of range" }), { status: 400, headers });
    }
    const board = tidy(((await store.get("board", { type: "json" })) || []).concat([{ n: name, s: score, k: level }]));
    await store.setJSON("board", board.slice(0, KEEP));
    const top = board.slice(0, TOP);
    const rank = top.findIndex(e => e.n === name) + 1;
    return new Response(JSON.stringify({ board: top, rank: rank }), { headers });
  }

  return new Response(JSON.stringify({ error: "method not allowed" }), { status: 405, headers });
};

export const config = { path: "/api/scores" };
