export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ""

export function apiUrl(path: string) {
  const trimmed = API_BASE_URL.replace(/\/$/, "")
  if (!trimmed) {
    return path
  }
  return `${trimmed}${path}`
}
