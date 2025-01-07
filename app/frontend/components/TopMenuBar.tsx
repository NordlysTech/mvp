'use client'

import { Minimize2, Square, X, Settings } from 'lucide-react'

const menuItems = ['File', 'Edit', 'View', 'Window', 'Help']

interface TopMenuBarProps {
  onSettingsClick: () => void
}

export default function TopMenuBar({ onSettingsClick }: TopMenuBarProps) {
  return (
    <div className="flex justify-between items-center h-8 theme-aware-bg theme-aware-border border-b">
      <div className="flex items-center px-2">
        {menuItems.map((item) => (
          <button
            key={item}
            className="px-3 py-1 text-sm theme-aware-text hover:bg-gray-200 dark:hover:bg-gray-800 rounded-sm"
          >
            {item}
          </button>
        ))}
      </div>
      <div className="flex items-center">
        <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800" onClick={onSettingsClick}>
          <Settings className="h-3 w-3 theme-aware-text" />
        </button>
        <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800">
          <Minimize2 className="h-3 w-3 theme-aware-text" />
        </button>
        <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800">
          <Square className="h-3 w-3 theme-aware-text" />
        </button>
        <button className="p-2 hover:bg-gray-200 dark:hover:bg-gray-800">
          <X className="h-3 w-3 theme-aware-text" />
        </button>
      </div>
    </div>
  )
}

