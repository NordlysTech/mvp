'use client'

import { FileText, Bot, BarChart2, Database, User, Settings, LogOut, History, Star, Bookmark, MessageSquare, Clock, Folder, PlusCircle, GitBranch, NetworkIcon, FileCheck } from 'lucide-react'

interface SidebarProps {
  onViewChange: (view: 'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession' | 'account' | 'actionAgents') => void
  currentView: 'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession' | 'account' | 'actionAgents'
  projects: string[]
  setCurrentProject: (projectName: string) => void
}

const sidebarSections = [
  {
    title: 'Core Tools',
    items: [
      { icon: Bot, label: 'AI Engineers Hub', color: 'text-green-400', action: 'agents' },
      { icon: FileText, label: 'PDF Draft', color: 'text-blue-400', badge: '3' },
      { icon: BarChart2, label: 'Data Insights', color: 'text-purple-400', comingSoon: true },
      { icon: NetworkIcon, label: 'DiagDigitize', color: 'text-orange-400', comingSoon: true },
    ]
  },
  {
    title: 'Workspace',
    items: [
      { icon: GitBranch, label: 'Workflow+', color: 'text-purple-400', action: 'workflow' },
      { icon: Star, label: 'Favorite Agents', color: 'text-yellow-400' },
      { icon: Bookmark, label: 'Saved Responses', color: 'text-pink-400' },
    ]
  },
  {
    title: 'Action Agents',
    items: [
      { icon: FileCheck, label: 'Action Agents', color: 'text-violet-400', action: 'actionAgents' },
    ]
  },
  {
    title: 'Projects',
    items: [
      { icon: PlusCircle, label: 'New Project', color: 'text-emerald-400', action: 'newProject' },
      { icon: Clock, label: 'Recent Projects', color: 'text-teal-400', action: 'recentProjects' },
      { icon: Folder, label: 'Project Archive', color: 'text-amber-400' },
    ]
  }
]

const bottomItems = [
  { icon: User, label: 'Account', color: 'text-gray-400', action: 'account' },
  { icon: Settings, label: 'Settings', color: 'text-gray-400' },
  { icon: LogOut, label: 'Log Out', color: 'text-gray-400' },
]

export default function Sidebar({ onViewChange, currentView, projects, setCurrentProject }: SidebarProps) {
  return (
    <div className="w-64 bg-gray-100 dark:bg-gradient-to-b dark:from-[#1a237e] dark:to-[#4a148c] border-r border-gray-200 dark:border-gray-800 flex flex-col">
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-8 theme-aware-text">Solvi</h1>
        <nav className="space-y-6">
          {sidebarSections.map((section) => (
            <div key={section.title}>
              <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-2">
                {section.title}
              </h2>
              <div className="space-y-1">
                {section.items.map((item) => (
                  <button
                    key={item.label}
                    className={`flex items-center justify-between w-full p-2 rounded-lg transition-colors group ${
                      currentView === item.action
                        ? 'bg-white/20 dark:bg-white/20 text-gray-900 dark:text-white'
                        : 'hover:bg-gray-200 dark:hover:bg-white/10 text-gray-700 dark:text-gray-200 hover:text-gray-900 dark:hover:text-white'
                    } ${item.comingSoon ? 'opacity-50 cursor-not-allowed' : ''}`}
                    onClick={() => {
                      if (item.action && !item.comingSoon) {
                        onViewChange(item.action as 'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession' | 'account' | 'actionAgents')
                      }
                    }}
                    disabled={item.comingSoon}
                  >
                    <div className="flex items-center">
                      <item.icon className={`w-5 h-5 mr-3 ${item.color}`} />
                      <span className="text-sm">
                        {item.label}
                      </span>
                    </div>
                    {item.badge && (
                      <span className="bg-gray-200 dark:bg-white/20 text-xs px-2 py-1 rounded-full text-gray-700 dark:text-gray-200">
                        {item.badge}
                      </span>
                    )}
                    {item.comingSoon && (
                      <span className="text-xs text-gray-500 dark:text-gray-400 ml-2">Coming Soon</span>
                    )}
                  </button>
                ))}
              </div>
            </div>
          ))}
          {projects.length > 0 && (
            <div>
              <h2 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-3 px-2">
                Projects
              </h2>
              <div className="space-y-1">
                {projects.map((project) => (
                  <button
                    key={project}
                    className={`flex items-center justify-between w-full p-2 rounded-lg transition-colors group ${
                      currentView === 'activeSession' && project === currentView
                        ? 'bg-white/20 dark:bg-white/20 text-gray-900 dark:text-white'
                        : 'hover:bg-gray-200 dark:hover:bg-white/10 text-gray-700 dark:text-gray-200 hover:text-gray-900 dark:hover:text-white'
                    }`}
                    onClick={() => {
                      setCurrentProject(project);
                      onViewChange('activeSession');
                    }}
                  >
                    <div className="flex items-center">
                      <MessageSquare className="w-5 h-5 mr-3 text-blue-400" />
                      <span className="text-sm">
                        {project}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}
        </nav>
      </div>
      <div className="mt-auto p-4 border-t border-gray-200 dark:border-gray-800">
        <nav className="space-y-1">
          {bottomItems.map((item) => (
            <button
              key={item.label}
              className="flex items-center w-full p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-white/10 transition-colors group"
              onClick={() => item.action && onViewChange(item.action as 'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession' | 'account' | 'actionAgents')}
            >
              <item.icon className={`w-5 h-5 mr-3 ${item.color}`} />
              <span className="text-sm text-gray-700 dark:text-gray-300 group-hover:text-gray-900 dark:group-hover:text-white">
                {item.label}
              </span>
            </button>
          ))}
        </nav>
      </div>
    </div>
  )
}

