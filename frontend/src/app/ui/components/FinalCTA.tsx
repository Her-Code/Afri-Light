import React from 'react'
import FCTAButton from '../Button/FCTAButton'

const FinalCTA = () => {
  return (
    <div className='flex flex-col items-center justify-center text-white mt-20 bg-blue-600'>
      <h1 className='font-bold text-2xl pt-10 pb-5'>Ready to save on Remittance</h1>
      <p className='text-xl mb-5'>Join thousands of users saving money on their international transfers to Africa.</p>
      <FCTAButton />
    </div>
  )
}

export default FinalCTA
