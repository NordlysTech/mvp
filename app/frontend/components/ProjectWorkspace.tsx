"use client";
import React from "react";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Send,
  Zap,
  Copy,
  Bot,
  FlaskRoundIcon as Flask,
  AlertTriangle,
  Thermometer,
  GitMerge,
  Columns,
  Gauge,
  Droplet,
  Leaf,
  GitBranch,
} from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { getMessages } from "../src/api";

interface Message {
  id: string;
  content: string;
  type: "user" | "agent" | "technical" | "safety" | "process";
  timestamp: Date;
  agentName?: string;
}

interface Conversation {
  id: number;
  name: string;
  messages: Message[];
}

interface ProjectWorkspaceProps {
  projectName: string;
  selectedAgents: string[];
  activeAgent: string | null;
  setActiveAgent: (agent: string | null) => void;
  conversations: Conversation[];
  activeConversation: number | null;
  onNewConversation: () => void;
  updateConversation: (updatedConversation: Conversation) => void;
}

const getInitials = (name: string) => {
  return name
    .split(" ")
    .map((word) => word[0])
    .join("")
    .toUpperCase();
};

const getAgentIcon = (agentName: string) => {
  const icons: { [key: string]: React.ElementType } = {
    "Reaction Kinetics Expert": Flask,
    "Safety & Risk Expert": AlertTriangle,
    "Heat Transfer Specialist": Thermometer,
    "Process Integration Expert": GitMerge,
    "Separation Technologies Expert": Columns,
    "Dynamics & Control Engineer": Gauge,
    "Materials & Corrosion Expert": Droplet,
    "Sustainability Engineer": Leaf,
    "Process Flow Expert": GitBranch,
  };
  return icons[agentName] || Bot;
};

const getAgentColor = (agentName: string) => {
  const colors: { [key: string]: string } = {
    "Reaction Kinetics Expert": "bg-emerald-500",
    "Safety & Risk Expert": "bg-red-500",
    "Heat Transfer Specialist": "bg-orange-500",
    "Process Integration Expert": "bg-indigo-500",
    "Separation Technologies Expert": "bg-blue-500",
    "Dynamics & Control Engineer": "bg-purple-500",
    "Materials & Corrosion Expert": "bg-cyan-500",
    "Sustainability Engineer": "bg-green-500",
    "Process Flow Expert": "bg-yellow-500",
  };
  return colors[agentName] || "bg-gray-500";
};

