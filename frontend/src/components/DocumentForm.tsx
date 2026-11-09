import { useState } from 'react'
import type { DocumentItem } from '../types'

interface DocumentFormProps {
  editingDoc: DocumentItem | null
  onCreate: (data: Omit<DocumentItem, 'id'>) => Promise<void>
  onUpdate: (id: number, data: Omit<DocumentItem, 'id'>) => Promise<void>
  onCancel: () => void
}

function DocumentForm({ editingDoc, onCreate, onUpdate, onCancel }: DocumentFormProps) {
  const [title, setTitle] = useState<string>(editingDoc?.title ?? '')
  const [content, setContent] = useState<string>(editingDoc?.content ?? '')
  const [error, setError] = useState<string>('')

  async function handleSubmit() {
    if (title.trim() === '') {
      setError('Title is required')
      return
    }
    setError('')
    const data: Omit<DocumentItem, 'id'> = { title: title.trim(), content }
    try {
      if (editingDoc === null) {
        await onCreate(data)
        setTitle('')
        setContent('')
      } else {
        await onUpdate(editingDoc.id, data)
        onCancel()
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Upload failed')
    }
  }

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        handleSubmit()
      }}
      className="flex flex-col gap-3"
    >
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Title"
        className="bg-zinc-950 border border-zinc-700 rounded px-3 py-2 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-accent"
      />
      {error && <p className="text-red-500 text-sm">{error}</p>}
      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Content"
        rows={4}
        className="bg-zinc-950 border border-zinc-700 rounded px-3 py-2 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-accent"
      />
      <div className="flex gap-3">
        <button
          disabled={title.trim() === ''}
          className="bg-accent-strong text-accent-contrast rounded px-4 py-2 font-medium hover:bg-accent transition self-start uppercase tracking-wide text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          {editingDoc === null ? 'Create' : 'Update'}
        </button>
        {editingDoc !== null && (
          <button
            type="button"
            onClick={onCancel}
            className="bg-blue-600 text-white rounded px-4 py-2 font-medium hover:bg-blue-500 transition self-start uppercase tracking-wide text-sm"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}

export default DocumentForm
