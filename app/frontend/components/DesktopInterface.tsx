'use client'

import { useState, useEffect } from 'react'
import TopMenuBar from './TopMenuBar'
import Sidebar from './Sidebar'
import MainContent from './MainContent'
import SelectedAgentsSidebar from './SelectedAgentsSidebar'
import Settings from './Settings'

interface Message {
  id: string;
  content: string;
  type: 'user' | 'agent';
  timestamp: Date;
  agentName?: string;
}

interface Conversation {
  id: number;
  name: string;
  messages: Message[];
}

interface Project {
  name: string;
  agents: string[];
  conversations: Conversation[];
  date: string;
  status: 'active' | 'completed' | 'pending';
}

export default function DesktopInterface() {
  const [currentView, setCurrentView] = useState<'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession'>('agents')
  const [selectedAgents, setSelectedAgents] = useState<string[]>([])
  const [projectName, setProjectName] = useState('')
  const [projectStep, setProjectStep] = useState(1)
  const [activeAgent, setActiveAgent] = useState<string | null>(null)
  const [projects, setProjects] = useState<Project[]>([])
  const [currentProject, setCurrentProject] = useState<Project | null>(null)
  const [activeConversation, setActiveConversation] = useState<number | null>(null)
  const [theme, setTheme] = useState<'light' | 'dark'>('dark')
  const [showSettings, setShowSettings] = useState(false)

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark')
  }, [theme])

  const handleViewChange = (view: 'agents' | 'recentProjects' | 'newProject' | 'workflow' | 'activeSession') => {
    setCurrentView(view)
  }

  const handleAgentSelection = (agents: string[]) => {
    setSelectedAgents(agents)
  }

  const handleProjectNameChange = (name: string) => {
    setProjectName(name)
  }

  const handleNextStep = () => {
    setProjectStep(2)
  }

  const handleProjectCreation = (name: string, agents: string[]) => {
    const newProject: Project = {
      name,
      agents,
      conversations: [{
        id: 1,
        name: 'Conversation 1',
        messages: []
      }],
      date: new Date().toISOString().split('T')[0],
      status: 'active'
    };
    setProjects(prev => [...prev, newProject]);
    setCurrentProject(newProject);
    setActiveConversation(1);
    setCurrentView('activeSession');
    setProjectStep(1);
    setProjectName('');
    setSelectedAgents([]);
  }

  const switchToProject = (projectName: string) => {
    const project = projects.find(p => p.name === projectName)
    if (project) {
      setCurrentProject(project)
      setActiveConversation(project.conversations[0].id)
      setCurrentView('activeSession')
    }
  }

  const handleNewConversation = () => {
    if (currentProject) {
      const newConversationId = (currentProject.conversations?.length || 0) + 1;
      const newConversation: Conversation = {
        id: newConversationId,
        name: `Conversation ${newConversationId}`,
        messages: []
      };
      const updatedProject = {
        ...currentProject,
        conversations: [...currentProject.conversations, newConversation]
      };
      setCurrentProject(updatedProject);
      setProjects(prev => prev.map(p => p.name === updatedProject.name ? updatedProject : p));
      setActiveConversation(newConversationId);
    }
  };

  const handleSelectConversation = (id: number) => {
    setActiveConversation(id)
  }

  const updateConversation = (updatedConversation: Conversation) => {
    if (currentProject) {
      const updatedConversations = currentProject.conversations.map(conv =>
        conv.id === updatedConversation.id ? updatedConversation : conv
      );
      const updatedProject = {
        ...currentProject,
        conversations: updatedConversations
      };
      setCurrentProject(updatedProject);
      setProjects(prev => prev.map(p => p.name === updatedProject.name ? updatedProject : p));
    }
  }

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light')
  }

  return (
    <div className={`flex flex-col h-screen theme-aware-bg`}>
      <TopMenuBar onSettingsClick={() => setShowSettings(true)} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar 
          onViewChange={handleViewChange} 
          currentView={currentView}
          projects={projects.map(p => p.name)}
          setCurrentProject={switchToProject}
        />
        <div className="flex-1 flex">
          <MainContent
            selectedCategory="Featured"
            onCategoryChange={() => {}}
            currentView={currentView}
            onAgentSelection={handleAgentSelection}
            onProjectNameChange={handleProjectNameChange}
            onNextStep={handleNextStep}
            projectStep={projectStep}
            projectName={projectName}
            selectedAgents={selectedAgents}
            activeAgent={activeAgent}
            onProjectCreation={handleProjectCreation}
            currentProject={currentProject}
            setActiveAgent={setActiveAgent}
            projects={projects}
            activeConversation={activeConversation}
            onNewConversation={handleNewConversation}
            conversations={currentProject?.conversations || []}
            updateConversation={updateConversation}
          />
          {currentView === 'activeSession' && currentProject && (
            <SelectedAgentsSidebar
              projectName={currentProject.name}
              selectedAgents={currentProject.agents}
              activeAgent={activeAgent}
              setActiveAgent={setActiveAgent}
              conversations={currentProject.conversations}
              activeConversation={activeConversation || 1}
              onNewConversation={handleNewConversation}
              onSelectConversation={handleSelectConversation}
            />
          )}
        </div>
      </div>
      {showSettings && (
        <Settings
          theme={theme}
          toggleTheme={toggleTheme}
          onClose={() => setShowSettings(false)}
        />
      )}
    </div>
  )
}

