'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Book, Cog, Calculator, FileText, Send } from 'lucide-react'

type Message = {
  id: number;
  text: string;
  sender: 'user' | 'ai';
  agent: 'knowledge' | 'action' | 'solver' | 'report';
}

const agentInfo = {
  knowledge: { name: 'Knowledge AI', icon: Book, color: 'text-blue-500' },
  action: { name: 'Action AI', icon: Cog, color: 'text-green-500' },
  solver: { name: 'Dynamic AI Solver', icon: Calculator, color: 'text-purple-500' },
  report: { name: 'Report Generator', icon: FileText, color: 'text-orange-500' },
}

export default function AIInterface() {
  const [activeAgent, setActiveAgent] = useState<'knowledge' | 'action' | 'solver' | 'report'>('knowledge')
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (input.trim()) {
      const newMessage: Message = {
        id: Date.now(),
        text: input.trim(),
        sender: 'user',
        agent: activeAgent,
      }
      setMessages([...messages, newMessage])
      setInput('')
      
      // Simulate AI response
      setTimeout(() => {
        const aiResponse: Message = {
          id: Date.now() + 1,
          text: `This is a simulated response from the ${agentInfo[activeAgent].name} agent.`,
          sender: 'ai',
          agent: activeAgent,
        }
        setMessages(prev => [...prev, aiResponse])
      }, 1000)
    }
  }

  return (
    <Card className="w-full max-w-4xl bg-gray-900/50 backdrop-blur-lg border-gray-800">
      <CardHeader>
        <CardTitle className="text-2xl font-bold text-center text-white">Solvi AI Interface</CardTitle>
        <CardDescription className="text-center text-gray-400">Interact with our advanced AI agents</CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="knowledge" className="w-full" onValueChange={(value) => setActiveAgent(value as any)}>
          <TabsList className="grid w-full grid-cols-4">
            {Object.entries(agentInfo).map(([key, { name, icon: Icon }]) => (
              <TabsTrigger key={key} value={key} className="flex items-center gap-2">
                <Icon className="w-4 h-4" />
                <span className="hidden sm:inline">{name}</span>
              </TabsTrigger>
            ))}
          </TabsList>
          {Object.keys(agentInfo).map((key) => (
            <TabsContent key={key} value={key} className="mt-4">
              <ScrollArea className="h-[400px] w-full rounded-md border border-gray-800 p-4">
                <AnimatePresence initial={false}>
                  {messages.filter(m => m.agent === key).map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ duration: 0.3 }}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`}
                    >
                      <div className={`flex items-start gap-2 max-w-[80%] ${message.sender === 'user' ? 'flex-row-reverse' : ''}`}>
                        <Avatar>
                          <AvatarFallback>{message.sender === 'user' ? 'U' : 'AI'}</AvatarFallback>
                          <AvatarImage src={message.sender === 'user' ? '/user-avatar.png' : `/ai-${key}-avatar.png`} />
                        </Avatar>
                        <div className={`rounded-lg p-3 ${message.sender === 'user' ? 'bg-blue-600' : 'bg-gray-800'}`}>
                          {message.text}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </ScrollArea>
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
      <CardFooter>
        <div className="flex w-full items-center space-x-2">
          <Input
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
            className="flex-grow"
          />
          <Button onClick={handleSend} className="bg-blue-600 hover:bg-blue-700">
            <Send className="w-4 h-4 mr-2" />
            Send
          </Button>
        </div>
      </CardFooter>
    </Card>
  )
}

