import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { StarryEffects } from '@/components/effects/StarryEffects'
import { Providers } from '@/components/providers/Providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Freedom.AI - 自由探索人生可能性',
  description: '让AI成为你探索自由人生的得力助手，在寻找自由的路上发现无限可能性',
  keywords: ['AI', '自由', '人生规划', '职业发展', '机会探索'],
  authors: [{ name: 'Freedom.AI Team' }],
  viewport: 'width=device-width, initial-scale=1',
  themeColor: '#6c5ce7',
  openGraph: {
    title: 'Freedom.AI - 自由探索人生可能性',
    description: '让AI成为你探索自由人生的得力助手',
    type: 'website',
    locale: 'zh_CN',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className="dark">
      <body className={inter.className}>
        <Providers>
          <StarryEffects />
          <div className="relative z-10">
            {children}
          </div>
        </Providers>
      </body>
    </html>
  )
}
