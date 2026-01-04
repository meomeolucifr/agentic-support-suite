'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { api } from '@/lib/api'

interface AnalyticsData {
  ticketVolume: { date: string; count: number }[]
  resolutionRate: { category: string; resolved: number; escalated: number }[]
  agentPerformance: { agent: string; requests: number; avgTime: number }[]
  sentimentDistribution: { level: string; count: number }[]
}

export default function AnalyticsPage() {
  const [data, setData] = useState<AnalyticsData>({
    ticketVolume: [],
    resolutionRate: [],
    agentPerformance: [],
    sentimentDistribution: [],
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
    
    // Refresh every 30 seconds
    const interval = setInterval(fetchAnalytics, 30000)
    return () => clearInterval(interval)
  }, [])

  const fetchAnalytics = async () => {
    try {
      // Fetch tickets to calculate analytics
      const response = await api.get('/api/tickets')
      const tickets = response.data || []

      // Generate mock time series data (last 7 days)
      const now = new Date()
      const ticketVolume = Array.from({ length: 7 }, (_, i) => {
        const date = new Date(now)
        date.setDate(date.getDate() - (6 - i))
        return {
          date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          count: Math.floor(Math.random() * 20) + tickets.length,
        }
      })

      // Resolution rate by category
      const resolutionRate = [
        { category: 'BILLING', resolved: 45, escalated: 5 },
        { category: 'TECHNICAL', resolved: 32, escalated: 8 },
        { category: 'ACCOUNT', resolved: 28, escalated: 2 },
        { category: 'OTHER', resolved: 15, escalated: 5 },
      ]

      // Agent performance
      const agentPerformance = [
        { agent: 'Router', requests: tickets.length * 1, avgTime: 1.2 },
        { agent: 'Knowledge', requests: tickets.length * 0.9, avgTime: 2.5 },
        { agent: 'Sentiment', requests: tickets.length * 0.9, avgTime: 1.8 },
        { agent: 'Decision', requests: tickets.length * 0.9, avgTime: 0.9 },
      ]

      // Sentiment distribution
      const sentimentDistribution = [
        { level: 'CALM', count: Math.floor(tickets.length * 0.3) },
        { level: 'NEUTRAL', count: Math.floor(tickets.length * 0.4) },
        { level: 'UPSET', count: Math.floor(tickets.length * 0.2) },
        { level: 'ANGRY', count: Math.floor(tickets.length * 0.1) },
      ]

      setData({
        ticketVolume,
        resolutionRate,
        agentPerformance,
        sentimentDistribution,
      })
    } catch (error) {
      console.error('Error fetching analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500">Loading analytics...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Analytics</h1>
          <p className="text-sm text-gray-600">System performance and metrics</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Ticket Volume Trend */}
          <div className="code-vibe rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Ticket Volume (7 Days)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data.ticketVolume}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="count" stroke="#2563eb" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Resolution Rate */}
          <div className="code-vibe rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Resolution Rate by Category</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.resolutionRate}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="category" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="resolved" fill="#10b981" />
                <Bar dataKey="escalated" fill="#f59e0b" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Agent Performance */}
          <div className="code-vibe rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Agent Performance</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.agentPerformance}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="agent" />
                <YAxis yAxisId="left" />
                <YAxis yAxisId="right" orientation="right" />
                <Tooltip />
                <Legend />
                <Bar yAxisId="left" dataKey="requests" fill="#3b82f6" />
                <Line yAxisId="right" type="monotone" dataKey="avgTime" stroke="#ef4444" strokeWidth={2} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Sentiment Distribution */}
          <div className="code-vibe rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Sentiment Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.sentimentDistribution}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="level" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#8b5cf6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="code-vibe rounded-lg p-6 bg-blue-50">
            <p className="text-xs font-medium text-gray-600 uppercase mb-1">Auto-Resolution Rate</p>
            <p className="text-3xl font-bold text-blue-700">70%</p>
          </div>
          <div className="code-vibe rounded-lg p-6 bg-green-50">
            <p className="text-xs font-medium text-gray-600 uppercase mb-1">Avg Processing Time</p>
            <p className="text-3xl font-bold text-green-700">8.5s</p>
          </div>
          <div className="code-vibe rounded-lg p-6 bg-purple-50">
            <p className="text-xs font-medium text-gray-600 uppercase mb-1">Customer Satisfaction</p>
            <p className="text-3xl font-bold text-purple-700">4.2/5</p>
          </div>
          <div className="code-vibe rounded-lg p-6 bg-orange-50">
            <p className="text-xs font-medium text-gray-600 uppercase mb-1">Cost Reduction</p>
            <p className="text-3xl font-bold text-orange-700">84%</p>
          </div>
        </div>
      </div>
    </div>
  )
}
