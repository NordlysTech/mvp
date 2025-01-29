'use client'

import { useState, useCallback } from 'react'
import { motion } from 'framer-motion'
import { ArrowLeft, Upload, X, FileText, AlertTriangle, Shield, ClipboardList, List, Gauge, Wrench, PenLineIcon as PipeLine, Layers } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { toast } from "@/components/ui/use-toast"
import { Card } from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import React from 'react'

const agentIcons: { [key: string]: React.ElementType } = {
  'HAZID Report Agent': AlertTriangle,
  'HAZOP Draft Agent': Shield,
  'Risk Assessment Draft Agent': AlertTriangle,
  'LOPA Draft Agent': Layers,
  'SRS Draft Agent': FileText,
  'ERP Draft Agent': ClipboardList,
  'Equipment List Agent': List,
  'Instruments List Agent': Gauge,
  'Line List Agent': PipeLine,
  'Valve Agent': Wrench,
}

interface Project {
  id: string
  name: string
}

interface DocumentUploadProps {
  agentName: string
  agentIcon?: React.ElementType
  onBack: () => void
  recentProjects: Project[]
}

const documentTypes = [
  'P&ID',
  'Process Flow Diagram',
  'Equipment Datasheet',
  'Operating Procedure',
  'Safety Document',
  'Technical Specification',
  'Other'
]

interface UploadedFile extends File {
  preview?: string
}

export default function DocumentUpload({ agentName, agentIcon, onBack, recentProjects }: DocumentUploadProps) {
  const [bundleName, setBundleName] = useState('')
  const [selectedType, setSelectedType] = useState<string>('')
  const [selectedProject, setSelectedProject] = useState<string>('')
  const [files, setFiles] = useState<UploadedFile[]>([])
  const [showNoProjectsDialog, setShowNoProjectsDialog] = useState(false)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(prev => [
      ...prev,
      ...acceptedFiles.map(file => Object.assign(file, {
        preview: URL.createObjectURL(file)
      }))
    ])
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg'],
      'text/*': ['.txt', '.csv']
    }
  })

  const removeFile = (name: string) => {
    setFiles(files => files.filter(file => file.name !== name))
  }

  const handleUpload = () => {
    if (!bundleName.trim()) {
      toast({
        title: "Bundle name required",
        description: "Please enter a name for this document bundle",
        variant: "destructive",
      })
      return
    }

    if (!selectedType) {
      toast({
        title: "Document type required",
        description: "Please select a document type",
        variant: "destructive",
      })
      return
    }

    if (!selectedProject) {
      toast({
        title: "Project required",
        description: "Please select a project",
        variant: "destructive",
      })
      return
    }

    if (files.length === 0) {
      toast({
        title: "No files selected",
        description: "Please add at least one file",
        variant: "destructive",
      })
      return
    }

    // Handle upload logic here
    toast({
      title: "Upload started",
      description: "Your documents are being processed",
    })
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="icon"
          onClick={onBack}
          className="rounded-full"
        >
          <ArrowLeft className="h-6 w-6" />
        </Button>
        <h2 className="text-3xl font-semibold text-gray-900 dark:text-white flex items-center">
          {agentIcon && React.createElement(agentIcon, { className: "w-8 h-8 mr-3 text-violet-500" })}
          {agentName}
        </h2>
      </div>

      <Card className="bg-white dark:bg-gray-900 border-gray-300 dark:border-gray-700 max-w-2xl mx-auto">
        <div className="p-6">
          <div className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="bundleName">Bundle Name</Label>
              <Input
                id="bundleName"
                placeholder="Enter a name for this document bundle"
                value={bundleName}
                onChange={(e) => setBundleName(e.target.value)}
                className="bg-white dark:bg-gray-800"
              />
            </div>

            <div {...getRootProps()} className="space-y-2">
              <Label>Documents</Label>
              <div className={`border-2 border-dashed rounded-lg p-8 text-center ${
                isDragActive ? 'border-primary bg-primary/5' : 'border-gray-300 dark:border-gray-700 bg-gray-100 dark:bg-gray-800'
              }`}>
                <input {...getInputProps()} />
                <Upload className="mx-auto h-12 w-12 text-gray-400" />
                <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                  Drop your files here, or click to select files
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-500">
                  Supports PDF, PNG, JPG, TXT, CSV
                </p>
              </div>
            </div>

            {files.length > 0 && (
              <div className="space-y-2">
                <Label>Selected Files</Label>
                <div className="space-y-2">
                  {files.map((file) => (
                    <div
                      key={file.name}
                      className="flex items-center justify-between p-2 bg-gray-100 dark:bg-gray-800 rounded-lg"
                    >
                      <div className="flex items-center space-x-2">
                        <FileText className="h-4 w-4 text-gray-500" />
                        <span className="text-sm text-gray-700 dark:text-gray-300">{file.name}</span>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removeFile(file.name)}
                        className="h-8 w-8"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Document Type</Label>
                <Select value={selectedType} onValueChange={setSelectedType}>
                  <SelectTrigger className="bg-white dark:bg-gray-800">
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    {documentTypes.map((type) => (
                      <SelectItem key={type} value={type}>
                        {type}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Project</Label>
                <Dialog open={showNoProjectsDialog} onOpenChange={setShowNoProjectsDialog}>
                  <DialogTrigger asChild>
                    <Select
                      value={selectedProject}
                      onValueChange={setSelectedProject}
                      onOpenChange={(open) => {
                        if (open && recentProjects.length === 0) {
                          setShowNoProjectsDialog(true)
                        }
                      }}
                    >
                      <SelectTrigger className="bg-white dark:bg-gray-800">
                        <SelectValue placeholder="Select project" />
                      </SelectTrigger>
                      <SelectContent>
                        {recentProjects.map((project) => (
                          <SelectItem key={project.id} value={project.id}>
                            {project.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>No Projects Available</DialogTitle>
                      <DialogDescription>
                        You haven't created any projects yet. Please create a project before uploading documents.
                      </DialogDescription>
                    </DialogHeader>
                    <Button onClick={() => setShowNoProjectsDialog(false)}>Close</Button>
                  </DialogContent>
                </Dialog>
              </div>
            </div>

            <Button
              className="w-full"
              size="lg"
              onClick={handleUpload}
            >
              Upload & Process
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}

