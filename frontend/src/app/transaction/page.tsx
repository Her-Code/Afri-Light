"use client";
import React, { useState } from "react";
import NavBar from "../pages/Navbar";

const mockData = [
  {
    id: 1,
    type: "Send",
    usdAmount: "12.50",
    sats: "25000",
    recipient: "mama@mtngcash.com",
    date: "May 17, 2025, 07:41 PM",
    status: "Completed",
  },
  {
    id: 2,
    type: "Send",
    usdAmount: "25.00",
    sats: "50000",
    recipient: "sister@airtel.pay",
    date: "May 16, 2025, 07:41 PM",
    status: "Completed",
  },
  {
    id: 3,
    type: "Receive",
    usdAmount: "50.00",
    sats: "100000",
    recipient: "me@afrilight.com",
    date: "May 15, 2025, 07:41 PM",
    status: "Completed",
  },
];

const TransactionsPage = () => {
  const [transactions] = useState(mockData);
  const [searchTerm, setSearchTerm] = useState("");
  const [dateFrom, setDateFrom] = useState("");
  const [dateTo, setDateTo] = useState("");

  const filteredTransactions = transactions.filter((tx) => {
    const matchesSearch = tx.recipient.includes(searchTerm) || tx.type.toLowerCase().includes(searchTerm.toLowerCase());
    const txDate = new Date(tx.date);
    const afterFrom = dateFrom ? txDate >= new Date(dateFrom) : true;
    const beforeTo = dateTo ? txDate <= new Date(dateTo) : true;
    return matchesSearch && afterFrom && beforeTo;
  });


  return (
    <div>
      <NavBar />
      <main className="p-6 pt-20">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
      <input
        type="text"
        placeholder="Search recipient or type..."
        className="w-full md:w-1/3 p-2 border border-gray-300 rounded-md"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />

      <div className="flex items-center gap-2">
        <label htmlFor="from">From</label>
        <input
          type="date"
          id="from"
          value={dateFrom}
          onChange={(e) => setDateFrom(e.target.value)}
          className="border border-gray-300 rounded-md p-1"
        />

        <label htmlFor="to">To</label>
        <input
          type="date"
          id="to"
          value={dateTo}
          onChange={(e) => setDateTo(e.target.value)}
          className="border border-gray-300 rounded-md p-1"
        />
      </div>
    </div>

      <section className="mb-6">
        <h1 className="text-3xl font-bold mb-1">Transaction History</h1>
        <p className="text-gray-600">Your recent transactions and their status</p>
      </section>

      <div className="bg-white border border-gray-300 rounded-lg shadow p-4 overflow-x-auto">
        <table className="w-full text-sm">
          <thead className="border-b border-gray-300 text-left">
            <tr className="text-gray-700">
              <th className="px-4 py-2">Type</th>
              <th className="px-4 py-2">Amount</th>
              <th className="px-4 py-2">Recipient</th>
              <th className="px-4 py-2">Date</th>
              <th className="px-4 py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {filteredTransactions.map((tx) => (
              <tr key={tx.id} className="border-b last:border-none">
                <td className="px-4 py-3">{tx.type}</td>
                <td className="px-4 py-3">
                  USD {tx.usdAmount} <br />
                  <span className="text-xs text-gray-500">{tx.sats} sats</span>
                </td>
                <td className="px-4 py-3">{tx.recipient}</td>
                <td className="px-4 py-3">{tx.date}</td>
                <td className="px-4 py-3">
                  <span
                    className={`inline-block px-3 py-1 text-xs rounded-full ${
                      tx.status === "Completed"
                        ? "bg-green-100 text-green-700"
                        : tx.status === "Pending"
                        ? "bg-yellow-100 text-yellow-700"
                        : "bg-red-100 text-red-700"
                    }`}
                  >
                    {tx.status}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      </main>
    </div>
  );
};

export default TransactionsPage;
