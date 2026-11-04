import { useState } from 'react'
import type { DocumentItem } from '../types'
import { semanticSearch } from '../api'

function DocumentSearch() {
  const [query, setQuery] = useState<string>('')
  const [results, setResult] = useState<DocumentItem[] | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')

  async function handleSearch() {
    try {
      setError('')
      setLoading(true)
      const data = await semanticSearch(query)
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Search failed')
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="flex flex-col gap-3">
      <form
        onSubmit={(e) => {
          e.preventDefault()
          handleSearch()
        }}
        className="flex gap-3"
      >
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by meaning…"
          className="flex-1 bg-zinc-950 border border-zinc-700 rounded px-3 py-2 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-accent"
        />
        <button
          disabled={query.trim() === '' || loading}
          className="bg-accent-strong text-accent-contrast rounded px-4 py-2 font-medium hover:bg-accent transition uppercase tracking-wide text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? '…' : 'Search'}
        </button>
      </form>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      {results !== null && results.length === 0 && (
        <p className="text-zinc-500 text-sm">No documents to search yet: add one to get started</p>
      )}

      {results !== null && results.length > 0 && (
        <ol className="flex flex-col gap-3">
          {results.map((doc, index) => (
            <li key={doc.id} className="bg-zinc-950 border border-zinc-800 rounded-lg p-4">
              <h3 className="font-semibold text-zinc-100">
                <span className="text-accent mr-2">#{index + 1}</span>
                {doc.title}
              </h3>
              <p className="text-zinc-400 text-sm mt-1 line-clamp-2">{doc.content}</p>
            </li>
          ))}
        </ol>
      )}
    </div>
  )
}

export default DocumentSearch
