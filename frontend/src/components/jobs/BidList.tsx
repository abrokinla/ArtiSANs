'use client';

interface Bid {
  id: number;
  artisan_username: string;
  amount: number;
  message: string;
  estimated_days: number;
  is_accepted: boolean;
  created_at: string;
}

interface BidListProps {
  bids: Bid[];
  isClient: boolean;
  jobStatus: string;
  onAcceptBid?: (bidId: number) => void;
}

export default function BidList({ bids, isClient, jobStatus, onAcceptBid }: BidListProps) {
  if (bids.length === 0) {
    return <p className="text-gray-500">No bids yet.</p>;
  }

  return (
    <div className="space-y-3">
      {bids.map((bid) => (
        <div key={bid.id} className="border rounded p-4">
          <div className="flex justify-between items-start">
            <div>
              <div className="font-semibold">{bid.artisan_username}</div>
              <div className="text-sm text-gray-600">{bid.message}</div>
              <div className="text-sm text-gray-500 mt-1">
                Estimated: {bid.estimated_days} day(s) • {new Date(bid.created_at).toLocaleDateString()}
              </div>
            </div>
            <div className="text-right">
              <div className="text-xl font-bold text-green-600">₦{bid.amount.toLocaleString()}</div>
              {isClient && jobStatus === 'bidding' && onAcceptBid && (
                <button
                  onClick={() => onAcceptBid(bid.id)}
                  className="mt-2 px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700"
                >
                  Accept Bid
                </button>
              )}
              {bid.is_accepted && (
                <span className="mt-2 inline-block px-2 py-1 bg-green-100 text-green-800 text-sm rounded">
                  Accepted
                </span>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
