const express = require("express");
const app = express();
const mongoose = require("mongoose");
const cors = require("cors");

app.use(express.json());
app.use(cors());

mongoose.connect("mongodb+srv://newberrj:YV68TsYLjtbiern@mern-demo.tx9fvl6.mongodb.net/MovieBookingDB?retryWrites=true&w=majority");

const TicketModel = require('./models/Ticket');

app.get("/getTickets", async (req, res) => {
  try {
    const result = await TicketModel.find({});
    res.json(result);
  } catch(err) {
    console.error("GET Error:", err);
    res.status(500).json({ error: err.message });
  }
});

app.post("/createTicket", async (req, res) => {
  try {
    const ticket = req.body;
    const newTicket = new TicketModel(ticket);
    await newTicket.save();
    res.json(ticket);
  } catch(err) {
    console.error("POST Error:", err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(3001, () => {
  console.log("Server is running on port 3001...");
});