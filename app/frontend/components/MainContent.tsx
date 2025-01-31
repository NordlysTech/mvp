'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Cog, Columns, Shield, Activity, Plus, FlaskRoundIcon as Flask, Gauge, AlertTriangle, Thermometer, Factory, Pipette, Workflow } from 'lucide-react'
import RecentProjects from './RecentProjects'
import NewProject from './NewProject'
import ProjectWorkspace from './ProjectWorkspace'
import WorkflowPlus from './WorkflowPlus'
import ActionAgents from './action-agents'


export interface Message {
  id: string;
  content: string;
  type: 'user' | 'agent';
  timestamp: Date;
  agentName?: string;
  answer:string;
}
interface Conversation {
  id: number;
  name: string;
  messages: Message[];
}

export interface Project {
  project_id: string;
  name: string;
  agents: string[];
  conversations: Conversation[];
  date: string;
  status: 'active' | 'completed' | 'pending';
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
    fullDescription: 'This agent specializes in the study of reaction rates and mechanisms. It helps optimize reactor design and operating conditions by providing insights into how different variables (e.g., temperature, pressure, concentrations) impact reaction kinetics.',
    useCases: [
      'Determining optimal reaction parameters for maximizing product yield.',
      'Troubleshooting reactor performance issues related to kinetics.',
      'Simulating and predicting the behavior of chemical reactions under various conditions.',
      'Analyzing kinetic data from experiments to develop rate equations.',
      'Assisting in the design of new reactors and reaction pathways.'
    ]
  },
  {
    title: 'Separation Technologies Expert',
    description: 'Enhance separation processes and column design',
    icon: Columns,
    color: 'bg-blue-500',
    fullDescription: 'This agent focuses on the different methods for separating components of a mixture. It assists in enhancing separation processes, with a particular focus on column design and optimization.',
    useCases: [
      'Selecting appropriate separation techniques for specific mixtures.',
      'Designing and optimizing separation columns (e.g., distillation, absorption).',
      'Troubleshooting issues related to separation efficiency.',
      'Developing control strategies for separation units.',
      'Evaluating the performance of different separation technologies.'
    ]
  },
  {
    title: 'Dynamics and Control Engineer',
    description: 'Process control and dynamic system optimization',
    icon: Gauge,
    color: 'bg-purple-500',
    fullDescription: 'This agent is an expert in process control and the dynamic behavior of systems. It helps optimize control strategies and ensure system stability, and ensures process safety.',
    useCases: [
      'Developing control system architectures for chemical processes.',
      'Tuning process controllers for optimal performance.',
      'Analyzing system stability and designing robust control strategies.',
      'Simulating the dynamic behavior of processes.',
      'Troubleshooting control system issues.'
    ]
  },
  {
    title: 'Safety and Risk Expert',
    description: 'HAZOP, risk assessment and safety protocols',
    icon: AlertTriangle,
    color: 'bg-red-500',
    fullDescription: 'This agent focuses on safety protocols and risk assessments (HAZOP) within chemical processes. It helps engineers to identify potential hazards and implement risk mitigation strategies.',
    useCases: [
      'Performing HAZOP studies to identify process hazards.',
      'Developing risk mitigation strategies to prevent accidents.',
      'Ensuring compliance with safety regulations.',
      'Investigating incidents and developing corrective actions.',
      'Implementing and reviewing safety protocols.'
    ]
  },
  {
    title: 'Heat Transfer Specialist',
    description: 'Thermal systems and exchanger design',
    icon: Thermometer,
    color: 'bg-orange-500',
    fullDescription: 'This agent specializes in heat transfer phenomena, such as thermal systems and exchanger design. It helps in optimizing heat management for efficient operations.',
    useCases: [
      'Designing and optimizing heat exchangers for various applications.',
      'Analyzing heat transfer performance of equipment.',
      'Troubleshooting heat-related problems in processes.',
      'Selecting appropriate insulation materials.',
      'Designing thermal systems for optimal efficiency.'
    ]
  },
  {
    title: 'Process Integration Expert',
    description: 'Plant-wide optimization and integration',
    icon: Factory,
    color: 'bg-indigo-500',
    fullDescription: 'This agent focuses on plant-wide optimization, seeking to integrate and optimize various unit operations to improve overall process efficiency, and provides plant wide performance improvement recommendations.',
    useCases: [
      'Optimizing the flow of materials and energy in a chemical plant.',
      'Identifying opportunities for waste heat recovery.',
      'Integrating different process units to maximize efficiency.',
      'Analyzing plant-wide performance to identify bottlenecks.',
      'Implementing plant-wide changes for improving yield and production.'
    ]
  },
  {
    title: 'Materials and Corrosion Expert',
    description: 'Material selection and corrosion prevention',
    icon: Pipette,
    color: 'bg-cyan-500',
    fullDescription: 'This agent is an expert in material selection and corrosion prevention, and supports optimal material selections for the processes. It ensures the integrity and longevity of the equipment used in the process.',
    useCases: [
      'Selecting appropriate materials for different operating conditions.',
      'Developing strategies to prevent corrosion.',
      'Analyzing material degradation and failure.',
      'Troubleshooting material-related issues in the process.',
      'Evaluating the life cycle of different materials in the process.'
    ]
  },
  {
    title: 'Sustainability Engineer',
    description: 'Green processes and environmental compliance',
    icon: Activity,
    color: 'bg-green-500',
    fullDescription: 'This agent focuses on green processes and environmental compliance. It ensures processes are environmentally friendly and comply with regulations and also supports with LCA.',
    useCases: [
      'Assessing the environmental impact of chemical processes.',
      'Developing sustainable process design alternatives.',
      'Ensuring compliance with environmental regulations.',
      'Identifying waste minimization and recycling opportunities.',
      'Implementing green technologies for manufacturing processes.'
    ]
  },
  {
    title: 'Process Flow Expert',
    description: 'PFD development and mass balance optimization',
    icon: Workflow,
    color: 'bg-yellow-500',
    fullDescription: 'This agent focuses on the development of process flow diagrams (PFDs) and mass balance optimization. It helps in the effective design and analysis of process workflows.',
    useCases: [
      'Developing accurate process flow diagrams (PFDs).',
      'Optimizing material flow and energy balance in a process.',
      'Troubleshooting mass balance issues in a process.',
      'Analyzing process bottlenecks and suggesting solutions.',
      'Improving the clarity of process documentation.'
    ]
  },
  {
    title: 'Build Your Own Agent',
    description: 'Create a custom ChemEng assistant',
    icon: Plus,
    color: 'bg-gray-500',
    fullDescription: 'Create a custom AI agent tailored to your specific chemical engineering needs.',
    useCases: [
      'Developing specialized agents for unique process requirements.',
      'Combining multiple expert domains into a single agent.',
      'Creating agents for proprietary technologies or methodologies.',
      'Customizing agent responses and knowledge base.',
      'Integrating with existing tools and databases.'
    ]
  },
]

