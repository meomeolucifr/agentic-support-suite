'use client'

'use client'

import { useEffect, useState } from 'react'
import { useSearchParams } from 'next/navigation'
import { api } from '@/lib/api'
import WorkflowProgress from '@/components/WorkflowProgress'

interface Ticket {
  ticket_id: string
  customer_id: string
  subject: string
  body: string
  status: string
  priority: string
  created_at: string
  decision?: string
  solution?: string
}

interface WorkflowStep {
  id: string
  name: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  result?: any
  duration?: number
}

export default function TicketsPage() {
  const searchParams = useSearchParams()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(searchParams.get('create') === 'true')
  const [creating, setCreating] = useState(false)
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([])
  const [showWorkflow, setShowWorkflow] = useState(false)

  const [formData, setFormData] = useState({
    customer_id: '',
    subject: '',
    body: '',
  })

  useEffect(() => {
    fetchTickets()
    
    // Refresh every 10 seconds
    const interval = setInterval(fetchTickets, 10000)
    return () => clearInterval(interval)
  }, [])

  const fetchTickets = async () => {
    try {
      const response = await api.get('/api/tickets')
      setTickets(response.data || [])
    } catch (error: any) {
      if (error.response?.status !== 404) {
        console.error('Error fetching tickets:', error)
      }
    } finally {
      setLoading(false)
    }
  }

  const initializeWorkflow = () => {
    setWorkflowSteps([
      { id: 'router', name: 'Router Agent - Classifying ticket', status: 'pending' },
      { id: 'knowledge', name: 'Knowledge Agent - Searching solutions', status: 'pending' },
      { id: 'sentiment', name: 'Sentiment Agent - Analyzing emotion', status: 'pending' },
      { id: 'decision', name: 'Decision Engine - Making decision', status: 'pending' },
      { id: 'complete', name: 'Processing complete', status: 'pending' },
    ])
  }

  const updateWorkflowStep = (stepId: string, status: WorkflowStep['status'], result?: any, duration?: number) => {
    setWorkflowSteps(prev => {
      const updated = prev.map(step => 
        step.id === stepId ? { ...step, status, result, duration } : step
      )
      return updated
    })
  }

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault()
    setCreating(true)
    setShowWorkflow(true)
    initializeWorkflow()

    const startTime = Date.now()

    try {
      // Simulate workflow steps (since we can't get real-time updates, we'll simulate based on response)
      updateWorkflowStep('router', 'processing')
      
      const response = await api.post('/api/tickets', formData, {
        timeout: 60000,
      })

      const totalDuration = (Date.now() - startTime) / 1000
      const workflow = response.data.workflow || {}

      // Update workflow steps with REAL data from agents
      const routerData = workflow.router || {}
      updateWorkflowStep('router', 'completed', { 
        category: routerData.category || 'UNKNOWN',
        subcategory: routerData.subcategory || '-',
        confidence: routerData.confidence ? `${(routerData.confidence * 100).toFixed(1)}%` : '-',
        reason: routerData.reason || '-'
      }, totalDuration * 0.25)
      
      setTimeout(() => {
        updateWorkflowStep('knowledge', 'processing')
        setTimeout(() => {
          const knowledgeData = workflow.knowledge || {}
          updateWorkflowStep('knowledge', 'completed', {
            similar_cases_found: knowledgeData.similar_cases_found || 0,
            similarity_score: knowledgeData.similarity_score ? knowledgeData.similarity_score.toFixed(3) : '-',
            solution: knowledgeData.solution || 'No solution found',
            confidence: knowledgeData.confidence ? `${(knowledgeData.confidence * 100).toFixed(1)}%` : '-'
          }, totalDuration * 0.25)
          
          setTimeout(() => {
            updateWorkflowStep('sentiment', 'processing')
            setTimeout(() => {
              const sentimentData = workflow.sentiment || {}
              updateWorkflowStep('sentiment', 'completed', {
                score: sentimentData.score ? sentimentData.score.toFixed(2) : '-',
                level: sentimentData.level || '-',
                urgency: sentimentData.urgency || '-',
                churn_risk: sentimentData.churn_risk ? 'Yes' : 'No',
                recommended_handler: sentimentData.recommended_handler || '-'
              }, totalDuration * 0.25)
              
              setTimeout(() => {
                updateWorkflowStep('decision', 'processing')
                setTimeout(() => {
                  const decisionData = workflow.decision || {}
                  updateWorkflowStep('decision', 'completed', {
                    decision: decisionData.decision || response.data.decision || 'ESCALATED',
                    confidence: decisionData.confidence ? `${(decisionData.confidence * 100).toFixed(1)}%` : '-',
                    priority: decisionData.priority || '-',
                    reasoning: decisionData.reasoning || '-'
                  }, totalDuration * 0.15)
                  
                  setTimeout(() => {
                    updateWorkflowStep('complete', 'completed', {
                      status: response.data.status,
                      message: response.data.message || 'Ticket processed successfully'
                    }, totalDuration * 0.1)
                    
                    // Save workflow to localStorage with REAL data
                    setTimeout(() => {
                      setWorkflowSteps(currentSteps => {
                        const finalSteps = currentSteps.map(step => {
                          if (step.id === 'router') {
                            return { ...step, result: routerData }
                          } else if (step.id === 'knowledge') {
                            return { ...step, result: knowledgeData }
                          } else if (step.id === 'sentiment') {
                            return { ...step, result: sentimentData }
                          } else if (step.id === 'decision') {
                            return { ...step, result: decisionData }
                          }
                          return step
                        })
                        localStorage.setItem(`workflow_${response.data.ticket_id}`, JSON.stringify(finalSteps))
                        localStorage.setItem(`workflow_data_${response.data.ticket_id}`, JSON.stringify(workflow))
                        return finalSteps
                      })
                    }, 100)
                    
                    // Save ticket to localStorage
                    const ticketData = {
                      ticket_id: response.data.ticket_id,
                      customer_id: formData.customer_id,
                      subject: formData.subject,
                      body: formData.body,
                      status: response.data.status,
                      priority: 'MEDIUM',
                      created_at: new Date().toISOString(),
                      decision: response.data.decision,
                      solution: response.data.solution,
                    }
                    localStorage.setItem(`ticket_${response.data.ticket_id}`, JSON.stringify(ticketData))
                    
                    // Don't auto-close, just refresh tickets list
                    fetchTickets()
                    setCreating(false)
                    
                    // Show success message with link to view details
                    alert(`Ticket created successfully!\n\nTicket ID: ${response.data.ticket_id}\nStatus: ${response.data.status}\n\nClick OK to view ticket details.`)
                    
                    // Navigate to ticket detail page
                    window.location.href = `/tickets/${response.data.ticket_id}`
                  }, 300)
                }, 500)
              }, 300)
            }, 500)
          }, 300)
        }, 500)
      }, 500)

    } catch (error: any) {
      console.error('Error creating ticket:', error)
      
      // Mark current step as error
      const currentStep = workflowSteps.find(s => s.status === 'processing')
      if (currentStep) {
        updateWorkflowStep(currentStep.id, 'error', error.message || 'Processing failed')
      }
      
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        alert('Request timed out. The ticket is being processed but may take longer. Please check back in a moment.')
      } else if (error.code === 'ECONNREFUSED') {
        alert('Cannot connect to server. Please make sure the Orchestrator is running on port 8000.')
      } else {
        alert(`Error: ${error.response?.data?.detail || error.message || 'Failed to create ticket'}`)
      }
      setCreating(false)
      setShowWorkflow(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Tickets</h1>
            <p className="text-sm text-gray-600">Manage and track support tickets</p>
          </div>
          <button
            onClick={() => {
              setShowCreate(!showCreate)
              if (showCreate) {
                setShowWorkflow(false)
                setWorkflowSteps([])
              }
            }}
            className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium shadow-sm"
          >
            {showCreate ? 'Cancel' : 'Create Ticket'}
          </button>
        </div>

        {/* Workflow Progress */}
        {showWorkflow && workflowSteps.length > 0 && (
          <div className="mb-6">
            <WorkflowProgress steps={workflowSteps} />
          </div>
        )}

        {/* Create Ticket Form */}
        {showCreate && (
          <div className="code-vibe rounded-lg p-6 mb-6 border-2 border-primary-200 bg-white shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Create New Ticket</h2>
            <form onSubmit={handleCreateTicket} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Customer ID
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.customer_id}
                    onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                    placeholder="CUST_001"
                    disabled={creating}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Subject
                  </label>
                  <input
                    type="text"
                    required
                    value={formData.subject}
                    onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                    placeholder="Brief description of the issue"
                    disabled={creating}
                  />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  required
                  value={formData.body}
                  onChange={(e) => setFormData({ ...formData, body: e.target.value })}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                  placeholder="Detailed description of the issue..."
                  disabled={creating}
                />
              </div>
              <button
                type="submit"
                disabled={creating}
                className="bg-primary-600 text-white px-6 py-2 rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 shadow-sm"
              >
                {creating && (
                  <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                )}
                {creating ? 'Processing...' : 'Submit Ticket'}
              </button>
            </form>
          </div>
        )}

        {/* Tickets Table */}
        <div className="code-vibe rounded-lg overflow-hidden bg-white shadow-sm">
          {loading ? (
            <div className="p-8 text-center text-gray-500">
              <p>Loading tickets...</p>
            </div>
          ) : tickets.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              <p className="mb-2">No tickets found</p>
              <button
                onClick={() => setShowCreate(true)}
                className="text-primary-600 hover:underline text-sm"
              >
                Create your first ticket
              </button>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Ticket ID
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Customer
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Subject
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Decision
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {tickets.map((ticket) => (
                    <tr key={ticket.ticket_id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <a
                          href={`/tickets/${ticket.ticket_id}`}
                          className="text-sm font-mono text-primary-600 hover:underline"
                        >
                          {ticket.ticket_id}
                        </a>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm text-gray-600">{ticket.customer_id}</span>
                      </td>
                      <td className="px-6 py-4">
                        <span className="text-sm text-gray-900">{ticket.subject}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
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
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-xs text-gray-600">
                          {ticket.decision || '-'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(ticket.created_at).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
