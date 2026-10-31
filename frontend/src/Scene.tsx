import { Suspense, useEffect, useMemo, useRef, useState } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { ContactShadows, Float, Html, OrbitControls } from '@react-three/drei'
import { LoaderCircle } from 'lucide-react'
import * as THREE from 'three'
import type { Finding, RequirementCoverage, Source, Task } from './types'
import { LOOK_PALETTE, type DetectiveLook } from './character-look'

export type EvidenceNode = { kind: 'source' | 'finding' | 'requirement' | 'task'; id: string }
type Pick = EvidenceNode
type Props = { sources?: Source[]; findings?: Finding[]; coverage?: RequirementCoverage[]; tasks?:Task[]; onSelect?: (pick: Pick) => void; selectedNode?:EvidenceNode|null; compact?: boolean; look?: DetectiveLook }
export type DetectiveActivity = 'welcome' | 'read' | 'inspect' | 'compare' | 'plan' | 'brief' | 'celebrate'

function Shinchan({ activity = 'inspect', animated = true, look = 'classic' }: { activity?: DetectiveActivity; animated?: boolean; look?: DetectiveLook }) {
  const whole = useRef<THREE.Group>(null)
  const rightArm = useRef<THREE.Group>(null)
  const leftArm = useRef<THREE.Group>(null)
  const head = useRef<THREE.Group>(null)
  const eyes = useRef<THREE.Mesh>(null)
  useFrame(({ clock }) => {
    const t = animated ? clock.getElapsedTime() : 0
    const hop = activity === 'celebrate' ? Math.max(0, Math.sin(t * 3.8)) * .2 : activity === 'welcome' ? Math.sin(t * 1.5) * .045 : Math.sin(t * 1.5) * .026
    if (whole.current) whole.current.position.y = hop
    if (rightArm.current) {
      const move = activity === 'welcome' ? -.34 + Math.sin(t * 2.2) * .22
        : activity === 'read' ? -.95 + Math.sin(t * 1.4) * .06
        : activity === 'compare' || activity === 'inspect' ? -.1 + Math.sin(t * 1.1) * .1
        : activity === 'plan' ? -.42 + Math.sin(t * 3.2) * .12
        : activity === 'brief' ? -.56 + Math.sin(t * 1.6) * .05
        : -.28 + Math.sin(t * 4) * .3
      rightArm.current.rotation.z = move
    }
    if (leftArm.current) {
      leftArm.current.rotation.z = activity === 'read' ? .68 + Math.sin(t * 1.4) * .05
        : activity === 'plan' ? .72 + Math.sin(t * 3.1) * .1
        : activity === 'compare' || activity === 'inspect' ? .22 + Math.sin(t * 1.5) * .08
        : activity === 'brief' ? .42
        : activity === 'celebrate' ? .48 - Math.sin(t * 4) * .28
        : .42
    }
    if (head.current) head.current.rotation.y = (activity === 'inspect' || activity === 'compare' ? Math.sin(t * .8) * .13 : activity === 'read' ? Math.sin(t * .7) * .06 : 0)
    if (eyes.current) {
      const blink = Math.sin(t * 0.62) > 0.985 ? 0.18 : 1
      eyes.current.scale.y = THREE.MathUtils.lerp(eyes.current.scale.y, blink, 0.55)
    }
  })
  const skin = '#f2bd98'
  const outfit = LOOK_PALETTE[look]
  return <group ref={whole} position={[0, 0, 0]}>
    {/* legs and signature yellow shorts */}
    <mesh position={[-.18,.52,0]} castShadow><capsuleGeometry args={[.13,.22,4,8]}/><meshStandardMaterial color={skin}/></mesh>
    <mesh position={[.18,.52,0]} castShadow><capsuleGeometry args={[.13,.22,4,8]}/><meshStandardMaterial color={skin}/></mesh>
    <mesh position={[0,.83,0]} castShadow><boxGeometry args={[.58,.38,.43]}/><meshStandardMaterial color={outfit.shorts} roughness={.72}/></mesh>
    {look==='action-kamen'&&<mesh position={[0,1.1,-.29]} rotation={[0,Math.PI/4,0]} castShadow><cylinderGeometry args={[.08,.43,.78,4,1,true]}/><meshStandardMaterial color="#df4439" side={THREE.DoubleSide} roughness={.72}/></mesh>}
    {/* red shirt */}
    <mesh position={[0,1.25,0]} castShadow><capsuleGeometry args={[.34,.52,5,12]}/><meshStandardMaterial color={outfit.shirt} roughness={.72}/></mesh>
    {/* little arms */}
    <group ref={rightArm} position={[.31,1.42,0]}>
      <mesh position={[.16,-.17,0]} rotation={[0,0,-.42]} castShadow><capsuleGeometry args={[.105,.37,4,8]}/><meshStandardMaterial color={outfit.shirt}/></mesh>
      <mesh position={[.28,-.36,0]} castShadow><sphereGeometry args={[.115,12,10]}/><meshStandardMaterial color={skin}/></mesh>
    </group>
    <group ref={leftArm} position={[-.3,1.42,0]} rotation={[0,0,.42]}>
      <mesh position={[-.13,-.19,0]} castShadow><capsuleGeometry args={[.1,.34,4,8]}/><meshStandardMaterial color={outfit.shirt}/></mesh>
      <mesh position={[-.2,-.37,0]} castShadow><sphereGeometry args={[.105,12,10]}/><meshStandardMaterial color={skin}/></mesh>
    </group>
    {/* oversized round head */}
    <group ref={head} position={[0,2.04,0]}>
    <group position={[0,-2.04,0]}>
    <mesh position={[0,2.04,0]} castShadow><sphereGeometry args={[.65,32,24]}/><meshStandardMaterial color={skin} roughness={.82}/></mesh>
    {/* ears */}
    <mesh position={[-.61,2.0,0]} castShadow><sphereGeometry args={[.15,16,12]}/><meshStandardMaterial color={skin}/></mesh>
    <mesh position={[.61,2.0,0]} castShadow><sphereGeometry args={[.15,16,12]}/><meshStandardMaterial color={skin}/></mesh>
    {/* iconic black cap and five spikes */}
    <mesh position={[0,2.48,-.02]} scale={[1.02,.48,.91]} castShadow><sphereGeometry args={[.59,24,16,0,Math.PI*2,0,Math.PI*.57]}/><meshStandardMaterial color="#1e1c1b" roughness={.6}/></mesh>
    {[-.46,-.24,0,.24,.46].map((x,i)=><mesh key={x} position={[x,2.74+(i%2)*.06,-.03]} rotation={[0,0,(i-2)*-.12]} castShadow><coneGeometry args={[.16,.32,7]}/><meshStandardMaterial color="#1e1c1b"/></mesh>)}
    {look==='pajama'&&<><mesh position={[0,2.85,-.06]} rotation={[0,0,-.22]} castShadow><coneGeometry args={[.18,.39,8]}/><meshStandardMaterial color="#527fb8"/></mesh><mesh position={[-.08,3.03,-.06]}><sphereGeometry args={[.075,10,8]}/><meshStandardMaterial color="#f2d56b"/></mesh></>}
    {look==='raincoat'&&<mesh position={[0,2.52,-.08]} rotation={[Math.PI/2,0,0]}><torusGeometry args={[.57,.085,8,24]}/><meshStandardMaterial color="#f1c438"/></mesh>}
    {/* eyes, brows, nose, cheeks */}
    <group ref={eyes} position={[0,2.15,.565]}>
      <mesh position={[-.19,0,0]} castShadow><sphereGeometry args={[.075,16,12]}/><meshStandardMaterial color="#171513"/></mesh>
      <mesh position={[.19,0,0]} castShadow><sphereGeometry args={[.075,16,12]}/><meshStandardMaterial color="#171513"/></mesh>
      <mesh position={[-.2,.18,-.035]} rotation={[0,0,-.16]}><capsuleGeometry args={[.045,.25,3,8]}/><meshStandardMaterial color="#201e1c"/></mesh>
      <mesh position={[.2,.18,-.035]} rotation={[0,0,.16]}><capsuleGeometry args={[.045,.25,3,8]}/><meshStandardMaterial color="#201e1c"/></mesh>
    </group>
    <mesh position={[0,2.02,.64]}><sphereGeometry args={[.085,12,10]}/><meshStandardMaterial color="#df9a75"/></mesh>
    <mesh position={[-.4,1.97,.5]}><sphereGeometry args={[.105,12,10]}/><meshStandardMaterial color="#f0786e"/></mesh>
    <mesh position={[.4,1.97,.5]}><sphereGeometry args={[.105,12,10]}/><meshStandardMaterial color="#f0786e"/></mesh>
    <mesh position={[0,1.86,.57]} rotation={[0,0,Math.PI]}><torusGeometry args={[.13,.025,6,16,Math.PI]}/><meshStandardMaterial color="#592f2b"/></mesh>
    </group>
    </group>
    {look==='action-kamen'&&<mesh position={[0,1.25,.37]}><dodecahedronGeometry args={[.11,0]}/><meshStandardMaterial color="#ffe15b" metalness={.18}/></mesh>}
    {look==='raincoat'&&<mesh position={[0,1.25,.37]}><sphereGeometry args={[.045,10,8]}/><meshStandardMaterial color="#fff0af"/></mesh>}
    {/* shoes */}
    <mesh position={[-.18,.25,.08]} castShadow><boxGeometry args={[.24,.13,.34]}/><meshStandardMaterial color={outfit.shoes}/></mesh>
    <mesh position={[.18,.25,.08]} castShadow><boxGeometry args={[.24,.13,.34]}/><meshStandardMaterial color={outfit.shoes}/></mesh>
  </group>
}