interface MainContentProps {
  selectedCategory: string
  onCategoryChange: (category: string) => void
  currentView: 'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession' | 'actionAgents'
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
  const [expandedAgent, setExpandedAgent] = useState<string | null>(null);

  const toggleAgentExpansion = (agentTitle: string) => {
    setExpandedAgent(expandedAgent === agentTitle ? null : agentTitle);
  };

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
                  onClick={() => toggleAgentExpansion(agent.title)}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                >
                  <div className={`w-12 h-12 ${agent.color} rounded-full flex items-center justify-center mb-2`}>
                    <agent.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="text-sm font-semibold mb-2 theme-aware-text">{agent.title}</h3>
                  <p className="text-xs text-gray-600 dark:text-gray-400 line-clamp-2">{agent.description}</p>
                </motion.button>
              ))}
            </div>
          </div>
          <AnimatePresence>
            {expandedAgent && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
                onClick={() => setExpandedAgent(null)}
              >
                <motion.div
                  className="bg-white dark:bg-gray-800 p-6 rounded-lg max-w-2xl w-full m-4 overflow-y-auto max-h-[80vh]"
                  onClick={(e) => e.stopPropagation()}
                  initial={{ scale: 0.9, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  exit={{ scale: 0.9, opacity: 0 }}
                >
                  <h3 className="text-xl font-semibold mb-4 theme-aware-text">{expandedAgent}</h3>
                  <p className="text-sm text-gray-700 dark:text-gray-300 mb-4">{agents.find((agent) => agent.title === expandedAgent)?.fullDescription}</p>
                  <h4 className="font-semibold mb-2 theme-aware-text">Use Cases:</h4>
                  <ul className="list-disc list-inside text-sm text-gray-600 dark:text-gray-400">
                    {(agents.find((agent) => agent.title === expandedAgent)?.useCases).map((useCase, index) => (
                      <li key={index}>{useCase}</li>
                    ))}
                  </ul>
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>
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
      {currentView === 'actionAgents' && <ActionAgents recentProjects={projects} />}
      {currentView === 'activeSession' && currentProject && (
        <ProjectWorkspace
          projectName={currentProject.name}
          projectId={currentProject.project_id}
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
