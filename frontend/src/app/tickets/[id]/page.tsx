'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { api } from '@/lib/api'
import WorkflowProgress from '@/components/WorkflowProgress'

interface WorkflowStep {
  id: string
  name: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  result?: any
  duration?: number
}

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

export default function TicketDetailPage() {
  const params = useParams()
  const router = useRouter()
  const ticketId = params.id as string
  const [ticket, setTicket] = useState<Ticket | null>(null)
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTicketData()
  }, [ticketId])

  const loadTicketData = () => {
    // Load ticket from API
    api.get(`/api/tickets/${ticketId}`)
      .then(response => {
        setTicket(response.data)
        
        // Build workflow steps from API data
        if (response.data.workflow) {
          const workflow = response.data.workflow
          const steps: WorkflowStep[] = []
          
          if (workflow.router) {
            steps.push({
              id: 'router',
              name: 'Router Agent - Classifying ticket',
              status: 'completed',
              result: {
                category: workflow.router.category,
                subcategory: workflow.router.subcategory || '-',
                confidence: workflow.router.confidence ? `${(workflow.router.confidence * 100).toFixed(1)}%` : '-',
                reason: workflow.router.reason || '-'
              }
            })
          }
          
          if (workflow.knowledge) {
            steps.push({
              id: 'knowledge',
              name: 'Knowledge Agent - Searching solutions',
              status: 'completed',
              result: {
                similar_cases_found: workflow.knowledge.similar_cases_found || 0,
                similarity_score: workflow.knowledge.similarity_score ? workflow.knowledge.similarity_score.toFixed(3) : '-',
                solution: workflow.knowledge.solution || 'No solution found',
                confidence: workflow.knowledge.confidence ? `${(workflow.knowledge.confidence * 100).toFixed(1)}%` : '-'
              }
            })
          }
          
          if (workflow.sentiment) {
            steps.push({
              id: 'sentiment',
              name: 'Sentiment Agent - Analyzing emotion',
              status: 'completed',
              result: {
                score: workflow.sentiment.score ? workflow.sentiment.score.toFixed(2) : '-',
                level: workflow.sentiment.level || '-',
                urgency: workflow.sentiment.urgency || '-',
                churn_risk: workflow.sentiment.churn_risk ? 'Yes' : 'No',
                recommended_handler: workflow.sentiment.recommended_handler || '-'
              }
            })
          }
          
          if (workflow.decision) {
            steps.push({
              id: 'decision',
              name: 'Decision Engine - Making decision',
              status: 'completed',
              result: {
                decision: workflow.decision.decision,
                confidence: workflow.decision.confidence ? `${(workflow.decision.confidence * 100).toFixed(1)}%` : '-',
                priority: workflow.decision.priority || '-',
                reasoning: workflow.decision.reasoning || '-'
              }
            })
          }
          
          steps.push({
            id: 'complete',
            name: 'Processing complete',
            status: 'completed',
            result: {
              status: response.data.status,
              message: 'Ticket processed successfully'
            }
          })
          
          setWorkflowSteps(steps)
        }
      })
      .catch(() => {
        // If API fails, try to load from localStorage
        const savedTicket = localStorage.getItem(`ticket_${ticketId}`)
        if (savedTicket) {
          setTicket(JSON.parse(savedTicket))
        }
        
        // Load workflow from localStorage
        const savedWorkflow = localStorage.getItem(`workflow_${ticketId}`)
        if (savedWorkflow) {
          setWorkflowSteps(JSON.parse(savedWorkflow))
        }
      })
      .finally(() => setLoading(false))
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500">Loading ticket...</p>
      </div>
    )
  }

  if (!ticket) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <button
            onClick={() => router.back()}
            className="text-primary-600 hover:underline mb-4"
          >
            ← Back to Tickets
          </button>
          <div className="text-center py-12">
            <p className="text-gray-500">Ticket not found</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button
          onClick={() => router.back()}
          className="text-primary-600 hover:underline mb-6 text-sm"
        >
          ← Back to Tickets
        </button>

        {/* Ticket Info */}
        <div className="code-vibe rounded-lg p-6 mb-6 bg-white shadow-sm">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 mb-2">{ticket.subject}</h1>
              <p className="text-sm text-gray-600">
                Ticket ID: <span className="font-mono">{ticket.ticket_id}</span>
              </p>
            </div>
            <span
              className={`px-3 py-1 text-xs font-medium rounded ${
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

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <p className="text-xs font-medium text-gray-500 uppercase mb-1">Customer</p>
              <p className="text-sm text-gray-900">{ticket.customer_id}</p>
            </div>
            <div>
              <p className="text-xs font-medium text-gray-500 uppercase mb-1">Created</p>
              <p className="text-sm text-gray-900">{new Date(ticket.created_at).toLocaleString()}</p>
            </div>
          </div>

          <div>
            <p className="text-xs font-medium text-gray-500 uppercase mb-1">Description</p>
            <p className="text-sm text-gray-700 whitespace-pre-wrap">{ticket.body}</p>
          </div>

          {ticket.decision && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-xs font-medium text-gray-500 uppercase mb-1">Decision</p>
              <p className="text-sm text-gray-900">{ticket.decision}</p>
            </div>
          )}

          {ticket.solution && (
            <div className="mt-4 pt-4 border-t border-gray-200">
              <p className="text-xs font-medium text-gray-500 uppercase mb-1">Solution</p>
              <p className="text-sm text-gray-700 whitespace-pre-wrap">{ticket.solution}</p>
            </div>
          )}
        </div>

        {/* Workflow Log */}
        {workflowSteps.length > 0 && (
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Processing Workflow</h2>
            <WorkflowProgress steps={workflowSteps} />
          </div>
        )}

        {workflowSteps.length === 0 && (
          <div className="code-vibe rounded-lg p-6 bg-white shadow-sm">
            <p className="text-sm text-gray-500 text-center">
              No workflow log available for this ticket
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

