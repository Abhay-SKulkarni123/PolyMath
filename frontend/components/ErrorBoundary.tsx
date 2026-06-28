'use client'

import { Component, ReactNode } from 'react'

interface Props {
  children: ReactNode
  fallback?: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: any) {
    console.error('Uncaught error:', error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback
      }

      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-md w-full bg-white shadow-lg rounded-lg p-8">
            <h2 className="text-2xl font-bold text-red-600 mb-4">
              Something went wrong
            </h2>
            <p className="text-gray-700 mb-4">
              We apologize for the inconvenience. An unexpected error occurred.
            </p>
            <details className="mb-4">
              <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
                Error details
              </summary>
              <pre className="mt-2 p-4 bg-gray-100 rounded text-xs overflow-auto">
                {this.state.error?.message}
                {this.state.error?.stack}
              </pre>
            </details>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition"
            >
              Try again
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}