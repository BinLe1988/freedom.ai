import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard - Freedom.AI',
  description: '你的自由度仪表板 - 探索人生可能性',
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-gray-900">
      {children}
    </div>
  )
}
