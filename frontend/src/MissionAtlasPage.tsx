import { lazy, Suspense, useEffect, useMemo, useState } from 'react'
import { ArrowRight, Bus, Compass, FolderOpen, LoaderCircle, MapPin, RefreshCw, Search, Sparkles, Trees, TriangleAlert } from 'lucide-react'
import { DetectiveBuddy } from './SceneLoader'
import type { DetectiveLook } from './character-look'
import type { LibraryCase } from './types'
import type { AtlasStop } from './MissionAtlasScene'

const MissionAtlasScene=lazy(()=>import('./MissionAtlasScene'))
type Props={library:LibraryCase[];look:DetectiveLook;busy:boolean;onOpenSample:(slug:string,station:'sources'|'map')=>void}
type Filter='all'|'unsolved'|'guided'
const PLACE:Record<string,{x:number;z:number;district:string;landmark:string}>= {
  'shinchan-school-fair-switcheroo':{x:-5.3,z:-2.5,district:'School Quarter',landmark:'Futaba Kindergarten'},
  'class-trip-switcheroo':{x:-3.6,z:-3.15,district:'School Quarter',landmark:'Futaba Kindergarten'},
  'shiros-lost-bell':{x:-5.5,z:1.9,district:'Pawprint Park',landmark:"Shiro's Park"},
  'action-kamen-showtime':{x:1.2,z:-3.5,district:'Festival Row',landmark:'Action Kamen Stage'},
  'scholarship-round-lab':{x:-4.7,z:2.9,district:'School Quarter',landmark:'Student Support Desk'},
  'kasukabe-flood-route':{x:-3.6,z:4.1,district:'Pawprint Park',landmark:'Riverside Shelter'},
  'festival-access-audit':{x:2.15,z:-2.35,district:'Festival Row',landmark:'Lantern Festival Grounds'},
  'rental-cost-forensics':{x:5.25,z:1.7,district:'Shopping Street',landmark:'Garden Flats'},
  'night-bus-route-audit':{x:.15,z:5.2,district:'Transit Corner',landmark:'Night Loop Stop'},
  'e-waste-drop-day':{x:5.35,z:3.4,district:'Civic Center',landmark:'Reuse Day Depot'},
  'community-microgrant':{x:-.1,z:4.95,district:'Garden Lane',landmark:'Nohara Community Garden'},
  'subscription-cancellation-case':{x:5.3,z:-.1,district:'Shopping Street',landmark:'Cloud Plus Shop'},
}
const FALLBACK=[{x:-5.3,z:-2.5,district:'School Quarter',landmark:'Futaba Kindergarten'},{x:-5.5,z:1.9,district:'Pawprint Park',landmark:"Shiro's Park"},{x:1.2,z:-3.5,district:'Festival Row',landmark:'Action Kamen Stage'},{x:5.25,z:1.7,district:'Shopping Street',landmark:'Garden Flats'},{x:.15,z:5.2,district:'Transit Corner',landmark:'Night Loop Stop'},{x:-.1,z:4.95,district:'Garden Lane',landmark:'Nohara Community Garden'}]
const titleCase=(value:string)=>value.replace(/[-_]/g,' ').replace(/\b\w/g,char=>char.toUpperCase())
function locationFor(item:LibraryCase,index:number){return PLACE[item.slug]||FALLBACK[index%FALLBACK.length]}

