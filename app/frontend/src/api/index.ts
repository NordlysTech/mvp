import { Project } from "@/components/DesktopInterface";
import axios from "axios";

const API_URL = "http://localhost:5000";

export const addMessageToCurrentConversation = async (
  queryText: any,
  projectId: string,
  conversationId: number
) => {
  try {
    const response = await axios.post(`${API_URL}/query`, {
      query: queryText, // Pass query data
      projectId: projectId,
      conversationId: conversationId,
    });
    console.log("Response of user query: ", response);
    return response.data;
  } catch (error) {
    console.error("Error fetching messages:", error);
    throw error; // Rethrow error for further handling
  }
};

export const createProjectFront = async (
  userId: string,
  name: string,
  agents: string[]
): Promise<Project | null> => {
  const newProject: Project = {
    project_id: "",
    name,
    agents,
    conversations: [
      {
        id: 1,
        name: "Conversation 1",
        messages: [],
      },
    ],
    date: new Date().toISOString().split("T")[0],
    status: "active",
  };

  try {
    const response = await axios.post(`${API_URL}/projects`, {
      user_id: userId,
      newProject,
    });

    const { project_id } = response.data;
    newProject.project_id = project_id; // Assign returned ID to the project

    return newProject;
  } catch (error) {
    console.error("Error creating project:", error);
    return null;
  }
};

export const getProjectsOfUserByIdFront = async (
  userId: string
): Promise<Project[]> => {
  try {
    const response = await axios.get(`${API_URL}/users/${userId}/projects`);
    const projects = response.data.projects;

    // Convert timestamps in messages to JavaScript Date objects
    projects.forEach((project: Project) => {
      project.conversations.forEach((conversation) => {
        conversation.messages.forEach((message) => {
          message.timestamp = new Date(message.timestamp); // Convert to Date object
        });
      });
    });

    return projects;
  } catch (error) {
    console.error("Error fetching projects:", error);
    return [];
  }
};
