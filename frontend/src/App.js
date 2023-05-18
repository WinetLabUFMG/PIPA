import './App.css';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';

import { isAuthenticated } from './services/Auth';
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


const PrivateRoute = ({children, redirectTo}) => {
  const auth = isAuthenticated()
  console.log("isAuth:", isAuthenticated)
  return auth ? children : <Navigate to="/" />
}

function App() {
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
