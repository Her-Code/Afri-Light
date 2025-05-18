import { Wallet } from 'lucide-react'
import React from 'react'
import WalletCard from '../ui/card/walletCard'
import NavBar from '../pages/Navbar'
import Stats from '../ui/card/Stats'
import TransactionCard from '../ui/card/TransactionCard'
import TransactionHistoryCard from '../ui/card/TransactionHustoryCard'

const page = () => {
  return (
    <div className=''>
    <NavBar />
    <div className='pt-20 px-10 flex'>
        <WalletCard />
        <section className='ml-10'>
            <Stats />
        </section>
    </div>
    <div className='ml-10'>
        <TransactionCard />
    </div>
    <div className='ml-10'>
      <TransactionHistoryCard />
    </div>
    </div>
  )
}

export default page
