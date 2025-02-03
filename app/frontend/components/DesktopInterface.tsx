"use client";

import { useState, useEffect, useRef } from "react";
import TopMenuBar from "./TopMenuBar";
import Sidebar from "./Sidebar";
import MainContent from "./MainContent";
import SelectedAgentsSidebar from "./SelectedAgentsSidebar";
import Settings from "./Settings";
import { createProjectFront, getProjectsOfUserByIdFront } from "../src/api";

export interface Message {
  id: string;
  content: string;
  type: "user" | "agent";
  timestamp: Date;
  agentName?: string;
  answer: string;
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
  status: "active" | "completed" | "pending";
}

export default function DesktopInterface() {
  const [currentView, setCurrentView] = useState<
    "agents" | "recentProjects" | "newProject" | "workflow" | "activeSession"
  >("agents");
  const [selectedAgents, setSelectedAgents] = useState<string[]>([]);
  const [projectName, setProjectName] = useState("");
  const [projectStep, setProjectStep] = useState(1);
  const [activeAgent, setActiveAgent] = useState<string | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [currentProject, setCurrentProject] = useState<Project | null>(null);
  const [activeConversation, setActiveConversation] = useState<number | null>(
    null
  );
  const [theme, setTheme] = useState<"light" | "dark">("dark");
  const [showSettings, setShowSettings] = useState(false);

  const [isLoading, setIsLoading] = useState(true); // Add loading state
  const [error, setError] = useState<string | null>(null); // Add error state

  useEffect(() => {
    document.documentElement.classList.toggle("dark", theme === "dark");
  }, [theme]);

  // Remove the cache ref as it's causing issues with state updates
  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setIsLoading(true);
        const userId = "user123";
        console.log("Fetching projects for user:", userId);

        const fetchedProjects = await getProjectsOfUserByIdFront(userId);
        console.log("Raw API response:", fetchedProjects);
        console.log("Response type:", typeof fetchedProjects);
        console.log("Is Array?", Array.isArray(fetchedProjects));

        if (fetchedProjects === null || fetchedProjects === undefined) {
          console.error("API returned null or undefined");
          setError("No data received from API");
          setProjects([]);
          return;
        }

        if (Array.isArray(fetchedProjects)) {
          console.log("Projects array length:", fetchedProjects.length);
          console.log("First project (if any):", fetchedProjects[0]);
          setProjects(fetchedProjects);
        } else {
          console.error("Expected array but received:", fetchedProjects);
          setError("Invalid projects data received");
          setProjects([]);
        }
      } catch (error) {
        console.error("Detailed fetch error:", error);
        setError(
          error instanceof Error ? error.message : "Failed to fetch projects"
        );
        setProjects([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchProjects();
  }, []); // Empty dependency array for initial load only

  // Add loading and error states to your UI
  useEffect(() => {
    if (isLoading) {
      console.log("Loading projects...");
    } else if (error) {
      console.log("Error:", error);
    } else {
      console.log("Projects loaded:", projects);
    }
  }, [isLoading, error, projects]);

  const handleViewChange = (
    view:
      | "agents"
      | "recentProjects"
      | "newProject"
      | "workflow"
      | "activeSession"
  ) => {
    setCurrentView(view);
  };

  const handleAgentSelection = (agents: string[]) => {
    setSelectedAgents(agents);
  };

  const handleProjectNameChange = (name: string) => {
    setProjectName(name);
  };

  const handleNextStep = () => {
    setProjectStep(2);
  };

  const handleProjectCreation = async (name: string, agents: string[]) => {
    const userId = "user123"; // Replace with dynamic user ID if available
    const newProject = await createProjectFront(userId, name, agents);

    if (newProject) {
      setProjects((prev) => [...prev, newProject]);
      setCurrentProject(newProject);
      setActiveConversation(1);
      setCurrentView("activeSession");
      setProjectStep(1);
      setProjectName("");
      setSelectedAgents([]);
    } else {
      // Handle error (e.g., show toast notification)
      console.error("Failed to create project");
    }
  };

  const switchToProject = (projectName: string) => {
    const project = projects.find((p) => p.name === projectName);
    if (project) {
      setCurrentProject(project);
      setActiveConversation(project.conversations[0].id);
      setCurrentView("activeSession");
    }
  };

  const handleNewConversation = () => {
    if (currentProject) {
      const newConversationId = (currentProject.conversations?.length || 0) + 1;
      const newConversation: Conversation = {
        id: newConversationId,
        name: `Conversation ${newConversationId}`,
        messages: [],
      };
      const updatedProject = {
        ...currentProject,
        conversations: [...currentProject.conversations, newConversation],
      };
      setCurrentProject(updatedProject);
      setProjects((prev) =>
        prev.map((p) => (p.name === updatedProject.name ? updatedProject : p))
      );
      setActiveConversation(newConversationId);
    }
  };

  const handleSelectConversation = (id: number) => {
    setActiveConversation(id);
  };

  const updateConversation = (updatedConversation: Conversation) => {
    if (currentProject) {
      const updatedConversations = currentProject.conversations.map((conv) =>
        conv.id === updatedConversation.id ? updatedConversation : conv
      );
      const updatedProject = {
        ...currentProject,
        conversations: updatedConversations,
      };
      setCurrentProject(updatedProject);
      setProjects((prev) =>
        prev.map((p) => (p.name === updatedProject.name ? updatedProject : p))
      );
    }
  };

  const toggleTheme = () => {
    setTheme((prevTheme) => (prevTheme === "light" ? "dark" : "light"));
  };

  return (
    <div className={`flex flex-col h-screen theme-aware-bg`}>
      <TopMenuBar onSettingsClick={() => setShowSettings(true)} />
      <div className="flex flex-1 overflow-hidden">
        <Sidebar
          onViewChange={handleViewChange}
          currentView={currentView}
          projects={projects.map((p) => p.name)}
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
            onViewChange={handleViewChange}
            setCurrentProject={switchToProject}
          />
          {currentView === "activeSession" && currentProject && (
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
  );
}
