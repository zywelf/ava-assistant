import type { DocumentItem, SearchResult } from './types'

// All the calls from the frontend to the backend API live here.
// The components never use fetch directly: they use these functions

const BASE_URL = 'http://localhost:8000'

/**
 * Read the error message sent by the backend, or use the fallback.
 *
 * Example: a 415 gives "Format not supported: .docx", a crash gives "Upload failed"
 */
async function errorMessage(res: Response, fallback: string): Promise<string> {
  const data = await res.json().catch(() => null) // The body may not be JSON
  // FastAPI sends "detail" as a string, but as a list for 422 validation errors
  return typeof data?.detail === 'string' ? data.detail : fallback
}

/** Get all the documents. */
export async function getDocuments(): Promise<DocumentItem[]> {
  const res = await fetch(`${BASE_URL}/documents`)
  const data = await res.json()
  return data
}

/**
 * Create a document from a title and a content.
 *
 * Example: createDocument({ title: 'Notes', content: 'Buy milk' })
 */
export async function createDocument(doc: Omit<DocumentItem, 'id'>): Promise<DocumentItem> {
  const res = await fetch(`${BASE_URL}/documents`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(doc), // Object to JSON text
  })
  return res.json()
}

/** Change the title and the content of the document with this id. */
export async function updateDocument(id: number, doc: Omit<DocumentItem, 'id'>): Promise<DocumentItem> {
  const res = await fetch(`${BASE_URL}/documents/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(doc),
  })
  return res.json()
}

/** Delete the document with this id (its chunks are deleted too). */
export async function deleteDocument(id: number): Promise<void> {
  await fetch(`${BASE_URL}/documents/${id}`, { method: 'DELETE' })
}

/**
 * Upload a file: the backend takes its text and saves it as a document.
 *
 * Throws an error with the backend message, like "Format not supported: .docx"
 */
export async function uploadDocument(file: File): Promise<DocumentItem> {
  const formData = new FormData()
  formData.append('file', file) // 'file' = the name of the parameter in the backend
  // No Content-Type header: with FormData the browser sets it by itself
  const res = await fetch(`${BASE_URL}/documents/upload`, {
    method: 'POST',
    body: formData,
  })
  if (!res.ok) {
    // fetch doesn't throw on 4xx/5xx, so we check it ourselves
    throw new Error(await errorMessage(res, 'Upload failed'))
  }
  return res.json()
}

/**
 * Find the 3 pieces of text closest in meaning to the query.
 *
 * Example: semanticSearch('car') also finds a document about "automobili"
 */
export async function semanticSearch(query: string): Promise<SearchResult[]> {
  // encodeURIComponent: makes the text safe in a URL, like "a & b" to "a%20%26%20b"
  const res = await fetch(`${BASE_URL}/documents/semantic-search?query=${encodeURIComponent(query)}`)
  if (!res.ok) {
    throw new Error(await errorMessage(res, 'Search failed'))
  }
  return res.json()
}