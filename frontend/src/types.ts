export interface DocumentItem {
  id: number
  title: string
  content: string
}

export interface SearchResult {
  document_id: number
  title: string
  position: number
  content: string
}