export default function MissionAtlasPage({library,look,busy,onOpenSample}:Props){
  const [filter,setFilter]=useState<Filter>('all');const [query,setQuery]=useState('');const [selectedSlug,setSelectedSlug]=useState<string|null>(null)
  const stops=useMemo<AtlasStop[]>(()=>library.map((item,index)=>({...item,...locationFor(item,index),order:index+1})),[library])
  const search=query.trim().toLowerCase()
  const visibleStops=useMemo(()=>stops.filter(stop=>(filter==='all'||stop.play_mode===(filter==='unsolved'?'challenge':'guided'))&&`${stop.title} ${stop.description} ${stop.question} ${stop.category} ${stop.landmark}`.toLowerCase().includes(search)),[stops,filter,search])
  useEffect(()=>{if(!visibleStops.some(stop=>stop.slug===selectedSlug))setSelectedSlug(visibleStops[0]?.slug||null)},[visibleStops,selectedSlug])
  const selected=visibleStops.find(stop=>stop.slug===selectedSlug)||null
  const unsolved=stops.filter(stop=>stop.play_mode==='challenge').length
  const jumpToRandom=()=>{if(!unsolved)return;const pool=stops.filter(stop=>stop.play_mode==='challenge');setFilter('unsolved');setQuery('');setSelectedSlug(pool[Math.floor(Math.random()*pool.length)]?.slug||null)}
  return <main className="club-page mission-atlas-page">
    <section className="club-hero atlas-hero"><div className="club-hero-copy"><div className="section-kicker"><Compass size={15}/> KASUKABE WALKABOUT · 3D FIELD MAP</div><h1>Every mystery has a place.</h1><p>Spin the neighborhood, spot a clue marker, and see where Shinchan’s next case begins. Red pins are unsolved. Blue pins are guided field trips.</p><div className="club-hero-actions"><button className="btn-primary" onClick={jumpToRandom}><Sparkles size={16}/> Surprise me with a case</button><span><b>{stops.length}</b> places to explore</span></div></div><div className="club-hero-art atlas-hero-art"><div className="club-speech"><span>SHINCHAN'S MAP TIP</span><b>Tap a pin, Junior! I hid mysteries all over Kasukabe!</b></div><DetectiveBuddy activity="welcome" look={look}/><div className="atlas-travel-stamp"><span>CLUB<br/>FIELD TRIP</span><Bus size={27}/></div></div></section>
    <div className="atlas-intro-row"><div><span className="section-kicker">THE NEIGHBORHOOD IS THE LEVEL SELECT</span><h2>Where should we patrol today?</h2><p>Choose a marker in the living 3D town or pick the same stop from the case route list.</p></div><div className="atlas-legend"><span><i className="legend-red"/> Unsolved</span><span><i className="legend-blue"/> Guided</span><span><i className="legend-yellow"/> Selected</span></div></div>
    <section className="atlas-workspace">
      <div className="atlas-map-panel"><div className="atlas-map-top"><div><span className="section-kicker"><MapPin size={13}/> INTERACTIVE TOWN MODEL</span><b>Kasuka-be! Field Atlas</b></div><span className="atlas-orbit-hint"><span>↻</span> Drag to orbit · scroll to zoom</span></div><div className="atlas-filter-row"><label className="atlas-search"><Search size={15}/><input value={query} onChange={event=>setQuery(event.target.value)} placeholder="Find a district or mystery"/></label><div className="atlas-filter-tabs">{([['all','All stops'],['unsolved','Unsolved'],['guided','Guided']] as const).map(([id,label])=><button key={id} className={filter===id?'active':''} onClick={()=>setFilter(id)}>{label}<span>{id==='all'?stops.length:id==='unsolved'?unsolved:stops.length-unsolved}</span></button>)}</div></div>
        <div className="atlas-map-stage"><Suspense fallback={<div className="atlas-scene-fallback"><LoaderCircle className="spin" size={23}/> Shinchan is unfolding the town map…</div>}><MissionAtlasScene stops={visibleStops} selectedSlug={selected?.slug||null} onSelect={setSelectedSlug}/></Suspense>{!visibleStops.length&&<div className="atlas-map-empty"><Search size={20}/><b>No mystery at this address.</b><button onClick={()=>{setQuery('');setFilter('all')}}>Show every stop</button></div>}</div>
        <div className="atlas-district-rail" aria-label="Case locations">{visibleStops.map(stop=><button key={stop.slug} className={`atlas-stop-row ${selected?.slug===stop.slug?'selected':''} ${stop.play_mode==='challenge'?'unsolved':''}`} onClick={()=>setSelectedSlug(stop.slug)}><span className="atlas-stop-number">{String(stop.order).padStart(2,'0')}</span><span className="atlas-stop-copy"><b>{stop.landmark}</b><small>{stop.title} · {stop.district}</small></span><i>{stop.play_mode==='challenge'?'LIVE CASE':'GUIDED'}</i><ArrowRight size={14}/></button>)}</div>
      </div>
      <aside className="atlas-case-panel">{selected?<><div className={`atlas-case-art ${selected.play_mode==='challenge'?'live':''}`}><div className="atlas-case-stamp">{selected.play_mode==='challenge'?'OPEN CASE':'GUIDED FILE'}</div><div className="atlas-case-building"><span>{selected.category.toLowerCase().includes('school')||selected.category.toLowerCase().includes('education')?'🏫':selected.category.toLowerCase().includes('mobility')?'🚌':selected.category.toLowerCase().includes('safety')?'🌳':selected.category.toLowerCase().includes('consumer')?'🛍️':selected.category.toLowerCase().includes('event')?'🎪':selected.category.toLowerCase().includes('civic')?'♻️':'🕵️'}</span><b>{selected.landmark}</b></div><div className="atlas-coordinates">KASUKABE DISTRICT · STOP {String(selected.order).padStart(2,'0')}</div></div><div className="atlas-case-detail"><div className="atlas-case-kicker"><span>{selected.district}</span><span className={`atlas-case-status ${selected.play_mode==='challenge'?'is-live':''}`}>{selected.play_mode==='challenge'?<><i/> UNSOLVED</>:'GUIDED'}</span></div><h2>{selected.title}</h2><p>{selected.description}</p><div className="atlas-case-question"><span>THE QUESTION</span><b>{selected.question}</b></div><div className="atlas-case-facts"><span><FolderOpen size={15}/>{selected.source_count} records</span><span><TriangleAlert size={15}/>{selected.requirement_count} checks</span><span><Trees size={15}/>{titleCase(selected.category)}</span></div><button className="btn-primary atlas-launch" disabled={busy} onClick={()=>onOpenSample(selected.slug,selected.play_mode==='challenge'?'sources':'map')}>{busy?<LoaderCircle className="spin" size={16}/>:<MapPin size={16}/>} {selected.play_mode==='challenge'?'Enter unsolved case':'Start guided patrol'} <ArrowRight size={16}/></button><small className="atlas-case-note">{selected.play_mode==='challenge'?'This file starts without an analysis. You investigate the records and submit your own verdict.':'Shinchan’s guided walkthrough and reviewed source pack are already inside.'}</small></div></>:<div className="atlas-no-case"><Compass size={30}/><h2>Pick your first stop</h2><p>Choose any pin on the map to see the case details.</p></div>}</aside>
    </section>
    <section className="atlas-shinchan-guide"><div className="atlas-guide-art"><DetectiveBuddy activity="inspect" look={look}/></div><div><span className="section-kicker">SHINCHAN'S STREET RULE</span><h3>Going somewhere? Bring your evidence along.</h3><p>A location starts a story. Inside the case, you still have to check source dates, compare the records, and decide what the evidence actually supports.</p></div><div className="atlas-guide-sign"><span>NORTH</span><b>↑</b><small>ASK THE SOURCE</small></div></section>
  </main>
}
