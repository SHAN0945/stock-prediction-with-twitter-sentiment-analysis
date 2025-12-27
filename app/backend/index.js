const express = require("express");
const { spawn } = require("child_process");
const cors = require("cors");

const app = express();
app.use(express.json());
app.use(cors());
app.post("/compute", (req, res) => {
    const inputData = req.body.input;
    
    const pythonProcess = spawn("python", ["compute.py", inputData]);

    let result = "";
    pythonProcess.stdout.on("data", (data) => {
        result += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
        console.error(`Error: ${data}`);
    });

    pythonProcess.on("close", (code) => {
        let data = result.trim().split("\n");
        data = JSON.parse(data[1]);
        console.log(data);
        
        
        res.json({ data });
    });
});

app.listen(3000, () => console.log("Server running on port 3000"));
