import Image from "next/image";
import Navbar from "./pages/Navbar";
import Hero from "./pages/Hero";
import LandingPage from "./pages/LandingPage";

export default function Home() {
  return (
    <div >
      <Navbar />
      <Hero />
      <LandingPage />
    </div>
  );
}
