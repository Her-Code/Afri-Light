import React from 'react'
import { CreditCard } from 'lucide-react';

const SendButton = () => {
  return (
    <button className='bg-[#313ad6] dark:bg-dark-2 border-dark dark:border-dark-2 rounded-lg inline-flex items-center justify-center py-3 px-7 text-center text-base text-white hover:border-body-color disabled:bg-gray-3 disabled:border-gray-3 disabled:text-dark-5 h-10 w-96 transition duration-300 hover:bg-blue-900'>
      <CreditCard className='mr-2' />
      Send Money
    </button>
  )
}

export default SendButton;