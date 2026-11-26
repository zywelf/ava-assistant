import { useState } from 'react'
import type { AskResponse } from '../types'
import { askQuestion } from '../api'

function DocumentAsk() {
  const [question, setQuestion] = useState<string>('')
  const [response, setResponse] = useState<AskResponse | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')
  const [openSource, setOpenSource] = useState<number | null>(null)

  async function handleAsk() {
    try {
      setError('')
      setResponse(null)
      setOpenSource(null)
      setLoading(true)
      const data = await askQuestion(question)
      setResponse(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Response failed')
    } finally {
      setLoading(false)
    }
  }
  return (
    <div className="flex flex-col gap-3">
      <form
        onSubmit={(e) => {
          e.preventDefault()
          handleAsk()
        }}
        className="flex gap-3"
      >
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="flex-1 bg-zinc-950 border border-zinc-700 rounded px-3 py-2 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-accent"
        />
        <button
          disabled={question.trim() === '' || loading}
          className="bg-accent-strong text-accent-contrast rounded px-4 py-2 font-medium hover:bg-accent transition uppercase tracking-wide text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? 'Thinking…' : 'Ask'}
        </button>
      </form>

      {error && <p className="text-red-500 text-sm">{error}</p>}

      {response !== null && (
        <div className="flex flex-col gap-3">
          <p className="bg-zinc-950 border-l-4 border-accent rounded p-4 text-zinc-100 whitespace-pre-wrap">
            {response.answer.split(/(\[\d+\])/).map((part, i) =>
              /^\[\d+\]$/.test(part) ? (
                <span
                  key={i}
                  onClick={() => setOpenSource(Number(part.slice(1, -1)))}
                  className="text-accent font-semibold cursor-pointer"
                >
                  {part}
                </span>
              ) : (
                part
              )
            )}
          </p>
          {response.sources.length > 0 && (
            <ol className="flex flex-col gap-2">
              {response.sources.map((source) => (
                <li
                  key={`${source.document_id}-${source.position}`}
                  onClick={() => setOpenSource(openSource === source.number ? null : source.number)}
                  className={`bg-zinc-950 border rounded-lg p-3 cursor-pointer hover:border-accent/50 transition-colors duration-300 ${
                    openSource === source.number ? 'border-accent' : 'border-zinc-800'
                  }`}
                >
                  <h3 className="text-sm font-semibold text-zinc-300">
                    <span className="text-accent mr-2">[{source.number}]</span>
                    {source.title}
                    <span className="text-zinc-500 font-normal"> · part {source.position + 1}</span>
                  </h3>
                  <p
                    className={`text-zinc-500 text-xs mt-1 ${openSource === source.number ? '' : 'line-clamp-2'}`}
                  >
                    {source.content}
                  </p>
                </li>
              ))}
            </ol>
          )}
        </div>
      )}
    </div>
  )
}

export default DocumentAsk
