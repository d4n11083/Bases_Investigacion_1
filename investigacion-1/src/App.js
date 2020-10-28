//import './App.css';
import {useEffect, useState} from 'react'
import { Users } from "./components/Users"

function App() {

  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch("/users").then(response => 
      response.json().then( data => {
        setUsers(data.Users);
      }) 
    );
  }, [])

  return (
    <div className="App">
      <h1>Usuarios</h1>
      <Users users={users}/>

    </div>
  );
}

export default App;
