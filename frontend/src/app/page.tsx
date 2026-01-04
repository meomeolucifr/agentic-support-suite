'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'
import { api } from '@/lib/api'

interface DashboardStats {
  totalTickets: number
  resolved: number
  escalated: number
  avgProcessingTime: number
  autoResolved: number
}

interface RecentTicket {
  ticket_id: string
  customer_id: string
  subject: string
  status: string
  created_at: string
}

export default function Home() {
  const [stats, setStats] = useState<DashboardStats>({
    totalTickets: 0,
    resolved: 0,
    escalated: 0,
    avgProcessingTime: 0,
    autoResolved: 0,
  })
  const [recentTickets, setRecentTickets] = useState<RecentTicket[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
    fetchRecentTickets()
    
    // Refresh every 5 seconds
    const interval = setInterval(() => {
      fetchStats()
      fetchRecentTickets()
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const fetchStats = async () => {
    try {
      // In production, this would come from a stats endpoint
      // For now, we'll calculate from tickets
      const response = await api.get('/api/tickets')
      const tickets = response.data || []
      
      const resolved = tickets.filter((t: any) => t.status === 'RESOLVED').length
      const escalated = tickets.filter((t: any) => t.status === 'ESCALATED').length
      
      setStats({
        totalTickets: tickets.length,
        resolved,
        escalated,
        avgProcessingTime: 8.5, // Mock data for now
        autoResolved: Math.floor(resolved * 0.7), // ~70% auto-resolve rate
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchRecentTickets = async () => {
    try {
      const response = await api.get('/api/tickets')
      const tickets = response.data || []
      setRecentTickets(tickets.slice(0, 5))
    } catch (error) {
      console.error('Error fetching tickets:', error)
    }
  }

  const statCards = [
    { label: 'Total Tickets', value: stats.totalTickets, color: 'text-gray-700', bg: 'bg-gray-50' },
    { label: 'Auto-Resolved', value: stats.autoResolved, color: 'text-green-700', bg: 'bg-green-50' },
    { label: 'Escalated', value: stats.escalated, color: 'text-orange-700', bg: 'bg-orange-50' },
    { label: 'Avg Processing', value: `${stats.avgProcessingTime.toFixed(1)}s`, color: 'text-blue-700', bg: 'bg-blue-50' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
          <p className="text-sm text-gray-600">AI Multi-Agent Customer Support System</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {statCards.map((card, idx) => (
            <div
              key={idx}
              className={`${card.bg} code-vibe rounded-lg p-6 hover-lift transition-all`}
            >
              <p className="text-xs font-medium text-gray-500 uppercase tracking-wide mb-1">
                {card.label}
              </p>
              <p className={`text-3xl font-bold ${card.color}`}>
                {loading ? '...' : card.value}
              </p>
            </div>
          ))}
        </div>

        {/* Quick Actions & Recent Tickets */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Quick Actions */}
          <div className="lg:col-span-1">
            <div className="code-vibe rounded-lg p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
              <div className="space-y-3">
                <Link
                  href="/tickets?create=true"
                  className="block w-full bg-primary-600 text-white text-center py-2 px-4 rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium shadow-sm"
                >
                  Create Ticket
                </Link>
                <Link
                  href="/agents"
                  className="block w-full bg-gray-100 text-gray-700 text-center py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
                >
                  View Agents
                </Link>
                <Link
                  href="/analytics"
                  className="block w-full bg-gray-100 text-gray-700 text-center py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium"
                >
                  View Analytics
                </Link>
              </div>
            </div>
          </div>

          {/* Recent Tickets */}
          <div className="lg:col-span-2">
            <div className="code-vibe rounded-lg p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Recent Tickets</h2>
                <Link href="/tickets" className="text-sm text-primary-600 hover:underline">
                  View All →
                </Link>
              </div>
              {recentTickets.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  <p className="text-sm">No tickets yet</p>
                  <Link href="/tickets?create=true" className="text-primary-600 hover:underline text-sm mt-2 inline-block">
                    Create your first ticket
                  </Link>
                </div>
              ) : (
                <div className="space-y-3">
                  {recentTickets.map((ticket) => (
                    <Link
                      key={ticket.ticket_id}
                      href={`/tickets/${ticket.ticket_id}`}
                      className="block p-4 bg-white rounded border border-gray-200 hover:border-primary-300 hover:shadow-sm transition-all"
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900">{ticket.subject}</p>
                          <p className="text-xs text-gray-500 mt-1">
                            {ticket.customer_id} • {new Date(ticket.created_at).toLocaleString()}
                          </p>
                        </div>
                        <span
                          className={`px-2 py-1 text-xs font-medium rounded ${
                            ticket.status === 'RESOLVED'
                              ? 'bg-green-100 text-green-800'
                              : ticket.status === 'ESCALATED'
                              ? 'bg-orange-100 text-orange-800'
                              : 'bg-gray-100 text-gray-800'
                          }`}
                        >
                          {ticket.status}
                        </span>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
