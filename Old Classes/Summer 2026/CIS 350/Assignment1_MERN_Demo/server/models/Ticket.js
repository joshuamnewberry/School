const mongoose = require("mongoose");

const TicketSchema = new mongoose.Schema({
  movieTitle: { type: String, required: true },
  theaterNumber: { type: Number, required: true },
  seatCount: { type: Number, required: true }
});

const TicketModel = mongoose.model("tickets", TicketSchema);
module.exports = TicketModel;