const renderContent = (content: string) => {
  const lines = content.split("\n");
  const result: JSX.Element[] = [];
  let tableContent: string[] = [];
  let isTable = false;

  lines.forEach((line, index) => {
    line = line.trim();
    console.log(line);
    if (line.startsWith("|")) {
      if (!isTable) {
        isTable = true;
      }
      tableContent.push(line);
      console.log(isTable);
    } else {
      if (isTable) {
        result.push(
          <div key={`table-${index}`} className="my-4 overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <tbody>
                {tableContent.map((row, i) => (
                  <tr
                    key={i}
                    className={
                      i === 0
                        ? "bg-gray-100 dark:bg-gray-800"
                        : "border-b border-gray-200 dark:border-gray-700"
                    }
                  >
                    {row
                      .split("|")
                      .filter(Boolean)
                      .map((cell, j) => (
                        <td
                          key={j}
                          className="px-4 py-2 whitespace-nowrap text-gray-900 dark:text-gray-200"
                        >
                          {cell.trim()}
                        </td>
                      ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        tableContent = [];
        isTable = false;
      }
      if (line.trim()) {
        result.push(
          <p key={index} className="mb-2 text-gray-900 dark:text-gray-200">
            {line}
          </p>
        );
      }
    }
  });

  if (isTable && tableContent.length > 0) {
    result.push(
      <div key="final-table" className="my-4 overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <tbody>
            {tableContent.map((row, i) => (
              <tr
                key={i}
                className={
                  i === 0
                    ? "bg-gray-100 dark:bg-gray-800"
                    : "border-b border-gray-200 dark:border-gray-700"
                }
              >
                {row
                  .split("|")
                  .filter(Boolean)
                  .map((cell, j) => (
                    <td
                      key={j}
                      className="px-4 py-2 whitespace-nowrap text-gray-900 dark:text-gray-200"
                    >
                      {cell.trim()}
                    </td>
                  ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return result;
};

const getAgentInitials = (agentName: string) => {
  const initials = agentName.match(/\b\w/g);
  return initials ? initials.join("").toUpperCase() : "";
};

const ProjectWorkspace = ({
  projectName,
  selectedAgents,
  activeAgent,
  setActiveAgent,
  conversations,
  activeConversation,
  onNewConversation,
  updateConversation,
}: ProjectWorkspaceProps) => {
  const [mockResponses, setMockResponses] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [query, setQuery] = useState("");
  const [userName] = useState("Alex Smith");
  const chatContainerRef = useRef<HTMLDivElement>(null);
  const [isAtBottom, setIsAtBottom] = useState(true);
  const [showAgentList, setShowAgentList] = useState(false);
  const [cursorPosition, setCursorPosition] = useState(0);

  const currentConversation = conversations.find(
    (c) => c.id === activeConversation
  ) || {
    id: 0,
    name: "New Conversation",
    messages: [],
  };


  useEffect(() => {
    const chatContainer = chatContainerRef.current;
    if (chatContainer && isAtBottom) {
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }, [currentConversation.messages, isAtBottom]);

  const handleScroll = () => {
    const chatContainer = chatContainerRef.current;
    if (chatContainer) {
      const { scrollTop, scrollHeight, clientHeight } = chatContainer;
      setIsAtBottom(scrollHeight - scrollTop === clientHeight);
    }
  };

  const handleSubmitQuery = async () => {
    if (!query.trim()) return;

    // Create and add user message immediately
    const userMessage: Message = {
      id: Date.now().toString(),
      content: query,
      type: "user",
      timestamp: new Date(),
    };

    const updatedConversation = {
      ...currentConversation,
      messages: [...currentConversation.messages, userMessage],
    };

    setQuery("");

    // Update UI with user message
    updateConversation(updatedConversation);
    setIsAtBottom(true);
    setIsLoading(true);

    try {
      // Fetch response from backend
      const data = await getMessages(query);
      setMockResponses(Array.isArray(data) ? data : [data]);

      // Create agent message with the response
      const agentMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: Array.isArray(data) ? data[0].content : data.content,
        type: Array.isArray(data) ? data[0].type : data.type,
        timestamp: new Date(),
        agentName: activeAgent,
      };

      // Update conversation with both messages
      const finalUpdatedConversation = {
        ...updatedConversation,
        messages: [...updatedConversation.messages, agentMessage],
      };

      updateConversation(finalUpdatedConversation);
    } catch (error) {
      console.error("Error fetching message:", error);
      // Optionally add error handling UI here
    } finally {
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newQuery = e.target.value;
    setQuery(newQuery);

    const cursorPos = e.target.selectionStart || 0;
    setCursorPosition(cursorPos);

    // Check if '@' is typed and no agent is selected yet
    if (newQuery[cursorPos - 1] === "@" && !newQuery.includes("@", cursorPos)) {
      setShowAgentList(true);
    } else {
      setShowAgentList(false);
    }
  };

  const handleAgentSelect = (agent: string) => {
    const beforeAt = query.slice(0, query.lastIndexOf("@"));
    const newQuery = `${beforeAt}@${agent} `;
    setQuery(newQuery);
    setShowAgentList(false);
    setActiveAgent(agent);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Backspace") {
      const cursorPos = e.currentTarget.selectionStart || 0;
      const textBeforeCursor = query.slice(0, cursorPos);
      const lastAtIndex = textBeforeCursor.lastIndexOf("@");

      if (lastAtIndex !== -1 && !textBeforeCursor.includes(" ", lastAtIndex)) {
        e.preventDefault();
        const newQuery =
          query.slice(0, lastAtIndex) + "@" + query.slice(cursorPos);
        setQuery(newQuery);
        setShowAgentList(true);
        e.currentTarget.setSelectionRange(lastAtIndex + 1, lastAtIndex + 1);
      }
    }
  };

  const renderFormattedQuery = (text: string) => {
    const parts = text.split(/(@[\w\s]+)/);
    return parts.map((part, index) => {
      if (part.startsWith("@") && part.trim().length > 1) {
        return (
          <span key={index} className="italic text-gray-300">
            {part.trim()}
          </span>
        );
      }
      return part;
    });
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-gray-50 dark:bg-[#0A192F]">
      <div className="flex-1 p-8 flex flex-col">
        <h2 className="text-3xl font-bold mb-6 theme-aware-text">
          {projectName} - {currentConversation.name}
        </h2>

        <div
          ref={chatContainerRef}
          className="flex-grow overflow-y-auto pr-4 space-y-6 bg-gray-50 dark:bg-[#0A192F]"
          onScroll={handleScroll}
          style={{
            scrollbarWidth: "none",
            msOverflowStyle: "none",
          }}
        >
          <AnimatePresence mode="wait">
            {currentConversation.messages.length === 0 ? (
              <motion.div
                key="welcome"
                className="flex flex-col items-center justify-center text-center px-4 h-[50vh]"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
              >
                <h3 className="text-4xl sm:text-5xl font-bold mb-6 bg-gradient-to-r from-emerald-400 to-blue-500 bg-clip-text text-transparent">
                  Welcome to Your Workspace
                </h3>
                <p className="text-xl sm:text-2xl theme-aware-text font-light leading-relaxed max-w-3xl">
                  Tag an agent using @ and submit your query to start building
                  extraordinary solutions today!
                </p>
              </motion.div>
            ) : (
              currentConversation.messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.3 }}
                  className="w-full"
                >
                  {message.type === "user" ? (
                    <div className="bg-gray-100 dark:bg-[#1C2B3A] rounded-lg p-6 shadow-lg mb-4">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <Avatar className="h-8 w-8">
                            <AvatarFallback className="bg-blue-500 text-white">
                              {getInitials(userName)}
                            </AvatarFallback>
                          </Avatar>
                          <span className="text-sm theme-aware-text">You</span>
                        </div>
                        <span className="text-sm theme-aware-text">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      <div className="theme-aware-text">
                        {renderFormattedQuery(message.content)}
                      </div>
                    </div>
                  ) : (
                    <div className="bg-white dark:bg-[#0A192F] rounded-lg p-6 shadow-lg mb-4">
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center gap-3">
                          <div
                            className={`w-10 h-10 ${getAgentColor(
                              message.agentName || ""
                            )} rounded-lg flex items-center justify-center`}
                          >
                            {React.createElement(
                              getAgentIcon(message.agentName || ""),
                              { className: "w-6 h-6 text-white" }
                            )}
                          </div>
                          <span className="text-sm text-gray-600 dark:text-gray-400">
                            {message.agentName}
                          </span>
                        </div>
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          {message.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                      <div className="text-gray-900 dark:text-gray-200 prose dark:prose-invert max-w-none">
                        {renderContent(message.content)}
                      </div>
                    </div>
                  )}
                </motion.div>
              ))
            )}
          </AnimatePresence>
        </div>
        <style jsx global>{`
          ::-webkit-scrollbar {
            display: none;
          }
        `}</style>
      </div>

      <div className="p-6 bg-gray-50 dark:bg-[#0A192F]">
        <div className="flex items-center space-x-2 max-w-5xl mx-auto">
          <div className="relative flex-1">
            <Popover open={showAgentList} onOpenChange={setShowAgentList}>
              <PopoverTrigger asChild>
                <div className="relative w-full">
                  <Input
                    type="text"
                    placeholder="Type @ to tag an agent, then ask your question..."
                    value={query}
                    onChange={handleInputChange}
                    onKeyDown={handleKeyDown}
                    onKeyPress={(e) => e.key === "Enter" && handleSubmitQuery()}
                    className="w-full bg-gray-50 dark:bg-[#0A192F] border-gray-300 dark:border-gray-800 theme-aware-text placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-emerald-500 focus:border-transparent rounded-full py-6 pr-14"
                    render={(props) => (
                      <div {...props} className={props.className}>
                        {renderFormattedQuery(query)}
                      </div>
                    )}
                  />
                </div>
              </PopoverTrigger>
              <PopoverContent
                className="w-64 bg-white dark:bg-[#1C2B3A] border-gray-300 dark:border-gray-800 theme-aware-text rounded-md shadow-lg"
                sideOffset={5}
                align="start"
              >
                <div className="grid gap-2 p-2">
                  {selectedAgents.map((agent) => (
                    <Button
                      key={agent}
                      variant="ghost"
                      className="flex items-center justify-start hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                      onClick={() => handleAgentSelect(agent)}
                    >
                      {React.createElement(getAgentIcon(agent), {
                        className: "w-4 h-4 mr-2",
                      })}
                      {agent}
                    </Button>
                  ))}
                </div>
              </PopoverContent>
            </Popover>
            <div className="absolute inset-y-0 right-0 flex items-center pr-3 space-x-2">
              <Button
                onClick={() => {}}
                className="bg-transparent hover:bg-gray-200 dark:hover:bg-gray-700 theme-aware-text rounded-full p-2"
              >
                <Copy className="w-4 h-4" />
              </Button>
              <Button
                onClick={() => {}}
                className="bg-transparent hover:bg-gray-200 dark:hover:bg-gray-700 theme-aware-text rounded-full p-2"
              >
                <Zap className="w-4 h-4" />
              </Button>
            </div>
          </div>
          <Button
            onClick={handleSubmitQuery}
            disabled={isLoading || !query.trim()}
            className={`${
              isLoading ? "bg-gray-400" : "bg-emerald-500 hover:bg-emerald-600"
            } text-white px-6 py-6 rounded-full`}
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-4 w-4 border-2 border-b-transparent border-white mr-2" />
            ) : (
              <Send className="w-4 h-4 mr-2" />
            )}
            {isLoading ? "Processing..." : "Send"}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ProjectWorkspace;
