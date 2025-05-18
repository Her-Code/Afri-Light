"use client";
import React from "react";
import SendButton from "../Button/SendButton";
import RecurrButton from "../Button/Recurr";

const WalletCard = () => {
  return (
    <div className="border border-gray-100 bg-white p-6 rounded-md w-[900px] h-[300px] shadow-lg">
      <h2 className="text-2xl font-medium ">Wallet Overview</h2>
      <p className="mb-4 text-gray-500 text-sm">Your current wallet balance and status</p>
      <section className="mb-2">
        <p className="text-sm text-gray-500">Current Balance</p>
        <p className="text-3xl font-semibold">2,500,000 sats</p>
        <p className="text-lg text-gray-600">≈ 0.02500000 BTC</p>
      </section>
      <div className="flex justify-between mt-6">
        <SendButton />
        <RecurrButton />
      </div>
    </div>
  );
};

export default WalletCard;
