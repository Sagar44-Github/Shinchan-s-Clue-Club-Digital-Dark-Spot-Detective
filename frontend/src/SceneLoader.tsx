import { lazy, Suspense } from 'react'
import { LoaderCircle } from 'lucide-react'
import type { DetectiveActivity, EvidenceNode } from './Scene'
import type { DetectiveLook } from './character-look'
import type { Finding, RequirementCoverage, Source, Task } from './types'
import './scene-loading.css'

const DetectiveScene = lazy(() => import('./Scene'))
const ShinchanBuddy = lazy(() => import('./Scene').then((scene) => ({ default: scene.ShinchanBuddy })))
type Props = { sources?: Source[]; findings?: Finding[]; coverage?:RequirementCoverage[]; tasks?:Task[]; onSelect?: (pick:EvidenceNode)=>void; selectedNode?:EvidenceNode|null; compact?:boolean; look?:DetectiveLook }

export default function SceneLoader(props:Props){
  return <Suspense fallback={<div className={`scene-wrap scene-loading ${props.compact?'scene-compact':''}`}><LoaderCircle className="spin" size={24}/><span>Setting up Shinchan's detective desk…</span></div>}><DetectiveScene {...props}/></Suspense>
}

export function DetectiveBuddy({activity='welcome',look='classic'}:{activity?:DetectiveActivity;look?:DetectiveLook}){
  return <Suspense fallback={<div className="buddy-scene buddy-loading"><LoaderCircle className="spin" size={21}/></div>}><ShinchanBuddy activity={activity} look={look}/></Suspense>
}
