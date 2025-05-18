import React from 'react'
import SendToMobileMoneyCard from '../ui/card/SendToMobileMoneyCard'
import NavBar from '../pages/Navbar'
import AboutTransferCard from '../ui/card/AboutTransferCard'
import TransferDetails from '../ui/card/AboutTransferCard'
import TransferPage from '../ui/card/AboutTransferCard'

const page = () => {
  return (
    <div>
      <NavBar />
      <div className='pt-20 pl-20'>
        <h1 className='font-bold text-3xl mb-3'>Send Money</h1>
      </div>
      <TransferPage />
    </div>
  )
}

export default page
