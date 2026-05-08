'use client';

import { useState } from 'react';

interface SubmitReviewFormProps {
  onSubmit: (data: { rating: number; comment: string }) => Promise<void>;
  disabled?: boolean;
}

export default function SubmitReviewForm({ onSubmit, disabled }: SubmitReviewFormProps) {
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!comment) return;

    try {
      setSubmitting(true);
      await onSubmit({ rating, comment });
      setComment('');
      setRating(5);
    } catch (err) {
      console.error('Failed to submit review:', err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-gray-50 rounded">
      <h3 className="font-semibold mb-3">Write a Review</h3>
      <div className="mb-3">
        <label className="block text-sm font-medium mb-1">Rating</label>
        <div className="flex gap-2">
          {[1, 2, 3, 4, 5].map((star) => (
            <button
              key={star}
              type="button"
              onClick={() => setRating(star)}
              className={`text-2xl ${star <= rating ? 'text-yellow-400' : 'text-gray-300'}`}
            >
              ★
            </button>
          ))}
        </div>
      </div>
      <div className="mb-3">
        <label className="block text-sm font-medium mb-1">Comment</label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          className="w-full px-3 py-2 border rounded"
          rows={3}
          required
        />
      </div>
      <button
        type="submit"
        disabled={submitting || disabled}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {submitting ? 'Submitting...' : 'Submit Review'}
      </button>
    </form>
  );
}
