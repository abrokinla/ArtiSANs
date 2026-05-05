'use client';

import { getCategories, searchArtisans, getJobs } from '@/lib/api';
import { useEffect, useState } from 'react';

export default function Home() {
  const [categories, setCategories] = useState<any[]>([]);
  const [featuredArtisans, setFeaturedArtisans] = useState<any[]>([]);
  const [featuredJobs, setFeaturedJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const cats = await getCategories();
        setCategories(cats);
        
        // Get some featured artisans
        const artisans = await searchArtisans({ min_rating: 4 });
        setFeaturedArtisans(artisans.slice(0, 6));
        
        // Get featured jobs (open/bidding)
        const jobs = await getJobs({ status: 'bidding' });
        setFeaturedJobs(jobs.results?.slice(0, 6) || jobs.slice(0, 6));
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">Find Trusted Local Artisans</h1>
          <p className="text-xl mb-8">Connect with verified professionals in your area</p>
          
          {/* Quick Search */}
          <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-4">
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="What service do you need?"
                className="flex-1 px-4 py-3 text-gray-800 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Your location"
                className="flex-1 px-4 py-3 text-gray-800 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button className="bg-blue-600 text-white px-8 py-3 rounded hover:bg-blue-700 font-semibold">
                Search
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Popular Services</h2>
          {loading ? (
            <div className="text-center">Loading...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {categories.map((cat) => (
                <div key={cat.id} className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
                  <h3 className="text-xl font-semibold mb-2">{cat.name}</h3>
                  <p className="text-gray-600 mb-4">{cat.description}</p>
                  <button className="text-blue-600 hover:text-blue-800 font-medium">
                    Browse {cat.name} →
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Featured Jobs */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Featured Jobs</h2>
          {loading ? (
            <div className="text-center">Loading...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {featuredJobs.map((job) => (
                <div key={job.id} className="border rounded-lg p-6 hover:shadow-lg transition">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-xl font-semibold">{job.title}</h3>
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">
                      {job.status}
                    </span>
                  </div>
                  <p className="text-gray-600 mb-4 line-clamp-2">{job.description}</p>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <span>{job.category_name}</span>
                    <span>{job.location}</span>
                  </div>
                  {job.budget && (
                    <div className="mt-2 font-semibold text-green-600">
                      Budget: ₦{job.budget.toLocaleString()}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Featured Artisans */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-12">Featured Artisans</h2>
          {loading ? (
            <div className="text-center">Loading...</div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {featuredArtisans.map((artisan) => (
                <div key={artisan.id} className="border rounded-lg p-6 hover:shadow-lg transition">
                  <div className="flex items-center mb-4">
                    <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
                    <div>
                      <h3 className="font-semibold">{artisan.first_name} {artisan.last_name}</h3>
                      <p className="text-sm text-gray-600">{artisan.location}</p>
                    </div>
                  </div>
                  <div className="flex items-center mb-2">
                    <span className="text-yellow-500 mr-1">★</span>
                    <span>{artisan.average_rating.toFixed(1)}</span>
                    <span className="text-gray-500 ml-1">({artisan.review_count} reviews)</span>
                  </div>
                  {artisan.is_verified && (
                    <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                      Verified
                    </span>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-blue-50 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to get started?</h2>
          <p className="text-xl text-gray-600 mb-8">Join thousands of satisfied customers today</p>
          <div className="space-x-4">
            <button className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 font-semibold">
              Find an Artisan
            </button>
            <button className="bg-white text-blue-600 border-2 border-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 font-semibold">
              Join as Artisan
            </button>
          </div>
        </div>
      </section>
    </main>
  );
}
