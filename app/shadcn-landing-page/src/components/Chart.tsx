import React, { useEffect, useRef, memo } from "react";

function TradingViewWidget({ stockSymbol = "MSFT" }) {
  const container = useRef(null);

  useEffect(() => {
    // Prevent multiple script injections
    if (!container.current || container.current.querySelector("iframe")) {
      return;
    }

    const script = document.createElement("script");
    script.src = "https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js";
    script.type = "text/javascript";
    script.async = true;
    script.innerHTML = JSON.stringify({
      autosize: true,
      symbol: `NASDAQ:${stockSymbol}`,
      interval: "D",
      timezone: "Etc/UTC",
      theme: "dark",
      style: "1",
      locale: "en",
      allow_symbol_change: true,
      support_host: "https://www.tradingview.com",
    });

    console.log("Loading TradingView widget for:", stockSymbol);
    container.current.appendChild(script);
  }, [stockSymbol]); // Re-run effect if stockSymbol changes

  return (
    <div className="tradingview-widget-container" ref={container} style={{ height: "100%", width: "100%" }}>
      <div className="tradingview-widget-container__widget" style={{ height: "calc(100% - 32px)", width: "100%" }}></div>
    </div>
  );
}

export default memo(TradingViewWidget);
