import React from 'react';

const riskColors = {
  high: 'bg-red-200',
  medium: 'bg-yellow-200',
  low: 'bg-green-200',
};

const FindingsTable = ({ findings }) => {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-2">Findings</h2>
      <table className="w-full border-collapse border">
        <thead>
          <tr>
            <th className="border p-2">Path</th>
            <th className="border p-2">Status</th>
            <th className="border p-2">Length</th>
            <th className="border p-2">Technologies</th>
            <th className="border p-2">Risk</th>
          </tr>
        </thead>
        <tbody>
          {findings.map((find, index) => (
            <tr key={index} className={riskColors[find.risk] || ''}>
              <td className="border p-2">{find.path}</td>
              <td className="border p-2">{find.status_code}</td>
              <td className="border p-2">{find.length}</td>
              <td className="border p-2">{find.technologies.join(', ')}</td>
              <td className="border p-2">{find.risk}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FindingsTable;   