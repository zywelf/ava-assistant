import { useState, useEffect } from 'react'
import type { DocumentItem } from '../types'
import * as api from '../api'

export function useDocuments() {
  const [docs, setDocs] = useState<DocumentItem[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [loadError, setLoadError] = useState<string>('')

  useEffect(() => {
    async function load() {
      try {
        setLoadError('')
        const data = await api.getDocuments()
        setDocs(data)
      } catch (e) {
        console.error(e)
        setLoadError('Impossibile caricare i documenti.')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  async function createDoc(data: Omit<DocumentItem, 'id'>) {
    const created = await api.createDocument(data)
    setDocs([...docs, created])
  }

  async function updateDoc(id: number, data: Omit<DocumentItem, 'id'>) {
    const saved = await api.updateDocument(id, data)
    setDocs(docs.map((doc) => (doc.id === id ? saved : doc)))
  }

  async function removeDoc(id: number) {
    await api.deleteDocument(id)
    setDocs(docs.filter((doc) => doc.id !== id))
  }

  async function uploadDoc(file: File) {
    const uploaded = await api.uploadDocument(file)
    setDocs([...docs, uploaded])
  }

  return { docs, loading, loadError, createDoc, updateDoc, removeDoc, uploadDoc }
}
