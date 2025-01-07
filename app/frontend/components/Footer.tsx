import Link from 'next/link'
import { Twitter, Instagram, GitlabIcon as GitHub, Linkedin } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="bg-gradient-to-b from-[#0B0D13]/95 to-[#0B0D13] backdrop-blur-lg text-white border-t border-white/10">
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
          {/* Company Info */}
          <div className="space-y-6">
            <div className="text-lg font-extralight tracking-widest">NORDLYS TECH</div>
            <p className="text-gray-400 font-light">
              Transforming engineering through advanced AI solutions and innovative technology.
            </p>
            <div className="space-y-2 text-gray-400 font-light">
              <p>Sollerudveien</p>
              <p>Lysaker, 0283 Norway</p>
              <p>contact@nordlystech.com</p>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-6">
            <h3 className="text-sm font-light tracking-widest text-gray-300">QUICK LINKS</h3>
            <div className="grid grid-cols-1 gap-3">
              <Link href="#features" className="text-gray-400 hover:text-white transition-colors font-light">
                Features
              </Link>
              <Link href="#about" className="text-gray-400 hover:text-white transition-colors font-light">
                About
              </Link>
              <Link href="#" className="text-gray-400 hover:text-white transition-colors font-light">
                Contact
              </Link>
              <Link href="#" className="text-gray-400 hover:text-white transition-colors font-light">
                Privacy Policy
              </Link>
            </div>
          </div>

          {/* Connect */}
          <div className="space-y-6">
            <h3 className="text-sm font-light tracking-widest text-gray-300">CONNECT</h3>
            <div className="flex gap-4">
              <a href="#" className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/10 transition-colors">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/10 transition-colors">
                <Instagram className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/10 transition-colors">
                <GitHub className="w-5 h-5" />
              </a>
              <a href="#" className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/10 transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10 text-center">
          <p className="text-gray-400 font-light">&copy; 2024 Nordlys Tech. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

