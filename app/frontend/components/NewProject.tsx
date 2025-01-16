'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { PlusCircle, ArrowRight, Book, Cog, Calculator, FileText, FlaskRoundIcon as Flask, Columns, Gauge, AlertTriangle, Thermometer, Factory, Pipette, Activity, Workflow, Send, Zap, Copy } from 'lucide-react'
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { toast } from "@/components/ui/use-toast"
import { ProjectService } from '@/src/api/UI_ProjectService'

const agents = [
  {
    title: 'Reaction Kinetics Expert',
    description: 'Optimize your reactor design and reaction conditions',
    icon: Flask,
    color: 'bg-emerald-500',
  },
  {
    title: 'Separation Technologies Expert',
    description: 'Enhance separation processes and column design',
    icon: Columns,
    color: 'bg-blue-500',
  },
  {
    title: 'Dynamics & Control Engineer',
    description: 'Process control and dynamic system optimization',
    icon: Gauge,
    color: 'bg-purple-500',
  },
  {
    title: 'Safety & Risk Expert',
    description: 'HAZOP, risk assessment, and safety protocols',
    icon: AlertTriangle,
    color: 'bg-red-500',
  },
  {
    title: 'Heat Transfer Specialist',
    description: 'Thermal systems and exchanger design',
    icon: Thermometer,
    color: 'bg-orange-500',
  },
  {
    title: 'Process Integration Expert',
    description: 'Plant-wide optimization and integration',
    icon: Factory,
    color: 'bg-indigo-500',
  },
  {
    title: 'Materials & Corrosion Expert',
    description: 'Material selection and corrosion prevention',
    icon: Pipette,
    color: 'bg-cyan-500',
  },
  {
    title: 'Sustainability Engineer',
    description: 'Green processes and environmental compliance',
    icon: Activity,
    color: 'bg-green-500',
  },
  {
    title: 'Process Flow Expert',
    description: 'PFD development and mass balance optimization',
    icon: Workflow,
    color: 'bg-yellow-500',
  },
]

interface NewProjectProps {
  onAgentSelection: (agents: string[]) => void
  onProjectNameChange: (name: string) => void
  onProjectCreation: (name: string, agents: string[]) => void
}

export default function NewProject({ onAgentSelection, onProjectNameChange, onProjectCreation }: NewProjectProps) {
  const [step, setStep] = useState(1)
  const [projectName, setProjectName] = useState('')
  const [selectedAgents, setSelectedAgents] = useState<string[]>([])
  const [query, setQuery] = useState('')

  const handleCreateProject = () => {
    if (projectName.trim() !== '') {
      setStep(2);
      onProjectNameChange(projectName);
    } else {
      toast({
        title: "Invalid Project Name",
        description: "Please enter a project name.",
        variant: "destructive",
      });
    }
  };

  const toggleAgent = (agentTitle: string) => {
    setSelectedAgents(prev => {
      let newAgents;
      if (prev.includes(agentTitle)) {
        newAgents = prev.filter(title => title !== agentTitle)
      } else if (prev.length < 4) {
        newAgents = [...prev, agentTitle]
      } else {
        toast({
          title: "Maximum agents reached",
          description: "You can select up to 4 agents for your project.",
          variant: "destructive",
        })
        return prev
      }
      onAgentSelection(newAgents)
      return newAgents
    })
  }

  const handleSubmitQuery = () => {
    // Handle query submission logic here
    console.log("Query submitted:", query)
    setQuery('')
  }

  const handleFinishProjectCreation = () => {
    if (selectedAgents.length > 0) {
      ProjectService.createProject({ name:projectName, agents: selectedAgents });
      onProjectCreation(projectName, selectedAgents)
    } else {
      toast({
        title: "No Agents Selected",
        description: "Please select at least one agent for your project.",
        variant: "destructive",
      });
    }
  };

  return (
    <div className="flex-1 overflow-auto p-8 flex flex-col">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="space-y-6 flex-grow"
      >
        <h2 className="text-3xl font-semibold flex items-center">
          <PlusCircle className="mr-2 text-emerald-500" />
          New Project
        </h2>

        {step === 1 ? (
          <Card className="bg-gray-100 dark:bg-gray-800 border-gray-300 dark:border-gray-700 max-w-md mx-auto">
            <CardContent className="p-6">
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Create New Project</h3>
                <p className="text-gray-600 dark:text-gray-400">Start by giving your project a name. This will help you identify and manage your project easily.</p>
                <Input
                  placeholder="Enter project name"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                  className="bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 text-gray-900 dark:text-white"
                />
                <Button onClick={handleCreateProject} className="w-full">
                  Next <ArrowRight className="ml-2 h-4 w-4" />
                </Button>
              </div>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-white">Select Agents for {projectName}</h3>
            <p className="text-gray-400">Choose up to 4 AI agents you'd like to involve in your project.</p>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {agents.map((agent) => (
                <motion.button
                  key={agent.title}
                  className={`p-4 bg-white dark:bg-gray-800 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors flex flex-col items-center text-center h-[180px] ${
                    selectedAgents.includes(agent.title)
                      ? 'ring-2 ring-emerald-500'
                      : ''
                  }`}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => toggleAgent(agent.title)}
                >
                  <div className={`w-12 h-12 ${agent.color} rounded-full flex items-center justify-center mb-3`}>
                    <agent.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-sm font-semibold mb-2 theme-aware-text">{agent.title}</h3>
                  <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">{agent.description}</p>
                </motion.button>
              ))}
            </div>
            <Button
              onClick={handleFinishProjectCreation}
              className="mt-6 w-full bg-emerald-500 hover:bg-emerald-600 text-white"
            >
              Create Project <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </div>
        )}
      </motion.div>

    </div>
  )
}

