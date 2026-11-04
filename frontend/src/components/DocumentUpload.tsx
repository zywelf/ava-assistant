import { useState } from 'react'

interface DocumentUploadProps {
  onUpload: (file: File) => Promise<void>
}

function DocumentUpload({ onUpload }: DocumentUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploadError, setUploadError] = useState<string>('')
  const [uploadSuccess, setUploadSuccess] = useState<string>('')
  const [inputKey, setInputKey] = useState<number>(0)

  async function handleUpload() {
    if (!selectedFile) return
    try {
      setUploadError('')
      await onUpload(selectedFile)
      setUploadSuccess(`"${selectedFile.name}" uploaded successfully`)
      setTimeout(() => setUploadSuccess(''), 3000)
      setSelectedFile(null)
      setInputKey((k) => k + 1)
    } catch (e) {
      setUploadError(e instanceof Error ? e.message : 'Upload failed')
    }
  }

  return (
    <div className="my-6 flex flex-wrap items-center gap-3">
      <input
        key={inputKey}
        type="file"
        onChange={(e) => setSelectedFile(e.target.files?.[0] ?? null)}
        className="text-sm text-zinc-400 file:mr-3 file:rounded-lg file:border-0 file:bg-zinc-800 file:px-4 file:py-2 file:text-sm file:font-medium file:text-zinc-100 hover:file:bg-zinc-700 file:cursor-pointer"
      />
      <button
        onClick={handleUpload}
        disabled={!selectedFile}
        className="rounded-lg bg-accent-strong px-4 py-2 text-sm font-semibold text-accent-contrast hover:bg-accent disabled:opacity-40 disabled:cursor-not-allowed transition"
      >
        Upload
      </button>
      {uploadError && <p className="w-full text-red-500 text-sm">{uploadError}</p>}
      {uploadSuccess && <p className="w-full text-emerald-500 text-sm">{uploadSuccess}</p>}
    </div>
  )
}

export default DocumentUpload
