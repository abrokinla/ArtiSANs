'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { getArtisanProfile } from '@/lib/api';

export default function ArtisanProfilePage() {
  const params = useParams();
  const id = params?.id as string;
  
  if (!id) {
    return <div className="p-8 text-center">Invalid artisan ID</div>;
  }
  const [artisan, setArtisan] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const t = localStorage.getItem('token');
    setToken(t);
    
    async function loadProfile() {
      try {
        const data = await getArtisanProfile(id as string, t!);
        setArtisan(data);
      } catch (error) {
        console.error('Error loading profile:', error);
      } finally {
        setLoading(false);
      }
    }
    
    if (t) {
      loadProfile();
    } else {
      setLoading(false);
    }
  }, [id]);

  const handleHire = () => {
    if (!token) {
      router.push('/auth');
      return;
    }
    // Navigate to job posting with artisan pre-selected
    router.push(`/jobs/post?artisan=${id}`);
  };

  if (loading) return <div className="text-center py-12">Loading...</div>;
  if (!artisan) return <div className="text-center py-12">Artisan not found</div>;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Profile */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-md p-6 mb-6">
              <div className="flex items-start mb-6">
                <div className="w-24 h-24 bg-gray-300 rounded-full mr-6"></div>
                <div className="flex-1">
                  <h1 className="text-3xl font-bold mb-2">
                    {artisan.user.first_name} {artisan.user.last_name}
                  </h1>
                  <p className="text-gray-600 mb-2">{artisan.location}</p>
                  <div className="flex items-center mb-2">
                    <span className="text-yellow-500 text-xl mr-1">★</span>
                    <span className="font-medium text-lg">{artisan.average_rating.toFixed(1)}</span>
                    <span className="text-gray-500 ml-2">({artisan.reviews_count} reviews)</span>
                  </div>
                  {artisan.is_verified && (
                    <span className="inline-block bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">
                      ✓ Verified Artisan
                    </span>
                  )}
                </div>
              </div>

              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-3">About</h2>
                <p className="text-gray-700">{artisan.bio || 'No bio provided.'}</p>
              </div>

              <div className="mb-6">
                <h2 className="text-xl font-semibold mb-3">Categories</h2>
                <div className="flex flex-wrap gap-2">
                  {artisan.categories.map((cat: string, idx: number) => (
                    <span key={idx} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                      {cat}
                    </span>
                  ))}
                </div>
              </div>

              {artisan.availability && (
                <div className="mb-6">
                  <h2 className="text-xl font-semibold mb-3">Availability</h2>
                  <p className="text-gray-700">{artisan.availability}</p>
                </div>
              )}
            </div>

            {/* Reviews Section */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Reviews</h2>
              {artisan.reviews && artisan.reviews.length > 0 ? (
                <div className="space-y-4">
                  {artisan.reviews.map((review: any, idx: number) => (
                    <div key={idx} className="border-b pb-4 last:border-b-0">
                      <div className="flex items-center mb-2">
                        <div className="w-10 h-10 bg-gray-300 rounded-full mr-3"></div>
                        <div>
                          <p className="font-medium">{review.reviewer_username}</p>
                          <div className="flex items-center">
                            {[1, 2, 3, 4, 5].map((star) => (
                              <span key={star} className={star <= review.rating ? 'text-yellow-500' : 'text-gray-300'}>
                                ★
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                      <p className="text-gray-700">{review.comment}</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-500">No reviews yet.</p>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6 sticky top-4">
              <div className="mb-4">
                <p className="text-gray-600 mb-1">Total Earnings</p>
                <p className="text-2xl font-bold">₦{parseFloat(artisan.total_earnings).toLocaleString()}</p>
              </div>
              
              <button
                onClick={handleHire}
                className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 font-semibold mb-3"
              >
                Hire {artisan.user.first_name}
              </button>
              
              <button className="w-full bg-gray-100 text-gray-700 py-3 rounded-lg hover:bg-gray-200 font-semibold">
                Send Message
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
