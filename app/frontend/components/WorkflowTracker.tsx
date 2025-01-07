'use client'

import { Clock, Maximize2, X, MessageSquare, Gauge, AlertTriangle, Share2 } from 'lucide-react'
import { motion } from 'framer-motion'
import { ScrollArea } from '@/components/ui/scroll-area'

interface Activity {
  id: string
  title: string
  description: string
  expert: string
  project: string
  timestamp: Date
  type: 'discussion' | 'analysis' | 'safety' | 'integration'
}

const activities: Activity[] = [
  {
    id: '1',
    title: 'Reactor Design Discussion',
    description: 'Optimization parameters for temperature control discussed',
    expert: 'Reaction Kinetics Expert',
    project: 'PO-002',
    timestamp: new Date(Date.now() - 10 * 60 * 1000), // 10 minutes ago
    type: 'discussion'
  },
  {
    id: '2',
    title: 'Heat Exchanger Analysis',
    description: 'Updated thermal calculations and efficiency metrics',
    expert: 'Heat Transfer Specialist',
    project: 'PO-002',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
    type: 'analysis'
  },
  {
    id: '3',
    title: 'Safety Protocol Review',
    description: 'HAZOP study documentation reviewed',
    expert: 'Safety & Risk Expert',
    project: 'PO-001',
    timestamp: new Date(Date.now() - 3 * 60 * 60 * 1000), // 3 hours ago
    type: 'safety'
  },
  {
    id: '4',
    title: 'Process Integration',
    description: 'Merged optimized parameters into main process flow',
    expert: 'Process Integration Expert',
    project: 'PO-002',
    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000), // 5 hours ago
    type: 'integration'
  },
]

const getActivityIcon = (type: Activity['type']) => {
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

const formatTimeAgo = (date: Date) => {
  const seconds = Math.floor((new Date().getTime() - date.getTime()) / 1000)
  const minutes = Math.floor(seconds / 60)
  const hours = Math.floor(minutes / 60)
  const days = Math.floor(hours / 24)

  if (days > 0) return `${days} day${days === 1 ? '' : 's'} ago`
  if (hours > 0) return `${hours} hour${hours === 1 ? '' : 's'} ago`
  if (minutes > 0) return `${minutes} minute${minutes === 1 ? '' : 's'} ago`
  return 'just now'
}

export default function WorkflowTracker() {
  return (
    <div className="w-80 bg-[#0d1117] text-gray-300 flex flex-col h-full border-l border-gray-800">
      <div className="flex items-center justify-between p-4 border-b border-gray-800">
        <div className="flex items-center gap-2">
          <h2 className="text-white text-lg font-semibold">Workflow Tracker</h2>
          <Clock className="w-4 h-4 text-gray-400" />
        </div>
        <div className="flex items-center gap-2">
          <button className="p-1 hover:bg-gray-800 rounded">
            <Maximize2 className="w-4 h-4 text-gray-400" />
          </button>
          <button className="p-1 hover:bg-gray-800 rounded">
            <X className="w-4 h-4 text-gray-400" />
          </button>
        </div>
      </div>
      
      <ScrollArea className="flex-1 p-4">
        <div className="space-y-6">
          {activities.map((activity, index) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="relative pl-5 before:absolute before:left-2 before:top-0 before:bottom-0 before:w-px before:bg-gray-800"
            >
              <div className="absolute left-0 top-1 p-1 rounded-full bg-[#0d1117]">
                {getActivityIcon(activity.type)}
              </div>
              
              <div className="space-y-1">
                <h3 className="text-white font-medium">{activity.title}</h3>
                <p className="text-gray-400 text-sm">{activity.description}</p>
                
                <div className="flex flex-col gap-1 text-xs text-gray-500">
                  <div>{activity.expert}</div>
                  <div className="flex items-center justify-between">
                    <span>Project: {activity.project}</span>
                    <span>{formatTimeAgo(activity.timestamp)}</span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </ScrollArea>
    </div>
  )
}

