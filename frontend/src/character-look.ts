export const DETECTIVE_LOOKS = [
  { id: 'classic', name: 'Classic Shinchan', note: 'Red tee · yellow shorts', icon: '🧢', accent: '#e94436' },
  { id: 'action-kamen', name: 'Action Kamen', note: 'Hero suit · cape', icon: '🦸', accent: '#3476d1' },
  { id: 'pajama', name: 'Sleepy Shinchan', note: 'Blue pajamas · night cap', icon: '🌙', accent: '#527fb8' },
  { id: 'raincoat', name: 'Rainy-Day Shinchan', note: 'Yellow coat · green boots', icon: '🌧️', accent: '#d5a931' },
] as const

export type DetectiveLook = typeof DETECTIVE_LOOKS[number]['id']

export const LOOK_PALETTE: Record<DetectiveLook, { shirt: string; shorts: string; shoes: string; accent: string }> = {
  classic: { shirt: '#e94436', shorts: '#ffd33e', shoes: '#f9f2e7', accent: '#e94436' },
  'action-kamen': { shirt: '#3476d1', shorts: '#e94436', shoes: '#fff5dc', accent: '#f3c839' },
  pajama: { shirt: '#527fb8', shorts: '#f2d56b', shoes: '#e7f0f7', accent: '#f1d36c' },
  raincoat: { shirt: '#f1c438', shorts: '#547b55', shoes: '#547b55', accent: '#5f9b69' },
}
