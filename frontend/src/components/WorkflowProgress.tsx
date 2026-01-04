'use client'

interface WorkflowStep {
  id: string
  name: string
  status: 'pending' | 'processing' | 'completed' | 'error'
  result?: any
  duration?: number
}

interface WorkflowProgressProps {
  steps: WorkflowStep[]
}

export default function WorkflowProgress({ steps }: WorkflowProgressProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-500 border-green-600'
      case 'processing':
        return 'bg-blue-500 border-blue-600 animate-pulse'
      case 'error':
        return 'bg-red-500 border-red-600'
      default:
        return 'bg-gray-300 border-gray-400'
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
        )
      case 'processing':
        return (
          <svg className="w-5 h-5 text-white animate-spin" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        )
      case 'error':
        return (
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        )
      default:
        return (
          <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        )
    }
  }

  return (
    <div className="code-vibe rounded-lg p-6 border-2 border-gray-200 bg-white shadow-sm">
      <h3 className="text-lg font-semibold text-gray-900 mb-6">Processing Workflow</h3>
      <div className="space-y-6 relative">
        {steps.map((step, index) => (
          <div key={step.id} className="flex items-start gap-4 relative">
            {/* Step Indicator */}
            <div className={`flex-shrink-0 w-10 h-10 rounded-full border-2 flex items-center justify-center ${getStatusColor(step.status)}`}>
              {getStatusIcon(step.status)}
            </div>

            {/* Connecting Line */}
            {index < steps.length - 1 && (
              <div className={`absolute left-5 w-0.5 h-16 mt-10 ${
                step.status === 'completed' ? 'bg-green-300' : 'bg-gray-300'
              }`} />
            )}

            {/* Step Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-1">
                <h4 className={`text-sm font-medium ${
                  step.status === 'completed' ? 'text-green-700' :
                  step.status === 'processing' ? 'text-blue-700' :
                  step.status === 'error' ? 'text-red-700' :
                  'text-gray-500'
                }`}>
                  {step.name}
                </h4>
                {step.duration && (
                  <span className="text-xs text-gray-500 font-mono">
                    {step.duration.toFixed(1)}s
                  </span>
                )}
              </div>

              {/* Step Result */}
              {step.result && step.status === 'completed' && (
                <div className="mt-2 p-3 bg-gray-50 rounded border border-gray-200">
                  {typeof step.result === 'object' ? (
                    <div className="space-y-1 text-xs">
                      {Object.entries(step.result).map(([key, value]) => (
                        <div key={key} className="flex gap-2">
                          <span className="font-medium text-gray-600 capitalize">{key}:</span>
                          <span className="text-gray-800">{String(value)}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-gray-700">{String(step.result)}</p>
                  )}
                </div>
              )}

              {/* Error Message */}
              {step.status === 'error' && step.result && (
                <div className="mt-2 p-3 bg-red-50 rounded border border-red-200">
                  <p className="text-xs text-red-700">{String(step.result)}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