function Folder({ position, label, color, onPick, selected }: {position:[number,number,number];label:string;color:string;onPick?:()=>void;selected?:boolean}) {
  const [hover,setHover]=useState(false)
  return <group position={position} onClick={(e)=>{e.stopPropagation();onPick?.()}} onPointerOver={(e)=>{e.stopPropagation();setHover(true);document.body.style.cursor='pointer'}} onPointerOut={()=>{setHover(false);document.body.style.cursor='default'}} scale={selected||hover?1.06:1}>
    <mesh position={[0,.12,0]} castShadow receiveShadow><boxGeometry args={[.72,.22,.54]}/><meshStandardMaterial color={color} roughness={.75}/></mesh>
    <mesh position={[-.17,.27,-.04]} castShadow><boxGeometry args={[.29,.12,.42]}/><meshStandardMaterial color={color} roughness={.75}/></mesh>
    <mesh position={[0,.31,.02]}><boxGeometry args={[.58,.02,.35]}/><meshStandardMaterial color="#fff9e9"/></mesh>
    <Html position={[0,.52,.05]} center distanceFactor={10} style={{pointerEvents:'none'}}><div className="scene-label">{label}</div></Html>
  </group>
}

function EvidenceThread({from,to,color}:{from:[number,number,number];to:[number,number,number];color:string}){
  const dx=to[0]-from[0],dz=to[2]-from[2],length=Math.sqrt(dx*dx+dz*dz)
  if(length<.08)return null
  return <mesh position={[(from[0]+to[0])/2,.405,(from[2]+to[2])/2]} rotation={[Math.PI/2,0,-Math.atan2(dx,dz)]}><cylinderGeometry args={[.014,.014,length,6]}/><meshStandardMaterial color={color} transparent opacity={.78} roughness={.7}/></mesh>
}

