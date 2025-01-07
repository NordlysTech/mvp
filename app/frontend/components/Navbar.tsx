'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { motion } from 'framer-motion'

export default function Navbar() {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <motion.nav
      className={`sticky top-0 z-50 transition-colors duration-300 ${
        isScrolled ? 'bg-[#0a0d1f]/80 backdrop-blur-lg' : 'bg-transparent'
      }`}
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="container mx-auto px-4 py-6 flex justify-between items-center">
        <Link href="/" className="text-lg font-extralight tracking-widest shimmer">
          NORDLYS TECH
        </Link>
        <div className="flex gap-6 items-center">
          <Link href="#features" className="hover:text-purple-300 transition-colors">
            Features
          </Link>
          <Link href="#about" className="hover:text-purple-300 transition-colors">
            About
          </Link>
          <Link
            href="#cta"
            className="gradient-button px-4 py-2 rounded-md hover:opacity-90 transition-opacity"
          >
            Get Demo
          </Link>
        </div>
      </div>
    </motion.nav>
  )
}

