import { useState } from 'react'
import type { DocumentItem } from './types'
import { useDocuments } from './hooks/useDocuments'
import DocumentForm from './components/DocumentForm'
import DocumentList from './components/DocumentList'
import DocumentUpload from './components/DocumentUpload'

function App() {
  const { docs, loading, loadError, createDoc, updateDoc, removeDoc, uploadDoc } = useDocuments()
  const [editingDoc, setEditingDoc] = useState<DocumentItem | null>(null)

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 py-10">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8 tracking-tight">
          <span className="text-red-500">⬢</span> BABY ULTRON
          <span className="text-zinc-500 text-lg font-normal"> / documenti</span>
        </h1>

        <DocumentForm
          key={editingDoc?.id ?? 'new'}
          editingDoc={editingDoc}
          onCreate={createDoc}
          onUpdate={updateDoc}
          onCancel={() => setEditingDoc(null)}
        />
        <DocumentUpload onUpload={uploadDoc} />

        {loading ? (
          <div className="flex justify-center py-10">
            <div className="h-8 w-8 border-4 border-zinc-700 border-t-red-500 rounded-full animate-spin"></div>
          </div>
        ) : loadError ? (
          <p className="text-red-500 text-center py-10">{loadError}</p>
        ) : (
          <DocumentList docs={docs} onEdit={(doc) => setEditingDoc(doc)} onDelete={removeDoc} />
        )}
      </div>
    </div>
  )
}

export default App
