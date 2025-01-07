'use client'

import { motion } from 'framer-motion'

export default function About() {
  return (
    <section id="about" className="py-20">
      <div className="container px-4 mx-auto max-w-4xl text-center">
        <motion.h2
          className="text-3xl md:text-5xl font-light mb-8"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          About
          <span className="gradient-text font-normal"> Solvi</span>
        </motion.h2>
        <div className="space-y-6">
          {[
            "At Nordlys Tech, we are developing Solvi, an advanced AI-driven eco-system that is redefining the future of chemical and process engineering. Solvi revolutionizes how engineers access and apply specialized knowledge, leveraging specialized AI agents that offer expertise in different areas of the industry.",
            "This empowers engineers to solve complex problems faster, more accurately, and with greater efficiency. At the core of Solvi is an intelligent, evolving eco-system that synthesizes vast amounts of data to deliver actionable solutions across a wide range of engineering challenges.",
            "Whether generating reports, aiding with simulations, or solving intricate calculations, Solvi offers a seamless, intuitive platform for engineers to work smarter. By integrating plant data and internal documents, Solvi enhances decision-making and streamlines operations, driving innovation and sustainable growth."
          ].map((paragraph, index) => (
            <motion.p
              key={index}
              className="text-xl text-gray-800" //Updated text color
              style={{ textAlign: 'justify' }}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              viewport={{ once: true }}
            >
              {paragraph}
            </motion.p>
          ))}
        </div>
      </div>
    </section>
  )
}

