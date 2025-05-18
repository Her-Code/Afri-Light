"use client";
import React, { useState } from "react";

const SendToMobileMoneyCard = () => {
  const [currency, setCurrency] = useState("USD");
  const [mobileProvider, setMobileProvider] = useState("");
  const [amount, setAmount] = useState(25);
  const [country, setCountry] = useState("");
  const [mobileNumber, setMobileNumber] = useState("");

  return (
    <div className="border border-gray-300 bg-white p-8 rounded-md w-full max-w-lg">
      <h2 className="text-2xl font-bold">Send to Mobile Money</h2>
      <p className="text-sm text-gray-500 mb-6">Send money to mobile money accounts across Africa</p>

      <div className="border border-gray-200 p-2 rounded-md mb-4">
        <h2>Currency Converter</h2>
        <label className="block text-sm font-semibold mb-2">Amount</label>
        <input
          type="number"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md mb-4"
        />
        <label className="block text-sm font-semibold mb-2">Currency</label>
        <select
          value={currency}
          onChange={(e) => setCurrency(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md mb-4"
        >
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
          <option value="GBP">GBP</option>
          <option value="KES">KES</option>
          <option value="NGN">NGN</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold mb-2">Mobile Money Provider</label>
        <select
          value={mobileProvider}
          onChange={(e) => setMobileProvider(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md mb-4"
        >
          <option value="">Select provider</option>
          <option value="MTN">MTN</option>
          <option value="Airtel">Airtel</option>
          <option value="Vodacom">Vodacom</option>
          <option value="Orange">Orange</option>
        </select>
      </div>

      <div className="mb-4">
        <label className="block text-sm font-semibold mb-2">Country</label>
        <select
          value={country}
          onChange={(e) => setCountry(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded-md mb-4"
        >
          <option value="">Select country</option>
          <option value="UGA">Uganda</option>
          <option value="KEN">Kenya</option>
          <option value="TZA">Tanzania</option>
          <option value="NGA">Nigeria</option>
        </select>
      </div>

      <div className="mb-6">
        <label className="block text-sm font-semibold mb-2">Recipient Mobile Money Number</label>
        <input
          type="text"
          value={mobileNumber}
          onChange={(e) => setMobileNumber(e.target.value)}
          placeholder="e.g., +256701234567"
          className="w-full p-2 border border-gray-300 rounded-md"
        />
        <p className="text-sm text-gray-500 mt-1">Enter the recipient's mobile money account number, including country code</p>
      </div>

      <button className="w-full bg-blue-600 text-white p-2 rounded-md">
        Send
      </button>
    </div>
  );
};

export default SendToMobileMoneyCard;
