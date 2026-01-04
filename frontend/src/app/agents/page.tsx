'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'

interface AgentStatus {
  name: string
  status: 'healthy' | 'unhealthy' | 'unknown'
  url: string
  responseTime?: number
  lastChecked?: string
}

const AGENT_URLS = {
  router: 'http://localhost:8001',
  knowledge: 'http://localhost:8002',
  sentiment: 'http://localhost:8003',
  decision: 'http://localhost:8004',
  orchestrator: 'http://localhost:8000',
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<AgentStatus[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAgents()
    
    // Check every 5 seconds
    const interval = setInterval(checkAgents, 5000)
    return () => clearInterval(interval)
  }, [])

  const checkAgents = async () => {
    const agentChecks = Object.entries(AGENT_URLS).map(async ([name, url]) => {
      const startTime = Date.now()
      try {
        const response = await fetch(`${url}/api/health`, { 
          signal: AbortSignal.timeout(3000) 
        })
        const responseTime = Date.now() - startTime
        const data = await response.json()
        
        return {
          name,
          status: response.ok ? 'healthy' : 'unhealthy',
          url,
          responseTime,
          lastChecked: new Date().toISOString(),
        } as AgentStatus
      } catch (error) {
        return {
          name,
          status: 'unhealthy' as const,
          url,
          responseTime: Date.now() - startTime,
          lastChecked: new Date().toISOString(),
        } as AgentStatus
      }
    })

    const results = await Promise.all(agentChecks)
    setAgents(results)
    setLoading(false)
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'unhealthy':
        return 'bg-red-100 text-red-800 border-red-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return '✓'
      case 'unhealthy':
        return '✗'
      default:
        return '?'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Agents</h1>
          <p className="text-sm text-gray-600">Monitor agent status and performance</p>
        </div>

        {loading ? (
          <div className="text-center py-12 text-gray-500">
            <p>Checking agent status...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div
                key={agent.name}
                className={`code-vibe rounded-lg p-6 border-2 ${getStatusColor(agent.status)} hover-lift transition-all`}
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold capitalize mb-1">
                      {agent.name} Agent
                    </h3>
                    <p className="text-xs text-gray-600 font-mono">{agent.url}</p>
                  </div>
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    agent.status === 'healthy' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                  }`}>
                    {getStatusIcon(agent.status)}
                  </div>
                </div>

                <div className="space-y-2 mt-4 pt-4 border-t border-current border-opacity-20">
                  <div className="flex justify-between text-xs">
                    <span className="opacity-75">Status:</span>
                    <span className="font-medium uppercase">{agent.status}</span>
                  </div>
                  {agent.responseTime !== undefined && (
                    <div className="flex justify-between text-xs">
                      <span className="opacity-75">Response Time:</span>
                      <span className="font-medium">{agent.responseTime}ms</span>
                    </div>
                  )}
                  {agent.lastChecked && (
                    <div className="flex justify-between text-xs">
                      <span className="opacity-75">Last Checked:</span>
                      <span className="font-mono text-xs">
                        {new Date(agent.lastChecked).toLocaleTimeString()}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Summary Stats */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="code-vibe rounded-lg p-6 bg-green-50">
            <p className="text-xs font-medium text-gray-600 uppercase mb-1">Healthy</p>
            <p className="text-3xl font-bold text-green-700">
              {agents.filter(a => a.status === 'healthy').length}
            </p>
          </div>
          <div className="code-vibe rounded-lg p-6 bg-red-50">
            <p className="text-xs font-medium text-gray-600 uppercase mb-1">Unhealthy</p>
            <p className="text-3xl font-bold text-red-700">
              {agents.filter(a => a.status === 'unhealthy').length}
            </p>
          </div>
          <div className="code-vibe rounded-lg p-6 bg-blue-50">
            <p className="text-xs font-medium text-gray-600 uppercase mb-1">Avg Response</p>
            <p className="text-3xl font-bold text-blue-700">
              {agents.length > 0
                ? Math.round(
                    agents.reduce((sum, a) => sum + (a.responseTime || 0), 0) / agents.length
                  )
                : 0}
              ms
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
