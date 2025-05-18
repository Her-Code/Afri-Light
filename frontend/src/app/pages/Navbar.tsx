"use client"
import { Zap } from "lucide-react";

import { useState, useEffect } from "react";

const NavBar = () => {
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) setIsOpen(false);
    };

    document.addEventListener("keydown", handleKeyDown);
    
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [isOpen]);

  useEffect(() => {
    document.body.style.overflow = isOpen ? "hidden" : "auto";
  }, [isOpen]);

  return (
    <nav className="fixed w-full p-3 bg-white z-50">
      <div className="flex items-center justify-between">

        <div>
          <p className="text-xl font-bold gap-2">
            <a href="/" className="flex items-center">
              <Zap/>
              AfriLight
            </a>
          </p>
        </div>


        <div className="md:hidden">
          <button onClick={() => setIsOpen(!isOpen)}>
            <svg 
              className="h-8 w-8 fill-current text-black"
              fill="none" strokeLinecap="round" 
              strokeLinejoin="round" strokeWidth="2" 
              viewBox="0 0 24 24" stroke="currentColor">
              <path d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
          </button>
        </div>

        <div className="hidden md:block">
          <ul className="flex space-x-8 text-sm font-sans">
            <li><a href="/dashboard" className="transition duration-300 hover:text-blue-400">Dashboard</a></li>
            <li><a href="/sendMoney" className="transition duration-300 hover:text-blue-400">Send Money</a></li>
            <li><a href="/transaction" className="transition duration-300 hover:text-blue-400">Transaction</a></li>
            <li>
              <a href="/profile">
                <img src="/user.svg" alt="user" className="h-6 w-6 rounded-full" />
              </a>
            </li>
          </ul>
        </div>


        {isOpen && (
          <div className="fixed inset-0 bg-black opacity-50 z-10" onClick={() => setIsOpen(false)}></div>
        )}


        <aside 
          className={`p-5 fixed top-0 left-0 w-64 bg-white h-full overflow-auto z-30 transform transition-all duration-300 ${
            isOpen ? "translate-x-0" : "-translate-x-full"
          }`}
        >
          <button className="absolute top-4 right-4" onClick={() => setIsOpen(false)}>
            <svg 
              className="w-6 h-6"
              fill="none" strokeLinecap="round" 
              strokeLinejoin="round" strokeWidth="2"
              viewBox="0 0 24 24" stroke="currentColor">
              <path d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>

          <span className="flex w-full items-center p-4 border-b gap-2">
            <a href="/" className="flex items-center">
              <Zap/>
              AfriLight
            </a>
          </span>

          <ul className="divide-y font-sans">
            <li><a href="/dashboard" className="block my-4 transition duration-300 hover:text-blue-400" onClick={() => setIsOpen(false)}>Dashboard</a></li>
            <li><a href="/sendMoney" className="block my-4 transition duration-300 hover:text-blue-400" onClick={() => setIsOpen(false)}>Send Money</a></li>
            <li><a href="/transaction" className="block my-4 transition duration-300 hover:text-blue-400" onClick={() => setIsOpen(false)}>Transaction</a></li>
            <li>
              <a href="/profile">
                <img src="/user.svg" alt="user" className="h-6 w-6 rounded-full" />
              </a>
            </li>
          </ul>
        </aside>

      </div>
    </nav>
  );
};

export default NavBar;
