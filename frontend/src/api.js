export const startScan = async (url, threads, rate) => {
  const response = await fetch('/api/start', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url, threads, rate }),
  });
  return response.json();
};

export const getStatus = async () => {
  const response = await fetch('/api/status');
  return response.json();
};

export const downloadReport = (filename) => {
  window.location.href = `/api/report/${filename}`;
};