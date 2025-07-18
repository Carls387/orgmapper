import React, { useState } from 'react';

export default function App() {
  const [company, setCompany] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  async function handleSearch() {
    if (!company) return;
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`/api/search?company=${encodeURIComponent(company)}`);
      if (!res.ok) throw new Error('API error');
      const data = await res.json();
      setResults(data);
    } catch (e) {
      setError('Failed to fetch results');
      setResults([]);
    }
    setLoading(false);
  }

  return (
    <div className="max-w-xl mx-auto p-4 font-sans">
      <h1 className="text-2xl font-bold mb-4">Employee Finder</h1>
      <input
        type="text"
        value={company}
        onChange={e => setCompany(e.target.value)}
        placeholder="Enter company name"
        className="w-full p-2 border border-gray-300 rounded mb-2"
      />
      <button
        onClick={handleSearch}
        className="px-4 py-2 bg-blue-600 text-white rounded"
        disabled={loading}
      >
        {loading ? 'Searching...' : 'Search'}
      </button>
      {error && <p className="mt-4 text-red-600">{error}</p>}
      <ul className="mt-6 space-y-4">
        {results.length === 0 && !loading && <li>No results found</li>}
        {results.map((emp, i) => (
          <li key={i} className="border p-3 rounded">
            <p className="font-semibold">{emp.name}</p>
            <p>{emp.job_title} at {emp.company}</p>
            <a
              href={emp.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 underline"
            >
              LinkedIn Profile
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