function CaseWorld({sources,findings,coverage,tasks,onSelect,selectedNode,compact,animated,look}:{sources:Source[];findings:Finding[];coverage:RequirementCoverage[];tasks:Task[];onSelect?:(x:Pick)=>void;selectedNode?:EvidenceNode|null;compact:boolean;animated:boolean;look:DetectiveLook}) {
  const folderColors=['#f5bc44','#ea6c4f','#69a9c5','#83b87e','#ba8bcb']
  const sourceNodes=sources.slice(0,5)
  const signalOrder:Record<string,number>={gap:0,conflict:1,freshness:2,partial:3,clear:4}
  const findingNodes=findings.filter(f=>f.type!=='clear').slice().sort((a,b)=>(signalOrder[a.type]??9)-(signalOrder[b.type]??9)).slice(0,5)
  const requirementNodes=coverage.slice(0,7)
  const signalById=new Map(findings.map(finding=>[finding.id,finding]))
  const taskNodes=tasks.slice().sort((a,b)=>(signalOrder[signalById.get(a.finding_id||'')?.type||'']??9)-(signalOrder[signalById.get(b.finding_id||'')?.type||'']??9)).slice(0,5)
  const rowPosition=(index:number,count:number,z:number):[number,number,number]=>[-2.8+(count<2?0:index*5.6/(count-1)),.43,z]
  const sourcePosition=(index:number):[number,number,number]=>rowPosition(index,sourceNodes.length,-2.15)
  const requirementPosition=(index:number):[number,number,number]=>rowPosition(index,requirementNodes.length,-.8)
  const findingPosition=(index:number):[number,number,number]=>rowPosition(index,findingNodes.length,.55)
  const taskPosition=(index:number):[number,number,number]=>rowPosition(index,taskNodes.length,1.9)
  return <>
    <color attach="background" args={['#dfedf3']}/>
    <fog attach="fog" args={['#dfedf3',11,21]}/>
    <ambientLight intensity={1.05}/><directionalLight position={[3,8,5]} intensity={2.1} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024}/>
    <mesh rotation={[-Math.PI/2,0,0]} position={[0,-.02,0]} receiveShadow><planeGeometry args={[30,30]}/><meshStandardMaterial color="#e9dcbf" roughness={1}/></mesh>
    {/* notebook-like work table */}
    <mesh position={[0,.18,0]} castShadow receiveShadow><boxGeometry args={[8,.28,6.15]}/><meshStandardMaterial color="#bc8655" roughness={.88}/></mesh>
    <mesh position={[0,.34,0]} receiveShadow><boxGeometry args={[7.82,.055,5.99]}/><meshStandardMaterial color="#fff6df" roughness={1}/></mesh>
    {[-3.25,3.25].flatMap(x=>[-2.35,2.35].map(z=><mesh key={`${x}-${z}`} position={[x,-.68,z]} castShadow><boxGeometry args={[.2,1.45,.2]}/><meshStandardMaterial color="#99683f"/></mesh>))}
    {/* pinboard frame in the back */}
    <mesh position={[0,2.18,-3.02]} castShadow><boxGeometry args={[5.6,2.5,.15]}/><meshStandardMaterial color="#d7ad72"/></mesh>
    <mesh position={[0,2.18,-2.92]}><boxGeometry args={[5.35,2.27,.04]}/><meshStandardMaterial color="#fff0c8"/></mesh>
    <mesh position={[-2.55,2.18,-2.86]}><boxGeometry args={[.05,2.3,.07]}/><meshStandardMaterial color="#e84b39"/></mesh>
    <mesh position={[2.55,2.18,-2.86]}><boxGeometry args={[.05,2.3,.07]}/><meshStandardMaterial color="#e84b39"/></mesh>
    <Float speed={animated?1.15:0} rotationIntensity={animated ? 0.025 : 0} floatIntensity={animated ? 0.08 : 0}><group position={compact?[-.72,.38,.2]:[-4.12,.38,.15]} scale={compact?1.12:.78}><Shinchan activity={compact?'welcome':'inspect'} animated={animated} look={look}/></group></Float>
    {/* Shiro's little kennel and detective magnifier props */}
    <mesh position={[2.8,.48,-.7]} castShadow><cylinderGeometry args={[.28,.31,.28,16]}/><meshStandardMaterial color="#f4d653"/></mesh>
    <mesh position={[2.8,.74,-.7]} castShadow><sphereGeometry args={[.25,16,12]}/><meshStandardMaterial color="#fffdf7"/></mesh>
    <mesh position={[2.92,.72,-.49]}><sphereGeometry args={[.045,10,8]}/><meshStandardMaterial color="#222"/></mesh>
    <mesh position={[2.67,.72,-.49]}><sphereGeometry args={[.045,10,8]}/><meshStandardMaterial color="#222"/></mesh>
    {/* paper clue lines behind the evidence nodes */}
    {coverage.flatMap((item,ri)=>(item.evidence||[]).map((evidence,ei)=>{const si=sourceNodes.findIndex(source=>source.id===evidence.source_id);if(si<0)return null;return <EvidenceThread key={`source-req-${item.requirement.id}-${ei}`} from={sourcePosition(si)} to={requirementPosition(ri)} color={item.status==='conflicting'?'#d74a39':item.status==='covered'?'#68956d':item.status==='partial'?'#4c86a8':'#d3a83c'}/> } ))}
    {requirementNodes.flatMap((item,ri)=>findingNodes.map(finding=>finding.requirement_category===item.requirement.category?<EvidenceThread key={`req-signal-${item.requirement.id}-${finding.id}`} from={requirementPosition(ri)} to={findingPosition(findingNodes.indexOf(finding))} color={finding.type==='conflict'?'#d74a39':finding.type==='freshness'?'#4c86a8':'#d3a83c'}/>:null))}
     {findingNodes.flatMap((finding,fi)=>taskNodes.map(task=>{const taskFinding=signalById.get(task.finding_id||'');return taskFinding?.id===finding.id||(taskFinding?.requirement_category&&taskFinding.requirement_category===finding.requirement_category)?<EvidenceThread key={`signal-task-${finding.id}-${task.id}`} from={findingPosition(fi)} to={taskPosition(taskNodes.indexOf(task))} color="#d3a83c"/>:null}))}
     {sourceNodes.map((s,i)=><Folder key={s.id} position={sourcePosition(i)} label={`S${i+1}`} color={folderColors[i%folderColors.length]} selected={selectedNode?.kind==='source'&&selectedNode.id===s.id} onPick={()=>onSelect?.({kind:'source',id:s.id})}/>) }
    {requirementNodes.map((item,index)=>{const position=requirementPosition(index);const color=item.status==='conflicting'?'#e35745':item.status==='covered'?'#83b87e':item.status==='partial'?'#74b6d1':'#f4c84c';const selected=selectedNode?.kind==='requirement'&&selectedNode.id===item.requirement.category;return <group key={item.requirement.id} position={position} scale={selected?1.12:1} onClick={event=>{event.stopPropagation();onSelect?.({kind:'requirement',id:item.requirement.category})}} onPointerOver={()=>document.body.style.cursor='pointer'} onPointerOut={()=>document.body.style.cursor='default'}><mesh castShadow><boxGeometry args={[.58,.12,.38]}/><meshStandardMaterial color={color} roughness={.72}/></mesh><mesh position={[0,.1,0]}><sphereGeometry args={[.055,10,8]}/><meshStandardMaterial color="#fffdf5"/></mesh><Html position={[0,.27,0]} center distanceFactor={10} style={{pointerEvents:'none'}}><div className="scene-label">CHECK {index+1}</div></Html></group>})}
     {findingNodes.map((f,i)=><group key={f.id} position={findingPosition(i)} scale={selectedNode?.kind==='finding'&&selectedNode.id===f.id?1.18:1} onClick={(e)=>{e.stopPropagation();onSelect?.({kind:'finding',id:f.id})}} onPointerOver={()=>document.body.style.cursor='pointer'} onPointerOut={()=>document.body.style.cursor='default'}>
      <mesh castShadow><cylinderGeometry args={[.19,.19,.16,16]}/><meshStandardMaterial color={f.type==='conflict'?'#e35745':f.type==='freshness'?'#6da4bf':'#f4c84c'}/></mesh>
      <mesh position={[0,.11,.01]}><sphereGeometry args={[.05,10,8]}/><meshStandardMaterial color="#fff9e6"/></mesh>
       <Html position={[0,.39,0]} center distanceFactor={10} style={{pointerEvents:'none'}}><div className="scene-label scene-label-find">{f.type==='conflict'?'SIGNAL':f.type==='freshness'?'DATE':'GAP'} {i+1}</div></Html>
    </group>)}
     {taskNodes.map((task,index)=>{const position=taskPosition(index);return <group key={task.id} position={position} scale={selectedNode?.kind==='task'&&selectedNode.id===task.id?1.18:1} onClick={event=>{event.stopPropagation();onSelect?.({kind:'task',id:task.id})}} onPointerOver={()=>document.body.style.cursor='pointer'} onPointerOut={()=>document.body.style.cursor='default'}><mesh castShadow><boxGeometry args={[.46,.09,.28]}/><meshStandardMaterial color={task.status==='verified'?'#83b87e':'#f4d16e'}/></mesh><mesh position={[0,.09,0]}><boxGeometry args={[.34,.035,.22]}/><meshStandardMaterial color="#fffdf5"/></mesh><Html position={[0,.25,0]} center distanceFactor={10} style={{pointerEvents:'none'}}><div className="scene-label">TASK {index+1}</div></Html></group>})}
    <mesh position={[2.55,.39,1.35]} rotation={[0,0,0]} castShadow><torusGeometry args={[.36,.045,8,28]}/><meshStandardMaterial color="#df6652"/></mesh>
    <mesh position={[2.8,.38,1.36]} rotation={[0,0,0]}><boxGeometry args={[.06,.5,.06]}/><meshStandardMaterial color="#7a5a43"/></mesh>
    <ContactShadows position={[0,.001,0]} opacity={.22} scale={10} blur={2.5} far={4}/>
  </>
}

