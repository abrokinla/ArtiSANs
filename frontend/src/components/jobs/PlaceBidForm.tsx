'use client';

import { useState } from 'react';

interface PlaceBidFormProps {
  jobId: string;
  token: string;
  onSubmit: (data: { amount: number; message: string; estimated_days: number }) => Promise<void>;
}

export default function PlaceBidForm({ jobId, token, onSubmit }: PlaceBidFormProps) {
  const [bidAmount, setBidAmount] = useState('');
  const [bidMessage, setBidMessage] = useState('');
  const [bidDays, setBidDays] = useState('1');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!bidAmount) return;

    try {
      setSubmitting(true);
      await onSubmit({
        amount: Number(bidAmount),
        message: bidMessage,
        estimated_days: Number(bidDays),
      });
      setBidAmount('');
      setBidMessage('');
      setBidDays('1');
    } catch (err) {
      console.error('Failed to place bid:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-gray-50 rounded">
      <h3 className="font-semibold mb-3">Place a Bid</h3>
      <div className="grid grid-cols-3 gap-4 mb-3">
        <div>
          <label className="block text-sm font-medium mb-1">Amount (₦)</label>
          <input
            type="number"
            value={bidAmount}
            onChange={(e) => setBidAmount(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-1">Estimated Days</label>
          <input
            type="number"
            value={bidDays}
            onChange={(e) => setBidDays(e.target.value)}
            className="w-full px-3 py-2 border rounded"
            min="1"
            required
          />
        </div>
      </div>
      <div className="mb-3">
        <label className="block text-sm font-medium mb-1">Message</label>
        <textarea
          value={bidMessage}
          onChange={(e) => setBidMessage(e.target.value)}
          className="w-full px-3 py-2 border rounded"
          rows={3}
          placeholder="Explain why you're the best fit..."
        />
      </div>
      <button
        type="submit"
        disabled={submitting}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {submitting ? 'Submitting...' : 'Place Bid'}
      </button>
    </form>
  );
}
