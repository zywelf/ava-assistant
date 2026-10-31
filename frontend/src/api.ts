import type { DocumentItem } from './types'

const BASE_URL = 'http://localhost:8000'

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
