import type { DocumentItem, SearchResult } from './types'

const BASE_URL = 'http://localhost:8000'

async function errorMessage(res: Response, fallback: string): Promise<string> {
  const data = await res.json().catch(() => null)
  return typeof data?.detail === 'string' ? data.detail : fallback
}

export async function getDocuments(): Promise<DocumentItem[]> {
  const res = await fetch(`${BASE_URL}/documents`)
  const data = await res.json()
  return data
}

export async function createDocument(doc: Omit<DocumentItem, 'id'>): Promise<DocumentItem> {
  const res = await fetch(`${BASE_URL}/documents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(doc),
  })
  return res.json()
}

export async function updateDocument(id: number, doc: Omit<DocumentItem, 'id'>): Promise<DocumentItem> {
  const res = await fetch(`${BASE_URL}/documents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(doc),
  })
  return res.json()
}

export async function deleteDocument(id: number): Promise<void> {
  await fetch(`${BASE_URL}/documents/${id}`, { method: 'DELETE' })
}

export async function uploadDocument(file: File): Promise<DocumentItem> {
  const formData = new FormData()
  formData.append('file', file)
  const res = await fetch(`${BASE_URL}/documents/upload`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) {
    throw new Error(await errorMessage(res, 'Upload failed'))
  }
  return res.json()
}

export async function semanticSearch(query: string): Promise<SearchResult[]> {
  const res = await fetch(`${BASE_URL}/documents/semantic-search?query=${encodeURIComponent(query)}`)
  if (!res.ok) {
    throw new Error(await errorMessage(res, 'Search failed'))
  }
  return res.json()
}
