import { useEffect, useState } from 'react'
import type { DocumentItem } from './types'
import { useDocuments } from './hooks/useDocuments'
import DocumentForm from './components/DocumentForm'
import DocumentList from './components/DocumentList'
import DocumentUpload from './components/DocumentUpload'
import DocumentSearch from './components/DocumentSearch'
import Section from './components/Section'

function App() {
  const { docs, loading, loadError, createDoc, updateDoc, removeDoc, uploadDoc } = useDocuments()
  const [editingDoc, setEditingDoc] = useState<DocumentItem | null>(null)
  const [mode, setMode] = useState<'ultron' | 'vision'>('ultron')

  useEffect(() => {
    document.documentElement.dataset.mode = mode
  }, [mode])

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 py-10">
      <div className="max-w-2xl mx-auto px-4">
        <h1 className="text-6xl font-bold mb-8 tracking-tight">
          <button
            type="button"
            onClick={() => setMode((m) => (m === 'ultron' ? 'vision' : 'ultron'))}
            aria-label="Toggle theme mode"
            className="text-accent cursor-pointer"
          >
            ⬢
          </button>{' '}
          AVA
          <span className="text-zinc-500 text-lg font-normal"> / documents</span>
        </h1>
        <Section
          title={editingDoc ? 'Edit document' : 'New document'}
          description={editingDoc ? `Editing "${editingDoc.title}"` : 'Write a title and content by hand'}
        >
          <DocumentForm
            key={editingDoc?.id ?? 'new'}
            editingDoc={editingDoc}
            onCreate={createDoc}
            onUpdate={updateDoc}
            onCancel={() => setEditingDoc(null)}
          />
        </Section>
        <Section title="Semantic Search" description="Search by meaning, not by exact words">
          <DocumentSearch />
        </Section>
        <Section title="Upload a file" description="Supported formats: TXT, MD, CSV, LOG, PDF">
          <DocumentUpload onUpload={uploadDoc} />
        </Section>
        <Section title={`Your documents (${docs.length})`} description="All your saved documents">
          {loading ? (
            <div className="flex justify-center py-10">
              <div className="h-8 w-8 border-4 border-zinc-700 border-t-accent rounded-full animate-spin"></div>
            </div>
          ) : loadError ? (
            <p className="text-red-500 text-center py-10">{loadError}</p>
          ) : (
            <DocumentList docs={docs} onEdit={(doc) => setEditingDoc(doc)} onDelete={removeDoc} />
          )}
        </Section>
      </div>
    </div>
  )
}

export default App
