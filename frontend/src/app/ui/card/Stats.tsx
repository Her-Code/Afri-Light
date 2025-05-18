import React from 'react'

const Stats = () => {
  return (
    <div className='border border-gray-100 bg-white p-6 w-[400px] shadow-lg rounded-md h-[300px]'> 
      <h2 className='text-2xl font-medium'>Quick Stats</h2>
      <p className='mb-4 text-gray-500 text-sm'>Your remittance activity</p>
        <section className='mb-2'>
            <p className='text-sm text-gray-500'>Total Sent</p>
            <p className='text-2xl mb-2 font-semibold'>225,000 sats</p>
            <p className='text-sm text-gray-500'>Total saved in Fees</p>
            <p className='text-2xl text-green-600 mb-2 font-bold'>$24.50</p>
            <p className='text-sm text-gray-500'>Countries Sent To</p>
            <p className='font-bold text-2xl'>3</p>
        </section>
    </div>
  )
}

export default Stats
