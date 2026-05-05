'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { 
  getJobs, placeBid, getJobBids, acceptBid,
  openJobForBidding, startJob, completeJob, confirmJobCompletion,
  createReview, getArtisanReviews,
} from '@/lib/api';
import { useAuth } from '@/context/AuthContext';
import PlaceBidForm from '@/components/jobs/PlaceBidForm';
import BidList from '@/components/jobs/BidList';
import SubmitReviewForm from '@/components/reviews/SubmitReviewForm';
import ReviewList from '@/components/reviews/ReviewList';
import Link from 'next/link';

interface Job {
  id: number;
  title: string;
  description: string;
  status: string;
  budget?: number;
  final_amount?: number;
  location: string;
  priority: string;
  category_name?: string;
  client_username: string;
  artisan_username?: string;
  artisan?: number;
  created_at: string;
  bids_count: number;
}

export default function JobDetailsPage() {
  const params = useParams();
  const id = params?.id as string;
  const router = useRouter();
  const { user, token } = useAuth();
  
  if (!id) {
    return <div className="p-8 text-center">Invalid job ID</div>;
  }
  
  const [job, setJob] = useState<Job | null>(null);
  const [bids, setBids] = useState<any[]>([]);
  const [reviews, setReviews] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id && token) {
      loadJob();
    }
  }, [id, token]);

  const loadJob = async () => {
    try {
      setLoading(true);
      const data = await getJobs();
      const jobData = Array.isArray(data) ? data.find((j: Job) => j.id === Number(id)) : null;
      
      if (!jobData) {
        setError('Job not found');
        return;
      }
      
      setJob(jobData);
      
      // Load bids if user is the client
      if (token && user?.role === 'client' && jobData.client_username === user.username) {
        const bidsData = await getJobBids(id, token);
        setBids(bidsData);
      }
      
      // Load reviews if job is completed and has an artisan
      if (jobData.status === 'completed' && jobData.artisan) {
        const reviewsData = await getArtisanReviews(jobData.artisan.toString());
        setReviews(reviewsData);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load job');
    } finally {
      setLoading(false);
    }
  };

  const handlePlaceBid = async (data: { amount: number; message: string; estimated_days: number }) => {
    if (!token || !user || user.role !== 'artisan') return;
    
    try {
      await placeBid(id, data, token);
      alert('Bid placed successfully!');
      loadJob();
    } catch (err: any) {
      alert(err.message || 'Failed to place bid');
    }
  };

  const handleAcceptBid = async (bidId: number) => {
    if (!token || !user || user.role !== 'client') return;
    
    if (!confirm('Accept this bid and assign the job?')) return;
    
    try {
      await acceptBid(bidId.toString(), token);
      alert('Bid accepted! Job assigned.');
      loadJob();
    } catch (err: any) {
      alert(err.message || 'Failed to accept bid');
    }
  };

  const handleOpenBidding = async () => {
    if (!token || !user || user.role !== 'client') return;
    
    try {
      await openJobForBidding(id, token);
      alert('Job opened for bidding!');
      loadJob();
    } catch (err: any) {
      alert(err.message || 'Failed to open bidding');
    }
  };

  const handleStartJob = async () => {
    if (!token || !user || user.role !== 'artisan') return;
    
    try {
      await startJob(id, token);
      alert('Job started!');
      loadJob();
    } catch (err: any) {
      alert(err.message || 'Failed to start job');
    }
  };

  const handleCompleteJob = async () => {
    if (!token || !user || user.role !== 'artisan') return;
    
    try {
      await completeJob(id, token);
      alert('Job marked as complete! Awaiting client confirmation.');
      loadJob();
    } catch (err: any) {
      alert(err.message || 'Failed to complete job');
    }
  };

  const handleConfirmCompletion = async () => {
    if (!token || !user || user.role !== 'client') return;
    
    if (!confirm('Confirm job completion and release payment?')) return;
    
    try {
      await confirmJobCompletion(id, token);
      alert('Job completed! Payment released to artisan.');
      loadJob();
    } catch (err: any) {
      alert(err.message || 'Failed to confirm completion');
    }
  };

  const handleSubmitReview = async (data: { rating: number; comment: string }) => {
    if (!token || !user || user.role !== 'client' || !job) return;
    
    try {
      await createReview({
        job: id,
        rating: data.rating,
        comment: data.comment,
      }, token);
      
      alert('Review submitted!');
      loadJob();
    } catch (err: any) {
      alert(err.message || 'Failed to submit review');
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-center text-red-600">{error}</div>;
  if (!job) return <div className="p-8 text-center">Job not found</div>;

  const isClient = user?.role === 'client' && job.client_username === user?.username;
  const isAssignedArtisan = user?.role === 'artisan' && job.artisan_username === user?.username;

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Link href="/dashboard" className="text-blue-600 hover:underline mb-4 inline-block">
        ← Back to Dashboard
      </Link>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h1 className="text-2xl font-bold mb-2">{job.title}</h1>
            <div className="flex gap-2 text-sm text-gray-600">
              <span className={`px-2 py-1 rounded ${
                job.status === 'completed' ? 'bg-green-100 text-green-800' :
                job.status === 'in_progress' ? 'bg-blue-100 text-blue-800' :
                job.status === 'assigned' ? 'bg-purple-100 text-purple-800' :
                job.status === 'bidding' ? 'bg-yellow-100 text-yellow-800' :
                'bg-gray-100 text-gray-800'
              }`}>
                {job.status.replace('_', ' ').toUpperCase()}
              </span>
              <span className="px-2 py-1 bg-gray-100 rounded">{job.priority.toUpperCase()}</span>
              {job.category_name && <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded">{job.category_name}</span>}
            </div>
          </div>
          {job.budget && (
            <div className="text-2xl font-bold text-green-600">
              ₦{job.budget.toLocaleString()}
            </div>
          )}
        </div>

        <p className="text-gray-700 mb-4">{job.description}</p>

        <div className="grid grid-cols-2 gap-4 text-sm text-gray-600 mb-4">
          <div>
            <strong>Location:</strong> {job.location}
          </div>
          <div>
            <strong>Client:</strong> {job.client_username}
          </div>
          {job.artisan_username && (
            <div>
              <strong>Artisan:</strong> {job.artisan_username}
            </div>
          )}
          {job.final_amount && (
            <div>
              <strong>Final Amount:</strong> ₦{job.final_amount.toLocaleString()}
            </div>
          )}
          <div>
            <strong>Posted:</strong> {new Date(job.created_at).toLocaleDateString()}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2 mb-4">
          {isClient && job.status === 'pending' && (
            <button
              onClick={handleOpenBidding}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Open for Bidding
            </button>
          )}
          
          {isAssignedArtisan && job.status === 'assigned' && (
            <button
              onClick={handleStartJob}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              Start Job
            </button>
          )}
          
          {isAssignedArtisan && job.status === 'in_progress' && (
            <button
              onClick={handleCompleteJob}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Mark as Complete
            </button>
          )}
          
          {isClient && job.status === 'completed' && (
            <button
              onClick={handleConfirmCompletion}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Confirm & Release Payment
            </button>
          )}
        </div>
      </div>

      {/* Bidding Section */}
      {(job.status === 'bidding' || job.status === 'assigned') && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Bids ({bids.length})</h2>
          
          {/* Place Bid Form (Artisans only) */}
          {user?.role === 'artisan' && job.status === 'bidding' && !isAssignedArtisan && (
            <PlaceBidForm 
              jobId={id} 
              token={token!} 
              onSubmit={handlePlaceBid} 
            />
          )}

          {/* Bids List */}
          <BidList 
            bids={bids} 
            isClient={isClient} 
            jobStatus={job.status}
            onAcceptBid={handleAcceptBid}
          />
        </div>
      )}

      {/* Reviews Section */}
      {job.status === 'completed' && (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Reviews</h2>
          
          {/* Submit Review (Client only) */}
          {isClient && reviews.length === 0 && (
            <SubmitReviewForm 
              onSubmit={handleSubmitReview}
            />
          )}

          {/* Reviews List */}
          <ReviewList reviews={reviews} />
        </div>
      )}
    </div>
  );
}
