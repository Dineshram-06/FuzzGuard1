import React, { useState } from 'react';

const ScanForm = ({ onStart }) => {
  const [url, setUrl] = useState('');
  const [threads, setThreads] = useState(5);
  const [rate, setRate] = useState(10);

  const handleSubmit = (e) => {
    e.preventDefault();
    onStart(url, threads, rate);
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6">
      <div className="mb-4">
        <label className="block text-gray-700">Target URL</label>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Threads</label>
        <input
          type="number"
          value={threads}
          onChange={(e) => setThreads(parseInt(e.target.value))}
          className="w-full p-2 border rounded"
          min="1"
          max="20"
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700">Rate (req/s)</label>
        <input
          type="number"
          value={rate}
          onChange={(e) => setRate(parseInt(e.target.value))}
          className="w-full p-2 border rounded"
          min="1"
          max="50"
        />
      </div>
      <button type="submit" className="bg-blue-500 text-white p-2 rounded w-full">
        Start Scan
      </button>
    </form>
  );
};

export default ScanForm;