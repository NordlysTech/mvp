'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import Sidebar from './Sidebar'
import AgentSelector from './AgentSelector'
import ChatInterface from './ChatInterface'

export type Agent = 'knowledge' | 'action' | 'solver' | 'report' | 'custom'

export default function AdvancedAIInterface() {
  const [selectedAgent, setSelectedAgent] = useState<Agent>('knowledge')

  return (
    <div className="flex w-full h-screen">
      <Sidebar />
      <motion.div 
        className="flex-grow p-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className="text-3xl font-bold mb-6">Solvi AI Interface</h1>
        <AgentSelector selectedAgent={selectedAgent} onSelectAgent={setSelectedAgent} />
        <ChatInterface selectedAgent={selectedAgent} />
      </motion.div>
    </div>
  )
}

