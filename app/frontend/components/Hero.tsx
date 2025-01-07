'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'

export default function Hero() {
  return (
    <section id="hero" className="min-h-screen flex items-center justify-center">
      <div className="container px-4 text-center z-10">
        <motion.h1
          className="text-5xl md:text-7xl font-light leading-tight mb-8"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          Developing{' '}
          <span className="gradient-text font-normal">Solvi</span>,
          <br />
          the Next Generation
          <br />
          <span className="gradient-text font-normal">AI-Driven</span> Eco System
        </motion.h1>
        <motion.p
          className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto mb-12"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          Transforming the Chemical and Process Engineering Industry through Advanced Artificial Intelligence Solutions
        </motion.p>
        <motion.div
          className="flex gap-4 justify-center"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          <Link
            href="#cta"
            className="gradient-button px-6 py-3 rounded-md text-lg hover:opacity-90 transition-opacity"
          >
            Join Waitlist
          </Link>
          <Link
            href="#features"
            className="border border-purple-500/20 px-6 py-3 rounded-md text-lg hover:bg-purple-500/10 transition-colors"
          >
            Learn More
          </Link>
        </motion.div>
      </div>
    </section>
  )
}

