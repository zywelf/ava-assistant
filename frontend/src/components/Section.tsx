import type { ReactNode } from 'react'

interface SectionProps {
  title: string
  description: string
  children: ReactNode
}

function Section({ title, description, children }: SectionProps) {
  return (
    <section className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 mb-6 hover:border-accent/50 transition-colors duration-300">
      <h2 className="text-lg font-semibold text-zinc-100">{title}</h2>
      <p className="text-zinc-500 text-sm mb-4">{description}</p>
      {children}
    </section>
  )
}

export default Section
