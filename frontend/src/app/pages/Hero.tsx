import React from 'react'
import GetStarted from '@/app/ui/Button/GetStarted';
import Login from '@/app/ui/Button/Login';

const Hero = () => {
  return (
    <div className="h-screen flex"
      style={{
        background: 'linear-gradient(to bottom, #ffffff, #ebebeb)',
      }}>
        <section className='flex flex-col pt-20 pl-10 pr-10'>
            <h1 className='font-bold text-6xl pt-30 pb-5'>
                <span>Fast, Low-Cost</span> <br />
                <span>Remittances to Africa</span> 
            </h1>
                <p className='text-neutral-700 text-2xl'>
                    <span>Send money to your loved ones instantly for a fraction</span><br />
                    <span>of the cost using the Lightning Network.</span> 
                </p>
            <div className='flex items-center justify-center mt-8'>
                <GetStarted />
                <Login />
            </div>
        </section>
      <img src="/hero.png" alt="hero" className="h-100 rounded-md mt-30" />
    </div>
  )
}

export default Hero
