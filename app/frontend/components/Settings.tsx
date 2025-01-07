import { Moon, Sun } from 'lucide-react'
import { Button } from "@/components/ui/button"

interface SettingsProps {
  theme: 'light' | 'dark'
  toggleTheme: () => void
  onClose: () => void
}

export default function Settings({ theme, toggleTheme, onClose }: SettingsProps) {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 w-80">
        <h2 className="text-2xl font-bold mb-4 theme-aware-text">Settings</h2>
        <div className="flex items-center justify-between mb-4">
          <span className="theme-aware-text">Theme</span>
          <Button
            onClick={toggleTheme}
            variant="outline"
            size="icon"
            className="theme-aware-bg theme-aware-text"
          >
            {theme === 'light' ? <Moon className="h-[1.2rem] w-[1.2rem]" /> : <Sun className="h-[1.2rem] w-[1.2rem]" />}
          </Button>
        </div>
        <Button onClick={onClose} className="w-full">Close</Button>
      </div>
    </div>
  )
}

