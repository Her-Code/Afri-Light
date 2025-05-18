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
            <div className="flex items-center gap-2 mb-4">
              <Music2 className="h-8 w-8 text-primary transition-colors duration-300 hover:text-blue-400" />
              <span className={'text-xl md:text-2xl font-bold'}>
                <span className="text-white">sherehe</span>
                <span className="text-blue-600">na</span>
                <span className="text-white">fullufullu</span>
              </span>
            </div>
            <p className="text-white/70 mb-6">
              Bringing the best vibes to your events with a mix of Kenyan music, Rhumba, Reggae, and more.
            </p>
            <div className="flex gap-4">
              <Link href="#" className="text-white/70 transition-transform transform hover:text-blue-500 hover:scale-110">
                <Twitter className="h-6 w-6" />
              </Link>
              <Link href="#" className="text-white/70 transition-transform transform hover:text-red-500 hover:scale-110">
                <Youtube className="h-6 w-6" />
              </Link>
              <Link href="#" className="text-white/70 transition-transform transform hover:text-pink-500 hover:scale-110">
                <Instagram className="h-6 w-6" />
              </Link>
              <Link href="#" className="text-white/70 transition-transform transform hover:text-blue-700 hover:scale-110">
                <Facebook className="h-6 w-6" />
              </Link>
            </div>
          </div>

          <div>
            <h3 className="text-xl font-bold mb-4">Quick Links</h3>
            <ul className="space-y-3">
              <li>
                <Link href="/" className="text-white/70 hover:text-blue-500 transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/mixes" className="text-white/70 hover:text-blue-500 transition-colors">
                  Mixes
                </Link>
              </li>
              <li>
                <Link href="/services" className="text-white/70 hover:text-blue-500 transition-colors">
                  Services
                </Link>
              </li>
              <li>
                <Link href="/gallery" className="text-white/70 hover:text-blue-500 transition-colors">
                  Gallery
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-white/70 hover:text-blue-500 transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Services Section (Replaces Events) */}
          <div>
            <h3 className="text-xl font-bold mb-4">Services</h3>
            <ul className="space-y-4">
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-medium">DJ & Live Mixes</span>
                  <span className="text-sm text-white/50">Customized music for events</span>
                </Link>
              </li>
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-medium">Event Hosting</span>
                  <span className="text-sm text-white/50">Engaging MCs & event coordination</span>
                </Link>
              </li>
              <li>
                <Link href="#" className="text-white/70 hover:text-blue-500 transition-colors block">
                  <span className="block font-medium">Private Parties</span>
                  <span className="text-sm text-white/50">House parties, weddings, birthdays</span>
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Section */}
          <div>
            <h3 className="text-xl font-bold mb-4">Contact</h3>
            <div className="space-y-4">
              <p className="flex items-start gap-3">
                <MessageCircle className="h-5 w-5 text-primary shrink-0 mt-1" />
                <span className="text-white/70">info@shereheanfullufullu.com</span>
              </p>
              <p className="flex items-start gap-3">
                <Headphones className="h-5 w-5 text-primary shrink-0 mt-1" />
                <span className="text-white/70">+254 123 456 789</span>
              </p>
              {/* <WhatsApp/> */}
            </div>
          </div>
        </div>

        <div className="border-t border-white/10 pt-8 text-center text-white/50">
          <p>© {new Date().getFullYear()} Dj Brownskin. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}