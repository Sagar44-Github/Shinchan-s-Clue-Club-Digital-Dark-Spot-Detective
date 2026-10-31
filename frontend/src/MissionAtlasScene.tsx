import { Canvas } from '@react-three/fiber'
import { ContactShadows, Edges, Float, Html, OrbitControls } from '@react-three/drei'
import * as THREE from 'three'
import type { LibraryCase } from './types'

export type AtlasStop = LibraryCase & { x:number; z:number; district:string; landmark:string; order:number }

export default function MissionAtlasScene({stops,selectedSlug,onSelect}:{stops:AtlasStop[];selectedSlug:string|null;onSelect:(slug:string)=>void}){
  return <div className="atlas-canvas-shell" aria-label="Interactive 3D map of Kasukabe mystery locations">
    <Canvas shadows dpr={[1,1.5]} camera={{position:[12,17,14],fov:34}} gl={{antialias:true,alpha:false}}>
      <color attach="background" args={['#b8dce7']}/>
      <fog attach="fog" args={['#b8dce7',22,38]}/>
      <ambientLight intensity={1.35}/>
      <directionalLight position={[8,15,8]} intensity={2.3} castShadow shadow-mapSize-width={1024} shadow-mapSize-height={1024}/>
      <group position={[0,-.2,0]}>
        <mesh rotation={[-Math.PI/2,0,0]} position={[0,-.18,0]} receiveShadow><planeGeometry args={[18,14]}/><meshStandardMaterial color="#e6d59f" roughness={1}/></mesh>
        <mesh position={[0,-.34,0]} castShadow><boxGeometry args={[18.2,.28,14.2]}/><meshStandardMaterial color="#cb9c55"/><Edges color="#25272b" linewidth={2}/></mesh>
        <Road position={[0,.015,0]} size={[18,.08,1.35]}/><Road position={[0,.02,2.65]} size={[18,.08,1.05]}/><Road position={[-2.1,.025,0]} size={[1.2,.085,14]}/><Road position={[3,.03,0]} size={[1,.09,14]}/>
        <Sidewalk position={[0,.05,-1.1]} size={[18,.12,.22]}/><Sidewalk position={[0,.05,1.1]} size={[18,.12,.22]}/><Sidewalk position={[0,.055,3.3]} size={[18,.12,.2]}/>
        <Crosswalk position={[-2.1,.08,-.82]} rotation={0}/><Crosswalk position={[3,.085,2.28]} rotation={Math.PI/2}/>
        <School position={[-5.5,0,-3.65]}/>
        <Park position={[-5.5,0,1.9]}/>
        <CommunityGarden position={[-.1,0,4.95]}/>
        <FestivalStage position={[1.2,0,-3.5]}/>
        <ShopRow position={[5.35,0,-3.8]}/>
        <BusStop position={[.15,0,5.2]}/>
        <TownHouses position={[-.1,0,-5.3]}/>
        <OfficeBlock position={[5.35,0,1.7]}/>
        <Bench position={[-1.25,.08,-3.95]}/><Bench position={[3.7,.08,.05]}/>
        {stops.map(stop=><MapStop key={stop.slug} stop={stop} selected={stop.slug===selectedSlug} onSelect={()=>onSelect(stop.slug)}/>)}
      </group>
      <ContactShadows position={[0,-.02,0]} opacity={.25} scale={19} blur={2.4} far={8}/>
      <OrbitControls enablePan={false} minDistance={14} maxDistance={26} minPolarAngle={.42} maxPolarAngle={1.08} minAzimuthAngle={-Math.PI/2.3} maxAzimuthAngle={Math.PI/2.3} target={[0,0,0]} makeDefault/>
    </Canvas>
    <div className="atlas-map-label atlas-label-school">FUTABA KINDERGARTEN</div>
    <div className="atlas-map-label atlas-label-park">SHIRO'S PARK</div>
    <div className="atlas-map-label atlas-label-stage">ACTION KAMEN STAGE</div>
    <div className="atlas-map-compass" aria-hidden="true"><span>N</span><b>✦</b></div>
  </div>
}

