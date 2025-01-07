import { X, Folder, File, FlaskRoundIcon as Flask, Columns, Gauge, AlertTriangle, Thermometer, Factory, Pipette, Activity, Workflow, MessageSquare, Plus } from 'lucide-react'

interface SelectedAgentsSidebarProps {
  projectName: string
  selectedAgents: string[]
  activeAgent: string | null
  setActiveAgent: (agent: string | null) => void
  conversations: { id: number; name: string }[]
  activeConversation: number
  onNewConversation: () => void
  onSelectConversation: (id: number) => void
}

const agentIcons: { [key: string]: React.ElementType } = {
  'Reaction Kinetics Expert': Flask,
  'Separation Technologies Expert': Columns,
  'Dynamics & Control Engineer': Gauge,
  'Safety & Risk Expert': AlertTriangle,
  'Heat Transfer Specialist': Thermometer,
  'Process Integration Expert': Factory,
  'Materials & Corrosion Expert': Pipette,
  'Sustainability Engineer': Activity,
  'Process Flow Expert': Workflow,
}

export default function SelectedAgentsSidebar({ 
  projectName, 
  selectedAgents, 
  activeAgent, 
  setActiveAgent,
  conversations,
  activeConversation,
  onNewConversation,
  onSelectConversation
}: SelectedAgentsSidebarProps) {
  return (
    <div className="w-64 bg-gray-50 dark:bg-[#1C2B3A] p-4 overflow-auto border-l border-gray-200 dark:border-gray-800">
      <h3 className="text-lg font-semibold mb-4 theme-aware-text">Project Structure</h3>
      <div className="space-y-4">
        <div className="space-y-2">
          <div className="flex items-center theme-aware-text bg-white dark:bg-[#1C2B3A] p-2 rounded-md">
            <Folder className="w-4 h-4 mr-2" />
            <span className="text-sm font-medium">{projectName}</span>
          </div>
          <div className="ml-4 space-y-2">
            {selectedAgents.map((agent) => {
              const AgentIcon = agentIcons[agent] || File
              return (
                <div
                  key={agent}
                  className={`flex items-start w-full p-2 rounded-md transition-colors ${
                    activeAgent === agent ? 'bg-emerald-500/20 theme-aware-text' : 'theme-aware-text'
                  }`}
                >
                  <div className="flex items-center">
                    <AgentIcon className="w-5 h-5 mr-3 flex-shrink-0 mt-0.5" />
                    <span className="text-sm break-words">{agent}</span>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
        
        <div className="space-y-2">
          <div className="flex items-center justify-between theme-aware-text">
            <div className="flex items-center">
              <MessageSquare className="w-4 h-4 mr-2" />
              <span className="text-sm font-medium">Conversations</span>
            </div>
            <button
              onClick={onNewConversation}
              className="p-1 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-full"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>
          <div className="ml-4 space-y-2">
            {conversations.map((conversation) => (
              <button
                key={conversation.id}
                className={`flex items-center w-full p-2 rounded-md cursor-pointer transition-colors ${
                  activeConversation === conversation.id 
                    ? 'bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200' 
                    : 'hover:bg-gray-200 dark:hover:bg-gray-800 text-gray-800 dark:text-gray-200'
                }`}
                onClick={() => onSelectConversation(conversation.id)}
              >
                <File className="w-4 h-4 mr-2" />
                <span className="text-sm truncate">{conversation.name}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

