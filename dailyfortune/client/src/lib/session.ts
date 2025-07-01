// Session management for fortune history
export function getSessionId(): string {
  let sessionId = localStorage.getItem('fortune-session-id');
  
  if (!sessionId) {
    sessionId = 'session-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('fortune-session-id', sessionId);
  }
  
  return sessionId;
}

export function clearSession(): void {
  localStorage.removeItem('fortune-session-id');
}