function Road({position,size}:{position:[number,number,number];size:[number,number,number]}){return <mesh position={position} receiveShadow><boxGeometry args={size}/><meshStandardMaterial color="#74858a" roughness={1}/><Edges color="#26292a" linewidth={1.5}/></mesh>}
function Sidewalk({position,size}:{position:[number,number,number];size:[number,number,number]}){return <mesh position={position} receiveShadow><boxGeometry args={size}/><meshStandardMaterial color="#fff0c2"/><Edges color="#443d32" linewidth={1.1}/></mesh>}
function Crosswalk({position,rotation}:{position:[number,number,number];rotation:number}){return <group position={position} rotation={[0,rotation,0]}>{Array.from({length:5},(_,i)=><mesh key={i} position={[-.36+i*.18,.05,0]}><boxGeometry args={[.09,.035,.72]}/><meshStandardMaterial color="#fff8dc"/></mesh>)}</group>}
function Tree({position,scale=1,color='#73a75f'}:{position:[number,number,number];scale?:number;color?:string}){return <group position={position} scale={scale}><mesh position={[0,.38,0]} castShadow><cylinderGeometry args={[.09,.14,.76,6]}/><meshStandardMaterial color="#946342"/><Edges color="#372b24"/></mesh><mesh position={[0,.98,0]} castShadow><coneGeometry args={[.52,.9,7]}/><meshStandardMaterial color={color} flatShading/><Edges color="#2c4936"/></mesh><mesh position={[0,1.42,0]} castShadow><coneGeometry args={[.35,.72,7]}/><meshStandardMaterial color={color} flatShading/><Edges color="#2c4936"/></mesh></group>}
function School({position}:{position:[number,number,number]}){return <group position={position}><Block position={[0,.7,0]} size={[3.1,1.4,1.65]} color="#83bfd0"/><mesh position={[0,1.55,0]} rotation={[0,Math.PI/4,0]} castShadow><coneGeometry args={[1.55,.6,4]}/><meshStandardMaterial color="#ed6952" flatShading/><Edges color="#282929"/></mesh><mesh position={[-.68,.58,.84]}><boxGeometry args={[.44,.68,.06]}/><meshStandardMaterial color="#ffd76a"/><Edges color="#282929"/></mesh><mesh position={[.15,.88,.84]}><boxGeometry args={[.42,.32,.06]}/><meshStandardMaterial color="#bde7ed"/><Edges color="#282929"/></mesh><Tree position={[-2,0,-.35]} scale={.8}/><Tree position={[2,0,.35]} scale={.8}/></group>}
function Park({position}:{position:[number,number,number]}){return <group position={position}><mesh position={[0,.05,0]} receiveShadow><cylinderGeometry args={[2.3,2.3,.12,9]}/><meshStandardMaterial color="#97bd75"/><Edges color="#34452c"/></mesh><Tree position={[-1.2,.1,-.35]} color="#6fae68"/><Tree position={[1.2,.1,-.5]} scale={.82} color="#72ab60"/><Tree position={[.45,.1,1.1]} scale={.7} color="#86b86a"/><Bench position={[0,.14,.25]}/></group>}
function CommunityGarden({position}:{position:[number,number,number]}){return <group position={position}><Block position={[0,.12,0]} size={[3.3,.24,1.5]} color="#7fa866"/><Edges color="#34452c"/><GardenBed position={[-.78,.28,0]}/><GardenBed position={[.45,.28,0]}/><Tree position={[1.85,0,-.35]} scale={.67} color="#72aa65"/></group>}
function GardenBed({position}:{position:[number,number,number]}){return <group position={position}><mesh position={[0,.18,0]}><boxGeometry args={[.9,.22,.62]}/><meshStandardMaterial color="#9a7045"/><Edges color="#372b24"/></mesh>{[-.22,0,.22].map((x,i)=><mesh key={i} position={[x,.46,0]}><sphereGeometry args={[.13,.5,5]}/><meshStandardMaterial color={i===1?'#f4c94e':'#6ca461'}/></mesh>)}</group>}
function FestivalStage({position}:{position:[number,number,number]}){return <group position={position}><Block position={[0,.27,0]} size={[2.25,.54,1.4]} color="#db765f"/><Block position={[0,.98,-.38]} size={[2.4,1.05,.15]} color="#f3c94f"/><mesh position={[-.82,.24,.76]}><boxGeometry args={[.12,.4,.1]}/><meshStandardMaterial color="#2b2b2b"/></mesh><mesh position={[.82,.24,.76]}><boxGeometry args={[.12,.4,.1]}/><meshStandardMaterial color="#2b2b2b"/></mesh></group>}
function ShopRow({position}:{position:[number,number,number]}){return <group position={position}><Block position={[-.65,.63,0]} size={[1.4,1.25,1.35]} color="#f3c261"/><Block position={[.82,.55,.05]} size={[1.45,1.1,1.35]} color="#dd8d77"/><Awning position={[-.65,1.03,.72]} color="#e85243"/><Awning position={[.82,.94,.76]} color="#4d9db3"/></group>}
function Awning({position,color}:{position:[number,number,number];color:string}){return <mesh position={position}><boxGeometry args={[1.25,.14,.55]}/><meshStandardMaterial color={color}/><Edges color="#282929"/></mesh>}
function BusStop({position}:{position:[number,number,number]}){return <group position={position}><mesh position={[0,.75,0]}><boxGeometry args={[1.25,1.35,.12]}/><meshStandardMaterial color="#b8e1e8" transparent opacity={.8}/><Edges color="#344c53"/></mesh><mesh position={[0,1.48,0]}><boxGeometry args={[1.5,.12,.38]}/><meshStandardMaterial color="#ed5141"/><Edges color="#282929"/></mesh><mesh position={[-.48,.24,.26]}><boxGeometry args={[.12,.48,.12]}/><meshStandardMaterial color="#303337"/></mesh><mesh position={[.48,.24,.26]}><boxGeometry args={[.12,.48,.12]}/><meshStandardMaterial color="#303337"/></mesh></group>}
function TownHouses({position}:{position:[number,number,number]}){return <group position={position}><House position={[-1,0,0]} color="#edbd88" roof="#bd634f"/><House position={[1,0,-.2]} color="#9ec8ca" roof="#e8bd4d"/></group>}
function House({position,color,roof}:{position:[number,number,number];color:string;roof:string}){return <group position={position}><Block position={[0,.5,0]} size={[1.2,1,1.1]} color={color}/><mesh position={[0,1.1,0]} rotation={[0,Math.PI/4,0]}><coneGeometry args={[.92,.58,4]}/><meshStandardMaterial color={roof} flatShading/><Edges color="#282929"/></mesh><mesh position={[.1,.38,.57]}><boxGeometry args={[.32,.58,.06]}/><meshStandardMaterial color="#8a543d"/><Edges color="#282929"/></mesh></group>}
function OfficeBlock({position}:{position:[number,number,number]}){return <group position={position}><Block position={[0,.62,0]} size={[2.5,1.25,1.55]} color="#c5d6d0"/><mesh position={[0,1.3,0]}><boxGeometry args={[2.65,.12,1.7]}/><meshStandardMaterial color="#e76e56"/><Edges color="#282929"/></mesh>{[-.7,0,.7].map(x=><mesh key={x} position={[x,.62,.8]}><boxGeometry args={[.42,.43,.05]}/><meshStandardMaterial color="#8fc9d8"/><Edges color="#282929"/></mesh>)}</group>}
function Block({position,size,color}:{position:[number,number,number];size:[number,number,number];color:string}){return <mesh position={position} castShadow receiveShadow><boxGeometry args={size}/><meshStandardMaterial color={color} flatShading/><Edges color="#292a29" linewidth={1.25}/></mesh>}
function Bench({position}:{position:[number,number,number]}){return <group position={position}><mesh position={[0,.26,0]}><boxGeometry args={[.95,.14,.28]}/><meshStandardMaterial color="#c88a48"/><Edges color="#3a2f28"/></mesh>{[-.34,.34].map(x=><mesh key={x} position={[x,.12,0]}><boxGeometry args={[.09,.27,.09]}/><meshStandardMaterial color="#51463a"/></mesh>)}</group>}

