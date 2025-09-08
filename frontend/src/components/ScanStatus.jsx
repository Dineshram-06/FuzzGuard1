import React from 'react';

const ScanStatus = ({ state, progress }) => {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-2">Scan Status</h2>
      <p>State: {state}</p>
      <p>Progress: {progress.toFixed(2)}%</p>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${progress}%` }}></div>
      </div>
    </div>
  );
};

export default ScanStatus;