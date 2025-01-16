'use client';

import axios from "axios";
import { toast } from "@/components/ui/use-toast";

export interface Project {
  name: string;
  agents: string[];
}

const API_BASE_URL = 'http://localhost:5000/projects';

export class ProjectService {
  /**
   * Create a new project in the backend
   * @param project Project data to be sent to the backend
   */
  static async createProject(projectData: Project): Promise<{ project_id: string }> {
    try {
      const response = await axios.post<{ success: boolean; project_id: string }>(
        API_BASE_URL,
        projectData
      );
      return response.data;
    } catch (error) {
      throw this.handleError(error);
    }
  }
  private static handleError(error: any): Error {
    if (axios.isAxiosError(error)) {
      const message = error.response?.data?.message || 'An error occurred';
      console.error('API Error:', message);
      return new Error(message);
    }
    return new Error('An unexpected error occurred');
  }
}