function MapStop({stop,selected,onSelect}:{stop:AtlasStop;selected:boolean;onSelect:()=>void}){
  const color=stop.play_mode==='challenge'?'#e94b3c':'#246b8d'
  return <group position={[stop.x,.05,stop.z]} onClick={onSelect}>
    <Float speed={selected?2.4:1.4} floatIntensity={selected?.2:.08} rotationIntensity={0}>
      <mesh position={[0,.38,0]} castShadow><sphereGeometry args={[selected?.29:.22,12,10]}/><meshStandardMaterial color={selected?'#ffd447':color} roughness={.42}/><Edges color="#25272b"/></mesh>
      <mesh position={[0,.12,0]} rotation={[Math.PI,0,0]}><coneGeometry args={[.17,.4,7]}/><meshStandardMaterial color={selected?'#ffd447':color}/><Edges color="#25272b"/></mesh>
      <mesh position={[0,-.06,0]} rotation={[-Math.PI/2,0,0]}><circleGeometry args={[.3,16]}/><meshBasicMaterial color="#27292a" transparent opacity={selected?.18:.11}/></mesh>
    </Float>
    <Html position={[0,.88,0]} center distanceFactor={11} zIndexRange={[40,0]}>
      <button type="button" aria-label={`Open map marker ${stop.order}: ${stop.title}`} title={`${stop.landmark}: ${stop.title}`} className={`atlas-pin-hit ${selected?'active':''} ${stop.play_mode==='challenge'?'unsolved':''}`} onPointerDown={event=>event.stopPropagation()} onClick={event=>{event.stopPropagation();onSelect()}}><span>{String(stop.order).padStart(2,'0')}</span></button>
    </Html>
  </group>
}
