import Link from "next/link"
import { Instagram, Twitter, Youtube, Music2, Facebook, Headphones, MessageCircle } from "lucide-react"
// import { orbitron } from "@/app/ui/fonts";
// import WhatsApp from "../components/buttons/whatsappButton";

export default function Footer() {
  return (
    <footer className="bg-[#061018] text-white pt-16 pb-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">
          <div>
            <h2 className="flex font-bold items-center gap-2 mb-4">
              Afri-Light
            </h2>
            <p className="text-white/70 mb-6">
              Fast, low-cost remittances to Africa powered by the Lightning Network.
            </p>
          </div>

          <div>
            <h3 className="text-xl font-bold mb-4">Company</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/" className="text-white/70 hover:text-blue-500 transition-colors">
                  About
                </Link>
              </li>
              <li>
                <Link href="/mixes" className="text-white/70 hover:text-blue-500 transition-colors">
                  Careers
                </Link>
              </li>
              <li>
                <Link href="/services" className="text-white/70 hover:text-blue-500 transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="text-xl font-bold mb-4">Resources</h3>
            <ul className="space-y-4">
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-normal">Blog</span>
                </Link>
              </li>
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-normal">Help Center</span>
                </Link>
              </li>
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-normal"> Partners </span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Section */}
          <div>
            <h3 className="text-xl font-bold mb-4">Legal</h3>
            <ul className="space-y-4">
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-normal">Privacy Policy</span>
                </Link>
              </li>
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-normal">Terms of Service</span>
                </Link>
              </li>
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-normal"> Compliance </span>
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-white/10 pt-8 text-center text-white/50">
          <p>© {new Date().getFullYear()} Afrilight. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}