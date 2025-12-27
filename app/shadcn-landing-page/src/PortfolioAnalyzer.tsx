import { useState } from 'react';

interface AnalysisResult {
  data: {
    correlation_matrix: number[][];
    average_correlation: number;
  };
}

const PortfolioAnalyzer = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [submittedTickers, setSubmittedTickers] = useState<string[]>([]);

  const analyzePortfolio = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const tickers = input.split(',').map(t => t.trim().toUpperCase()).filter(Boolean);
      
      if (tickers.length < 2) {
        throw new Error('Please enter at least two stock tickers');
      }

      setSubmittedTickers(tickers);

      const response = await fetch('http://localhost:3000/compute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tickers ,input })
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      setResult(await response.json());
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to analyze portfolio');
    } finally {
      setLoading(false);
    }
  };

  // Calculate recommendation based on average correlation
  const recommendation = result?.data?.average_correlation ? 
    result.data.average_correlation > 0.65 ?
      "Your portfolio is highly correlated. Consider diversifying into other sectors or asset classes." :
      "Your portfolio is well-diversified!"
    : '';

  return (
    <div className="max-w-4xl mx-auto p-6 text-black">
      <h1 className="text-2xl font-bold mb-6 text-white">Portfolio Correlation Analyzer</h1>
      
      <form onSubmit={analyzePortfolio} className="mb-8">
        <div className="mb-4">
          <label className="block mb-2 font-medium">
            Enter stock tickers (comma-separated):
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="e.g., AAPL, MSFT, TSLA"
              className="w-full mt-1 p-2 border rounded"
            />
          </label>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? 'Analyzing...' : 'Analyze Portfolio'}
        </button>
      </form>

      {error && (
        <div className="p-4 mb-4 text-red-700 bg-red-100 rounded-lg">
          Error: {error}
        </div>
      )}

      {result && (
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Analysis Results</h2>
          
          <div className="mb-6">
            <h3 className="font-medium mb-2">Correlation Matrix</h3>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr>
                    <th className="p-2 border bg-gray-50"></th>
                    {submittedTickers.map(ticker => (
                      <th key={ticker} className="p-2 border bg-gray-50">
                        {ticker}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {submittedTickers.map((ticker, i) => (
                    <tr key={ticker}>
                      <td className="p-2 border bg-gray-50 font-medium">{ticker}</td>
                      {result.data.correlation_matrix[i].map((corr, j) => (
                        <td
                          key={`${i}-${j}`}
                          className="p-2 border text-center"
                        >
                          {corr.toFixed(4)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="mb-4">
            <p className="font-medium">
              Average Correlation: {' '}
              <span className="font-normal">
                {result.data.average_correlation.toFixed(4)}
              </span>
            </p>
          </div>

          {recommendation && (
            <div className="p-4 bg-blue-50 rounded-lg">
              <p className="text-blue-800">{recommendation}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default PortfolioAnalyzer;