export function ShinchanBuddy({ activity = 'welcome', look = 'classic' }: { activity?: DetectiveActivity; look?: DetectiveLook }) {
  const [animated, setAnimated] = useState(true)
  useEffect(() => {
    const query = window.matchMedia('(prefers-reduced-motion: reduce)')
    const update = () => setAnimated(!query.matches && !document.documentElement.classList.contains('reduce-motion'))
    update()
    query.addEventListener?.('change', update)
    document.addEventListener('shinchan:motion-preference',update)
    return () => {query.removeEventListener?.('change', update);document.removeEventListener('shinchan:motion-preference',update)}
  }, [])
  const propColor = LOOK_PALETTE[look].accent
  return <div className={`buddy-scene buddy-${activity}`} aria-label={`Animated 3D Shinchan ${activity} animation`}>
    <Canvas dpr={[1, 1.25]} camera={{ position: [0, 1.65, 7.2], fov: 34 }} gl={{ antialias: true, alpha: true, powerPreference: 'low-power' }}>
      <color attach="background" args={['#f5e9d2']} />
      <ambientLight intensity={1.35} />
      <directionalLight position={[3, 6, 5]} intensity={2.05} castShadow />
      <group position={[0, -.05, 0]} scale={.84}><Shinchan activity={activity} animated={animated} look={look}/></group>
      <mesh position={[0, .04, -.12]} receiveShadow><cylinderGeometry args={[1.33, 1.4, .13, 40]} /><meshStandardMaterial color="#fff9e9" roughness={.82} /></mesh>
      <mesh position={[0, -.17, -.12]}><cylinderGeometry args={[1.28, 1.34, .12, 40]} /><meshStandardMaterial color="#d59e61" roughness={.8} /></mesh>
      <Float speed={animated ? 1.8 : 0} rotationIntensity={animated ? .16 : 0} floatIntensity={animated ? .2 : 0}><mesh position={[1.02, 1.85, .06]}><torusGeometry args={[.22, .043, 8, 24]} /><meshStandardMaterial color={propColor} metalness={.2} roughness={.36} /></mesh></Float>
      <Float speed={animated ? 1.4 : 0} rotationIntensity={animated ? .2 : 0} floatIntensity={animated ? .25 : 0}><mesh position={[-1.04, 1.57, -.1]} rotation={[.16, .26, -.22]}><boxGeometry args={[.37, .47, .07]} /><meshStandardMaterial color="#fffdf7" roughness={.94} /></mesh></Float>
      <Float speed={animated ? 2.2 : 0} rotationIntensity={animated ? .4 : 0} floatIntensity={animated ? .32 : 0}><mesh position={[.98, .77, .24]}><octahedronGeometry args={[.14, 0]} /><meshStandardMaterial color="#f2c649" emissive="#e8b734" emissiveIntensity={.16} /></mesh></Float>
    </Canvas>
  </div>
}

