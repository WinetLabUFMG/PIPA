import './App.css';
import { useState, useEffect} from 'react';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';

import Home from './pages/Home/Home';
import FormularioCadastro from './pages/FormCadastro/FormCadastro';
import Usuarios from './pages/Usuarios/Usuarios';
import Usuario from './pages/Usuario/Usuario';
import Navbar from './layout/Navbar';
import Footer from './layout/Footer'
import GrupoPoliticas from './pages/GrupoPoliticas/GrupoPoliticas'
import GrupoPolitica  from './pages/GrupoPolitica/GrupoPolitica'
import CriarGrupo from './pages/CriarGrupo/CriarGrupo';
import SolicitaçãoCadastramento from './pages/SolicitaçãoCadastro/SolicitaçãoCadastramento';

function App() {
  const [auth, setAuth] = useState()

  useEffect(() => {
    fetch(`http://localhost:5000/auth`,{
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then((resp) => resp.json())
        .then((data) => {
            console.log("authorization:", data)
            setAuth(data)
        })
        .catch((error)=> console.log(error))
  }, [])

  const isAuthenticated = () => ( auth == "true" );

  const PrivateRoute = ({children}) => {
    return isAuthenticated ? children : <Navigate to="/" />
  }

  return (

      <Router>
       <div className='AppContainer'>
        <Navbar />

        <Routes>
          <Route exact path='/' index element={<SolicitaçãoCadastramento/>} />
          <Route exact path='/home' element={<PrivateRoute>
            <Home />
          </PrivateRoute>} />
          <Route exact path='/cadastro' element={<PrivateRoute>
            <FormularioCadastro />
          </PrivateRoute>} />
          <Route exact path='/usuarios' element={<PrivateRoute>
            <Usuarios />
          </PrivateRoute>} />
          <Route exact path='/usuario/:username' element={<PrivateRoute>
            <Usuario />
          </PrivateRoute>} />
          <Route exact path='/politicas' element={<PrivateRoute>
            <GrupoPoliticas />
          </PrivateRoute>} />
          <Route exact path='/politica/:policyID' element={<PrivateRoute>
            <GrupoPolitica />
          </PrivateRoute>} />
          <Route exact path='/criargrupo' element={<PrivateRoute>
            <CriarGrupo />
          </PrivateRoute>} />

        </Routes>

        <Footer />
      </div>
      </Router>
  );
}

export default App;
