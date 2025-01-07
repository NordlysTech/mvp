'use client'

import { motion } from 'framer-motion'

export default function CTA() {
  return (
    <section id="cta" className="py-20">
      <div className="container px-4 mx-auto max-w-6xl">
        <motion.div
          className="bg-gradient-to-br from-blue-600/10 to-purple-600/10 border border-white/5 rounded-lg p-12 flex flex-col md:flex-row items-center justify-between gap-8"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <div className="md:w-1/2 text-center md:text-left">
            <h2 className="text-3xl md:text-4xl font-light mb-6">
              Ready to Transform Your Engineering Workflow?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join the waitlist for early access to Solvi and be among the first to experience the future of engineering.
            </p>
          </div>
          <div className="md:w-1/2">
            <form className="space-y-4">
              <input
                type="email"
                placeholder="Enter your email"
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-md focus:outline-none focus:border-purple-500"
                required
              />
              <input
                type="text"
                placeholder="Organization name"
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-md focus:outline-none focus:border-purple-500"
                required
              />
              <textarea
                placeholder="Leave a comment (optional)"
                className="w-full px-4 py-2 bg-white/5 border border-white/10 rounded-md focus:outline-none focus:border-purple-500 h-24"
              ></textarea>
              <button
                type="submit"
                className="w-full gradient-button py-3 rounded-md text-lg hover:opacity-90 transition-opacity"
              >
                Join Waitlist
              </button>
            </form>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

