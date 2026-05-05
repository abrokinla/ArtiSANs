'use client';

interface Review {
  id: number;
  rating: number;
  comment: string;
  reviewer_username: string;
  created_at: string;
}

interface ReviewListProps {
  reviews: Review[];
}

export default function ReviewList({ reviews }: ReviewListProps) {
  if (reviews.length === 0) {
    return <p className="text-gray-500">No reviews yet.</p>;
  }

  return (
    <div className="space-y-3">
      {reviews.map((review) => (
        <div key={review.id} className="border rounded p-4">
          <div className="flex justify-between items-start">
            <div>
              <div className="font-semibold">{review.reviewer_username}</div>
              <div className="text-yellow-400">
                {'★'.repeat(review.rating)}{'☆'.repeat(5 - review.rating)}
              </div>
              <div className="text-gray-700 mt-1">{review.comment}</div>
            </div>
            <div className="text-sm text-gray-500">
              {new Date(review.created_at).toLocaleDateString()}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
