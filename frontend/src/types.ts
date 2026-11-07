export interface DocumentItem {
  id: number
  title: string
  content: string
}

export interface SearchResult {
  document_id: string
  title: string
  position: string
  content: string
}
