'use client'

import { Send, Zap, Copy } from 'lucide-react'

export default function QueryInput() {
  return (
    <div className="p-4 border-t border-gray-800 bg-gray-900/50">
      <div className="max-w-6xl mx-auto flex items-center gap-2">
        <input
          type="text"
          placeholder="Ask anything..."
          className="flex-1 bg-gray-800 text-white rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button className="p-3 bg-gray-800 hover:bg-gray-700 rounded-lg">
          <Copy className="w-5 h-5" />
        </button>
        <button className="p-3 bg-gray-800 hover:bg-gray-700 rounded-lg">
          <Zap className="w-5 h-5" />
        </button>
        <button className="p-3 bg-emerald-500 hover:bg-emerald-600 rounded-lg">
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  )
}

