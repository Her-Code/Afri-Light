import React from 'react'
import Service from '../ui/components/Services'
import StepByStep from '../ui/components/StepByStep'
import FinalCTA from '../ui/components/FinalCTA'

const LandingPage = () => {
  return (
    <>
        <section className='flex flex-col items-center justify-center mt-20'>
            <h1 className='font-bold text-2xl mb-2.5'>Why Choose AfriLight?</h1><br />
            <p className='text-xl text-neutral-700 mb-10'>
              <span>Our cutting-edge technology combines the speed of Lightning Network with the </span><br />
              <span className='pl-55'>convenience of mobile money.</span>
            </p>
            <Service />
        </section>
        <section className='flex flex-col items-center justify-center mt-20'>
          <h1 className='font-bold text-2xl mb-3'>How It Works</h1>
          <p className='text-xl text-neutral-700'>Sending money with AfriLight is quick and easy, even if you're new to digital currencies.</p>
        </section>
        <StepByStep />
        <FinalCTA />
    </>
  )
}

export default LandingPage
