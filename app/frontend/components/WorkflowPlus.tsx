'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { MessageSquare, Gauge, AlertTriangle, Share2, Search, Filter, Plus, ChevronDown, ChevronRight } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"

interface Conversation {
  id: string
  title: string
  project: string
  projectId: string
  experts: string[]
  timestamp: Date
  type: 'discussion' | 'analysis' | 'safety' | 'integration'
  status: 'active' | 'completed' | 'pending'
}

const conversations: Conversation[] = [
  {
    id: '1',
    title: 'Optimization of Distillation Column Parameters',
    project: 'Ethylene Plant',
    projectId: 'PO-002',
    experts: ['Separation Technologies Expert', 'Process Integration Expert'],
    timestamp: new Date(Date.now() - 10 * 60 * 1000),
    type: 'analysis',
    status: 'active'
  },
  {
    id: '2',
    title: 'Heat Integration Network Design Review',
    project: 'Ethylene Plant',
    projectId: 'PO-002',
    experts: ['Heat Transfer Specialist'],
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
    type: 'discussion',
    status: 'completed'
  },
  {
    id: '3',
    title: 'HAZOP Analysis for New Reactor Unit',
    project: 'Methanol Synthesis',
    projectId: 'PO-001',
    experts: ['Safety & Risk Expert'],
    timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000),
    type: 'safety',
    status: 'active'
  },
  {
    id: '4',
    title: 'Process Control Strategy Implementation',
    project: 'Ammonia Plant',
    projectId: 'PO-003',
    experts: ['Process Integration Expert'],
    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000),
    type: 'integration',
    status: 'pending'
  },
  {
    id: '5',
    title: 'Reactor Kinetics Model Validation',
    project: 'Methanol Synthesis',
    projectId: 'PO-001',
    experts: ['Reaction Kinetics Expert'],
    timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    type: 'analysis',
    status: 'completed'
  },
]

const getTypeIcon = (type: Conversation['type']) => {
  switch (type) {
    case 'discussion':
      return <MessageSquare className="w-4 h-4 text-blue-400" />
    case 'analysis':
      return <Gauge className="w-4 h-4 text-emerald-400" />
    case 'safety':
      return <AlertTriangle className="w-4 h-4 text-amber-400" />
    case 'integration':
      return <Share2 className="w-4 h-4 text-purple-400" />
  }
}

const getStatusColor = (status: Conversation['status']) => {
  switch (status) {
    case 'active':
      return 'bg-emerald-500/20 text-emerald-400'
    case 'completed':
      return 'bg-blue-500/20 text-blue-400'
    case 'pending':
      return 'bg-amber-500/20 text-amber-400'
  }
}

const formatTimeAgo = (date: Date) => {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days}d ago`
  if (hours > 0) return `${hours}h ago`
  if (minutes > 0) return `${minutes}m ago`
  return 'just now'
}

interface ProjectGroupProps {
  projectId: string
  projectName: string
  conversations: Conversation[]
}

function ProjectGroup({ projectId, projectName, conversations }: ProjectGroupProps) {
  const [isExpanded, setIsExpanded] = useState(true)

  return (
    <div className="space-y-2">
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="flex items-center gap-2 w-full text-left p-2 hover:bg-gray-200 dark:hover:bg-gray-800 rounded-lg transition-colors"
      >
        {isExpanded ? (
          <ChevronDown className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        ) : (
          <ChevronRight className="w-4 h-4 text-gray-600 dark:text-gray-400" />
        )}
        <span className="font-medium text-gray-900 dark:text-white">{projectId}: {projectName}</span>
        <span className="text-sm text-gray-700 dark:text-gray-300">({conversations.length})</span>
      </button>
      
      {isExpanded && (
        <div className="ml-6 space-y-3">
          {conversations.map((conversation) => (
            <motion.div
              key={conversation.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600 transition-colors"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-3">
                  <div className="mt-1">{getTypeIcon(conversation.type)}</div>
                  <div>
                    <h3 className="text-gray-900 dark:text-white font-medium mb-1">{conversation.title}</h3>
                    <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                      <span>{conversation.experts.join(', ')}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <Badge className={`${getStatusColor(conversation.status)}`}>
                    {conversation.status}
                  </Badge>
                  <span className="text-sm text-gray-700 dark:text-gray-300">{formatTimeAgo(conversation.timestamp)}</span>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      )}
    </div>
  )
}

export default function WorkflowPlus() {
  const [searchQuery, setSearchQuery] = useState('')

  const groupedConversations = conversations.reduce((acc, conversation) => {
    const key = `${conversation.projectId}-${conversation.project}`
    if (!acc[key]) {
      acc[key] = []
    }
    acc[key].push(conversation)
    return acc
  }, {} as Record<string, Conversation[]>)

  const filteredGroups = Object.entries(groupedConversations)
    .filter(([key, conversations]) => {
      const [projectId, projectName] = key.split('-')
      return conversations.some(conv => 
        conv.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        projectName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        projectId.toLowerCase().includes(searchQuery.toLowerCase())
      )
    })

  return (
    <div className="p-6 bg-gray-50 dark:bg-[#0A192F]">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Workflow+</h1>
        <Button className="bg-emerald-500 hover:bg-emerald-600">
          <Plus className="w-4 h-4 mr-2" />
          New Conversation
        </Button>
      </div>

      <div className="flex flex-col gap-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-700 w-4 h-4" />
          <Input
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-10 bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-700 text-gray-900 dark:text-gray-100"
          />
        </div>

        <ScrollArea className="h-[calc(100vh-250px)]">
          <div className="space-y-6">
            {filteredGroups.map(([key, conversations]) => {
              const [projectId, projectName] = key.split('-')
              return (
                <ProjectGroup
                  key={projectId}
                  projectId={projectId}
                  projectName={projectName}
                  conversations={conversations}
                />
              )
            })}
          </div>
        </ScrollArea>
      </div>
    </div>
  )
}

