'use client'

import { useEffect, useRef } from 'react'

export default function AuroraBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    canvas.width = window.innerWidth
    canvas.height = window.innerHeight

    const createAuroraGradient = (x: number, y: number, radius: number) => {
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius)
      gradient.addColorStop(0, 'rgba(15, 23, 42, 0)')
      gradient.addColorStop(0.5, 'rgba(56, 30, 114, 0.3)')
      gradient.addColorStop(1, 'rgba(15, 23, 42, 0)')
      return gradient
    }

    const drawAurora = (time: number) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      const centerX = canvas.width / 2
      const centerY = canvas.height / 2
      const maxRadius = Math.max(canvas.width, canvas.height)

      for (let i = 0; i < 3; i++) {
        const offset = i * (Math.PI * 2 / 3)
        const x = centerX + Math.cos(time * 0.0005 + offset) * 200
        const y = centerY + Math.sin(time * 0.0005 + offset) * 200
        ctx.fillStyle = createAuroraGradient(x, y, maxRadius)
        ctx.fillRect(0, 0, canvas.width, canvas.height)
      }

      requestAnimationFrame(drawAurora)
    }

    drawAurora(0)

    const handleResize = () => {
      canvas.width = window.innerWidth
      canvas.height = window.innerHeight
    }

    window.addEventListener('resize', handleResize)

    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }, [])

  return (
    <canvas
      ref={canvasRef}
      className="fixed top-0 left-0 w-full h-full pointer-events-none z-[-1]"
    />
  )
}

