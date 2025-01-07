'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { Clock, Users, Calendar, ArrowRight, Zap, LayoutGrid, Table2 } from 'lucide-react'
import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"

interface Project {
  id: number;
  name: string;
  date: string;
  agents: string[];
  status: 'active' | 'completed' | 'pending';
}

interface RecentProjectsProps {
  projects: Project[];
}

function TableView({ projects }: { projects: Project[] }) {
  return (
    <Card className="bg-white dark:bg-gray-800/50 backdrop-blur-lg border-gray-200 dark:border-gray-700">
      <CardContent className="p-0">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200 dark:border-gray-700">
              <th className="text-left font-semibold text-gray-700 dark:text-gray-300 p-4">Project Title</th>
              <th className="text-left font-semibold text-gray-700 dark:text-gray-300 p-4">Date</th>
              <th className="text-left font-semibold text-gray-700 dark:text-gray-300 p-4">Agents Involved</th>
              <th className="text-left font-semibold text-gray-700 dark:text-gray-300 p-4">Status</th>
              <th className="text-left font-semibold text-gray-700 dark:text-gray-300 p-4">Action</th>
            </tr>
          </thead>
          <tbody>
            {projects.map((project) => (
              <tr key={project.id} className="border-b border-gray-200 dark:border-gray-700 last:border-b-0">
                <td className="p-4">
                  <div className="font-medium text-gray-900 dark:text-white">{project.name}</div>
                </td>
                <td className="p-4">
                  <div className="flex items-center text-gray-700 dark:text-gray-300">
                    <Calendar className="w-4 h-4 mr-2 text-gray-500 dark:text-gray-400" />
                    {project.date}
                  </div>
                </td>
                <td className="p-4">
                  <div className="flex items-center text-gray-700 dark:text-gray-300">
                    <Users className="w-4 h-4 mr-2 text-gray-500 dark:text-gray-400" />
                    {project.agents.join(", ")}
                  </div>
                </td>
                <td className="p-4">
                  <StatusBadge status={project.status} />
                </td>
                <td className="p-4">
                  <button className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors flex items-center">
                    View Details
                    <ArrowRight className="w-4 h-4 ml-1" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </CardContent>
    </Card>
  )
}

function GridView({ projects }: { projects: Project[] }) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {projects.map((project) => (
        <Card key={project.id} className="bg-white dark:bg-gray-800/50 backdrop-blur-lg border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800/70 transition-colors">
          <CardContent className="p-6">
            <div className="space-y-4">
              <div className="space-y-2">
                <div className="flex items-center text-gray-600 dark:text-gray-400 text-sm">
                  <Calendar className="w-4 h-4 mr-2" />
                  {project.date}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{project.name}</h3>
              </div>
              <div className="flex items-start gap-2">
                <Users className="w-4 h-4 mt-1 text-gray-500 dark:text-gray-400" />
                <div className="text-sm text-gray-700 dark:text-gray-300">{project.agents.join(", ")}</div>
              </div>
              <div className="flex items-center justify-between pt-2">
                <StatusBadge status={project.status} />
                <button className="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 transition-colors flex items-center text-sm">
                  View Details
                  <ArrowRight className="w-4 h-4 ml-1" />
                </button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

function StatusBadge({ status }: { status: string }) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
      case 'active':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300'
    }
  }

  return (
    <Badge className={`${getStatusColor(status)} flex items-center`}>
      <Zap className="w-3 h-3 mr-1" />
      {status}
    </Badge>
  )
}

export default function RecentProjects({ projects }: RecentProjectsProps) {
  const [view, setView] = useState<'grid' | 'table'>('grid')

  return (
    <div className="flex-1 overflow-auto p-8 bg-gray-50 dark:bg-[#0A192F]">
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <h2 className="text-3xl font-semibold flex items-center text-gray-900 dark:text-white">
            <Clock className="mr-2 text-blue-600 dark:text-blue-400" />
            Recent Projects
          </h2>

          <Tabs value={view} onValueChange={(value) => setView(value as 'grid' | 'table')}>
            <TabsList className="grid w-24 grid-cols-2 bg-gray-200 dark:bg-gray-700">
              <TabsTrigger value="grid" className="px-3 py-1.5">
                <LayoutGrid className="h-5 w-5" />
              </TabsTrigger>
              <TabsTrigger value="table" className="px-3 py-1.5">
                <Table2 className="h-5 w-5" />
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        <motion.div
          key={view}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
        >
          {view === 'grid' ? <GridView projects={projects} /> : <TableView projects={projects} />}
        </motion.div>
      </div>
    </div>
  )
}

