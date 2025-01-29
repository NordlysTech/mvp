'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { FileText, AlertTriangle, Shield, ClipboardList, FileCheck, List, Gauge, Wrench, PenLineIcon as PipeLine, Layers } from 'lucide-react'
import { Card } from "@/components/ui/card"
import DocumentUpload from './document-upload'

const agents = [
  {
    title: 'HAZID Report Agent',
    description: 'Generate HAZID reports from process documentation',
    icon: AlertTriangle,
    color: 'bg-red-500',
  },
  {
    title: 'HAZOP Draft Agent',
    description: 'Create HAZOP study drafts from process data',
    icon: Shield,
    color: 'bg-orange-500',
  },
  {
    title: 'Risk Assessment Draft Agent',
    description: 'Analyze and draft risk assessment reports',
    icon: AlertTriangle,
    color: 'bg-yellow-500',
  },
  {
    title: 'LOPA Draft Agent',
    description: 'Generate Layer of Protection Analysis drafts',
    icon: Layers,
    color: 'bg-green-500',
  },
  {
    title: 'SRS Draft Agent',
    description: 'Create Safety Requirement Specification drafts',
    icon: FileText,
    color: 'bg-blue-500',
  },
  {
    title: 'ERP Draft Agent',
    description: 'Generate Emergency Response Plan drafts',
    icon: ClipboardList,
    color: 'bg-purple-500',
  },
  {
    title: 'Equipment List Agent',
    description: 'Generate and maintain equipment lists',
    icon: List,
    color: 'bg-indigo-500',
  },
  {
    title: 'Instruments List Agent',
    description: 'Create and update instrument lists',
    icon: Gauge,
    color: 'bg-cyan-500',
  },
  {
    title: 'Line List Agent',
    description: 'Generate and maintain line lists',
    icon: PipeLine,
    color: 'bg-teal-500',
  },
  {
    title: 'Valve Agent',
    description: 'Create and update valve information',
    icon: Wrench,
    color: 'bg-emerald-500',
  },
]

interface ActionAgentsProps {
  recentProjects: { id: string; name: string }[]
}

export default function ActionAgents({ recentProjects }: ActionAgentsProps) {
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null)

  return (
    <div className="flex-1 overflow-auto p-8 bg-gray-50 dark:bg-[#0A192F]">
      {!selectedAgent ? (
        <div className="space-y-6">
          <h2 className="text-3xl font-semibold flex items-center text-gray-900 dark:text-white">
            <FileCheck className="mr-2 text-violet-500" />
            Action Agents
          </h2>
          <p className="text-gray-600 dark:text-gray-300 max-w-3xl">
            Select an agent to upload documents and generate automated drafts for various engineering documentation.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {agents.map((agent) => (
              <motion.button
                key={agent.title}
                className=""
                onClick={() => setSelectedAgent(agent.title)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Card className="p-4 h-[180px] w-full bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors border border-gray-200 dark:border-gray-700">
                  <div className="flex flex-col items-center text-center">
                    <div className={`w-12 h-12 ${agent.color} rounded-full flex items-center justify-center mb-2`}>
                      <agent.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-sm font-semibold mb-2 theme-aware-text">{agent.title}</h3>
                    <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">{agent.description}</p>
                  </div>
                </Card>
              </motion.button>
            ))}
          </div>
        </div>
      ) : (
        <DocumentUpload 
          agentName={selectedAgent} 
          agentIcon={agents.find(agent => agent.title === selectedAgent)?.icon}
          onBack={() => setSelectedAgent(null)}
          recentProjects={recentProjects}
        />
      )}
    </div>
  )
}

