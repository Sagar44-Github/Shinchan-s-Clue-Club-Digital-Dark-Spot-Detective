import { motion } from 'framer-motion'
import { Check, Settings2, ShieldCheck, X } from 'lucide-react'
import { DetectiveBuddy } from './SceneLoader'
import { DETECTIVE_LOOKS, type DetectiveLook } from './character-look'

type Props={open:boolean;onClose:()=>void;name:string;onName:(name:string)=>void;cases:number;sources:number;verified:number;reducedMotion:boolean;onReducedMotion:(value:boolean)=>void;inkMode:boolean;onInkMode:(value:boolean)=>void;theme:'light'|'dark';onThemeChange:(theme:'light'|'dark')=>void;look:DetectiveLook;onLook:(look:DetectiveLook)=>void}

export default function ProfilePanel({open,onClose,name,onName,cases,sources,verified,reducedMotion,onReducedMotion,inkMode,onInkMode,theme,onThemeChange,look,onLook}:Props){
  if(!open)return null
  return <motion.div className="profile-scrim" initial={{opacity:0}} animate={{opacity:1}} exit={{opacity:0}} onMouseDown={event=>event.target===event.currentTarget&&onClose()}>
    <motion.aside className="profile-panel" role="dialog" aria-modal="true" aria-labelledby="profile-title" initial={{x:28,opacity:0}} animate={{x:0,opacity:1}} exit={{x:28,opacity:0}}>
      <header className="profile-panel-head"><div><span className="section-kicker">YOUR CLUE CLUB CARD</span><h2 id="profile-title">Detective profile</h2></div><button className="profile-close" onClick={onClose} aria-label="Close profile"><X size={20}/></button></header>
      <div className="profile-hero"><div className="profile-hero-art"><DetectiveBuddy activity="welcome" look={look}/></div><div><span className="profile-rank">★ JUNIOR DETECTIVE ★</span><b>{name||'Junior Detective'}</b><small>Clubhouse member · saved on this device</small></div></div>
      <section className="profile-look-picker" aria-labelledby="profile-look-title"><div className="profile-settings-head"><span className="profile-palette">✦</span><div><b id="profile-look-title">Choose Shinchan's look</b><small>Pick the buddy who patrols with you across the club.</small></div></div><div className="profile-look-grid">{DETECTIVE_LOOKS.map(option=><button key={option.id} type="button" className={`profile-look-option ${look===option.id?'selected':''}`} aria-pressed={look===option.id} onClick={()=>onLook(option.id)}><span className="profile-look-icon">{option.icon}</span><span className="profile-look-copy"><b>{option.name}</b><small>{option.note}</small></span>{look===option.id&&<Check className="profile-look-check" size={17}/>}</button>)}</div></section>
      <label className="profile-name-field">Your detective name<input value={name} maxLength={32} onChange={event=>onName(event.target.value)} placeholder="Junior Detective"/><small>This name and the settings below stay in this browser. No account or profile is sent to a server.</small></label>
      <div className="profile-stats"><article><b>{cases}</b><span>case files</span></article><article><b>{sources}</b><span>sources gathered</span></article><article><b>{verified}</b><span>clues checked</span></article></div>
      <div className="profile-settings-head"><Settings2 size={16}/><b>Clubhouse settings</b></div>
      <label className="profile-toggle"><span><b>Clubhouse lighting</b><small>{theme==='dark'?'Night desk: deep blue-charcoal surfaces, warm paper cards and clear amber accents.':'Day desk: warm paper surfaces, ink outlines and Shinchan red accents.'}</small></span><input type="checkbox" checked={theme==='dark'} onChange={event=>onThemeChange(event.target.checked?'dark':'light')}/><i>{theme==='dark'?<Check size={13}/>:null}</i></label>
      <label className="profile-toggle"><span><b>Reduce animation</b><small>Pause character movement and floating effects.</small></span><input type="checkbox" checked={reducedMotion} onChange={event=>onReducedMotion(event.target.checked)}/><i>{reducedMotion?<Check size={13}/>:null}</i></label>
      <label className="profile-toggle"><span><b>Ink outline mode</b><small>Use crisp black outlines and stronger contrast.</small></span><input type="checkbox" checked={inkMode} onChange={event=>onInkMode(event.target.checked)}/><i>{inkMode?<Check size={13}/>:null}</i></label>
      <div className="profile-honesty"><ShieldCheck size={16}/><p><b>Shinchan's detective rule</b><br/>Your case files belong to this local app. “Not found” still means not found in the sources you reviewed.</p></div>
      <button className="profile-done" onClick={onClose}>Back to the mystery <Check size={15}/></button>
    </motion.aside>
  </motion.div>
}
