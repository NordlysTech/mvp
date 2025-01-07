'use client'

import { motion } from 'framer-motion'
import { Book, Cog, Calculator, FileText } from 'lucide-react'

const features = [
  {
    title: 'Knowledge AI Agents',
    description: 'AI-powered systems designed to comprehend and analyze complex engineering principles, offering expert insights and support.',
    icon: Book,
    gradient: 'from-blue-600/10 to-purple-600/10',
    hoverGradient: 'from-blue-600/20 to-purple-600/20',
    iconColor: 'text-blue-400',
    titleColor: 'text-blue-300',
  },
  {
    title: 'Action AI Agents',
    description: 'Task-oriented AI models that execute domain-specific engineering tasks.',
    icon: Cog,
    gradient: 'from-purple-600/10 to-indigo-600/10',
    hoverGradient: 'from-purple-600/20 to-indigo-600/20',
    iconColor: 'text-purple-400',
    titleColor: 'text-purple-300',
  },
  {
    title: 'Advanced Dynamic AI Solvers',
    description: 'Real-time, numerical and analytical adaptive solutions for troubleshooting, problem solving, and system bottleneck analysis.',
    icon: Calculator,
    gradient: 'from-indigo-600/10 to-blue-600/10',
    hoverGradient: 'from-indigo-600/20 to-blue-600/20',
    iconColor: 'text-indigo-400',
    titleColor: 'text-indigo-300',
  },
  {
    title: 'Tailored Report and Document Generation',
    description: 'Knowledge and Standards based AI agents that transform data into actionable insights by generating multi-level reports both for engineers, operators, and business decisions makers.',
    icon: FileText,
    gradient: 'from-blue-600/10 to-purple-600/10',
    hoverGradient: 'from-blue-600/20 to-purple-600/20',
    iconColor: 'text-blue-400',
    titleColor: 'text-blue-300',
  },
]

export default function Features() {
  return (
    <section id="features" className="py-20">
      <div className="container px-4 mx-auto max-w-6xl">
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
        >
          <h2 className="text-3xl md:text-5xl font-light mb-6">
            Powered by
            <span className="gradient-text font-normal"> Proprietary Advanced AI</span>
          </h2>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Solvi combines cutting-edge artificial intelligence with deep engineering expertise and knowledge.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              className={`feature-block bg-gradient-to-br ${feature.gradient} backdrop-blur-md border border-white/5 rounded-xl p-6 shadow-lg hover:shadow-2xl hover:bg-gradient-to-br ${feature.hoverGradient} transition-all`}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              viewport={{ once: true }}
            >
              <feature.icon className={`w-12 h-12 mb-4 ${feature.iconColor}`} />
              <h3 className={`text-xl font-medium mb-2 ${feature.titleColor}`}>{feature.title}</h3>
              <p className="text-gray-300">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}

