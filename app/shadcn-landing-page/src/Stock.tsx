import TradingViewWidget from "./components/Chart"
import { useState } from "react"
import StockInfo from "./components/StockInfo";

function Stock() {
    const [stockSymbol, setStockSymbol] = useState("");
    const [stockNameSet, setStockNameSet] = useState(false);

    function handleStockSymbolChange(val:string) {
        setStockSymbol(val);
        setStockNameSet(true);
    }   
    return (
    <div>
        {!stockNameSet && (
            <div className="flex flex-col items-center justify-center min-h-[50vh] gap-8 p-8 text-center">
                <h1 className="text-4xl md:text-5xl font-bold mb-4">Stock Analysis</h1>
                
                <div className="flex gap-4 w-full max-w-2xl mx-auto">
                    <input
                        type="text"
                        value={stockSymbol}
                        onChange={(e) => setStockSymbol(e.target.value)}
                        placeholder="Enter stock symbol"
                        className="flex-1 py-4 px-6 text-lg rounded-full border-2 border-gray-300 
                                focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200
                                transition-all duration-300 placeholder-gray-400 text-black"
                    />
                    
                    <button
                        onClick={() => handleStockSymbolChange(stockSymbol)}
                        className="py-4 px-8 text-lg font-medium text-white bg-blue-600 rounded-full 
                                hover:bg-blue-700 transition-colors duration-300 
                                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
                    >
                        Search
                    </button>
                </div>
            </div>
        )}
        {stockNameSet &&(
            <div style={{ height: "50vh", width: "100%" }}>
            <TradingViewWidget stockSymbol={stockSymbol} />
            <StockInfo stockSymbol={stockSymbol} />
        </div>
        )}

    </div>
  )
}

export default Stock
