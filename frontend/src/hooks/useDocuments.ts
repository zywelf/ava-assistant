import { useState, useEffect } from 'react'
import type { DocumentItem } from '../types'
import * as api from '../api'

/**
 * Keep the list of documents and give the functions to change it.
 *
 * Example: const { docs, createDoc, removeDoc } = useDocuments()
 */
export function useDocuments() {
  const [docs, setDocs] = useState<DocumentItem[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [loadError, setLoadError] = useState<string>('')

  // Load the documents once, when the page opens ([] = only the first time)
  useEffect(() => {
    async function load() {
      try {
        setLoadError('')
        const data = await api.getDocuments()
        setDocs(data)
      } catch (e) {
        console.error(e)
        setLoadError('Could not load documents.')
      } finally {
        setLoading(false) // Stop the spinner, with or without errors
      }
    }
    load()
  }, [])

  // Each function calls the API, then updates the list with a NEW array,
  // so React sees the change and redraws the page

  /** Create a document and add it at the end of the list. */
  async function createDoc(data: Omit<DocumentItem, 'id'>) {
    const created = await api.createDocument(data)
    setDocs([...docs, created])
  }

  /** Change a document and replace it in the list. */
  async function updateDoc(id: number, data: Omit<DocumentItem, 'id'>) {
    const saved = await api.updateDocument(id, data)
    setDocs(docs.map((doc) => (doc.id === id ? saved : doc)))
  }

  /** Delete a document and remove it from the list. */
  async function removeDoc(id: number) {
    await api.deleteDocument(id)
    setDocs(docs.filter((doc) => doc.id !== id))
  }

  /** Upload a file and add the new document at the end of the list. */
  async function uploadDoc(file: File) {
    const uploaded = await api.uploadDocument(file)
    setDocs([...docs, uploaded])
  }

  return { docs, loading, loadError, createDoc, updateDoc, removeDoc, uploadDoc }
}