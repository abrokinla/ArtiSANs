'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getMyProfile, getMyJobs } from '@/lib/api';
import { useAuth } from '@/context/AuthContext';

export default function DashboardPage() {
  const [profile, setProfile] = useState<any>(null);
  const [jobs, setJobs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const { user, token } = useAuth();

  useEffect(() => {
    if (!token) {
      router.push('/auth');
      return;
    }

    async function loadDashboard() {
      try {
        const profileData = await getMyProfile(token!);
        setProfile(profileData);

        const jobsData = await getMyJobs(token!);
        setJobs(jobsData);
      } catch (error) {
        console.error('Error loading dashboard:', error);
      } finally {
        setLoading(false);
      }
    }

    loadDashboard();
  }, [router, token]);

  if (loading) return <div className="text-center py-12">Loading...</div>;
  if (!user) return null;

  const activeJobs = jobs.filter((j: any) => ['assigned', 'in_progress'].includes(j.status));
  const completedJobs = jobs.filter((j: any) => j.status === 'completed');

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold mb-8">Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-600 text-sm mb-1">Total Jobs</h3>
            <p className="text-3xl font-bold">{jobs.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-600 text-sm mb-1">Active Jobs</h3>
            <p className="text-3xl font-bold text-blue-600">{activeJobs.length}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-gray-600 text-sm mb-1">Completed</h3>
            <p className="text-3xl font-bold text-green-600">{completedJobs.length}</p>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <div className="flex gap-4 flex-wrap">
            {user.role === 'client' && (
              <button
                onClick={() => router.push('/jobs/post')}
                className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
              >
                Post a Job
              </button>
            )}
            <button
              onClick={() => router.push('/search')}
              className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
            >
              Find Artisans
            </button>
            {user.role === 'artisan' && (
              <button
                onClick={() => router.push('/dashboard/my-bids')}
                className="bg-purple-600 text-white px-6 py-2 rounded hover:bg-purple-700"
              >
                My Bids
              </button>
            )}
            <button
              onClick={() => router.push('/profile/edit')}
              className="bg-gray-600 text-white px-6 py-2 rounded hover:bg-gray-700"
            >
              Edit Profile
            </button>
          </div>
        </div>

        {/* Active Jobs */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Active Jobs</h2>
          {activeJobs.length === 0 ? (
            <p className="text-gray-500">
              No active jobs.{' '}
              {user.role === 'client' ? (
                <a href="/jobs/post" className="text-blue-600">Post a job</a>
              ) : (
                <a href="/jobs" className="text-blue-600">Find jobs</a>
              )}{' '}
              to get started.
            </p>
          ) : (
            <div className="space-y-4">
              {activeJobs.map((job: any) => (
                <div key={job.id} className="border rounded-lg p-4">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold">{job.title}</h3>
                      <p className="text-gray-600 text-sm">{job.location}</p>
                      <p className="text-gray-700 mt-1">{job.description}</p>
                    </div>
                    <span className={`px-3 py-1 rounded-full text-xs ${
                      job.status === 'in_progress' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'
                    }`}>
                      {job.status}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Profile Summary */}
        {profile && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Profile Summary</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-gray-600 text-sm">Phone</p>
                <p className="font-medium">{profile.phone_number}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Location</p>
                <p className="font-medium">{profile.location || 'Not set'}</p>
              </div>
              <div>
                <p className="text-gray-600 text-sm">Subscription</p>
                <p className="font-medium capitalize">{profile.subscription_tier}</p>
              </div>
              {user.role === 'artisan' && (
                <div>
                  <p className="text-gray-600 text-sm">Bids Remaining</p>
                  <p className="font-medium">{profile.bids_remaining}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
