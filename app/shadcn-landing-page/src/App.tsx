import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Home from "./Home";
import Stock from "./Stock";
import PortfolioAnalyzer from "./PortfolioAnalyzer";

function App() {
  return (
    <>
    <Router>
      <Routes>
        <Route path="/" element={<Home></Home>} />
        <Route path="/stock" element={<Stock/>} />
        <Route path="PortfolioAnalyzer" element={<PortfolioAnalyzer/>} />
      </Routes>
    </Router>
    </>
  );
}

export default App;
