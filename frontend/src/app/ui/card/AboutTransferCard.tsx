"use client";
import React from "react";
import SendToMobileMoneyCard from "@/app/ui/card/SendToMobileMoneyCard"; 

const TransferPage = () => {
  return (
    <div className="flex flex-col lg:flex-row lg:gap-1 gap-6 p-6">
      
      <div className="w-full lg:w-2/3">
        <SendToMobileMoneyCard />
      </div>

      <div className="w-full lg:w-1/3 flex flex-col gap-6">
        
        <div className="bg-white border border-gray-300 p-6 rounded-lg">
          <h2 className="text-xl font-bold mb-4">About this transfer</h2>

          <div className="mb-4">
            <h3 className="font-semibold text-gray-700 mb-1">How it works</h3>
            <p className="text-sm text-gray-600">
              We use the Bitcoin Lightning Network to send money instantly and with minimal fees. Your recipient will receive funds directly to their mobile money account.
            </p>
          </div>

          <div className="mb-4">
            <h3 className="font-semibold text-gray-700 mb-1">Fees</h3>
            <p className="text-sm text-gray-600">
              You pay only <strong>1%</strong> fee, compared to 7–10% with traditional remittance services. No hidden charges.
            </p>
          </div>

          <div>
            <h3 className="font-semibold text-gray-700 mb-1">Delivery time</h3>
            <p className="text-sm text-gray-600">
              Funds are typically delivered to the recipient's mobile money account within <strong>5 minutes</strong>.
            </p>
          </div>
        </div>

        <div className="bg-white border border-gray-300 p-6 rounded-lg">
          <h2 className="text-xl font-bold mb-4">Supported Providers</h2>
          <ul className="space-y-3 text-sm text-gray-700">
            <li className="flex border p-4 rounded-md border-gray-400 items-center gap-2">
              <span className="text-xl">📱</span> MTN Mobile Money
            </li>
            <li className="flex border p-4 rounded-md border-gray-400 items-center gap-2">
              <span className="text-xl">📲</span> Airtel Money
            </li>
            <li className="flex border p-4 rounded-md border-gray-400 items-center gap-2">
              <span className="text-xl">💰</span> M-Pesa
            </li>
            <li className="flex border p-4 rounded-md border-gray-400 items-center gap-2">
              <span className="text-xl">🟠</span> Orange Money
            </li>
          </ul>
        </div>

      </div>
    </div>
  );
};

export default TransferPage;