export default function DetectiveScene({sources=[],findings=[],coverage=[],tasks=[],onSelect,selectedNode=null,compact=false,look='classic'}:Props) {
  const [failed,setFailed]=useState(false)
  const [webgl,setWebgl]=useState<boolean|null>(null)
  const [reducedMotion,setReducedMotion]=useState(false)
  useEffect(()=>{
    try{const c=document.createElement('canvas');setWebgl(!!(c.getContext('webgl2')||c.getContext('webgl')))}catch{setWebgl(false)}
    const q=window.matchMedia('(prefers-reduced-motion: reduce)');const update=()=>setReducedMotion(q.matches||document.documentElement.classList.contains('reduce-motion'));update();q.addEventListener?.('change',update);document.addEventListener('shinchan:motion-preference',update);return()=>{q.removeEventListener?.('change',update);document.removeEventListener('shinchan:motion-preference',update)}
  },[])
  const selectedSources=useMemo(()=>sources, [sources])
  if (failed||webgl===false) return <div className="scene-fallback"><div className="fallback-mascot">🕵️‍♂️</div><p>3D scene unavailable here. Use the accessible evidence list.</p><button onClick={()=>{setFailed(false);setWebgl(true)}}>Try again</button><div className="fallback-evidence">{selectedSources.map((s,i)=><button key={s.id} onClick={()=>onSelect?.({kind:'source',id:s.id})}>{i+1}. {s.title}</button>)}</div></div>
  if(webgl===null)return <div className="scene-fallback"><LoaderCircle className="spin" size={22}/><p>Setting up Shinchan's detective desk…</p></div>
  return <div className={`scene-wrap ${compact?'scene-compact':''}`}>
    <Canvas shadows dpr={[1,1.5]} camera={{position:compact?[2.5,3.8,7.8]:[0,8,9.5],fov:compact?39:40}} gl={{antialias:true,alpha:false,powerPreference:'high-performance'}} onCreated={({gl})=>{gl.setClearColor('#dfedf3');gl.domElement.addEventListener('webglcontextlost',(event)=>{event.preventDefault();setFailed(true)},{once:true})}}>
    <Suspense fallback={null}><CaseWorld sources={selectedSources} findings={findings} coverage={coverage} tasks={tasks} onSelect={onSelect} selectedNode={selectedNode} compact={compact} animated={!reducedMotion} look={look}/></Suspense>
      <OrbitControls enablePan={false} minDistance={7} maxDistance={17} maxPolarAngle={Math.PI*.48} minPolarAngle={Math.PI*.2} target={[0,1.1,0]} makeDefault/>
    </Canvas>
    <div className="scene-hint"><span className="hint-orbit">↻</span> Drag to look around · click a clue to inspect</div>
  </div>
}
