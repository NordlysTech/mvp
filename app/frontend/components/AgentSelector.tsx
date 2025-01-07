import { motion } from 'framer-motion'
import { Book, Cog, Calculator, FileText, Plus } from 'lucide-react'
import { Agent } from './AdvancedAIInterface'

const agents = [
  { id: 'knowledge', name: 'Knowledge AI', icon: Book, color: 'bg-blue-500' },
  { id: 'action', name: 'Action AI', icon: Cog, color: 'bg-green-500' },
  { id: 'solver', name: 'Dynamic AI Solver', icon: Calculator, color: 'bg-purple-500' },
  { id: 'report', name: 'Report Generator', icon: FileText, color: 'bg-orange-500' },
  { id: 'custom', name: 'Custom Agent', icon: Plus, color: 'bg-gray-500' },
]

interface AgentSelectorProps {
  selectedAgent: Agent
  onSelectAgent: (agent: Agent) => void
}

export default function AgentSelector({ selectedAgent, onSelectAgent }: AgentSelectorProps) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 mb-6">
      {agents.map((agent) => (
        <motion.button
          key={agent.id}
          className={`p-4 rounded-lg ${
            selectedAgent === agent.id ? 'bg-gray-700' : 'bg-gray-800'
          } hover:bg-gray-700 transition-colors flex flex-col items-center justify-center`}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onSelectAgent(agent.id as Agent)}
        >
          <div className={`w-12 h-12 ${agent.color} rounded-full flex items-center justify-center mb-2`}>
            <agent.icon className="w-6 h-6 text-white" />
          </div>
          <span className="text-sm font-medium">{agent.name}</span>
        </motion.button>
      ))}
    </div>
  )
}

