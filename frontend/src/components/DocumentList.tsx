import type { DocumentItem } from '../types'

interface DocumentListProps {
  docs: DocumentItem[]
  onEdit: (doc: DocumentItem) => void
  onDelete: (id: number) => void
}

function DocumentList({ docs, onEdit, onDelete }: DocumentListProps) {
  return (
    <ul className="flex flex-col gap-3">
      {docs.map((doc) => (
        <li
          key={doc.id}
          className="bg-zinc-950 border border-zinc-800 rounded-xl p-4 hover:border-accent/50 transition"
        >
          <h2 className="font-semibold text-zinc-100">{doc.title}</h2>
          <p className="text-zinc-400 text-sm mt-1 line-clamp-3">{doc.content}</p>
          <div className="flex items-center gap-2 mt-2">
            <button onClick={() => onDelete(doc.id)} className=" text-red-500 text-sm hover:text-red-400">
              Delete
            </button>
            <button onClick={() => onEdit(doc)} className="text-blue-500 text-sm hover:text-blue-400">
              Edit
            </button>
          </div>
        </li>
      ))}
    </ul>
  )
}

export default DocumentList
