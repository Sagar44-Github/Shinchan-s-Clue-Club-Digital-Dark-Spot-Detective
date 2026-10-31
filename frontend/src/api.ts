import type { AnalysisRun, LibraryCase, MissionItem, ResearchCase, Requirement, Task, VaultSource } from './types'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api'
async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers)
  if (!(init.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  let response: Response
  try { response = await fetch(`${API}${path}`, { ...init, headers }) }
  catch { throw new Error('The case service is offline. Start the backend with the setup instructions in README.md.') }
  if (!response.ok) {
    let message = `Request failed (${response.status})`
    try { const body = await response.json(); message = body.detail || body.message || message } catch { /* keep status */ }
    throw new Error(message)
  }
  return response.json() as Promise<T>
}

export const api = {
  health: () => request<{ok:boolean;ai_configured:boolean}>('/health'),
  listCases: () => request<any[]>('/cases'),
  library: () => request<LibraryCase[]>('/library'),
  missions: () => request<MissionItem[]>('/missions'),
  vaultSources: () => request<VaultSource[]>('/vault/sources'),
  reuseSource: (caseId:string, sourceId:string) => request<{source:VaultSource;already_present:boolean;case:ResearchCase}>(`/cases/${caseId}/sources/reuse`,{method:'POST',body:JSON.stringify({source_id:sourceId})}),
  openLibrary: (slug:string) => request<ResearchCase>(`/library/${slug}`,{method:'POST'}),
  submitChallenge: (id:string, answerId:string) => request<{correct:boolean;attempts:number;solved_at:string;hint?:string;resolution?:string;case:ResearchCase}>(`/cases/${id}/challenge/answer`,{method:'POST',body:JSON.stringify({answer_id:answerId})}),
  challengeHint: (id:string, level:number) => request<{level:number;hint:string;has_more:boolean}>(`/cases/${id}/challenge/hint`,{method:'POST',body:JSON.stringify({level})}),
  getCase: (id: string) => request<ResearchCase>(`/cases/${id}`),
  createCase: (data: {title:string;question:string;context:string;jurisdiction:string;decision_date:string;requirements:Requirement[]}) => request<ResearchCase>('/cases', {method:'POST', body:JSON.stringify(data)}),
  demo: () => request<ResearchCase>('/demo', {method:'POST'}),
  addText: (id:string, data:{title:string;text:string;url:string;publisher:string;published_date:string}) => request(`/cases/${id}/sources/text`, {method:'POST',body:JSON.stringify(data)}),
  addUrl: (id:string, data:{url:string;title:string;publisher:string;published_date:string}) => request(`/cases/${id}/sources/url`, {method:'POST',body:JSON.stringify(data)}),
  addFile: (id:string, file:File, meta:{title:string;publisher:string;published_date:string}) => {const form=new FormData();form.append('file',file);form.append('title',meta.title);form.append('publisher',meta.publisher);form.append('published_date',meta.published_date);return request(`/cases/${id}/sources/upload`,{method:'POST',body:form})},
  removeSource: (caseId:string, sourceId:string) => request(`/cases/${caseId}/sources/${sourceId}`, {method:'DELETE'}),
  analyze: (id:string) => request<{run:AnalysisRun;case:ResearchCase}>(`/cases/${id}/analyze`, {method:'POST'}),
  updateTask: (id:string, patch:Partial<Task>) => request<Task>(`/tasks/${id}`, {method:'PATCH',body:JSON.stringify(patch)}),
  updateCase: (id:string, patch:Partial<ResearchCase>) => request<ResearchCase>(`/cases/${id}`,{method:'PATCH',body:JSON.stringify(patch)}),
  deleteCase: (id:string) => request(`/cases/${id}`,{method:'DELETE'}),
  reportUrl: (id:string) => `${API}/cases/${id}/report.md`,
}
