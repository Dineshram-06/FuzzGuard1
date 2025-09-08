import React, { useState, useEffect } from 'react';
import './index.css';
import { startScan, getStatus } from './api';
import ScanForm from './components/ScanForm';
import ScanStatus from './components/ScanStatus';
import FindingsTable from './components/FindingsTable';
import ReportDownload from './components/ReportDownload';

function App() {
  const [status, setStatus] = useState({ state: 'idle', progress: 0, results: [], report_files: {} });

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const data = await getStatus();
        setStatus(data);
      } catch (error) {
        console.error('Error fetching status:', error);
      }
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  const handleStartScan = async (url, threads, rate) => {
    try {
      await startScan(url, threads, rate);
    } catch (error) {
      console.error('Error starting scan:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <div className="max-w-4xl mx-auto bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold mb-6 text-center">FuzzGuard</h1>
        <ScanForm onStart={handleStartScan} />
        <ScanStatus state={status.state} progress={status.progress} />
        {status.results.length > 0 && <FindingsTable findings={status.results} />}
        {status.state === 'completed' && <ReportDownload files={status.report_files} />}
      </div>
    </div>
  );
}

export default App;