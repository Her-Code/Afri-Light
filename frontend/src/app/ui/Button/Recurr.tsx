import React from 'react'
import { Clock } from 'lucide-react';

const RecurrButton = () => {
  return (
    <button className='bg-white dark:bg-dark-2 border-dark dark:border-dark-2 rounded-lg inline-flex items-center justify-center py-3 px-7 text-center text-base text-black hover:border-body-color disabled:bg-gray-3 disabled:border-gray-3 disabled:text-dark-5 h-10 w-96 transition duration-300 hover:bg-[#f8f8fa]'>
      <Clock className='mr-2' />
      Recurring Payments
    </button>
  )
}

export default RecurrButton;