"use client";
import React from "react";

const TransactionHistoryCard = () => {
  return (
    <div className="border border-gray-100 mt-10 bg-white p-6 rounded-lg w-[1280px] shadow-md">

      <div className="border-t border-gray-300 pt-6">
        <h3 className="text-xl font-semibold">Transaction History</h3>
        <p className="text-sm mb-4 text-gray-500">Your recent transactions and their status</p>

        <table className="w-full text-sm table-auto">
          <thead className="border-b border-gray-300">
            <tr>
              <th className="px-4 py-2 text-left">Type</th>
              <th className="px-4 py-2 text-left">Amount</th>
              <th className="px-4 py-2 text-left">Recipient</th>
              <th className="px-4 py-2 text-left">Date</th>
              <th className="px-4 py-2 text-left">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td className="px-4 py-2">Send</td>
              <td className="px-4 py-2">USD 12.50</td>
              <td className="px-4 py-2">mama@mtngcash.com</td>
              <td className="px-4 py-2">May 17, 2025, 07:41 PM</td>
              <td className="px-4 py-2 text-green-500">Completed</td>
            </tr>
            <tr>
              <td className="px-4 py-2">Send</td>
              <td className="px-4 py-2">USD 25.00</td>
              <td className="px-4 py-2">sister@airtel.pay</td>
              <td className="px-4 py-2">May 16, 2025, 07:41 PM</td>
              <td className="px-4 py-2 text-green-500">Completed</td>
            </tr>
            <tr>
              <td className="px-4 py-2">Receive</td>
              <td className="px-4 py-2">USD 50.00</td>
              <td className="px-4 py-2">me@afrilight.com</td>
              <td className="px-4 py-2">May 15, 2025, 07:41 PM</td>
              <td className="px-4 py-2 text-green-500">Completed</td>
            </tr>
            <tr>
              <td className="px-4 py-2">Send</td>
              <td className="px-4 py-2">USD 75.00</td>
              <td className="px-4 py-2">brother@mpesa.com</td>
              <td className="px-4 py-2">May 18, 2025, 07:41 PM</td>
              <td className="px-4 py-2 text-amber-500">Pending</td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>
  );
};

export default TransactionHistoryCard;
