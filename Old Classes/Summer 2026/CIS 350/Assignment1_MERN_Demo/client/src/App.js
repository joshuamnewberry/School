import './App.css';
import { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [listOfTickets, setListOfTickets] = useState([]);
  const [movieTitle, setMovieTitle] = useState("");
  const [theaterNumber, setTheaterNumber] = useState(0);
  const [seatCount, setSeatCount] = useState(0);

  useEffect(() => {
    axios.get("http://localhost:3001/getTickets").then((response) => {
      setListOfTickets(response.data);
    });
  }, []);

  const createTicket = () => {
    axios.post("http://localhost:3001/createTicket", {
      movieTitle,
      theaterNumber,
      seatCount,
    }).then((response) => {
      setListOfTickets([
        ...listOfTickets,
        { movieTitle, theaterNumber, seatCount },
      ]);
    });
  };

  return (
    <div className="App">
      <div className="display">
        {listOfTickets.map((ticket, index) => (
          <div key={index}>
            <h3>Movie: {ticket.movieTitle}</h3>
            <p>Theater: {ticket.theaterNumber} | Seats: {ticket.seatCount}</p>
          </div>
        ))}
      </div>

      <div>
        <input type="text" placeholder="Movie Title..." onChange={(e) => setMovieTitle(e.target.value)} />
        <input type="number" placeholder="Theater Number..." onChange={(e) => setTheaterNumber(Number(e.target.value))} />
        <input type="number" placeholder="Seat Count..." onChange={(e) => setSeatCount(Number(e.target.value))} />
        <button onClick={createTicket}>Book Ticket</button>
      </div>
    </div>
  );
}

export default App;