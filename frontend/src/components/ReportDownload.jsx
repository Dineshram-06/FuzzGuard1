import React from 'react';
import { downloadReport } from '../api';

const ReportDownload = ({ files }) => {
  return (
    <div>
      <h2 className="text-xl font-semibold mb-2">Download Reports</h2>
      <button onClick={() => downloadReport(files.json)} className="bg-green-500 text-white p-2 rounded mr-2">
        JSON
      </button>
      <button onClick={() => downloadReport(files.csv)} className="bg-green-500 text-white p-2 rounded mr-2">
        CSV
      </button>
      <button onClick={() => downloadReport(files.md)} className="bg-green-500 text-white p-2 rounded">
        Markdown
      </button>
    </div>
  );
};

export default ReportDownload;