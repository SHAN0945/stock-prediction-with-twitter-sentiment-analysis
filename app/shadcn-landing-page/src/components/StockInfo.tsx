import React, { useState, useRef, useEffect } from 'react';
import { stocksData } from '@/data/data'; // Assuming this path is correct

interface StockInfoProps {
  stockSymbol: string;
}

// A simple loading spinner component - enhanced styling
const LoadingSpinner = () => (
  <div className="flex justify-center items-center my-8"> {/* Increased margin */}
    <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600"></div> {/* Theme color & size */}
    <p className="ml-3 text-slate-600">Loading prediction...</p> {/* Adjusted text color */}
  </div>
);

function StockInfo({ stockSymbol }: StockInfoProps) {
  const [showPrediction, setShowPrediction] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const predictionRef = useRef<HTMLDivElement>(null);

  // Ensure stock lookup is case-insensitive and handles potential undefined result
  const stock = stockSymbol ? stocksData[stockSymbol.toLowerCase()] : undefined;

  const handlePredictClick = () => {
    setIsLoading(true);
    setShowPrediction(false); // Hide previous prediction if any

    setTimeout(() => {
      setIsLoading(false);
      setShowPrediction(true);

      // Scroll logic using 0ms timeout
      setTimeout(() => {
        if (predictionRef.current) {
          predictionRef.current.scrollIntoView({
            behavior: 'smooth',
            block: 'nearest' // Changed from 'start' for potentially better view
          });
        }
      }, 0); // Use 0ms for ensuring DOM update before scroll

    }, 2000); // Simulate network delay/computation
  };

  // Render error state
  if (!stock) {
    return (
      <div className="max-w-4xl mx-auto mt-10 p-6 bg-red-50 border border-red-300 rounded-lg shadow-md text-center">
        <p className="text-red-700 font-medium">
          Stock data not found for symbol: <span className="font-bold">{stockSymbol || 'N/A'}</span>.
        </p>
        <p className="text-red-600 text-sm mt-2">
          Please check the symbol or ensure the data source is correct.
        </p>
      </div>
    );
  }

  // Render stock information
  return (
    <div className=" mx-auto mt-10 mb-10 flex align-middle justify-center"> {/* Added max-width and margin */}
      <div className="bg-white p-6 rounded-lg shadow-lg border border-slate-200 w-[90vw]">
        {/* Stock Header */}
        <div className="mb-6 pb-4 border-b border-slate-200">
          <h2 className="text-3xl font-bold text-slate-800">
            {stock.name}
            <span className="text-2xl text-slate-500 font-medium ml-2">({stock.symbol})</span>
          </h2>
        </div>

        {/* Main Content Row */}
        <div className='flex flex-col md:flex-row md:items-start gap-8 w-full mb-6'> {/* Increased gap */}
          {/* Left Column: Stock Details & Button */}
          <div className="w-full md:w-1/3 flex-shrink-0"> {/* Adjusted width */}
            <dl className="space-y-2"> {/* Using definition list */}
              <div className="flex justify-between py-1">
                <dt className="text-sm font-medium text-slate-500">Price:</dt>
                <dd className="text-sm text-slate-800 font-semibold">${stock.price.toFixed(2)}</dd>
              </div>
              <div className="flex justify-between py-1">
                <dt className="text-sm font-medium text-slate-500">Market Cap:</dt>
                <dd className="text-sm text-slate-800">${stock.marketCap}</dd>
              </div>
              <div className="flex justify-between py-1">
                <dt className="text-sm font-medium text-slate-500">Discriminator Loss:</dt>
                <dd className="text-sm text-slate-800 font-mono">{stock.discriminator_loss.toFixed(6)}</dd>
              </div>
              <div className="flex justify-between py-1">
                <dt className="text-sm font-medium text-slate-500">Generator Loss:</dt>
                <dd className="text-sm text-slate-800 font-mono">{stock.generator_loss.toFixed(6)}</dd>
              </div>
              <div className="flex justify-between py-1">
                <dt className="text-sm font-medium text-slate-500">Test RMSE:</dt>
                <dd className="text-sm text-slate-800 font-mono">{stock.test_rmse.toFixed(6)}</dd>
              </div>
               <div className="flex justify-between py-1">
                <dt className="text-sm font-medium text-slate-500">Epoch:</dt>
                <dd className="text-sm text-slate-800">{stock.epoch}</dd>
              </div>
            </dl>
            <button
              onClick={handlePredictClick}
              className={`mt-6 w-full bg-orange-500 text-white px-4 py-2 rounded-md text-sm font-medium transition-colors duration-200 ease-in-out ${
                isLoading
                  ? 'opacity-50 cursor-not-allowed'
                  : 'hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2' // Added focus styles
              }`}
              disabled={isLoading}
            >
              {isLoading ? 'Loading Prediction...' : "Predict Tomorrow's Price"}
            </button>
          </div>

          {/* Right Column: Stock Chart */}
          <div className="w-full md:w-2/3"> {/* Adjusted width */}
             <div className="border border-slate-200 rounded-lg p-1 shadow-sm overflow-hidden"> {/* Added subtle border/padding */}
                <img
                  src={stock.modelImg}
                  alt={`${stock.symbol} Historical Chart`}
                  className="w-full h-auto rounded-md"
                />
             </div>
          </div>
        </div>

        {/* Loading Spinner - appears below main content */}
        {isLoading && <LoadingSpinner />}

        {/* Prediction Section - Conditionally Rendered */}
        {!isLoading && showPrediction && (
          <div className='mt-12 pt-8 border-t border-slate-200'> {/* Increased top margin & added separator */}
            <div className='flex flex-col lg:flex-row lg:items-start gap-8 w-full'>

              {/* Left Column (Optional): Tweets & Sentiment */}
              {stock.tweets && stock.score && stock.tweets.length === stock.score.length && (
                <div className="w-full lg:w-1/3 flex-shrink-0 bg-slate-50 p-4 rounded-lg border border-slate-200">
                   <h3 className="text-lg font-semibold text-slate-700 mb-4 text-center md:text-left">
                     Recent Tweets & Sentiment
                   </h3>
                   <div className="space-y-3 max-h-96 overflow-y-auto pr-2"> {/* Added max-height & scroll */}
                     {stock.tweets.map((tweet, index) => (
                       <div key={index} className="p-3 border border-slate-200 rounded-md shadow-sm bg-white hover:shadow-md transition-shadow duration-200 ease-in-out">
                         <p className="text-slate-700 text-sm mb-1">{tweet}</p>
                         <p className="text-xs font-medium text-indigo-700">
                           Sentiment Score: {stock.score[index]}
                         </p>
                       </div>
                     ))}
                   </div>
                   <div>
                   </div>
                </div>
              )}

              {/* Right Column: Prediction Image & Price */}
              <div ref={predictionRef} className='w-full lg:w-2/3 flex flex-col items-center'>
                <h3 className="text-lg font-semibold text-slate-700 mb-4 text-center w-full">
                    Price Prediction Analysis
                </h3>
                <div className="border border-slate-200 rounded-lg p-1 shadow-sm overflow-hidden w-full">
                    <img
                      src={stock.predImg}
                      alt={`Predicted ${stock.symbol} Price Chart`}
                      className="w-full h-auto rounded-md"
                    />
                </div>
                {/* Safely access predicted price */}
                {stock.pred !== undefined ? (
                  <p className="text-indigo-700 mt-4 p-3 text-2xl font-semibold text-center"> {/* Centered text */}
                    Predicted Price: ${stock.pred.toFixed(2)}
                  </p>
                ) : (
                  <p className="text-amber-600 mt-4 p-3 text-base text-center"> {/* Using amber for warning */}
                    Predicted price data not available.
                  </p>
                )}
              </div>
            </div>
            <div className="flex align-middle justify-center border border-slate-200 rounded-lg p-1 shadow-sm overflow-hidden h-[60vh]"> {/* Reduced height */}
                  <img
                  src={stock.lossImg}
                  alt={`${stock.symbol} Historical Chart`}
                  className="w-auto h-[60vh] rounded-md "
                  />
              </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default StockInfo;