'use client'

import { motion } from 'framer-motion'
import { Cog, Columns, Shield, Activity, Plus, FlaskRoundIcon as Flask, Gauge, AlertTriangle, Thermometer, Factory, Pipette, Workflow } from 'lucide-react'
import RecentProjects from './RecentProjects'
import NewProject from './NewProject'
import ProjectWorkspace from './ProjectWorkspace'
import WorkflowPlus from './WorkflowPlus'

interface Conversation {
  id: number;
  name: string;
  messages: any[];
}

interface Project {
  name: string;
  agents: string[];
  conversations: Conversation[];
}

const categories = [
  'Featured',
  'Engineering',
  'Procurement & Commissioning',
  'Project Management',
  'Safety',
  'Modeling and Simulation',
]

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
    description: 'HAZOP, risk assessment and safety protocols',
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
  {
    title: 'Build Your Own Agent',
    description: 'Create a custom ChemEng assistant',
    icon: Plus,
    color: 'bg-gray-500',
  },
]

interface MainContentProps {
  selectedCategory: string
  onCategoryChange: (category: string) => void
  currentView: 'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession'
  onAgentSelection: (agents: string[]) => void
  onProjectNameChange: (name: string) => void
  onNextStep: () => void
  projectStep: number
  projectName: string
  selectedAgents: string[]
  activeAgent: string | null
  onProjectCreation: (name: string, agents: string[]) => void
  currentProject: Project | null
  setActiveAgent: (agent: string | null) => void
  projects: Project[];
  activeConversation: number | null;
  onNewConversation: () => void;
  conversations: Conversation[];
  updateConversation: (updatedConversation: Conversation) => void;
}

export default function MainContent({
  selectedCategory,
  onCategoryChange,
  currentView,
  onAgentSelection,
  onProjectNameChange,
  onNextStep,
  projectStep,
  projectName,
  selectedAgents,
  activeAgent,
  onProjectCreation,
  currentProject,
  setActiveAgent,
  projects,
  activeConversation,
  onNewConversation,
  conversations,
  updateConversation
}: MainContentProps) {
  return (
    <div className="flex-1 overflow-auto bg-gray-50 dark:bg-[#0A192F]">
      {currentView === 'agents' && (
        <div className="p-8">
          <h2 className="text-2xl font-semibold mb-6 theme-aware-text">
            Welcome Home
          </h2>

          <div className="flex space-x-2 mb-8 overflow-x-auto pb-2">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => onCategoryChange(category)}
                className={`px-4 py-2 rounded-full whitespace-nowrap transition-colors ${
                  selectedCategory === category
                    ? 'bg-emerald-500 text-white'
                    : 'bg-gray-200 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-700'
                }`}
              >
                {category}
              </button>
            ))}
          </div>

          <div className="max-w-6xl mx-auto">
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {agents.map((agent) => (
                <motion.button
                  key={agent.title}
                  className="p-4 bg-white dark:bg-gray-800 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors flex flex-col items-center text-center h-[180px] border border-gray-200 dark:border-gray-700"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className={`w-12 h-12 ${agent.color} rounded-full flex items-center justify-center mb-3`}>
                    <agent.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-sm font-semibold mb-2 text-gray-800 dark:text-white">{agent.title}</h3>
                  <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">{agent.description}</p>
                </motion.button>
              ))}
            </div>
          </div>
        </div>
      )}
      {currentView === 'recentProjects' && <RecentProjects projects={projects} />}
      {currentView === 'newProject' && (
        <NewProject
          onAgentSelection={onAgentSelection}
          onProjectNameChange={onProjectNameChange}
          onProjectCreation={onProjectCreation}
        />
      )}
      {currentView === 'workflow' && <WorkflowPlus />}
      {currentView === 'activeSession' && currentProject && (
        <ProjectWorkspace
          projectName={currentProject.name}
          selectedAgents={currentProject.agents}
          activeAgent={activeAgent}
          setActiveAgent={setActiveAgent}
          conversations={conversations}
          activeConversation={activeConversation}
          onNewConversation={onNewConversation}
          updateConversation={updateConversation}
        />
      )}
    </div>
  )
}

